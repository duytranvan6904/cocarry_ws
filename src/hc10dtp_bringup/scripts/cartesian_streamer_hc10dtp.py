#!/usr/bin/env python3
"""
cartesian_streamer_hc10dtp.py
────────────────────────────
Nhận tọa độ Cartesian (PoseStamped) từ AI/Camera node,
giải IK và stream joint angles xuống MotoROS2
qua chế độ Point Queue Mode — phiên bản cho HC10DTP.

Quy trình khởi động (2 terminal):
  Terminal 1: ros2 launch hc10dtp_moveit_config hc10dtp_start.launch.py
              (khởi động: move_group, RViz, robot_state_publisher, restamp_joint_states)
  Terminal 2: python3 cartesian_streamer_hc10dtp.py --demo line

Lưu ý kiến trúc:
  MotoROS2 driver chạy trực tiếp trên YRC1000/YRC1000micro
  và tự expose các services (không namespace).

AI node gửi lệnh qua:
  /cartesian_streamer/target_pose  → geometry_msgs/PoseStamped
  hoặc
  /cartesian_streamer/target_xyz   → Float64MultiArray [x, y, z]
                                     (orientation giữ nguyên từ vị trí hiện tại)

Test tích hợp:
  python3 cartesian_streamer_hc10dtp.py --demo circle
  python3 cartesian_streamer_hc10dtp.py --demo line
  python3 cartesian_streamer_hc10dtp.py --demo lissajous
"""

import math
import threading
import argparse
import time as _time

import rclpy
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectoryPoint
from builtin_interfaces.msg import Duration

from moveit_msgs.srv import GetPositionIK, GetPositionFK
from moveit_msgs.msg import PositionIKRequest, RobotState
from motoros2_interfaces.srv import StartPointQueueMode, QueueTrajPoint, ResetError
from std_srvs.srv import Trigger, SetBool

# ── Hằng số ────────────────────────────────────────────────────────
JOINT_NAMES = [
    'joint_1_s', 'joint_2_l', 'joint_3_u',
    'joint_4_r', 'joint_5_b', 'joint_6_t'
]
GROUP_NAME   = 'hc10dtp_arm'
EE_LINK      = 'tool0'
BASE_FRAME   = 'base_link'

# Workspace an toàn (mét) — HC10DTP có tầm với 1.2m, điều chỉnh theo môi trường
WS_X = (-1.4,  1.4)
WS_Y = (-1.4,  1.4)
WS_Z = ( 0.05, 1.5)

# ── Tunable stream parameters ──────────────────────────────────────
# Tần suất stream tick (Hz). 20Hz là giá trị ổn định cho MotoROS2
# Tăng lên 50Hz để chuyển động mượt mà hơn (robot internal 100Hz)
DEFAULT_STREAM_HZ = 50

# Queue point duration: khoảng cách thời gian giữa mỗi điểm.
# Phải ≥ STREAM_PERIOD_SEC.
QUEUE_DT_SEC = 0.02  # ~50Hz motion rate cho HC10DTP
QUEUE_RETRY_BACKOFF_SEC = 0.02

# IK timeout
IK_TIMEOUT_SEC = 0.3

# Smooth: tỉ lệ tiến về target mỗi tick (0.0–1.0)
# 0.15 cho chuyển động rất mượt mà (cobot safety-first)
SMOOTH_ALPHA = 0.5

# An toàn: bước nhảy joint tối đa cho phép mỗi tick (rad) — PER JOINT
# Khớp thân (J1/J2/J3): quán tính lớn, cho phép delta rộng hơn
# Khớp cổ tay (J4/J5/J6): quán tính nhỏ, dễ flip → giới hạn chặt
# Khi vượt limit → CLAMP (không reject) để tránh death spiral
MAX_JOINT_DELTA_PER_AXIS = [
    0.20,   # J1 (S) — base rotation: ~11.5°/tick
    0.20,   # J2 (L) — lower arm:     ~11.5°/tick
    0.20,   # J3 (U) — upper arm:     ~11.5°/tick
    0.12,   # J4 (R) — wrist roll:    ~6.9°/tick (ngăn flip)
    0.12,   # J5 (B) — wrist pitch:   ~6.9°/tick (ngăn flip)
    0.12,   # J6 (T) — wrist twist:   ~6.9°/tick (ngăn flip)
]

# ── Giới hạn tốc độ Cartesian (Safety) ──────────────────────────
# Tốc độ tối đa End-Effector trong không gian Cartesian (m/s)
# ISO 10218-2 / ISO/TS 15066: collaborative speed limit thường 0.25 m/s
MAX_CARTESIAN_VELOCITY = 0.1     # m/s — rất chậm, an toàn cho thí nghiệm
MAX_CARTESIAN_ACCELERATION = 0.50 # m/s² — gia tốc tối đa, hạn chế giật

# Tốc độ góc tối đa cho mỗi khớp (rad/s) — PER JOINT
# Khớp cổ tay chậm hơn nhiều để ngăn quay nhanh gần người
MAX_JOINT_VELOCITIES = [
    0.30,   # J1 (S) — base rotation
    0.30,   # J2 (L) — lower arm
    0.30,   # J3 (U) — upper arm
    0.10,   # J4 (R) — wrist roll:  RẤT CHẬM
    0.10,   # J5 (B) — wrist pitch: RẤT CHẬM
    0.10,   # J6 (T) — wrist twist: RẤT CHẬM
]

# ── Soft Joint Limits cho co-carrying ────────────────────────────
# HOME_JOINTS = [1.5705, 0.0748, -1.0491, -0.0304, -0.5231, -0.0017]
# Tư thế: J1 quay ~90°, khuỷu tay hướng xuống, cổ tay gần neutral
# Giới hạn mỗi khớp quanh tư thế home, tránh cấu hình nguy hiểm (flip)
SOFT_JOINT_LIMITS = [
    (0.00,   3.14),    # J1 (S) — chỉ cho phép 0°~180° (hướng về phía người)
    (-0.80,  1.20),    # J2 (L) — -45°~70° quanh home (0.07)
    (-2.00,  1.05),    # J3 (U) — -115°~60° quanh home (-1.05), khuỷu xuống
    (-1.05,  1.05),    # J4 (R) — ±60° quanh center (ngăn wrist roll flip)
    (-2.09,  0.52),    # J5 (B) — -120°~30° quanh home (-0.52)
    (-1.05,  1.05),    # J6 (T) — ±60° quanh center (ngăn wrist twist flip)
]

# Debug watchdog: nếu queue point được accept nhưng joint gần như đứng yên
NO_MOTION_WARN_SEC = 5.0
NO_MOTION_EPS_RAD = 1e-3
NO_MOTION_MIN_ACCEPTED_POINTS = 10
QUEUE_PREBUFFER_POINTS = 3
STREAM_STATE_IDLE = 'idle'
STREAM_STATE_SEEDING = 'seeding'
STREAM_STATE_PREBUFFERING = 'prebuffering'
STREAM_STATE_STREAMING = 'streaming'


class CartesianStreamer(Node):

    def __init__(
        self,
        stream_hz: float = DEFAULT_STREAM_HZ,
        queue_dt_sec: float = QUEUE_DT_SEC,
        prebuffer_points: int = QUEUE_PREBUFFER_POINTS,
        retry_backoff_sec: float = QUEUE_RETRY_BACKOFF_SEC,
        auto_enable: bool = False,
    ):
        super().__init__('cartesian_streamer')
        self._stream_hz = stream_hz
        self._stream_period_sec = 1.0 / stream_hz
        self._auto_enable = auto_enable

        self._cb = ReentrantCallbackGroup()

        # ── State ────────────────────────────────────────────────
        self._current_joints: list[float] = [0.0] * 6
        self._got_joints = False
        self._queue_mode_active = False
        self._stream_state = STREAM_STATE_IDLE
        self._queue_call_inflight = False
        self._accepted_points = 0
        self._queue_debug_log_count = 0
        self._active_queue_service_name = ''
        self._pending_point_to_resend: JointTrajectoryPoint | None = None
        self._last_queued_joints: list[float] = [0.0] * 6
        self._queue_dt_sec = max(queue_dt_sec, 0.01)
        self._prebuffer_target = max(prebuffer_points, 1)
        self._retry_backoff_sec = max(retry_backoff_sec, 0.0)
        self._accepted_since_seed = 0
        self._seed_request_sent = False
        # time_from_start phải tích lũy (cumulative) từ seed point.
        # MotoROS2 dùng cumulative timestamp.
        self._cumulative_time_ns: int = 0
        # Lock bảo vệ _queue_call_inflight khỏi race condition
        self._send_lock = threading.Lock()
        self._next_send_not_before_ns = self.get_clock().now().nanoseconds
        self._last_motion_time = self.get_clock().now()
        self._last_warn_time = self.get_clock().now()
        self._tick_count = 0
        self._queue_sent_count = 0
        self._rate_window_start = self.get_clock().now()
        self._window_ack_count = 0
        self._window_busy_count = 0
        self._window_retry_count = 0
        self._window_reject_count = 0
        self._window_max_joint_delta = 0.0
        self._last_ack_time = None
        self._window_ack_interval_sum = 0.0
        self._window_ack_interval_count = 0
        # Số hold-points liên tiếp đã gửi (không tính vào cumulative time)
        self._hold_point_count = 0
        self._auto_recovery_count = 0   # Đếm số lần auto-recovery queue mode
        self._recovery_in_progress = False  # Đang trong quá trình recovery

        # Target Cartesian pose (được smooth từng bước)
        self._target_pose: Pose | None = None
        self._last_target_update_ns = 0
        # Pose đang thực sự gửi (smooth intermediate)
        self._current_ee_pose: Pose | None = None
        
        self._last_smooth_time_ns = self.get_clock().now().nanoseconds
        self._prev_ee_velocity = [0.0, 0.0, 0.0]
        self._latest_ik_solution: list[float] | None = None
        self._ik_request_pending = False

        # IK failure counter — để phát hiện stuck
        self._ik_fail_count = 0
        self._last_ok_joints: list[float] = [0.0] * 6
        self._prev_joint_snapshot: list[float] = [0.0] * 6

        # ── Subscribers ──────────────────────────────────────────
        self._js_sub = self.create_subscription(
            JointState, '/joint_states',
            self._on_joint_state, 10, callback_group=self._cb)

        self._pose_sub = self.create_subscription(
            PoseStamped, '/cartesian_streamer/target_pose',
            self._on_target_pose, 10, callback_group=self._cb)

        # Convenience: chỉ gửi XYZ, orientation giữ nguyên
        self._xyz_sub = self.create_subscription(
            Float64MultiArray, '/cartesian_streamer/target_xyz',
            self._on_target_xyz, 10, callback_group=self._cb)

        # Publisher: vị trí EE hiện tại (để AI biết feedback)
        self._ee_pub = self.create_publisher(
            PoseStamped, '/cartesian_streamer/current_pose', 10)

        # ── Service clients ──────────────────────────────────────
        self._ik_cli = self.create_client(
            GetPositionIK, '/compute_ik', callback_group=self._cb)

        self._start_queue_cli = self.create_client(
            StartPointQueueMode, '/start_point_queue_mode',
            callback_group=self._cb)
        self._queue_point_cli = self.create_client(
            QueueTrajPoint, '/queue_traj_point',
            callback_group=self._cb)
        self._queue_point_cli_alt = self.create_client(
            QueueTrajPoint, '/queue_point',
            callback_group=self._cb)

        self._stop_traj_cli = self.create_client(
            Trigger, '/stop_traj_mode',
            callback_group=self._cb)

        self._fk_cli = self.create_client(
            GetPositionFK, '/compute_fk', callback_group=self._cb)

        self._reset_error_cli = self.create_client(
            ResetError, '/reset_error', callback_group=self._cb)

        # ── Services (enable / disable từ UI) ────────────────────
        self.create_service(
            SetBool, '/cartesian_streamer/enable',
            self._srv_enable, callback_group=self._cb)

        # ── Timers ───────────────────────────────────────────────
        self._stream_timer = self.create_timer(
            self._stream_period_sec, self._stream_tick, callback_group=self._cb)

        # Chỉ chờ joint_states, KHÔNG tự động enable robot.
        self._startup_timer = self.create_timer(
            0.5, self._wait_for_joints, callback_group=self._cb)

        self.get_logger().info(
            'CartesianStreamer khởi động (chờ Enable Robot từ UI).\n'
            f'  Stream rate:       {self._stream_hz:.0f} Hz (period={self._stream_period_sec*1000:.1f}ms)\n'
            f'  Queue dt:          {self._queue_dt_sec:.3f} s\n'
            f'  Prebuffer points:  {self._prebuffer_target}\n'
            f'  Retry backoff:     {self._retry_backoff_sec*1000:.1f} ms\n'
            '  Gửi PoseStamped lên: /cartesian_streamer/target_pose\n'
            '  Gửi XYZ lên:        /cartesian_streamer/target_xyz\n'
            '  Nhận EE pose tại:   /cartesian_streamer/current_pose'
        )

    # ═══════════════════════════════════════════════════════════════
    # JOINT STATE CALLBACK
    # ═══════════════════════════════════════════════════════════════

    def _on_joint_state(self, msg: JointState):
        for i, name in enumerate(JOINT_NAMES):
            if name in msg.name:
                self._current_joints[i] = msg.position[msg.name.index(name)]
        if not self._got_joints:
            self._got_joints = True
            self._last_ok_joints = list(self._current_joints)
            self._prev_joint_snapshot = list(self._current_joints)
            self._last_queued_joints = list(self._current_joints)
            self.get_logger().info(
                'Nhận joint_states: '
                + str([f'{v:.3f}' for v in self._current_joints])
            )
            return

        max_joint_change = max(
            abs(a - b) for a, b in zip(self._current_joints, self._prev_joint_snapshot)
        )
        if max_joint_change > NO_MOTION_EPS_RAD:
            self._last_motion_time = self.get_clock().now()
        self._prev_joint_snapshot = list(self._current_joints)

    # ═══════════════════════════════════════════════════════════════
    # TARGET CALLBACKS
    # ═══════════════════════════════════════════════════════════════

    def _on_target_pose(self, msg: PoseStamped):
        """Nhận PoseStamped đầy đủ (position + orientation)."""
        if not self._queue_mode_active:
            return
        if not self._check_workspace(msg.pose.position):
            return
        self._target_pose = msg.pose
        self._last_target_update_ns = self.get_clock().now().nanoseconds

    def _on_target_xyz(self, msg: Float64MultiArray):
        """
        Nhận chỉ XYZ [x, y, z].
        Orientation được giữ nguyên từ vị trí hiện tại hoặc default.
        """
        if not self._queue_mode_active:
            return
        if len(msg.data) < 3:
            return
        pos = Point(x=msg.data[0], y=msg.data[1], z=msg.data[2])
        if not self._check_workspace(pos):
            return

        pose = Pose()
        pose.position = pos
        # Giữ orientation hiện tại nếu có, không thì dùng default (EE hướng xuống)
        if self._current_ee_pose is not None:
            pose.orientation = self._current_ee_pose.orientation
        else:
            pose.orientation = Quaternion(x=0.0, y=1.0, z=0.0, w=0.0)
        self._target_pose = pose
        self._last_target_update_ns = self.get_clock().now().nanoseconds

    def _check_workspace(self, pos: Point) -> bool:
        """Kiểm tra điểm nằm trong workspace an toàn."""
        ok = (WS_X[0] <= pos.x <= WS_X[1] and
              WS_Y[0] <= pos.y <= WS_Y[1] and
              WS_Z[0] <= pos.z <= WS_Z[1])
        if not ok:
            self.get_logger().warn(
                f'Ngoài workspace: ({pos.x:.3f}, {pos.y:.3f}, {pos.z:.3f})\n'
                f'  X: {WS_X}, Y: {WS_Y}, Z: {WS_Z}',
                throttle_duration_sec=1.0
            )
        return ok

    # ═══════════════════════════════════════════════════════════════
    # STARTUP
    # ═══════════════════════════════════════════════════════════════

    def _wait_for_joints(self):
        """Chỉ chờ joint_states, KHÔNG tự động enable robot."""
        if not self._got_joints:
            self.get_logger().info('Chờ /joint_states...', throttle_duration_sec=2.0)
            return
        self._startup_timer.cancel()

        # Tính FK để biết EE hiện tại, publish /cartesian_streamer/current_pose
        initial_pose = self._solve_fk_sync(list(self._current_joints))
        if initial_pose:
            self._current_ee_pose = initial_pose
            fb = PoseStamped()
            fb.header.frame_id = BASE_FRAME
            fb.header.stamp = self.get_clock().now().to_msg()
            fb.pose = initial_pose
            self._ee_pub.publish(fb)
            if self._auto_enable:
                self.get_logger().info(
                    f'Đã nhận joint_states. EE hiện tại: '
                    f'({initial_pose.position.x:.4f}, '
                    f'{initial_pose.position.y:.4f}, '
                    f'{initial_pose.position.z:.4f}). '
                    f'Auto-enable is ON. Tự động bật robot sau 1s...'
                )
                import threading
                threading.Timer(1.0, self._enable_step_1_reset_error).start()
            else:
                self.get_logger().info(
                    f'Đã nhận joint_states. EE hiện tại: '
                    f'({initial_pose.position.x:.4f}, '
                    f'{initial_pose.position.y:.4f}, '
                    f'{initial_pose.position.z:.4f}). '
                    f'Chờ Enable Robot từ UI...'
                )
        else:
            self.get_logger().info('Đã nhận joint_states nhưng giải FK thất bại.')

    # ── Enable / Disable services (gọi từ UI) ────────────────────

    def _srv_enable(self, request, response):
        """Service /cartesian_streamer/enable — bật/tắt robot."""
        if request.data:
            if self._queue_mode_active:
                response.success = True
                response.message = 'Robot đã enabled rồi'
                return response
            if not self._got_joints:
                response.success = False
                response.message = 'Chưa nhận được joint_states'
                return response
            # Bắt đầu chuỗi enable: reset_error → stop_traj → start_queue (servo tự động bật theo MotoROS2)
            self.get_logger().info('Enable Robot: bắt đầu chuỗi khởi động...')
            self._enable_step_1_reset_error()
            response.success = True
            response.message = 'Đang enable robot...'
        else:
            # Disable
            self._disable_robot()
            response.success = True
            response.message = 'Robot disabled'
        return response

    def _enable_step_1_reset_error(self):
        self.get_logger().info('Enable: reset_error...')
        self._call_trigger_chained(
            self._reset_error_cli, 'reset_error', self._enable_step_2_stop_traj)

    def _enable_step_2_stop_traj(self):
        self.get_logger().info('Enable: stop_traj_mode (giải phóng mode cũ)...')
        self._call_trigger_chained(
            self._stop_traj_cli, 'stop_traj_mode', self._enable_step_3_delay_before_queue)

    def _enable_step_3_delay_before_queue(self):
        import threading
        self.get_logger().info('Enable: chờ 1.5s để hệ thống ổn định trước khi start queue...')
        threading.Timer(1.5, self._enable_step_4_start_queue).start()

    def _enable_step_4_start_queue(self):
        self.get_logger().info('Enable: StartPointQueueMode...')
        if not self._start_queue_cli.wait_for_service(timeout_sec=3.0):
            self.get_logger().error('Service StartPointQueueMode không khả dụng!')
            return
        fut = self._start_queue_cli.call_async(StartPointQueueMode.Request())

        def _done(f):
            res = f.result()
            self.get_logger().info(
                f'StartPointQueueMode response: code={res.result_code.value}, msg="{res.message}"'
            )
            # Chấp nhận cả 0 và 1 vì firmware Yaskawa có thể trả về 0 = SUCCESS hoặc 1 = SUCCESS
            if res.result_code.value in (0, 1):
                self._queue_mode_active = True
                self._stream_state = STREAM_STATE_SEEDING
                self._accepted_since_seed = 0
                self._seed_request_sent = False
                self._pending_point_to_resend = None
                self._cumulative_time_ns = 0
                self._hold_point_count = 0
                self._next_send_not_before_ns = self.get_clock().now().nanoseconds
                self.get_logger().info('✓ Robot ENABLED — Point Queue Mode active. Servo ON!')
            else:
                self.get_logger().error(f'StartPointQueueMode FAILED: {res.message}')
        fut.add_done_callback(_done)

    def _disable_robot(self):
        """Tắt Point Queue Mode và reset state."""
        self.get_logger().info('Disable Robot: dừng stream, tắt traj mode...')
        self._queue_mode_active = False
        self._stream_state = STREAM_STATE_IDLE
        self._target_pose = None
        self._seed_request_sent = False
        self._pending_point_to_resend = None
        # Gọi stop_traj_mode
        if self._stop_traj_cli.wait_for_service(timeout_sec=1.0):
            self._stop_traj_cli.call_async(Trigger.Request())
        self.get_logger().info('✗ Robot DISABLED.')

    def _auto_re_enable(self):
        """Tự động re-enable queue mode sau khi bị drop (one-shot timer)."""
        self.get_logger().info('Auto-recovery: bắt đầu re-enable queue mode...')
        self._recovery_in_progress = False
        # Reset state để enable lại
        self._queue_call_inflight = False
        self._pending_point_to_resend = None
        self._seed_request_sent = False
        # Cập nhật lại _last_queued_joints từ current_joints
        # (vì robot đã dừng ở vị trí hiện tại)
        if self._got_joints:
            self._last_queued_joints = list(self._current_joints)
        # Reset smooth state để tránh nhảy cóc khi re-enable
        if self._current_ee_pose is not None:
            self._target_pose = None
            self._prev_ee_velocity = [0.0, 0.0, 0.0]
        # Bắt đầu lại chuỗi enable (step 1 → 2 → 3 → 4)
        self._enable_step_1_reset_error()

    def _call_trigger_chained(self, client, name, next_step_cb):
        """Helper để gọi service bất kỳ và chuyển sang bước tiếp theo."""
        if not client.wait_for_service(timeout_sec=3.0):
            self.get_logger().warn(f'Service {name} không khả dụng, bỏ qua.')
            next_step_cb()
            return

        req = client.srv_type.Request()
        fut = client.call_async(req)
        def _done(f):
            try:
                res = f.result()
                code = getattr(getattr(res, 'result_code', None), 'value', 'N/A')
                msg = getattr(res, 'message', '')
                success = getattr(res, 'success', None)
                if success is None:
                    self.get_logger().info(f'{name}: code={code}, msg="{msg}"')
                else:
                    self.get_logger().info(
                        f'{name}: success={success}, code={code}, msg="{msg}"'
                    )
            except Exception as e:
                self.get_logger().error(f'Error calling {name}: {e}')
            next_step_cb()
        fut.add_done_callback(_done)

    # ═══════════════════════════════════════════════════════════════
    # STREAM LOOP
    # ═══════════════════════════════════════════════════════════════

    def _stream_tick(self):
        try:
            if not self._queue_mode_active or not self._got_joints:
                return

            self._tick_count += 1
            self._log_runtime_rates()
            self._check_no_motion_watchdog()
            now = self.get_clock().now()
            if now.nanoseconds < self._next_send_not_before_ns:
                return

            # ── Bước 0: Khởi tạo ─────────────────────────────────────
            if self._stream_state == STREAM_STATE_SEEDING:
                # Bootstrap initial EE pose via FK
                initial_pose = self._solve_fk_sync(list(self._current_joints))
                if initial_pose:
                    self._current_ee_pose = initial_pose
                    fb = PoseStamped()
                    fb.header.frame_id = BASE_FRAME
                    fb.header.stamp = self.get_clock().now().to_msg()
                    fb.pose = initial_pose
                    self._ee_pub.publish(fb)
                    self.get_logger().info(
                        f'Bootstrap EE pose via FK: '
                        f'({initial_pose.position.x:.4f}, '
                        f'{initial_pose.position.y:.4f}, '
                        f'{initial_pose.position.z:.4f})'
                    )

                # Quy tắc queue mode: điểm đầu tiên phải đúng trạng thái hiện tại, t=0, v=0.
                if not self._seed_request_sent:
                    if self._send_joint_point(list(self._current_joints), force_seed=True):
                        self._seed_request_sent = True
                        self.get_logger().info('Đã gửi seed point (current joints, t=0), chờ ACK...')
                return

            # ── Prebuffering: gửi hold-points (không tăng cumulative time) ──
            if self._stream_state == STREAM_STATE_PREBUFFERING:
                self._send_joint_point(list(self._last_queued_joints), is_hold=True)
                return

            # ── Streaming state ───────────────────────────────────────
            if self._target_pose is None:
                # Nếu chưa có target: gửi hold-point để giữ queue alive,
                # KHÔNG tăng cumulative time.
                self._send_joint_point(list(self._last_queued_joints), is_hold=True)
                return

            # ── Bước 1: Smooth pose (interpolate về target) ──────────
            smoothed = self._smooth_pose(self._target_pose)
            self._current_ee_pose = smoothed  # cập nhật EE pose ngay lập tức để tick sau dùng
            
            # ── Bước 2: Publish feedback EE pose ─────────────────────
            fb = PoseStamped()
            fb.header.frame_id = BASE_FRAME
            fb.header.stamp = self.get_clock().now().to_msg()
            fb.pose = smoothed
            self._ee_pub.publish(fb)

            # ── Bước 3: Request IK async (nếu chưa pending) ──────────
            if not self._ik_request_pending:
                self._request_ik_async(smoothed)

            # ── Bước 4: Dùng IK solution mới nhất (nếu có) ──────────
            joint_solution = self._latest_ik_solution

            if joint_solution is None:
                # IK chưa có (hoặc delay) → giữ vị trí cũ (hold-point)
                self._send_joint_point(list(self._last_queued_joints), is_hold=True)
                return

            self._latest_ik_solution = None

            # ── An toàn: kiểm tra soft joint limits ────────────────────
            joint_solution_list = list(joint_solution)
            was_limit_clamped = False
            for i, (jval, (lo, hi)) in enumerate(zip(joint_solution_list, SOFT_JOINT_LIMITS)):
                if jval < lo:
                    joint_solution_list[i] = lo
                    was_limit_clamped = True
                elif jval > hi:
                    joint_solution_list[i] = hi
                    was_limit_clamped = True
            
            if was_limit_clamped:
                self.get_logger().warn(
                    f'IK solution ngoài soft limit. Đã clamp vào biên để bảo vệ robot.',
                    throttle_duration_sec=1.0)
            
            joint_solution = tuple(joint_solution_list)

            # ── An toàn: CLAMP bước nhảy joint PER-AXIS ────────────
            # So sánh với _last_queued_joints (không phải _current_joints).
            # Thay vì REJECT toàn bộ (gây death spiral), ta CLAMP từng joint
            # → robot vẫn di chuyển hướng đúng, chỉ chậm hơn.
            was_clamped = False
            clamped_joints = list(joint_solution)
            for i in range(len(clamped_joints)):
                delta = clamped_joints[i] - self._last_queued_joints[i]
                limit = MAX_JOINT_DELTA_PER_AXIS[i]
                if abs(delta) > limit:
                    clamped_joints[i] = self._last_queued_joints[i] + limit * (1.0 if delta > 0 else -1.0)
                    was_clamped = True

            if was_clamped:
                self.get_logger().info(
                    f'IK delta clamped → joints: [{", ".join(f"{j:.3f}" for j in clamped_joints)}]',
                    throttle_duration_sec=2.0)

            joint_solution = clamped_joints
            self._last_ok_joints = joint_solution

            max_delta = max(abs(j - c) for j, c in
                            zip(joint_solution, self._last_queued_joints))
            self.get_logger().info(
                f'IK OK → Δmax={max_delta:.4f} rad, '
                f'joints: [{", ".join(f"{j:.3f}" for j in joint_solution)}]',
                throttle_duration_sec=2.0)

            # ── Bước 5: Gửi xuống robot (motion point) ────────────────
            self._window_max_joint_delta = max(self._window_max_joint_delta, max_delta)
            self._send_joint_point(joint_solution, is_hold=False)
        except Exception as e:
            self.get_logger().error(f'_stream_tick exception: {e}')

    # ═══════════════════════════════════════════════════════════════
    # IK SOLVER (Bất đồng bộ)
    # ═══════════════════════════════════════════════════════════════

    def _request_ik_async(self, target_pose: Pose):
        """
        Giải IK bất đồng bộ cho target_pose.
        """
        self._ik_request_pending = True
        
        # Build request
        req = GetPositionIK.Request()
        req.ik_request = PositionIKRequest()
        req.ik_request.group_name         = GROUP_NAME
        req.ik_request.ik_link_name       = EE_LINK
        req.ik_request.avoid_collisions   = False
        req.ik_request.timeout.sec        = 0
        req.ik_request.timeout.nanosec    = int(IK_TIMEOUT_SEC * 1e9)

        # Target pose
        ps = PoseStamped()
        ps.header.frame_id = BASE_FRAME
        ps.header.stamp    = self.get_clock().now().to_msg()
        ps.pose            = target_pose
        req.ik_request.pose_stamped = ps

        # Dùng _last_queued_joints làm seed cho IK.
        seed = RobotState()
        seed.joint_state.name     = JOINT_NAMES
        seed.joint_state.position = list(self._last_queued_joints)
        req.ik_request.robot_state = seed

        try:
            ros_future = self._ik_cli.call_async(req)
            ros_future.add_done_callback(self._on_ik_result)
        except Exception as e:
            self._ik_request_pending = False
            self.get_logger().error(f'IK async request exception: {e}')

    def _on_ik_result(self, future):
        """Callback khi nhận được kết quả IK."""
        self._ik_request_pending = False
        try:
            result = future.result()
            # error_code: 1 = SUCCESS
            if result.error_code.val == 1:
                js = result.solution.joint_state
                positions = [0.0] * 6
                for i, name in enumerate(JOINT_NAMES):
                    if name in js.name:
                        idx = list(js.name).index(name)
                        positions[i] = js.position[idx]
                self._latest_ik_solution = positions
        except Exception as e:
            self.get_logger().error(f'IK result exception: {e}', throttle_duration_sec=2.0)

    def _solve_fk_sync(self, joints: list[float]) -> Pose | None:
        """Giải FK đồng bộ cho list joints."""
        if not self._fk_cli.wait_for_service(timeout_sec=1.0):
            return None

        req = GetPositionFK.Request()
        req.header.frame_id = BASE_FRAME
        req.header.stamp = self.get_clock().now().to_msg()
        req.fk_link_names = [EE_LINK]
        
        seed = RobotState()
        seed.joint_state.name = JOINT_NAMES
        seed.joint_state.position = joints
        req.robot_state = seed

        event = threading.Event()
        result_holder = [None]

        def _done_cb(future):
            result_holder[0] = future
            event.set()

        try:
            ros_future = self._fk_cli.call_async(req)
            ros_future.add_done_callback(_done_cb)
            if not event.wait(timeout=0.5):
                return None
            
            res = result_holder[0].result()
            if res and res.pose_stamped:
                return res.pose_stamped[0].pose
            return None
        except Exception as e:
            self.get_logger().error(f'FK exception: {e}')
            return None

    # ═══════════════════════════════════════════════════════════════
    # POSE SMOOTHING
    # ═══════════════════════════════════════════════════════════════

    def _smooth_pose(self, target: Pose) -> Pose:
        """
        Interpolate từ current_ee_pose về target bằng Trapezoidal Velocity Profile.
        Không dùng exponential smoothing (alpha) để tránh xung đột với acceleration.
        """
        if self._current_ee_pose is None:
            self._current_ee_pose = Pose(
                position=Point(
                    x=target.position.x,
                    y=target.position.y,
                    z=target.position.z,
                ),
                orientation=target.orientation,
            )
            self._prev_ee_velocity = [0.0, 0.0, 0.0]
            self._last_smooth_time_ns = self.get_clock().now().nanoseconds
            return self._current_ee_pose

        # ===== Tính DT THỰC TẾ thay vì DT CỨNG =====
        now_ns = self.get_clock().now().nanoseconds
        if not hasattr(self, '_last_smooth_time_ns'):
            self._last_smooth_time_ns = now_ns - int(self._stream_period_sec * 1e9)
        dt = max((now_ns - self._last_smooth_time_ns) / 1e9, 1e-4)
        dt = min(dt, 0.1)  # Clamp để tránh spike khi tick bị delay
        self._last_smooth_time_ns = now_ns

        # ===== Tính toán lỗi (Error) =====
        error = [
            target.position.x - self._current_ee_pose.position.x,
            target.position.y - self._current_ee_pose.position.y,
            target.position.z - self._current_ee_pose.position.z,
        ]
        dist = math.sqrt(sum(e*e for e in error))
        
        # ===== VELOCITY PROFILE: Trapezoidal =====
        if dist < 1e-5:
            desired_speed = 0.0
        else:
            # Vùng giảm tốc: khoảng cách cần thiết để dừng lại từ max_vel với max_accel
            decel_dist = (MAX_CARTESIAN_VELOCITY ** 2) / (2.0 * MAX_CARTESIAN_ACCELERATION)
            if dist < decel_dist:
                # Nếu đang gần target → giảm tốc độ (S-curve tự nhiên)
                desired_speed = math.sqrt(2.0 * MAX_CARTESIAN_ACCELERATION * dist)
            else:
                # Nếu xa target → chạy full speed
                desired_speed = MAX_CARTESIAN_VELOCITY
        
        desired_speed = min(desired_speed, MAX_CARTESIAN_VELOCITY)
        
        if dist > 1e-5:
            direction = [e / dist for e in error]
        else:
            direction = [0.0, 0.0, 0.0]
        
        desired_vel = [desired_speed * d for d in direction]
        
        # ===== ACCELERATION LIMITING =====
        if not hasattr(self, '_prev_ee_velocity'):
            self._prev_ee_velocity = [0.0, 0.0, 0.0]
        max_dv = MAX_CARTESIAN_ACCELERATION * dt
        vel = list(desired_vel)
        for i in range(3):
            dv = vel[i] - self._prev_ee_velocity[i]
            if abs(dv) > max_dv:
                vel[i] = self._prev_ee_velocity[i] + max_dv * (1.0 if dv > 0 else -1.0)
        
        # Đảm bảo vận tốc tổng hợp không vượt quá MAX_CARTESIAN_VELOCITY
        speed = math.sqrt(sum(v*v for v in vel))
        if speed > MAX_CARTESIAN_VELOCITY:
            scale = MAX_CARTESIAN_VELOCITY / speed
            vel = [v * scale for v in vel]
        
        self._prev_ee_velocity = list(vel)
        
        # ===== ÁP DỤNG =====
        result = Pose()
        result.position.x = self._current_ee_pose.position.x + vel[0] * dt
        result.position.y = self._current_ee_pose.position.y + vel[1] * dt
        result.position.z = self._current_ee_pose.position.z + vel[2] * dt
        
        # SLERP orientation: track từ từ (sử dụng tốc độ quay dựa trên dt)
        orientation_speed = 5.0 # rad/s tracking tốc độ hướng
        blend_factor = min(1.0, orientation_speed * dt)
        result.orientation = self._slerp_quat(self._current_ee_pose.orientation, target.orientation, blend_factor)
        return result

    @staticmethod
    def _lerp(a: float, b: float, t: float) -> float:
        return a + t * (b - a)

    @staticmethod
    def _slerp_quat(q0: Quaternion, q1: Quaternion, t: float) -> Quaternion:
        """Spherical linear interpolation giữa 2 quaternion."""
        def to_arr(q): return [q.x, q.y, q.z, q.w]
        def dot(a, b): return sum(x*y for x, y in zip(a, b))

        a, b = to_arr(q0), to_arr(q1)
        d = dot(a, b)
        if d < 0:  # chọn shortest path
            b = [-x for x in b]
            d = -d
        d = min(1.0, d)
        if d > 0.9995:  # quá gần → lerp thường
            r = [a[i] + t*(b[i]-a[i]) for i in range(4)]
        else:
            theta0 = math.acos(d)
            theta  = theta0 * t
            sin0, sin1 = math.sin(theta0), math.sin(theta)
            s0 = math.cos(theta) - d * sin1 / sin0
            s1 = sin1 / sin0
            r  = [s0*a[i] + s1*b[i] for i in range(4)]
        norm = math.sqrt(sum(x*x for x in r))
        r = [x/norm for x in r]
        return Quaternion(x=r[0], y=r[1], z=r[2], w=r[3])

    # ═══════════════════════════════════════════════════════════════
    # GỬI ĐIỂM XUỐNG ROBOT (QUEUE_TRAJ_POINT)
    # ═══════════════════════════════════════════════════════════════

    def _send_joint_point(
        self,
        joints: list[float],
        force_seed: bool = False,
        is_hold: bool = False,
    ):
        """
        Gửi một JointTrajectoryPoint xuống MotoROS2 queue.

        Args:
            joints: joint positions [6]
            force_seed: True = seed point (t=0, v=0)
            is_hold: True = hold-point (giữ vị trí, KHÔNG tăng cumulative time).
                     Dùng khi chưa có target hoặc IK thất bại.
        """
        # Thread-safe guard
        if force_seed and self._stream_state != STREAM_STATE_SEEDING:
            self.get_logger().warn(
                f'Bỏ qua seed point vì state hiện tại là {self._stream_state}',
                throttle_duration_sec=1.0
            )
            return False
        with self._send_lock:
            if self._queue_call_inflight:
                return False
            self._queue_call_inflight = True

        queue_cli = self._select_queue_client()
        if queue_cli is None:
            self.get_logger().warn(
                'Service queue_point/queue_traj_point chưa sẵn sàng.',
                throttle_duration_sec=1.0
            )
            with self._send_lock:
                self._queue_call_inflight = False
            return False
        if not self._active_queue_service_name:
            self._active_queue_service_name = getattr(queue_cli, 'srv_name', '<unknown>')
            self.get_logger().info(f'Đang stream qua service: {self._active_queue_service_name}')

        point = JointTrajectoryPoint()
        request = QueueTrajPoint.Request()
        request.joint_names = JOINT_NAMES

        if force_seed:
            # Seed point: vị trí hiện tại, v=0, t=0. Reset bộ đếm tích lũy.
            point.positions = list(self._current_joints)
            point.velocities = [0.0] * len(JOINT_NAMES)
            point.time_from_start = Duration(sec=0, nanosec=0)
            self._cumulative_time_ns = 0
        elif self._pending_point_to_resend is not None:
            # Retry điểm bị BUSY: KHÔNG tăng cumulative (timestamp đã tính từ lần trước).
            point = self._pending_point_to_resend
        elif is_hold:
            # Hold-point: gửi vị trí hiện tại với dt bình thường để MotoROS2 không reject.
            dt_ns = int(self._queue_dt_sec * 1e9)
            self._cumulative_time_ns += dt_ns
            total_sec  = self._cumulative_time_ns // 1_000_000_000
            total_nsec = self._cumulative_time_ns  % 1_000_000_000
            point.positions = [float(j) for j in joints]
            point.velocities = [0.0] * len(JOINT_NAMES)
            point.time_from_start = Duration(sec=int(total_sec), nanosec=int(total_nsec))
            self._hold_point_count += 1
        else:
            # MOTION point: time_from_start TĂNG LŨY TIẾN (cumulative).
            dt_ns = int(self._queue_dt_sec * 1e9)
            self._cumulative_time_ns += dt_ns
            total_sec  = self._cumulative_time_ns // 1_000_000_000
            total_nsec = self._cumulative_time_ns  % 1_000_000_000
            point.positions = [float(j) for j in joints]
            dt = max(self._queue_dt_sec, 1e-3)
            raw_velocities = [
                float((target - queued) / dt)
                for target, queued in zip(joints, self._last_queued_joints)
            ]
            # Clamp per-joint velocity for safety (khớp cổ tay chậm hơn)
            clamped_velocities = [
                max(-MAX_JOINT_VELOCITIES[i], min(MAX_JOINT_VELOCITIES[i], v))
                for i, v in enumerate(raw_velocities)
            ]
            point.velocities = clamped_velocities
            point.time_from_start = Duration(sec=int(total_sec), nanosec=int(total_nsec))
            self._hold_point_count = 0  # reset hold counter

        request.point = point

        self._queue_sent_count += 1
        self._next_send_not_before_ns = self.get_clock().now().nanoseconds
        fut = queue_cli.call_async(request)
        fut.add_done_callback(lambda f, p=point, h=is_hold: self._on_queue_result(f, p, h))
        return True

    def _on_queue_result(self, future, sent_point: JointTrajectoryPoint, was_hold: bool = False):
        with self._send_lock:
            self._queue_call_inflight = False
        try:
            res = future.result()
            code = getattr(res.result_code, 'value', -1) if hasattr(res, 'result_code') else -1
            msg = getattr(res, 'message', '')
            if code == 4:
                # BUSY: giữ lại điểm để resend ở tick tiếp theo.
                # Rollback cumulative timer.
                if was_hold:
                    rollback_ns = int(self._queue_dt_sec * 1e9)  # hold dùng cùng dt
                else:
                    rollback_ns = int(self._queue_dt_sec * 1e9)
                self._cumulative_time_ns = max(0, self._cumulative_time_ns - rollback_ns)
                self._pending_point_to_resend = sent_point
                self._window_busy_count += 1
                self._window_retry_count += 1
                backoff_ns = int(self._retry_backoff_sec * 1e9)
                self._next_send_not_before_ns = self.get_clock().now().nanoseconds + backoff_ns
                self.get_logger().warn(
                    f'Queue BUSY, sẽ resend (backoff {self._retry_backoff_sec*1000:.0f}ms): msg="{msg}"',
                    throttle_duration_sec=1.0
                )
                return
            # ── Queue mode bị drop → auto-recovery ──────────────
            if code == 2:  # "Must call start_point_queue_mode service"
                self._pending_point_to_resend = None
                self._window_reject_count += 1
                if not self._recovery_in_progress:
                    self._queue_mode_active = False
                    self._stream_state = STREAM_STATE_IDLE
                    self._auto_recovery_count += 1
                    if self._auto_recovery_count <= 3:
                        self._recovery_in_progress = True
                        self.get_logger().warn(
                            f'⚠ Queue mode bị drop! Auto-recovery lần '
                            f'{self._auto_recovery_count}/3...')
                        # Gọi lại enable sau 500ms (one-shot)
                        import threading
                        threading.Timer(0.5, self._auto_re_enable).start()
                    else:
                        self.get_logger().error(
                            '✗ Đã thử recovery 3 lần thất bại. '
                            'Dừng stream. Cần restart thủ công.')
                return
            # Tương thích cả 2 biến thể firmware (SUCCESS=0 hoặc SUCCESS=1).
            if code not in (0, 1):
                self.get_logger().error(
                    f'Yaskawa TỪ CHỐI ĐIỂM! Mã lỗi (result_code): {code}, Message: "{msg}"',
                    throttle_duration_sec=1.0
                )
                self._pending_point_to_resend = None
                self._window_reject_count += 1
                return
            self._pending_point_to_resend = None
            self._last_queued_joints = list(sent_point.positions)
            self._accepted_points += 1
            self._auto_recovery_count = 0  # Reset recovery counter khi thành công
            self._window_ack_count += 1
            now = self.get_clock().now()
            if self._last_ack_time is not None:
                self._window_ack_interval_sum += (now - self._last_ack_time).nanoseconds / 1e9
                self._window_ack_interval_count += 1
            self._last_ack_time = now
            self._next_send_not_before_ns = now.nanoseconds
            if self._stream_state == STREAM_STATE_SEEDING:
                self._stream_state = STREAM_STATE_PREBUFFERING
                self._accepted_since_seed = 0
                self._seed_request_sent = False
                self.get_logger().info('Seed ACK nhận được, bắt đầu prebuffer.')
            elif self._stream_state == STREAM_STATE_PREBUFFERING:
                self._accepted_since_seed += 1
                if self._accepted_since_seed >= self._prebuffer_target:
                    self._stream_state = STREAM_STATE_STREAMING
                    self.get_logger().info(
                        f'Pre-buffer hoàn tất ({self._prebuffer_target} points), '
                        f'bắt đầu stream ổn định. Đang chờ target...'
                    )
            if self._accepted_points % 20 == 0:
                t_sec = sent_point.time_from_start.sec + sent_point.time_from_start.nanosec / 1e9
                self.get_logger().info(
                    f'QueueTrajPoint accepted #{self._accepted_points}: '
                    f't={t_sec:.3f}s, hold={was_hold}'
                )
            if self._queue_debug_log_count < 5:
                self._queue_debug_log_count += 1
                t_sec = sent_point.time_from_start.sec + sent_point.time_from_start.nanosec / 1e9
                self.get_logger().info(
                    f'Queue accepted sample#{self._queue_debug_log_count}: '
                    f'svc={self._active_queue_service_name}, '
                    f't_cumul={t_sec:.4f}s, code={code}, msg="{msg}", '
                    f'hold={was_hold}'
                )
        except Exception as e:
            self.get_logger().error(f'Lỗi khi nhận phản hồi từ queue_traj_point: {e}')

    def _select_queue_client(self):
        if self._queue_point_cli.service_is_ready():
            return self._queue_point_cli
        if self._queue_point_cli_alt.service_is_ready():
            return self._queue_point_cli_alt
        return None

    def _log_runtime_rates(self):
        now = self.get_clock().now()
        elapsed = (now - self._rate_window_start).nanoseconds / 1e9
        if elapsed < 5.0:
            return
        tick_hz = self._tick_count / elapsed
        queue_send_hz = self._queue_sent_count / elapsed
        ack_hz = self._window_ack_count / elapsed
        busy_hz = self._window_busy_count / elapsed
        inter_ack_ms = (
            (self._window_ack_interval_sum / self._window_ack_interval_count) * 1000.0
            if self._window_ack_interval_count > 0 else 0.0
        )
        cumul_sec = self._cumulative_time_ns / 1e9
        self.get_logger().info(
            'Runtime rate: '
            f'state={self._stream_state}, '
            f'tick_hz={tick_hz:.1f}, queue_send_hz={queue_send_hz:.1f}, '
            f'ack_hz={ack_hz:.1f}, busy_hz={busy_hz:.1f}, '
            f'retry_count={self._window_retry_count}, '
            f'reject_count={self._window_reject_count}, '
            f'inter_ack_ms={inter_ack_ms:.1f}, '
            f'max_joint_delta={self._window_max_joint_delta:.3f}, '
            f'cumul_time={cumul_sec:.2f}s, '
            f'hold_count={self._hold_point_count}'
        )
        if self._last_target_update_ns > 0:
            target_age_s = (now.nanoseconds - self._last_target_update_ns) / 1e9
            if target_age_s > 2.0:
                self.get_logger().warn(
                    f'Target stream stale: không có target mới trong {target_age_s:.1f}s'
                )
        self._tick_count = 0
        self._queue_sent_count = 0
        self._rate_window_start = now
        self._window_ack_count = 0
        self._window_busy_count = 0
        self._window_retry_count = 0
        self._window_reject_count = 0
        self._window_max_joint_delta = 0.0
        self._window_ack_interval_sum = 0.0
        self._window_ack_interval_count = 0

    def _check_no_motion_watchdog(self):
        if self._accepted_points < NO_MOTION_MIN_ACCEPTED_POINTS:
            return
        # Chỉ cảnh báo nếu đang gửi motion points (không phải hold)
        if self._hold_point_count > 0:
            return
        now = self.get_clock().now()
        since_motion = (now - self._last_motion_time).nanoseconds / 1e9
        since_warn = (now - self._last_warn_time).nanoseconds / 1e9
        if since_motion >= NO_MOTION_WARN_SEC and since_warn >= NO_MOTION_WARN_SEC:
            self._last_warn_time = now
            self.get_logger().warn(
                'QueueTrajPoint đã được accept nhưng joint_states hầu như không đổi. '
                'Kiểm tra: 1) Robot ở mode AUTO? 2) Servo ON? 3) E-stop cleared?'
            )

# ═══════════════════════════════════════════════════════════════════
# DEMO NODE: Test Cartesian trajectory
# ═══════════════════════════════════════════════════════════════════

class CartesianDemoPublisher(Node):
    """
    Node test: publish các điểm Cartesian theo pattern.

    Dùng:
        python3 cartesian_streamer.py --demo circle
        python3 cartesian_streamer.py --demo line
        python3 cartesian_streamer.py --demo lissajous
    """

    def __init__(self, mode: str = 'line', omega: float = 0.5, amplitude: float = 0.1, stream_period_sec: float = 1.0/DEFAULT_STREAM_HZ):
        super().__init__('cartesian_demo')
        self._mode = mode
        self._omega = omega          # rad/s — tốc độ góc
        self._amplitude = amplitude  # mét — biên độ chuyển động
        self._stream_period = stream_period_sec
        self._t = 0.0

        self._pub = self.create_publisher(
            Float64MultiArray, '/cartesian_streamer/target_xyz', 10)

        # Đọc EE pose hiện tại để biết điểm xuất phát
        self._base_x = 0.0
        self._base_y = 0.0
        self._base_z = 0.0

        self._ee_sub = self.create_subscription(
            PoseStamped, '/cartesian_streamer/current_pose',
            self._on_ee, 10)

        self._got_base = False
        # Timer chưa bắt đầu — chỉ chuyển động SAU KHI có EE feedback
        self._timer = None
        self._start_time = None

        period_sec = 2.0 * math.pi / self._omega
        self.get_logger().info(
            f'CartesianDemo [{mode}] khởi động:\n'
            f'  omega={omega:.2f} rad/s (period={period_sec:.1f}s)\n'
            f'  amplitude={amplitude*100:.1f} cm\n'
            f'  Đợi EE feedback trước khi chạy...'
        )

    def _on_ee(self, msg: PoseStamped):
        if not self._got_base:
            self._base_x = msg.pose.position.x
            self._base_y = msg.pose.position.y
            self._base_z = msg.pose.position.z
            self._got_base = True
            self.get_logger().info(
                f'Base EE: ({self._base_x:.4f}, '
                f'{self._base_y:.4f}, {self._base_z:.4f})')
            # Bắt đầu publish target SAU KHI biết vị trí thật
            if self._timer is None:
                self._start_time = self.get_clock().now()
                self._timer = self.create_timer(self._stream_period, self._tick)
                self.get_logger().info('▶ Bắt đầu demo pattern!')

    def _tick(self):
        if not self._got_base:
            return  # chưa có vị trí gốc
        self._t += self._stream_period  # step khớp với stream rate
        amp = self._amplitude
        w = self._omega

        if self._mode == 'line':
            # Tiến lùi trên trục Y
            x = self._base_x
            y = self._base_y + amp * math.sin(w * self._t)
            z = self._base_z

        elif self._mode == 'circle':
            # Vòng tròn trên mặt phẳng XY, bắt đầu mượt mà từ gốc (t=0 -> x=0, y=0)
            x = self._base_x + amp * math.sin(w * self._t)
            y = self._base_y + amp * (1.0 - math.cos(w * self._t))
            z = self._base_z

        elif self._mode == 'lissajous':
            # Đường hình số 8 (Lissajous) trên mặt phẳng XY, bắt đầu từ gốc
            x = self._base_x + amp * math.sin(w * self._t)
            y = self._base_y + (amp / 2.0) * math.sin(2 * w * self._t)
            z = self._base_z

        else:
            return

        msg = Float64MultiArray()
        msg.data = [x, y, z]
        self._pub.publish(msg)
        self.get_logger().info(
            f'[{self._mode}] t={self._t:.2f}s → ({x:.4f}, {y:.4f}, {z:.4f})',
            throttle_duration_sec=1.0)


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    global MAX_CARTESIAN_VELOCITY, MAX_CARTESIAN_ACCELERATION, MAX_JOINT_VELOCITIES, SMOOTH_ALPHA
    parser = argparse.ArgumentParser(
        description='Cartesian Streamer cho MotoROS2 Point Queue Mode',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
  # Test cơ bản: di chuyển tuyến tính trên trục X, 5cm, chậm
  python3 cartesian_streamer.py --demo line

  # Vòng tròn nhanh hơn, biên độ lớn hơn
  python3 cartesian_streamer.py --demo circle --omega 1.0 --amplitude 0.08

  # Lissajous pattern
  python3 cartesian_streamer.py --demo lissajous --omega 0.3

  # Chỉ chạy streamer, chờ target từ AI/Camera node
  python3 cartesian_streamer.py

  # Tune queue parameters
  python3 cartesian_streamer.py --demo line --queue-dt 0.06 --retry-backoff-ms 20
""")
    parser.add_argument(
        '--stream-hz', type=float, default=DEFAULT_STREAM_HZ,
        help=f'Tần số stream tick (Hz) [default: {DEFAULT_STREAM_HZ}]')
    parser.add_argument(
        '--queue-dt', type=float, default=None,
        help=f'time delta giữa mỗi motion point (giây) [default: 1/stream_hz]')
    parser.add_argument(
        '--prebuffer', type=int, default=QUEUE_PREBUFFER_POINTS,
        help=f'số điểm prebuffer trước khi vào streaming [default: {QUEUE_PREBUFFER_POINTS}]')
    parser.add_argument(
        '--retry-backoff-ms', type=float, default=QUEUE_RETRY_BACKOFF_SEC * 1000.0,
        help=f'backoff (ms) khi queue trả BUSY [default: {QUEUE_RETRY_BACKOFF_SEC*1000:.0f}]')
    parser.add_argument(
        '--demo', choices=['circle', 'line', 'lissajous'],
        default=None,
        help='Chạy demo pattern (không cần AI node ngoài)')
    parser.add_argument(
        '--omega', type=float, default=0.5,
        help='Tốc độ góc cho demo pattern (rad/s) [default: 0.5]')
    parser.add_argument(
        '--amplitude', type=float, default=0.05,
        help='Biên độ cho demo pattern (mét) [default: 0.05]')
    parser.add_argument(
        '--max-vel', type=float, default=MAX_CARTESIAN_VELOCITY,
        help=f'Tốc độ Cartesian tối đa (m/s) [default: {MAX_CARTESIAN_VELOCITY}]')
    parser.add_argument(
        '--max-accel', type=float, default=MAX_CARTESIAN_ACCELERATION,
        help=f'Gia tốc Cartesian tối đa (m/s²) [default: {MAX_CARTESIAN_ACCELERATION}]')
    parser.add_argument(
        '--max-joint-vel', type=float, default=None,
        help='Scale tốc độ góc tối đa mỗi khớp (rad/s). Ghi đè đồng đều.')
    parser.add_argument(
        '--smooth-alpha', type=float, default=SMOOTH_ALPHA,
        help=f'Hệ số smooth (0.0-1.0, thấp=mượt) [default: {SMOOTH_ALPHA}]')
    args, ros_args = parser.parse_known_args()

    # Áp dụng CLI overrides lên các hằng số an toàn
    MAX_CARTESIAN_VELOCITY = max(args.max_vel, 0.01)
    MAX_CARTESIAN_ACCELERATION = max(args.max_accel, 0.01)
    if args.max_joint_vel is not None:
        v = max(args.max_joint_vel, 0.01)
        MAX_JOINT_VELOCITIES = [v] * len(JOINT_NAMES)
    SMOOTH_ALPHA = max(0.01, min(1.0, args.smooth_alpha))

    rclpy.init(args=ros_args)

    executor = MultiThreadedExecutor(num_threads=4)

    stream_hz = max(args.stream_hz, 1.0)
    # queue_dt defaults to 1/stream_hz if not explicitly set
    queue_dt = args.queue_dt if args.queue_dt is not None else (1.0 / stream_hz)
    queue_dt = max(queue_dt, 0.01)

    streamer = CartesianStreamer(
        stream_hz=stream_hz,
        queue_dt_sec=queue_dt,
        prebuffer_points=max(args.prebuffer, 1),
        retry_backoff_sec=max(args.retry_backoff_ms, 0.0) / 1000.0,
        auto_enable=bool(args.demo),
    )
    executor.add_node(streamer)

    if args.demo:
        demo = CartesianDemoPublisher(
            mode=args.demo,
            omega=args.omega,
            amplitude=args.amplitude,
            stream_period_sec=1.0 / stream_hz,
        )
        executor.add_node(demo)

    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        streamer.get_logger().info('Graceful shutdown: tắt Point Queue Mode trước khi thoát...')
        # Gọi stop_traj_mode đồng bộ để controller không bị alarm
        try:
            if streamer._queue_mode_active:
                streamer._queue_mode_active = False
                streamer._stream_state = STREAM_STATE_IDLE
                if streamer._stop_traj_cli.wait_for_service(timeout_sec=2.0):
                    stop_req = Trigger.Request()
                    stop_fut = streamer._stop_traj_cli.call_async(stop_req)
                    # Chờ tối đa 3 giây cho service trả lời
                    end_time = _time.time() + 3.0
                    while not stop_fut.done() and _time.time() < end_time:
                        rclpy.spin_once(streamer, timeout_sec=0.1)
                    if stop_fut.done():
                        streamer.get_logger().info('✓ stop_traj_mode thành công. Controller sạch sẽ.')
                    else:
                        streamer.get_logger().warn('⚠ stop_traj_mode timeout, nhưng đã gửi yêu cầu.')
                else:
                    streamer.get_logger().warn('⚠ stop_traj_mode service không sẵn sàng.')
            else:
                streamer.get_logger().info('Robot chưa enable, không cần stop_traj_mode.')
        except Exception as e:
            streamer.get_logger().warn(f'Lỗi khi shutdown: {e}')
        streamer.get_logger().info('Shutdown hoàn tất. Tủ điện sẽ KHÔNG bị alarm.')
        executor.shutdown()
        rclpy.shutdown()


if __name__ == '__main__':
    main()