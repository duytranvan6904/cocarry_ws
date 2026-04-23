#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import numpy as np
import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python import BaseOptions
import os
import threading

from human_hand_msgs.msg import HandPrediction, HandState
from std_srvs.srv import Trigger, SetBool
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge
import message_filters
from image_geometry import PinholeCameraModel

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

class KinectTrackerNode(Node):
    def __init__(self):
        super().__init__('kinect_tracker')

        self.declare_parameter('model_path', '')
        self.declare_parameter('offset_x', 0.0)
        self.declare_parameter('offset_y', 0.0)
        self.declare_parameter('offset_z', 0.0)

        self.model_path = self.get_parameter('model_path').value
        self.offset_x = self.get_parameter('offset_x').value
        self.offset_y = self.get_parameter('offset_y').value
        self.offset_z = self.get_parameter('offset_z').value

        self.pred_pub = self.create_publisher(HandState, '/hand_position', 10)
        self.calib_srv = self.create_service(Trigger, '/kinect2/calibrate_origin', self.calibrate_cb)

        self.current_raw_x = 0.0
        self.current_raw_y = 0.0
        self.current_raw_z = 0.0

        self.bridge = CvBridge()
        self.camera_model = PinholeCameraModel()
        self.has_camera_info = False

        if not os.path.exists(self.model_path):
            self.get_logger().error(f'Model not found: {self.model_path}')
            return

        base_options = BaseOptions(model_asset_path=self.model_path)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_poses=1,
            min_pose_detection_confidence=0.5,
            min_pose_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.landmarker = vision.PoseLandmarker.create_from_options(options)

        # Setup ROS 2 subscribers
        self.info_sub = self.create_subscription(CameraInfo, '/kinect2/qhd/camera_info', self.camera_info_cb, 10)
        
        self.color_sub = message_filters.Subscriber(self, Image, '/kinect2/qhd/image_color_rect')
        self.depth_sub = message_filters.Subscriber(self, Image, '/kinect2/qhd/image_depth_rect')
        
        self.ts = message_filters.ApproximateTimeSynchronizer([self.color_sub, self.depth_sub], 10, 0.1)
        self.ts.registerCallback(self.image_callback)

        self.get_logger().info('Kinect Tracker Node Started. Waiting for images...')

    def calibrate_cb(self, request, response):
        self.offset_x = self.current_raw_x
        self.offset_y = self.current_raw_y
        self.offset_z = self.current_raw_z
        
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

    def camera_info_cb(self, msg):
        if not self.has_camera_info:
            self.camera_model.fromCameraInfo(msg)
            self.has_camera_info = True
            self.get_logger().info("Received Camera Info!")

    def image_callback(self, color_msg, depth_msg):
        if not self.has_camera_info:
            return

        try:
            # kinect2_bridge publishes color as BGRX (4-channel) — use passthrough then drop X
            raw = self.bridge.imgmsg_to_cv2(color_msg, desired_encoding='passthrough')
            if raw.ndim == 3 and raw.shape[2] == 4:
                color_image = raw[:, :, :3].copy()   # BGRX → BGR
            elif raw.ndim == 2:
                color_image = cv2.cvtColor(raw, cv2.COLOR_GRAY2BGR)
            else:
                color_image = raw
            # Kinect2 bridge depth image is 16UC1 (millimeters)
            depth_image = self.bridge.imgmsg_to_cv2(depth_msg, "16UC1")
        except Exception as e:
            self.get_logger().error(f"CV Bridge Error: {e}")
            return

        if color_image is None or color_image.size == 0:
            return
        h, w = color_image.shape[:2]
        rgb_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

        result = self.landmarker.detect(mp_image)

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
                        d = depth_image[ny, nx] / 1000.0 # Convert mm to meters
                        if 0.1 < d < 4.5:
                            depth_values.append(d)

                if depth_values:
                    depth_m = np.median(depth_values)
                    
                    # Deproject using image_geometry
                    ray = self.camera_model.projectPixelTo3dRay((px, py))
                    point_3d = (ray[0] * depth_m, ray[1] * depth_m, depth_m)
                    
                    self.current_raw_x = float(point_3d[0])
                    self.current_raw_y = float(point_3d[1])
                    self.current_raw_z = float(point_3d[2])
                    
                    self.offset_x = self.get_parameter('offset_x').value
                    self.offset_y = self.get_parameter('offset_y').value
                    self.offset_z = self.get_parameter('offset_z').value

                    # Standardize coordinates (Kinect Z is forward, X is right, Y is down)
                    x_ws = self.current_raw_x - self.offset_x
                    y_ws = -(self.current_raw_z - self.offset_z)
                    z_ws = -(self.current_raw_y - self.offset_y)

                    msg = HandState()
                    msg.header.stamp = self.get_clock().now().to_msg()
                    msg.header.frame_id = 'kinect_world'
                    msg.is_tracked = True
                    msg.x = x_ws
                    msg.y = y_ws
                    msg.z = z_ws
                    self.pred_pub.publish(msg)

        if wrist_pixel:
            cv2.circle(color_image, wrist_pixel, 10, WRIST_COLOR, -1)
            cv2.circle(color_image, wrist_pixel, 12, (255, 255, 255), 2)
            info_text = f"X:{self.current_raw_x:+.3f} Y:{self.current_raw_y:+.3f} Z:{self.current_raw_z:.3f} m"
            cv2.putText(color_image, info_text, (wrist_pixel[0]+20, wrist_pixel[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

        cv2.imshow("Kinect V2 Tracking", color_image)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = KinectTrackerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
