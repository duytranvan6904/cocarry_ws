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
from collections import deque

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Point, Quaternion
from std_msgs.msg import String, Bool
from human_hand_msgs.msg import HandPrediction, HandState
from std_srvs.srv import Trigger
# Publish filtered coords to UI
from geometry_msgs.msg import PointStamped



class CameraFilterState:
    def __init__(self, median_size):
        from collections import deque
        self.last_raw_p_cam = None
        self.outlier_count = 0
        self.median_buffer_y = deque(maxlen=median_size)
        self.recent_buffer = deque(maxlen=15)
        self.smoothed_p_cam = None
        self.is_holding_position = False
        self.hold_p_cam = None
        self.stationary_counter = 0
        self.last_moving_p_cam = None

    def reset(self):
        self.last_raw_p_cam = None
        self.outlier_count = 0
        self.median_buffer_y.clear()
        self.recent_buffer.clear()
        self.smoothed_p_cam = None
        self.is_holding_position = False
        self.hold_p_cam = None
        self.stationary_counter = 0
        self.last_moving_p_cam = None

class CoordTransformNode(Node):


    def __init__(self):
        super().__init__('coord_transform')
        self._declare_all_params()
        self._load_params()
        self._setup_pubsub()
        self._current_robot_pose = None  # To store the latest EE pose
        self._mode = 'ground_truth'      # Default mode
        self._running = False            # Whether to forward data
        self._last_p_cam = None          # Lưu tọa độ tay thô mới nhất từ camera
        self._p_cam_init = None          # Lưu tọa độ tay thô tại thời điểm bấm Calibrate
        self._last_p_base = None         # Lưu tọa độ target gần nhất (rate-limiting)
        
        # Dynamic Deadband (chống nhiễu rung tay) — params loaded from YAML
        self._calib_buffer = deque(maxlen=40)  # 2s ở 20fps cho calibration
        self._recent_buffer = deque(maxlen=15)  # ~0.75s ở 20fps, đủ lớn để lọc noise camera
        self._noise_tolerance = 0.005          # Sẽ được cập nhật lúc calib
        self._is_holding_position = False
        self._moving_deadzone_tol = self._filter_deadband_depth_tol
        self._stationary_threshold = self._filter_stationary_threshold
        # Ngưỡng Y (camera frame sau median) để kích hoạt deadband B tại vùng đích
        self._deadband_y_threshold = self._filter_deadband_y_threshold
        # Ngưỡng std tối đa khi tay đứng yên tại đích (lớn hơn để dừng chắc)
        self._moving_deadzone_tol_near_target = self._filter_deadband_near_target_tol
        
        # Tạo 2 filter state riêng biệt cho ground_truth (UI vẽ) và prediction (robot chạy)
        self._actual_filter = CameraFilterState(self._filter_median_size_y)
        self._pred_filter = CameraFilterState(self._filter_median_size_y)
        
        # Target Snap state: theo dõi xem snap có đang được áp dụng không
        self._pred_snap_active = False

        # Target Zone Auto-Snap state
        self._tz_counters      = [0, 0, 0]   # frame counter cho mỗi target zone
        self._tz_snapping      = False        # đang trong phase snap (override target)
        self._tz_snap_idx      = -1           # index của zone đang snap
        self._tz_snap_start_ns = 0            # thời điểm bắt đầu snap
        
        self.get_logger().info(
            'CoordTransformNode khởi động.\n'
            f'  Object offset (cam frame): {self._obj_offset}\n'
            f'  Translation cam→base:      {self._t_cam_to_base}\n'
            f'  EE orientation (xyzw):     {self._ee_orient}\n'
            f'  Prediction step:           {self._pred_step}\n'
            f'  Axis remap:                {self._axis_remap}\n'
            f'  Axis sign:                 {self._axis_sign}\n'
            f'  Workspace X: {self._ws_x}, Y: {self._ws_y}, Z: {self._ws_z}\n'
            f'  Filter outlier_threshold:  {self._filter_outlier_threshold}m\n'
            f'  Filter median_size_y:      {self._filter_median_size_y}\n'
            f'  Filter deadband_tol:       {self._filter_deadband_depth_tol*1000:.1f}mm\n'
            f'  Filter stationary_thresh:  {self._filter_stationary_threshold} frames\n'
            f'  Filter max_rate:           {self._filter_max_rate*100:.1f}cm/frame\n'
            f'  Filter EMA moving(x,y,z):  ({self._filter_ema_x_moving},{self._filter_ema_y_moving},{self._filter_ema_z_moving})\n'
            f'  Filter EMA hold  (x,y,z):  ({self._filter_ema_x_hold},{self._filter_ema_y_hold},{self._filter_ema_z_hold})'
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
        self.declare_parameter('prediction_step', 5)

        # Workspace safety bounds (robot base frame, meters)
        self.declare_parameter('workspace_x_min', -1.0)
        self.declare_parameter('workspace_x_max',  1.0)
        self.declare_parameter('workspace_y_min', -0.5)
        self.declare_parameter('workspace_y_max',  1.3)
        self.declare_parameter('workspace_z_min',  0.05)
        self.declare_parameter('workspace_z_max',  1.5)

        # Axis remap
        self.declare_parameter('axis_remap', [0, 1, 2])
        self.declare_parameter('axis_sign', [-1.0, 1.0, 1.0])

        # ── Filter Parameters (tất cả có thể ghi đè qua YAML) ────────────
        self.declare_parameter('filter.outlier_threshold',    0.15)
        self.declare_parameter('filter.median_size_y',        3)
        self.declare_parameter('filter.deadband_depth_tol',   0.015)
        self.declare_parameter('filter.stationary_threshold', 3)
        self.declare_parameter('filter.max_rate',             0.05)
        self.declare_parameter('filter.ema_x_moving',         0.75)
        self.declare_parameter('filter.ema_y_moving',         0.5)
        self.declare_parameter('filter.ema_z_moving',         0.75)
        self.declare_parameter('filter.ema_x_hold',           0.08)
        self.declare_parameter('filter.ema_y_hold',           0.02)
        self.declare_parameter('filter.ema_z_hold',           0.05)
        # Target Snap: khoảng cách tối đa (m) để snap prediction về actual hand khi tay đứng yên
        # 0.10 = 10cm — đủ lớn để bắt overshoot GRU thông thường, đủ nhỏ để không trigger khi đang di chuyển
        self.declare_parameter('filter.pred_snap_radius',     0.10)

        # Ngưỡng Y (camera frame, đã qua median filter) để kích hoạt deadband dừng (meters)
        # Khi tay chưa vượt ngưỡng này → không áp dụng deadband B (robot xuất phát ngay)
        # Khi tay đã vượt ngưỡng → áp dụng deadband với tol cao hơn để dừng chắc tại đích
        self.declare_parameter('filter.deadband_y_threshold',      0.30)
        self.declare_parameter('filter.deadband_near_target_tol',  0.025)

        # ── Target Zone Auto-Snap ──────────────────────────────────────────
        self.declare_parameter('target_zones.enabled',            True)
        self.declare_parameter('target_zones.snap_radius',        0.08)
        self.declare_parameter('target_zones.snap_frames',        20)
        self.declare_parameter('target_zones.snap_duration_sec',  1.5)
        self.declare_parameter('target_zones.t1_x', 0.0)
        self.declare_parameter('target_zones.t1_y', 0.8)
        self.declare_parameter('target_zones.t1_z', 0.5)
        self.declare_parameter('target_zones.t2_x', 0.2)
        self.declare_parameter('target_zones.t2_y', 0.8)
        self.declare_parameter('target_zones.t2_z', 0.5)
        self.declare_parameter('target_zones.t3_x', -0.2)
        self.declare_parameter('target_zones.t3_y', 0.8)
        self.declare_parameter('target_zones.t3_z', 0.5)

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

        # Axis remap
        self._axis_remap = list(self.get_parameter('axis_remap').value)
        self._axis_sign = list(self.get_parameter('axis_sign').value)

        # Filter params
        self._filter_outlier_threshold    = self.get_parameter('filter.outlier_threshold').value
        self._filter_median_size_y        = int(self.get_parameter('filter.median_size_y').value)
        self._filter_deadband_depth_tol   = self.get_parameter('filter.deadband_depth_tol').value
        self._filter_stationary_threshold = int(self.get_parameter('filter.stationary_threshold').value)
        self._filter_max_rate             = self.get_parameter('filter.max_rate').value
        self._filter_ema_x_moving         = self.get_parameter('filter.ema_x_moving').value
        self._filter_ema_y_moving         = self.get_parameter('filter.ema_y_moving').value
        self._filter_ema_z_moving         = self.get_parameter('filter.ema_z_moving').value
        self._filter_ema_x_hold           = self.get_parameter('filter.ema_x_hold').value
        self._filter_ema_y_hold           = self.get_parameter('filter.ema_y_hold').value
        self._filter_ema_z_hold           = self.get_parameter('filter.ema_z_hold').value
        self._filter_pred_snap_radius     = self.get_parameter('filter.pred_snap_radius').value
        self._filter_deadband_y_threshold     = self.get_parameter('filter.deadband_y_threshold').value
        self._filter_deadband_near_target_tol = self.get_parameter('filter.deadband_near_target_tol').value

        # Target Zone params
        self._tz_enabled     = self.get_parameter('target_zones.enabled').value
        self._tz_snap_radius = self.get_parameter('target_zones.snap_radius').value
        self._tz_snap_frames = int(self.get_parameter('target_zones.snap_frames').value)
        self._tz_snap_dur    = self.get_parameter('target_zones.snap_duration_sec').value
        self._target_zones = [
            np.array([
                self.get_parameter('target_zones.t1_x').value,
                self.get_parameter('target_zones.t1_y').value,
                self.get_parameter('target_zones.t1_z').value,
            ]),
            np.array([
                self.get_parameter('target_zones.t2_x').value,
                self.get_parameter('target_zones.t2_y').value,
                self.get_parameter('target_zones.t2_z').value,
            ]),
            np.array([
                self.get_parameter('target_zones.t3_x').value,
                self.get_parameter('target_zones.t3_y').value,
                self.get_parameter('target_zones.t3_z').value,
            ]),
        ]

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

        # Publish: tọa độ tay ĐÃ LỌC (camera frame) để UI vẽ thay vì raw
        # Format: PointStamped với x/y/z là tọa độ camera sau khi qua toàn bộ filter
        self._filtered_hand_pub = self.create_publisher(
            PointStamped,
            '/coord_transform/filtered_hand_position',
            10,
        )

        # Publish: tọa độ tay thực tế (base frame) dùng cho adaptive control
        self._hand_base_pub = self.create_publisher(
            PoseStamped,
            '/cartesian_streamer/hand_base_pose',
            10,
        )

        # Publish: trạng thái node (để UI theo dõi)
        self._status_pub = self.create_publisher(
            String,
            '/coord_transform/status',
            10,
        )

        # Publish: run_status để auto-stop UI khi target zone snap hoàn tất
        self._run_status_pub = self.create_publisher(Bool, '/run_status', 5)

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

        if len(self._calib_buffer) < 10:
            if self._last_p_cam is None:
                self._p_cam_init = np.array([0.0, 0.0, 0.0])
                self.get_logger().warn("Chưa đủ dữ liệu camera! Dùng [0,0,0] làm mốc.")
                self._noise_tolerance = 0.005 # Default 5mm
            else:
                self._p_cam_init = self._last_p_cam.copy()
                self._noise_tolerance = 0.005 # Default 5mm
        else:
            calib_data = np.array(self._calib_buffer)
            self._p_cam_init = np.mean(calib_data, axis=0)
            std_dev = np.std(calib_data, axis=0)
            self._noise_tolerance = np.max(std_dev) * 4.0
            
            # Giới hạn dung sai trong khoảng 5mm -> 6cm
            # Camera depth noise thực tế lên tới 50mm, cần headroom đủ lớn
            self._noise_tolerance = np.clip(self._noise_tolerance, 0.005, 0.06)
            
        # Reset trạng thái cho các bộ lọc
        self._actual_filter.reset()
        self._pred_filter.reset()
        
        self._actual_filter.smoothed_p_cam = self._p_cam_init.copy()
        self._actual_filter.hold_p_cam = self._p_cam_init.copy()
        self._actual_filter.is_holding_position = True
        
        self._pred_filter.smoothed_p_cam = self._p_cam_init.copy()
        self._pred_filter.hold_p_cam = self._p_cam_init.copy()
        self._pred_filter.is_holding_position = True

        msg = (f"Captured Init Pose! P_init=({pos.x:.3f}, {pos.y:.3f}, {pos.z:.3f}), "
               f"Cam_init=({self._p_cam_init[0]:.3f}, {self._p_cam_init[1]:.3f}, {self._p_cam_init[2]:.3f}), "
               f"Noise_Tol={self._noise_tolerance*1000:.1f}mm\n"
               f"Orientation=({ori.x:.3f}, {ori.y:.3f}, {ori.z:.3f}, {ori.w:.3f})")
        self.get_logger().info(msg)
        
        response.success = True
        response.message = msg
        return response

    def _on_run_status(self, msg: Bool):
        was_running = self._running
        self._running = msg.data
        
        if self._running and not was_running:
            # Re-sync: cập nhật mốc camera về vị trí tay HIỆN TẠI
            if self._last_p_cam is not None and self._p_cam_init is not None:
                self._p_cam_init = self._last_p_cam.copy()
                self._last_p_base = None  # Reset rate-limiter
                
                # Reset và cập nhật mốc cho bộ lọc mới
                self._actual_filter.reset()
                self._pred_filter.reset()
                
                self._actual_filter.smoothed_p_cam = self._last_p_cam.copy()
                self._actual_filter.hold_p_cam = self._last_p_cam.copy()
                self._actual_filter.is_holding_position = True
                
                self._pred_filter.smoothed_p_cam = self._last_p_cam.copy()
                self._pred_filter.hold_p_cam = self._last_p_cam.copy()
                self._pred_filter.is_holding_position = True

                self.get_logger().info(
                    f'Re-sync camera init: {self._p_cam_init.round(3)}')

        status_str = "RUNNING" if self._running else "STOPPED"
        self.get_logger().info(f'Trạng thái tracking: {status_str}')

    def _on_mode(self, msg: String):
        new_mode = msg.data.strip().lower()
        if new_mode != self._mode:
            self.get_logger().info(f'Đã chuyển mode: {self._mode} -> {new_mode}')
            self._mode = new_mode
            # Full reset state để tránh kế thừa trạng thái cũ giữa các mode
            self._actual_filter.reset()
            self._pred_filter.reset()

    def _on_hand_state(self, msg: HandState):
        """Xử lý HandState cho cả 2 mode để luôn cập nhật quỹ đạo thực tế (UI)"""
        if not msg.is_tracked:
            return
            
        p_cam = np.array([msg.x, msg.y, msg.z])
        self._last_p_cam = p_cam
        self._calib_buffer.append(p_cam)
        
        # Lọc quỹ đạo thực tế
        p_cam_filtered = self._apply_filter(p_cam, self._actual_filter)
        if p_cam_filtered is None:
            return
            
        # Luôn publish quỹ đạo thực tế đã lọc để UI vẽ (Actual)
        filtered_pt = PointStamped()
        filtered_pt.header.frame_id = 'camera_frame'
        filtered_pt.header.stamp = self.get_clock().now().to_msg()
        filtered_pt.point.x = float(p_cam_filtered[0])
        filtered_pt.point.y = float(p_cam_filtered[1])
        filtered_pt.point.z = float(p_cam_filtered[2])
        self._filtered_hand_pub.publish(filtered_pt)
        
        # Publish hand base pose for adaptive control
        if self._p_cam_init is not None:
            p_cam_delta = p_cam_filtered - self._p_cam_init + self._obj_offset
            remap = self._axis_remap
            signs = self._axis_sign
            p_remapped = np.array([
                signs[0] * p_cam_delta[remap[0]],
                signs[1] * p_cam_delta[remap[1]],
                signs[2] * p_cam_delta[remap[2]],
            ])
            p_base = self._R_cam_to_base @ p_remapped + self._t_cam_to_base
            p_clamped, _ = self._clamp_to_workspace(p_base)
            
            hand_msg = PoseStamped()
            hand_msg.header.frame_id = 'base_link'
            hand_msg.header.stamp = self.get_clock().now().to_msg()
            hand_msg.pose.position.x = float(p_clamped[0])
            hand_msg.pose.position.y = float(p_clamped[1])
            hand_msg.pose.position.z = float(p_clamped[2])
            hand_msg.pose.orientation.x = float(self._ee_orient[0])
            hand_msg.pose.orientation.y = float(self._ee_orient[1])
            hand_msg.pose.orientation.z = float(self._ee_orient[2])
            hand_msg.pose.orientation.w = float(self._ee_orient[3])
            self._hand_base_pub.publish(hand_msg)
        
        # Nếu đang ở ground_truth, dùng quỹ đạo này điều khiển robot
        if self._mode == 'ground_truth':
            self._transform_and_publish_target(p_cam_filtered)

    def _on_prediction(self, msg: HandPrediction):
        """Xử lý HandPrediction khi mode = prediction hoặc ergonomics"""
        if self._mode not in ['prediction', 'ergonomics']:
            return

        # Lấy tọa độ theo prediction_step
        if hasattr(msg, 'pred_x') and len(msg.pred_x) > 0:
            step = min(self._pred_step, len(msg.pred_x) - 1)
            p_cam = np.array([msg.pred_x[step], msg.pred_y[step], msg.pred_z[step]])
        else:
            p_cam = np.array([msg.x, msg.y, msg.z])
            
        # Lọc quỹ đạo dự đoán bằng state riêng
        p_cam_filtered = self._apply_filter(p_cam, self._pred_filter)
        if p_cam_filtered is None:
            return

        # ─── TARGET SNAP (Bắt dính mục tiêu) ─────────────────────────────────
        # Khi tay người dùng đã được xác nhận đứng yên (actual_filter đang HOLD),
        # lập tức ép điểm dự đoán về đúng vị trí tay thực tế để dừng robot ngay lập tức.
        # Bỏ qua khoảng cách lệch của GRU vì tốc độ hội tụ GRU khá chậm.
        if (self._actual_filter.is_holding_position and
                self._actual_filter.hold_p_cam is not None):
            actual_hold = self._actual_filter.hold_p_cam
            dist_pred_to_actual = np.linalg.norm(p_cam_filtered - actual_hold)
            
            if not self._pred_snap_active:
                self.get_logger().info(
                    f'[SNAP ON] Tay thực tế đứng yên. Ép dừng robot (GRU đang lệch {dist_pred_to_actual*100:.1f}cm).',
                    throttle_duration_sec=1.0
                )
                self._pred_snap_active = True
            p_cam_filtered = actual_hold.copy()
        else:
            # Tay đang di chuyển → không snap, chạy theo GRU prediction
            if self._pred_snap_active:
                self.get_logger().info('[SNAP OFF] Tay di chuyển lại. Trả quyền cho GRU.')
                self._pred_snap_active = False
        # ─────────────────────────────────────────────────────────────────────

        self._transform_and_publish_target(p_cam_filtered)

    def _apply_filter(self, p_cam: np.ndarray, state: CameraFilterState):
        """Hàm dùng chung để áp dụng các bộ lọc (outlier, median, deadband, EMA)"""
        if not np.all(np.isfinite(p_cam)):
            self.get_logger().warn(
                f'Tọa độ không hợp lệ: {p_cam}',
                throttle_duration_sec=1.0,
            )
            return None

        # ─── Outlier Rejection (Loại bỏ đỉnh nhọn) ─────────
        if state.last_raw_p_cam is not None:
            deviation_from_last = np.linalg.norm(p_cam - state.last_raw_p_cam)
            if deviation_from_last > self._filter_outlier_threshold:
                state.outlier_count += 1
                if state.outlier_count < 5:
                    self.get_logger().warn(f'Outlier rejected #{state.outlier_count} (jumped {deviation_from_last*1000:.1f}mm). Ignoring.')
                    return None
                else:
                    self.get_logger().info(f'Too many outliers ({state.outlier_count}). Resetting filter to new position.')
                    state.outlier_count = 0
            else:
                state.outlier_count = 0
        
        state.last_raw_p_cam = p_cam.copy()

        # ─── Median Pre-filter cho trục Y (depth, nhiễu nhất) ────
        state.median_buffer_y.append(p_cam[1])
        min_median = max(3, self._filter_median_size_y // 2 + 1)  # ít nhất 3 mẫu
        if len(state.median_buffer_y) >= min_median:
            p_cam = p_cam.copy()
            p_cam[1] = float(np.median(state.median_buffer_y))

        # ─── Dynamic Deadband Logic ─────────────────────────
        state.recent_buffer.append(p_cam)
        
        should_hold = state.is_holding_position
        hold_position = state.hold_p_cam.copy() if state.hold_p_cam is not None else None

        if len(state.recent_buffer) >= 5:
            recent_data = np.array(state.recent_buffer)
            mean_pos = np.mean(recent_data, axis=0)

            # Y sau khi lọc median (index 1 của p_cam trong camera frame = depth)
            # Theo axis_remap [0,1,2] và axis_sign [−1,1,1], Y robot ≈ Y camera.
            # Chỉ áp dụng deadband khi tay đã vượt ngưỡng Y đặt trước.
            y_current = float(mean_pos[1])
            deadband_active = (y_current >= self._deadband_y_threshold)

            # (A) Initial deadband: tay ở gần vị trí calibrate — luôn áp dụng bất kể Y
            if self._p_cam_init is not None and not should_hold:
                deviation_from_init = np.linalg.norm(mean_pos - self._p_cam_init)
                if deviation_from_init < self._noise_tolerance:
                    should_hold = True
                    hold_position = self._p_cam_init.copy()
            
            if not should_hold and deadband_active:
                # (B) Moving deadband: chỉ kích hoạt khi tay đã vào vùng đích (Y >= threshold)
                # Dùng ngưỡng std cao hơn (2.5cm) để dừng chắc chắn tại đích.
                recent_std = np.std(recent_data, axis=0)
                max_std = float(np.max(recent_std))

                # Dùng _moving_deadzone_tol_near_target (0.025) khi đã đến vùng đích
                tol = self._moving_deadzone_tol_near_target
                if max_std < tol:
                    state.stationary_counter += 1
                else:
                    state.stationary_counter = 0
                    state.last_moving_p_cam = p_cam.copy()

                if state.stationary_counter >= self._filter_stationary_threshold:
                    should_hold = True
                    hold_position = mean_pos.copy()
            elif not deadband_active and not should_hold:
                # Chưa đến vùng đích → không giữ, reset counter để robot xuất phát sớm
                state.stationary_counter = 0

        # Force release if hand deviates too far from locked position
        if state.is_holding_position and state.hold_p_cam is not None:
            check_pos = mean_pos if 'mean_pos' in locals() else p_cam
            dev_from_locked = np.linalg.norm(check_pos - state.hold_p_cam)
            if dev_from_locked > 0.050:  # 5.0cm release threshold (chống nhiễu, rung tay khi mang tải)
                should_hold = False

        if should_hold:
            if not state.is_holding_position:
                state.is_holding_position = True
                state.hold_p_cam = hold_position.copy() if hold_position is not None else p_cam.copy()
                self.get_logger().info(
                    f'Deadband: HOLD at ({state.hold_p_cam[0]:.3f}, {state.hold_p_cam[1]:.3f}, {state.hold_p_cam[2]:.3f})',
                    throttle_duration_sec=2.0)
        else:
            if state.is_holding_position:
                self.get_logger().info(
                    f'Deadband: RELEASE — motion detected',
                    throttle_duration_sec=2.0)
            state.is_holding_position = False
            state.stationary_counter = 0

        # Fix #1: Khi HOLD → bypass EMA hoàn toàn, gán cứng smoothed = hold_p_cam
        # Tránh micro-delta liên tục do EMA hội tụ (0.1-0.4mm/frame) gây robot rung.
        if state.is_holding_position and state.hold_p_cam is not None:
            state.smoothed_p_cam = state.hold_p_cam.copy()
            return state.smoothed_p_cam.copy()  # Trả về BẢN SAO

        # Moving: dùng mean_pos hoặc p_cam gốc
        target_p_cam = mean_pos.copy() if 'mean_pos' in locals() else p_cam.copy()

        if state.smoothed_p_cam is None:
            state.smoothed_p_cam = target_p_cam.copy()
        else:
            alpha_x = self._filter_ema_x_moving
            alpha_y = self._filter_ema_y_moving
            alpha_z = self._filter_ema_z_moving

            state.smoothed_p_cam[0] = alpha_x * target_p_cam[0] + (1.0 - alpha_x) * state.smoothed_p_cam[0]
            state.smoothed_p_cam[1] = alpha_y * target_p_cam[1] + (1.0 - alpha_y) * state.smoothed_p_cam[1]
            state.smoothed_p_cam[2] = alpha_z * target_p_cam[2] + (1.0 - alpha_z) * state.smoothed_p_cam[2]

        return state.smoothed_p_cam.copy()  # Fix #1: LUÔN trả về bản sao

    def _transform_and_publish_target(self, p_cam_to_use: np.ndarray):
        """Tính toán target pose từ p_cam đã lọc và gửi xuống robot"""
        if self._p_cam_init is None or not self._running:
            self.get_logger().debug(
                f'Skip robot target: p_cam_init={self._p_cam_init is not None}, running={self._running}',
                throttle_duration_sec=2.0)
            return

        # Bước 2: Lấy độ dời tương đối từ camera, cộng thêm object offset
        p_cam_delta = p_cam_to_use - self._p_cam_init + self._obj_offset

        # Bước 2.5: Axis remap (camera frame → robot frame trước khi xoay)
        remap = self._axis_remap
        signs = self._axis_sign
        p_remapped = np.array([
            signs[0] * p_cam_delta[remap[0]],
            signs[1] * p_cam_delta[remap[1]],
            signs[2] * p_cam_delta[remap[2]],
        ])

        # Bước 3: Transform sang robot base frame
        # P_target = R * displacement + P_init
        p_base = self._R_cam_to_base @ p_remapped + self._t_cam_to_base

        # Bước 4: Safety clamp — giới hạn trong workspace robot
        p_clamped, was_clamped = self._clamp_to_workspace(p_base)
        if was_clamped:
            self.get_logger().warn(
                f'Tọa độ bị clamp: {p_base} → {p_clamped}',
                throttle_duration_sec=1.0,
            )

        # Bước 4.5: Target Zone Auto-Snap — override nếu robot vào gần đích
        # CHỈ KÍCH HOẠT nếu tay đã hoàn toàn đứng yên theo logic deadband
        state = self._actual_filter if self._mode == 'ground_truth' else self._pred_filter
        snap_pos = self._check_target_zone_snap(p_clamped, state.is_holding_position)
        if snap_pos is not None:
            p_clamped = snap_pos

        # Bước 4.6: Rate-limiting — giới hạn bước nhảy tọa độ mỗi frame
        if self._last_p_base is not None:
            for i in range(3):
                delta = p_clamped[i] - self._last_p_base[i]
                if abs(delta) > self._filter_max_rate:
                    p_clamped[i] = self._last_p_base[i] + self._filter_max_rate * np.sign(delta)
        self._last_p_base = p_clamped.copy()

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
            f'[{self._mode.upper()}] Transform: cam{p_cam_to_use.round(3)} → base{p_clamped.round(3)}',
            throttle_duration_sec=2.0,
        )
    # ─── Target Zone Auto-Snap ────────────────────────────────────────────

    def _check_target_zone_snap(self, p_base: np.ndarray, is_holding: bool):
        """
        Kiểm tra EE robot có vào gần target zone không.
        Chỉ đếm frame nếu tay đã dừng hoàn toàn (is_holding = True).
        Trả về: pose override nếu đang snap, None nếu bình thường.
        """
        if not self._tz_enabled or not self._running:
            return None

        # Phase snap đang diễn ra — giữ pose cố định cho đến hết duration
        if self._tz_snapping:
            elapsed = (self.get_clock().now().nanoseconds - self._tz_snap_start_ns) / 1e9
            if elapsed < self._tz_snap_dur:
                return self._target_zones[self._tz_snap_idx].copy()
            else:
                # Snap hoàn tất → publish Stop Run
                self._tz_snapping = False
                stop_msg = Bool()
                stop_msg.data = False
                self._run_status_pub.publish(stop_msg)
                self.get_logger().info(
                    f'[TARGET ZONE] ✓ Đã đến T{self._tz_snap_idx + 1}. '
                    f'Auto Stop Run sau {self._tz_snap_dur:.1f}s hold.'
                )
                # Trả về pose cuối cùng (frame này robot vẫn ở đích)
                return self._target_zones[self._tz_snap_idx].copy()

        # NẾU TAY CHƯA ĐỨNG YÊN (CHƯA VÀO DEADBAND) -> Không làm gì cả
        if not is_holding:
            self._tz_counters = [0, 0, 0]
            return None

        # Kiểm tra khoảng cách EE đến từng zone
        for i, tz_pos in enumerate(self._target_zones):
            dist = np.linalg.norm(p_base - tz_pos)
            
            # Log hỗ trợ debug khi người dùng vào gần đích (trong vòng 30cm)
            if dist <= 0.30:
                if dist <= self._tz_snap_radius:
                    self._tz_counters[i] += 1
                    self.get_logger().info(
                        f'[TARGET ZONE] T{i + 1}: {dist * 100:.1f}cm '
                        f'(NẰM TRONG VÙNG! {self._tz_counters[i]}/{self._tz_snap_frames} frames)',
                        throttle_duration_sec=0.5
                    )
                    if self._tz_counters[i] >= self._tz_snap_frames:
                        # Kích hoạt snap!
                        self._tz_snapping = True
                        self._tz_snap_idx = i
                        self._tz_snap_start_ns = self.get_clock().now().nanoseconds
                        self._tz_counters = [0, 0, 0]  # reset tất cả
                        self.get_logger().info(
                            f'[TARGET ZONE] ★ SNAP vào T{i + 1}! '
                            f'Giữ pose {self._tz_snap_dur:.1f}s rồi auto-stop.'
                        )
                        return tz_pos.copy()
                else:
                    # Ngoài vùng snap (nhưng < 30cm) → decay counter, log báo hiệu
                    self._tz_counters[i] = max(0, self._tz_counters[i] - 1)
                    self.get_logger().info(
                        f'[TARGET ZONE] T{i + 1} ở gần: {dist * 100:.1f}cm '
                        f'(Cần đẩy thêm vào < {self._tz_snap_radius * 100:.1f}cm để snap)',
                        throttle_duration_sec=1.0
                    )
            else:
                self._tz_counters[i] = max(0, self._tz_counters[i] - 1)

        return None

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
