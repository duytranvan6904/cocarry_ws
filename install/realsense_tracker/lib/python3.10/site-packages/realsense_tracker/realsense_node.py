#!/usr/bin/env python3
import pyrealsense2 as rs
import numpy as np
import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python import BaseOptions
import time
import os
import threading

import rclpy
from rclpy.node import Node
from human_hand_msgs.msg import HandPrediction, HandState
from std_srvs.srv import Trigger, SetBool

RIGHT_WRIST_ID = 16

POSE_CONNECTIONS = [
    (11, 12),
    (11, 13), (13, 15),
    (12, 14), (14, 16),
    (11, 23), (12, 24),
    (23, 24),
    (23, 25), (25, 27),
    (24, 26), (26, 28),
]

SKELETON_COLOR = (0, 255, 128)
JOINT_COLOR = (255, 200, 0)
WRIST_COLOR = (0, 0, 255)

def draw_skeleton(image, landmarks, w, h):
    points = {}
    for idx, lm in enumerate(landmarks):
        if lm.visibility > 0.5:
            px = int(lm.x * w)
            py = int(lm.y * h)
            px = max(0, min(px, w - 1))
            py = max(0, min(py, h - 1))
            points[idx] = (px, py)

    for start, end in POSE_CONNECTIONS:
        if start in points and end in points:
            cv2.line(image, points[start], points[end], SKELETON_COLOR, 2, cv2.LINE_AA)

    for idx, pt in points.items():
        color = WRIST_COLOR if idx == RIGHT_WRIST_ID else JOINT_COLOR
        radius = 7 if idx == RIGHT_WRIST_ID else 4
        cv2.circle(image, pt, radius, color, -1, cv2.LINE_AA)
        cv2.circle(image, pt, radius + 2, (255, 255, 255), 1, cv2.LINE_AA)

    return points

class RealSenseTrackerNode(Node):
    def __init__(self):
        super().__init__('realsense_tracker')

        self.declare_parameter('model_path', '')
        self.declare_parameter('offset_x', 0.0)
        self.declare_parameter('offset_y', 0.0)
        self.declare_parameter('offset_z', 0.0)

        self.model_path = self.get_parameter('model_path').value
        self.offset_x = self.get_parameter('offset_x').value
        self.offset_y = self.get_parameter('offset_y').value
        self.offset_z = self.get_parameter('offset_z').value

        self.pred_pub = self.create_publisher(HandState, '/hand_position', 10)
        
        self.calib_srv = self.create_service(Trigger, '/realsense/calibrate_origin', self.calibrate_cb)

        self.current_raw_x = 0.0
        self.current_raw_y = 0.0
        self.current_raw_z = 0.0

        self.is_running = True

        self.thread = threading.Thread(target=self.tracking_loop, daemon=True)
        self.thread.start()
        self.get_logger().info('RealSense Tracker Node Started.')

    def calibrate_cb(self, request, response):
        self.offset_x = self.current_raw_x
        self.offset_y = self.current_raw_y
        self.offset_z = self.current_raw_z
        
        # update parameters locally so they can be read later or saved
        self.set_parameters([
            rclpy.Parameter('offset_x', rclpy.Parameter.Type.DOUBLE, float(self.offset_x)),
            rclpy.Parameter('offset_y', rclpy.Parameter.Type.DOUBLE, float(self.offset_y)),
            rclpy.Parameter('offset_z', rclpy.Parameter.Type.DOUBLE, float(self.offset_z)),
        ])

        try:
            import yaml
            yaml_path = '/home/duy/Experiment/hrc_ws/src/hrc_bringup/config/all_params.yaml'
            if os.path.exists(yaml_path):
                with open(yaml_path, 'r') as f:
                    data = yaml.safe_load(f)
                if 'realsense_tracker' in data:
                    data['realsense_tracker']['ros__parameters']['offset_x'] = float(self.offset_x)
                    data['realsense_tracker']['ros__parameters']['offset_y'] = float(self.offset_y)
                    data['realsense_tracker']['ros__parameters']['offset_z'] = float(self.offset_z)
                    with open(yaml_path, 'w') as f:
                        yaml.dump(data, f)
        except Exception as e:
            self.get_logger().error(f"Failed to save calib: {e}")

        msg = f'Calibrated successfully. Origin set to ({self.offset_x:.3f}, {self.offset_y:.3f}, {self.offset_z:.3f})'
        self.get_logger().info(msg)
        response.success = True
        response.message = msg
        return response



    def tracking_loop(self):
        if not os.path.exists(self.model_path):
            self.get_logger().error(f'Model not found: {self.model_path}')
            return

        ctx = rs.context()
        devices = ctx.query_devices()
        if len(devices) == 0:
            self.get_logger().error("No RealSense devices found!")
            return

        dev = devices[0]
        dev.hardware_reset()
        time.sleep(5)

        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

        profile = pipeline.start(config)
        
        for _ in range(15):
            pipeline.wait_for_frames(timeout_ms=5000)

        align = rs.align(rs.stream.color)

        base_options = BaseOptions(model_asset_path=self.model_path)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_poses=1,
            min_pose_detection_confidence=0.5,
            min_pose_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        landmarker = vision.PoseLandmarker.create_from_options(options)

        timestamp_ms = 0
        consecutive_failures = 0

        try:
            while rclpy.ok() and self.is_running:
                try:
                    frames = pipeline.wait_for_frames(timeout_ms=10000)
                    consecutive_failures = 0
                except RuntimeError:
                    consecutive_failures += 1
                    if consecutive_failures >= 10:
                        self.get_logger().error("Camera not responding")
                        break
                    continue

                aligned_frames = align.process(frames)
                color_frame = aligned_frames.get_color_frame()
                depth_frame = aligned_frames.get_depth_frame()

                if not color_frame or not depth_frame:
                    continue

                color_image = np.asanyarray(color_frame.get_data())
                depth_image = np.asanyarray(depth_frame.get_data())
                depth_intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics
                h, w, _ = color_image.shape

                rgb_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
                timestamp_ms += 33

                result = landmarker.detect_for_video(mp_image, timestamp_ms)

                wrist_pixel = None
                if result.pose_landmarks and len(result.pose_landmarks) > 0:
                    landmarks = result.pose_landmarks[0]
                    drawn_points = draw_skeleton(color_image, landmarks, w, h)
                    right_wrist = landmarks[RIGHT_WRIST_ID]

                    if right_wrist.visibility > 0.5:
                        px = int(right_wrist.x * w)
                        py = int(right_wrist.y * h)
                        px = max(0, min(px, w - 1))
                        py = max(0, min(py, h - 1))
                        wrist_pixel = (px, py)

                        depth_values = []
                        for dx in range(-2, 3):
                            for dy in range(-2, 3):
                                nx = max(0, min(px + dx, w - 1))
                                ny = max(0, min(py + dy, h - 1))
                                d = depth_frame.get_distance(nx, ny)
                                if 0.1 < d < 3.0:
                                    depth_values.append(d)

                        if depth_values:
                            depth_m = np.median(depth_values)
                            point_3d = rs.rs2_deproject_pixel_to_point(depth_intrinsics, [px, py], depth_m)
                            
                            self.current_raw_x = float(point_3d[0])
                            self.current_raw_y = float(point_3d[1])
                            self.current_raw_z = float(point_3d[2])
                            
                            self.offset_x = self.get_parameter('offset_x').value
                            self.offset_y = self.get_parameter('offset_y').value
                            self.offset_z = self.get_parameter('offset_z').value

                            x_ws = self.current_raw_x - self.offset_x
                            y_ws = -(self.current_raw_z - self.offset_z)
                            z_ws = -(self.current_raw_y - self.offset_y)

                            msg = HandState()
                            msg.header.stamp = self.get_clock().now().to_msg()
                            msg.header.frame_id = 'realsense_world'
                            msg.is_tracked = True
                            msg.x = x_ws
                            msg.y = y_ws
                            msg.z = z_ws
                            self.pred_pub.publish(msg)

                # Hiển thị ảnh OpenCV
                if wrist_pixel:
                    cv2.circle(color_image, wrist_pixel, 10, WRIST_COLOR, -1)
                    cv2.circle(color_image, wrist_pixel, 12, (255, 255, 255), 2)
                    info_text = f"X:{self.current_raw_x:+.3f} Y:{self.current_raw_y:+.3f} Z:{self.current_raw_z:.3f} m"
                    cv2.putText(color_image, info_text, (wrist_pixel[0]+20, wrist_pixel[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

                cv2.imshow("RealSense Tracking (Press Q in this window to stop node)", color_image)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:
                    self.is_running = False
                    # Stop node if Q is pressed
                    os._exit(0)

        finally:
            landmarker.close()
            pipeline.stop()
            cv2.destroyAllWindows()

def main(args=None):
    rclpy.init(args=args)
    node = RealSenseTrackerNode()
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
