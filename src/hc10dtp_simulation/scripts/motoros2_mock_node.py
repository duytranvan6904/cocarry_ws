#!/usr/bin/env python3
"""
motoros2_mock_node.py
─────────────────────
Giả lập (Mock) các service của MotoROS2 driver để cartesian_streamer
có thể hoạt động mà KHÔNG cần robot thật.

Khi chạy ở chế độ fake hardware (ros2_control mock_components/GenericSystem),
node này đóng vai trò trung gian:

  cartesian_streamer  ──(MotoROS2 services)──►  motoros2_mock_node
                                                      │
                                                      ▼
                                               ros2_control
                                          (joint_trajectory_controller)
                                                      │
                                                      ▼
                                               GenericSystem (fake HW)
                                                      │
                                                      ▼
                                              /joint_states  ──► RViz

Mock node cung cấp:
  - /yaskawa/start_point_queue_mode   (StartPointQueueMode)  → trả READY
  - /yaskawa/queue_traj_point         (QueueTrajPoint)       → forward tới JTC
  - /yaskawa/queue_point              (QueueTrajPoint)       → alias
  - /queue_point                      (QueueTrajPoint)       → alias
  - /yaskawa/stop_traj_mode           (Trigger)              → trả success
  - /yaskawa/reset_error              (Trigger)              → trả success
  - /yaskawa/servo_on                 (Trigger)              → trả success
  - /yaskawa/joint_states             (JointState publisher) → relay /joint_states

Cách dùng:
  Terminal 1: ros2 launch hc10dtp_simulation sim_start.launch.py
  Terminal 2: python3 cartesian_streamer_hc10dtp.py --demo line
"""

import rclpy
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.action import ActionClient

from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from std_srvs.srv import Trigger
from builtin_interfaces.msg import Duration

from motoros2_interfaces.srv import StartPointQueueMode, QueueTrajPoint

from control_msgs.action import FollowJointTrajectory

JOINT_NAMES = [
    'joint_1_s', 'joint_2_l', 'joint_3_u',
    'joint_4_r', 'joint_5_b', 'joint_6_t',
]


class MotoROS2MockNode(Node):
    """
    Giả lập tất cả các service mà MotoROS2 driver cung cấp.
    Chuyển tiếp lệnh queue_traj_point thành FollowJointTrajectory action
    hoặc trực tiếp publish lên /hc10dtp_arm_controller/joint_trajectory.
    """

    def __init__(self):
        super().__init__('motoros2_mock')
        self._cb = ReentrantCallbackGroup()

        self._queue_mode_active = False
        self._accepted_count = 0
        self._last_joints = [0.0] * 6

        # ── Mock Services ────────────────────────────────────────────
        # 1. StartPointQueueMode
        self._start_queue_srv = self.create_service(
            StartPointQueueMode,
            '/yaskawa/start_point_queue_mode',
            self._handle_start_queue,
            callback_group=self._cb,
        )

        # 2. QueueTrajPoint (3 biến thể mà cartesian_streamer thử)
        self._queue_traj_srv = self.create_service(
            QueueTrajPoint,
            '/yaskawa/queue_traj_point',
            self._handle_queue_point,
            callback_group=self._cb,
        )
        self._queue_point_srv = self.create_service(
            QueueTrajPoint,
            '/yaskawa/queue_point',
            self._handle_queue_point,
            callback_group=self._cb,
        )
        self._queue_point_bare_srv = self.create_service(
            QueueTrajPoint,
            '/queue_point',
            self._handle_queue_point,
            callback_group=self._cb,
        )

        # 3. stop_traj_mode (Trigger)
        self._stop_traj_srv = self.create_service(
            Trigger,
            '/yaskawa/stop_traj_mode',
            self._handle_trigger_ok,
            callback_group=self._cb,
        )

        # 4. reset_error (Trigger)
        self._reset_error_srv = self.create_service(
            Trigger,
            '/yaskawa/reset_error',
            self._handle_trigger_ok,
            callback_group=self._cb,
        )

        # 5. servo_on (Trigger)
        self._servo_on_srv = self.create_service(
            Trigger,
            '/yaskawa/servo_on',
            self._handle_trigger_ok,
            callback_group=self._cb,
        )

        # ── Relay /joint_states → /yaskawa/joint_states ──────────────
        self._js_pub = self.create_publisher(JointState, '/yaskawa/joint_states', 10)
        self._js_sub = self.create_subscription(
            JointState, '/joint_states',
            self._on_joint_state, 10,
            callback_group=self._cb,
        )

        # ── Publisher tới ros2_control JointTrajectoryController ──────
        # Dùng topic interface (không cần action) để gửi điểm nhanh nhất
        self._jtc_pub = self.create_publisher(
            JointTrajectory,
            '/hc10dtp_arm_controller/joint_trajectory',
            10,
        )

        self.get_logger().info(
            '╔══════════════════════════════════════════════╗\n'
            '║   MotoROS2 Mock Node — Simulation Mode      ║\n'
            '║   Tất cả /yaskawa/* services đã sẵn sàng    ║\n'
            '║   Joint states relay: /joint_states →        ║\n'
            '║                       /yaskawa/joint_states  ║\n'
            '╚══════════════════════════════════════════════╝'
        )

    # ── Service Handlers ──────────────────────────────────────────────

    def _handle_start_queue(self, request, response):
        """Giả lập StartPointQueueMode → trả READY (code=1)."""
        self._queue_mode_active = True
        self._accepted_count = 0
        response.result_code.value = 1  # READY
        response.message = 'Mock: Point Queue Mode activated (simulation)'
        self.get_logger().info('✓ StartPointQueueMode → READY (mock)')
        return response

    def _handle_queue_point(self, request, response):
        """
        Giả lập QueueTrajPoint.
        Nhận JointTrajectoryPoint từ cartesian_streamer,
        forward tới ros2_control JointTrajectoryController.
        """
        if not self._queue_mode_active:
            response.result_code.value = 2  # WRONG_MODE
            response.message = 'Mock: Queue mode not active. Call start_point_queue_mode first.'
            return response

        # Trích xuất joint positions từ request
        point = request.point
        joint_names = list(request.joint_names) if request.joint_names else JOINT_NAMES

        # Forward tới JointTrajectoryController
        traj_msg = JointTrajectory()
        traj_msg.joint_names = joint_names

        # Tạo trajectory point với thời gian ngắn (di chuyển ngay lập tức)
        traj_point = JointTrajectoryPoint()
        traj_point.positions = list(point.positions)
        if point.velocities:
            traj_point.velocities = list(point.velocities)
        # Thời gian thực thi: 0.067s (= QUEUE_DT mặc định của cartesian_streamer)
        traj_point.time_from_start = Duration(sec=0, nanosec=67_000_000)

        traj_msg.joint_names = joint_names
        traj_msg.points = [traj_point]
        self._jtc_pub.publish(traj_msg)

        self._last_joints = list(point.positions)
        self._accepted_count += 1

        # Trả SUCCESS (code=1)
        response.result_code.value = 1  # SUCCESS
        response.message = ''

        if self._accepted_count <= 3 or self._accepted_count % 50 == 0:
            self.get_logger().info(
                f'QueueTrajPoint #{self._accepted_count} → forwarded to JTC. '
                f'joints=[{", ".join(f"{j:.3f}" for j in point.positions)}]'
            )
        return response

    def _handle_trigger_ok(self, request, response):
        """Handler chung cho các Trigger service (luôn trả success)."""
        response.success = True
        response.message = 'Mock: OK (simulation)'
        return response

    # ── Joint State Relay ─────────────────────────────────────────────

    def _on_joint_state(self, msg: JointState):
        """Relay /joint_states → /yaskawa/joint_states."""
        relay = JointState()
        relay.header = msg.header
        relay.name = msg.name
        relay.position = msg.position
        relay.velocity = msg.velocity
        relay.effort = msg.effort
        self._js_pub.publish(relay)


def main():
    rclpy.init()
    executor = MultiThreadedExecutor(num_threads=4)
    node = MotoROS2MockNode()
    executor.add_node(node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.get_logger().info('MotoROS2 Mock Node shutdown.')
        executor.shutdown()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
