#!/usr/bin/env python3
"""
transform_node.py
─────────────────
Node cầu nối giữa trajectory_predictor và cartesian_streamer.

Pipeline:
  /ml/predicted_position (HandPrediction, camera frame)
    → [object offset] → [cam→base transform] → [safety clamp]
  → /cartesian_streamer/target_pose (PoseStamped, robot base frame)

Cách chạy độc lập để test:
  ros2 run coord_transform transform_node --ros-args \
    --params-file /path/to/transform_params.yaml
"""

import numpy as np
from scipy.spatial.transform import Rotation

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Point, Quaternion
from std_msgs.msg import String, Bool
from human_hand_msgs.msg import HandPrediction, HandState
from std_srvs.srv import Trigger


class CoordTransformNode(Node):

    def __init__(self):
        super().__init__('coord_transform')
        self._declare_all_params()
        self._load_params()
        self._setup_pubsub()
        self._current_robot_pose = None  # To store the latest EE pose
        self._mode = 'ground_truth'      # Default mode
        self._running = False            # Whether to forward data
        self.get_logger().info(
            'CoordTransformNode khởi động.\n'
            f'  Object offset (cam frame): {self._obj_offset}\n'
            f'  Translation cam→base:      {self._t_cam_to_base}\n'
            f'  EE orientation (xyzw):     {self._ee_orient}\n'
            f'  Prediction step:           {self._pred_step}\n'
            f'  Workspace X: {self._ws_x}, Y: {self._ws_y}, Z: {self._ws_z}'
        )

    # ─── Parameter declarations ──────────────────────────────────────────

    def _declare_all_params(self):
        # Object offset: từ wrist landmark → điểm gắn robot trên vật (meters, camera frame)
        self.declare_parameter('object_offset_x', 0.0)
        self.declare_parameter('object_offset_y', 0.0)
        self.declare_parameter('object_offset_z', 0.0)

        # Rotation camera frame → robot base frame (quaternion xyzw)
        # Xác định bằng calibration script
        self.declare_parameter('cam_to_base_qx', 0.0)
        self.declare_parameter('cam_to_base_qy', 0.0)
        self.declare_parameter('cam_to_base_qz', 0.0)
        self.declare_parameter('cam_to_base_qw', 1.0)

        # Translation: vị trí origin camera trong robot base frame (meters)
        self.declare_parameter('cam_to_base_tx', 0.5)
        self.declare_parameter('cam_to_base_ty', 0.0)
        self.declare_parameter('cam_to_base_tz', 1.2)

        # EE orientation mặc định cho robot khi co-carrying (quaternion xyzw)
        # Default: EE hướng xuống (phù hợp với co-carrying ngang)
        self.declare_parameter('ee_orient_x', 0.0)
        self.declare_parameter('ee_orient_y', 1.0)
        self.declare_parameter('ee_orient_z', 0.0)
        self.declare_parameter('ee_orient_w', 0.0)

        # Dùng bước dự đoán thứ mấy (0=hiện tại, N=lookahead xa hơn)
        # Tăng để bù đắp độ trễ pipeline: camera latency + IK + queue buffer
        self.declare_parameter('prediction_step', 3)

        # Workspace safety bounds (robot base frame, meters)
        self.declare_parameter('workspace_x_min', -1.0)
        self.declare_parameter('workspace_x_max',  1.0)
        self.declare_parameter('workspace_y_min', -1.0)
        self.declare_parameter('workspace_y_max',  1.0)
        self.declare_parameter('workspace_z_min',  0.05)
        self.declare_parameter('workspace_z_max',  1.5)

    def _load_params(self):
        # Object offset
        self._obj_offset = np.array([
            self.get_parameter('object_offset_x').value,
            self.get_parameter('object_offset_y').value,
            self.get_parameter('object_offset_z').value,
        ])

        # Rotation matrix từ quaternion
        qx = self.get_parameter('cam_to_base_qx').value
        qy = self.get_parameter('cam_to_base_qy').value
        qz = self.get_parameter('cam_to_base_qz').value
        qw = self.get_parameter('cam_to_base_qw').value
        self._R_cam_to_base = Rotation.from_quat([qx, qy, qz, qw]).as_matrix()

        # Translation
        self._t_cam_to_base = np.array([
            self.get_parameter('cam_to_base_tx').value,
            self.get_parameter('cam_to_base_ty').value,
            self.get_parameter('cam_to_base_tz').value,
        ])

        # EE orientation
        self._ee_orient = [
            self.get_parameter('ee_orient_x').value,
            self.get_parameter('ee_orient_y').value,
            self.get_parameter('ee_orient_z').value,
            self.get_parameter('ee_orient_w').value,
        ]

        self._pred_step = int(self.get_parameter('prediction_step').value)

        # Workspace bounds
        self._ws_x = (
            self.get_parameter('workspace_x_min').value,
            self.get_parameter('workspace_x_max').value,
        )
        self._ws_y = (
            self.get_parameter('workspace_y_min').value,
            self.get_parameter('workspace_y_max').value,
        )
        self._ws_z = (
            self.get_parameter('workspace_z_min').value,
            self.get_parameter('workspace_z_max').value,
        )

    def _setup_pubsub(self):
        # Subscribe: tọa độ dự đoán từ trajectory_predictor
        self._pred_sub = self.create_subscription(
            HandPrediction,
            '/ml/predicted_position',
            self._on_prediction,
            10,
        )

        # Subscribe: tọa độ thô từ hand_position
        self._hand_sub = self.create_subscription(
            HandState,
            '/hand_position',
            self._on_hand_state,
            10,
        )

        # Subscribe: chế độ stream từ UI
        self._mode_sub = self.create_subscription(
            String,
            '/trajectory_mode',
            self._on_mode,
            10,
        )

        # Subscribe: trạng thái Run từ UI
        self._run_status_sub = self.create_subscription(
            Bool,
            '/run_status',
            self._on_run_status,
            10,
        )

        # Publish: target pose cho cartesian_streamer
        self._target_pub = self.create_publisher(
            PoseStamped,
            '/cartesian_streamer/target_pose',
            10,
        )

        # Publish: debug pose (để kiểm tra trong RViz)
        self._debug_pub = self.create_publisher(
            PoseStamped,
            '/coord_transform/debug_pose',
            10,
        )

        # Publish: trạng thái node (để UI theo dõi)
        self._status_pub = self.create_publisher(
            String,
            '/coord_transform/status',
            10,
        )

        # Subscribe: vị trí hiện tại của robot (từ cartesian_streamer)
        self._current_pose_sub = self.create_subscription(
            PoseStamped,
            '/cartesian_streamer/current_pose',
            self._on_current_pose,
            10,
        )

        # Service: Capture initial pose for relative displacement
        self._capture_srv = self.create_service(
            Trigger,
            '/coord_transform/capture_init_pose',
            self._on_capture_init_pose
        )

    # ─── Callback ────────────────────────────────────────────────────────

    def _on_current_pose(self, msg: PoseStamped):
        """Lưu lại vị trí EE hiện tại để dùng cho việc setup điểm gốc (Relative Displacement)."""
        self._current_robot_pose = msg.pose

    def _on_capture_init_pose(self, request, response):
        """Cập nhật P_init (t_cam_to_base) và ee_orient bằng vị trí robot hiện tại."""
        if self._current_robot_pose is None:
            response.success = False
            response.message = "Chưa nhận được vị trí hiện tại của robot từ /cartesian_streamer/current_pose"
            self.get_logger().warn(response.message)
            return response

        # Cập nhật t_cam_to_base
        pos = self._current_robot_pose.position
        self._t_cam_to_base = np.array([pos.x, pos.y, pos.z])
        
        # Cập nhật orientation
        ori = self._current_robot_pose.orientation
        self._ee_orient = [ori.x, ori.y, ori.z, ori.w]

        # Reset object offset về 0 (vì dùng relative displacement)
        self._obj_offset = np.array([0.0, 0.0, 0.0])

        msg = (f"Captured Init Pose! P_init=({pos.x:.3f}, {pos.y:.3f}, {pos.z:.3f}), "
               f"Orientation=({ori.x:.3f}, {ori.y:.3f}, {ori.z:.3f}, {ori.w:.3f})")
        self.get_logger().info(msg)
        
        response.success = True
        response.message = msg
        return response

    def _on_run_status(self, msg: Bool):
        self._running = msg.data
        status_str = "RUNNING" if self._running else "STOPPED"
        self.get_logger().info(f'Trạng thái tracking: {status_str}')

    def _on_mode(self, msg: String):
        self._mode = msg.data
        self.get_logger().info(f'Đã chuyển mode: {self._mode}')

    def _on_hand_state(self, msg: HandState):
        """Xử lý HandState khi mode = ground_truth"""
        if self._mode != 'ground_truth':
            return
        if not msg.is_tracked:
            return
            
        p_cam = np.array([msg.x, msg.y, msg.z])
        self._process_and_publish(p_cam)

    def _on_prediction(self, msg: HandPrediction):
        """Xử lý HandPrediction khi mode = prediction"""
        if self._mode != 'prediction':
            return

        # Lấy tọa độ theo prediction_step
        if hasattr(msg, 'pred_x') and len(msg.pred_x) > 0:
            step = min(self._pred_step, len(msg.pred_x) - 1)
            p_cam = np.array([msg.pred_x[step], msg.pred_y[step], msg.pred_z[step]])
        else:
            p_cam = np.array([msg.x, msg.y, msg.z])
            
        self._process_and_publish(p_cam)

    def _process_and_publish(self, p_cam: np.ndarray):
        """Hàm dùng chung để clamp và tính pose đích"""
        if not self._running:
            return

        # Bước 1: Kiểm tra tọa độ hợp lệ (không phải NaN/Inf)
        if not np.all(np.isfinite(p_cam)):
            self.get_logger().warn(
                f'Tọa độ không hợp lệ: {p_cam}',
                throttle_duration_sec=1.0,
            )
            return

        # Bước 2: Thêm object offset (Thường = 0 nếu dùng Relative Displacement)
        p_cam_obj = p_cam + self._obj_offset

        # Bước 3: Transform sang robot base frame
        # P_target = R * displacement + P_init
        p_base = self._R_cam_to_base @ p_cam_obj + self._t_cam_to_base

        # Bước 4: Safety clamp — giới hạn trong workspace robot
        p_clamped, was_clamped = self._clamp_to_workspace(p_base)
        if was_clamped:
            self.get_logger().warn(
                f'Tọa độ bị clamp: {p_base} → {p_clamped}',
                throttle_duration_sec=1.0,
            )

        # Bước 5: Tạo và publish PoseStamped
        target = PoseStamped()
        target.header.frame_id = 'base_link'
        target.header.stamp = self.get_clock().now().to_msg()
        target.pose.position.x = float(p_clamped[0])
        target.pose.position.y = float(p_clamped[1])
        target.pose.position.z = float(p_clamped[2])
        target.pose.orientation.x = float(self._ee_orient[0])
        target.pose.orientation.y = float(self._ee_orient[1])
        target.pose.orientation.z = float(self._ee_orient[2])
        target.pose.orientation.w = float(self._ee_orient[3])

        self._target_pub.publish(target)
        self._debug_pub.publish(target)

        self.get_logger().info(
            f'[{self._mode.upper()}] Transform: cam{p_cam.round(3)} → base{p_clamped.round(3)}',
            throttle_duration_sec=2.0,
        )

    def _clamp_to_workspace(self, p: np.ndarray):
        """Clamp điểm vào workspace an toàn. Trả về (p_clamped, was_clamped)."""
        p_c = np.array([
            np.clip(p[0], self._ws_x[0], self._ws_x[1]),
            np.clip(p[1], self._ws_y[0], self._ws_y[1]),
            np.clip(p[2], self._ws_z[0], self._ws_z[1]),
        ])
        was_clamped = not np.allclose(p, p_c)
        return p_c, was_clamped


def main(args=None):
    rclpy.init(args=args)
    node = CoordTransformNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
