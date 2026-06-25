#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import os
import threading
import pyrealsense2 as rs

# ---------------------------------------------------------------------------
# Landmark indices (MediaPipe Pose 33-landmark model)
# ---------------------------------------------------------------------------
IDX_L_SHOULDER  = 11
IDX_R_SHOULDER  = 12
IDX_R_ELBOW     = 14
IDX_R_WRIST     = 16
IDX_R_PINKY     = 18
IDX_R_INDEX     = 20
IDX_R_HIP       = 24

# ---------------------------------------------------------------------------
# Drawing helpers (pure OpenCV – no mediapipe.framework dependency)
# ---------------------------------------------------------------------------
POSE_CONNECTIONS = [
    (11, 12),
    (11, 13), (13, 15),
    (12, 14), (14, 16),
    (15, 17), (15, 19), (15, 21),
    (16, 18), (16, 20), (16, 22),
    (11, 23), (12, 24),
    (23, 24),
]
SKELETON_COLOR = (0, 255, 128)
JOINT_COLOR    = (255, 200, 0)
HIGHLIGHT_COLOR= (0, 80, 255)   # right arm joints

RIGHT_ARM_IDS = {IDX_R_SHOULDER, IDX_R_ELBOW, IDX_R_WRIST, IDX_R_PINKY, IDX_R_INDEX}

def draw_skeleton(image, landmarks, w, h):
    points = {}
    for idx, lm in enumerate(landmarks):
        if lm.visibility > 0.4:
            px = int(np.clip(lm.x * w, 0, w - 1))
            py = int(np.clip(lm.y * h, 0, h - 1))
            points[idx] = (px, py)

    for start, end in POSE_CONNECTIONS:
        if start in points and end in points:
            color = HIGHLIGHT_COLOR if (start in RIGHT_ARM_IDS or end in RIGHT_ARM_IDS) else SKELETON_COLOR
            cv2.line(image, points[start], points[end], color, 2, cv2.LINE_AA)

    for idx, pt in points.items():
        color = HIGHLIGHT_COLOR if idx in RIGHT_ARM_IDS else JOINT_COLOR
        radius = 7 if idx in RIGHT_ARM_IDS else 4
        cv2.circle(image, pt, radius, color, -1, cv2.LINE_AA)
        cv2.circle(image, pt, radius + 2, (255, 255, 255), 1, cv2.LINE_AA)

# ---------------------------------------------------------------------------
# RULA score colour coding
# ---------------------------------------------------------------------------
def score_color(score):
    if score <= 4:   return (0, 200, 0)    # green – acceptable
    elif score <= 6: return (0, 165, 255)  # orange – investigate
    else:            return (0, 0, 220)    # red – act immediately


class RulaTrackerNode(Node):
    def __init__(self):
        super().__init__('rula_tracker_node')

        self.declare_parameter('model_path', '')

        model_path = self.get_parameter('model_path').get_parameter_value().string_value

        if not model_path or not os.path.exists(model_path):
            self.get_logger().fatal(
                f"model_path '{model_path}' not found. "
                "Pass --ros-args -p model_path:=/absolute/path/to/pose_landmarker.task")
            raise SystemExit(1)

        if os.path.getsize(model_path) == 0:
            self.get_logger().fatal(f"model file is empty (0 bytes): {model_path}")
            raise SystemExit(1)

        self.publisher_ = self.create_publisher(Float32MultiArray, '/rula_scores', 10)

        # MediaPipe PoseLandmarker (Tasks API)
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_poses=1,
            min_pose_detection_confidence=0.5,
            min_pose_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.detector = vision.PoseLandmarker.create_from_options(options)
        self.timestamp_ms = 0
        self.is_running = True

        # Tracking loop in background thread (same pattern as realsense_tracker)
        self.thread = threading.Thread(target=self.tracking_loop, daemon=True)
        self.thread.start()
        self.get_logger().info(f'RULA Tracker Node started. Model: {model_path}')

    # ------------------------------------------------------------------
    # Geometry helpers
    # ------------------------------------------------------------------
    @staticmethod
    def vec(a, b):
        return np.array(b) - np.array(a)

    @staticmethod
    def angle_between(a, b, c):
        """Angle at vertex b, formed by ba and bc."""
        ba = np.array(a) - np.array(b)
        bc = np.array(c) - np.array(b)
        cos = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-8)
        return np.degrees(np.arccos(np.clip(cos, -1.0, 1.0)))

    # ------------------------------------------------------------------
    # RULA calculation
    # ------------------------------------------------------------------
    def calculate_rula_score(self, wlm):
        """
        wlm: pose_world_landmarks[0]  (metric-scale, gravity-aligned)

        Returns dict with per-component scores and raw angles.
        """
        def pt(idx):
            return np.array([wlm[idx].x, wlm[idx].y, wlm[idx].z])

        r_shoulder = pt(IDX_R_SHOULDER)
        r_elbow    = pt(IDX_R_ELBOW)
        r_wrist    = pt(IDX_R_WRIST)
        l_shoulder = pt(IDX_L_SHOULDER)
        l_hip      = pt(23)
        r_hip      = pt(IDX_R_HIP)
        r_index    = pt(IDX_R_INDEX)
        
        # Calculate midpoints
        r_n = (l_shoulder + r_shoulder) / 2.0  # neck ~ mid-shoulder
        r_t = (l_hip + r_hip) / 2.0            # mid-hip/torso

        # ---- Step 1: Upper Arm Angles ----
        # 1a. Sagittal angle (alpha_s)
        trunk_vec = r_t - r_n
        upper_arm_vec = r_elbow - r_shoulder
        cos_a_s = np.dot(trunk_vec, upper_arm_vec) / (np.linalg.norm(trunk_vec) * np.linalg.norm(upper_arm_vec) + 1e-8)
        alpha_s = np.degrees(np.arccos(np.clip(cos_a_s, -1.0, 1.0)))
        
        if alpha_s <= 20:
            ua_score = 1
        elif alpha_s <= 45:
            ua_score = 2
        elif alpha_s <= 90:
            ua_score = 3
        else:
            ua_score = 4
            
        # 1b. Coronal angle (alpha_c) - Abduction
        shoulder_up = r_n - r_shoulder
        cos_a_c = np.dot(shoulder_up, upper_arm_vec) / (np.linalg.norm(shoulder_up) * np.linalg.norm(upper_arm_vec) + 1e-8)
        alpha_c = np.degrees(np.arccos(np.clip(cos_a_c, -1.0, 1.0))) - 90.0
        
        if abs(alpha_c) > 10.0:
            ua_score += 1

        # ---- Step 2: Lower Arm Angles ----
        # 2a. Sagittal angle (beta_s) - Flexion
        forearm_vec = r_wrist - r_elbow
        cos_b_s = np.dot(forearm_vec, upper_arm_vec) / (np.linalg.norm(forearm_vec) * np.linalg.norm(upper_arm_vec) + 1e-8)
        beta_s = np.degrees(np.arccos(np.clip(cos_b_s, -1.0, 1.0)))
        
        if 60 <= beta_s <= 100:
            la_score = 1
        else:
            la_score = 2
            
        # 2b. Transversal angle (beta_t) - Deviation
        shoulder_axis = r_shoulder - r_n
        cos_b_t = np.dot(shoulder_axis, forearm_vec) / (np.linalg.norm(shoulder_axis) * np.linalg.norm(forearm_vec) + 1e-8)
        beta_t = 90.0 - np.degrees(np.arccos(np.clip(cos_b_t, -1.0, 1.0)))
        
        if abs(beta_t) > 10.0:
            la_score += 1

        # ---- Step 3: Wrist Angle ----
        # Sagittal angle (gamma_s) - Bend
        hand_vec = r_index - r_wrist
        cos_g = np.dot(forearm_vec, hand_vec) / (np.linalg.norm(forearm_vec) * np.linalg.norm(hand_vec) + 1e-8)
        gamma = np.degrees(np.arccos(np.clip(cos_g, -1.0, 1.0)))
        
        # gamma measures deviation from straight (0 degrees)
        if gamma <= 15:
            wrist_score = 1
        else:
            wrist_score = 2

        total = ua_score + la_score + wrist_score

        return dict(
            upper_arm_score=ua_score,
            lower_arm_score=la_score,
            wrist_score=wrist_score,
            total_score=total,
            angles=dict(upper_arm=alpha_s, flexion=beta_s, wrist=gamma))

    # ------------------------------------------------------------------
    # Overlay helpers
    # ------------------------------------------------------------------
    @staticmethod
    def draw_panel(image, scores):
        h, w = image.shape[:2]
        panel_w, panel_h = 320, 170
        x0, y0 = 10, 10

        # semi-transparent background
        overlay = image.copy()
        cv2.rectangle(overlay, (x0, y0), (x0 + panel_w, y0 + panel_h), (20, 20, 20), -1)
        cv2.addWeighted(overlay, 0.55, image, 0.45, 0, image)

        total  = scores['total_score']
        color  = score_color(total)
        font   = cv2.FONT_HERSHEY_SIMPLEX
        y      = y0 + 28

        cv2.putText(image, f"RULA Score A: {total}", (x0 + 10, y),
                    font, 0.75, color, 2, cv2.LINE_AA)
        y += 28

        items = [
            ("Upper Arm", scores['upper_arm_score'], scores['angles']['upper_arm']),
            ("Lower Arm", scores['lower_arm_score'], scores['angles']['flexion']),
            ("Wrist",     scores['wrist_score'],     scores['angles']['wrist']),
        ]
        for label, sc, ang in items:
            cv2.putText(image, f"  {label}: {sc}  ({ang:.1f} deg)",
                        (x0 + 10, y), font, 0.52, (220, 220, 220), 1, cv2.LINE_AA)
            y += 24

    # ------------------------------------------------------------------
    # Main tracking loop (runs in background thread)
    # ------------------------------------------------------------------
    def tracking_loop(self):
        # --- RealSense pipeline ---
        ctx = rs.context()
        devices = ctx.query_devices()
        if len(devices) == 0:
            self.get_logger().error("No RealSense devices found!")
            return

        devices[0].hardware_reset()
        import time; time.sleep(4)

        pipeline = rs.pipeline()
        cfg = rs.config()
        cfg.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        pipeline.start(cfg)

        # Warm-up frames
        for _ in range(15):
            pipeline.wait_for_frames(timeout_ms=5000)

        align = rs.align(rs.stream.color)
        consecutive_failures = 0

        try:
            while rclpy.ok() and self.is_running:
                try:
                    frames = pipeline.wait_for_frames(timeout_ms=5000)
                    consecutive_failures = 0
                except RuntimeError:
                    consecutive_failures += 1
                    if consecutive_failures >= 10:
                        self.get_logger().error("Camera not responding, stopping.")
                        break
                    continue

                aligned = align.process(frames)
                color_frame = aligned.get_color_frame()
                if not color_frame:
                    continue

                color_image = np.asanyarray(color_frame.get_data())
                h, w, _ = color_image.shape

                # MediaPipe inference
                rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
                self.timestamp_ms += 33
                result = self.detector.detect_for_video(mp_image, self.timestamp_ms)

                if result.pose_landmarks and result.pose_world_landmarks:
                    draw_skeleton(color_image, result.pose_landmarks[0], w, h)
                    scores = self.calculate_rula_score(result.pose_world_landmarks[0])
                    self.draw_panel(color_image, scores)

                    # Publish
                    msg = Float32MultiArray()
                    msg.data = [
                        float(scores['upper_arm_score']),
                        float(scores['lower_arm_score']),
                        float(scores['wrist_score']),
                        0.0, # Placeholder for removed twist score
                        float(scores['total_score']),
                    ]
                    self.publisher_.publish(msg)
                else:
                    cv2.putText(color_image, "No pose detected",
                                (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 50, 220), 2)

                cv2.imshow("RULA Real-time Tracker", color_image)
                key = cv2.waitKey(1) & 0xFF
                if key in (ord('q'), 27):
                    self.is_running = False
                    os._exit(0)

        finally:
            self.detector.close()
            pipeline.stop()
            cv2.destroyAllWindows()


def main(args=None):
    rclpy.init(args=args)
    node = RulaTrackerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.is_running = False
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
