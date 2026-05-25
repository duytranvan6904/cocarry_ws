#!/usr/bin/env python3
"""
go_home.py
──────────
Đưa robot HC10DTP về vị trí Home bằng Point Queue Mode (queue_traj_point).

Sử dụng queue_traj_point thay vì FollowJointTrajectory action vì
đã xác nhận hoạt động ổn định trên phần cứng HC10DTP + YRC1000.

Cách dùng:
    export ROS_DOMAIN_ID=10
    source ~/cocarry_ws/install/setup.bash
    python3 src/hc10dtp_bringup/scripts/go_home.py
"""

import rclpy
from rclpy.node import Node
import time
import math

from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectoryPoint
from builtin_interfaces.msg import Duration
from std_srvs.srv import Trigger
from motoros2_interfaces.srv import (
    StartPointQueueMode, QueueTrajPoint, ResetError
)

JOINT_NAMES = [
    'joint_1_s', 'joint_2_l', 'joint_3_u',
    'joint_4_r', 'joint_5_b', 'joint_6_t'
]

# Vị trí Home đã capture từ robot thật
HOME_JOINTS = [1.570532, 0.074803, -1.049094, -0.030408, -0.523142, -0.001725]

# Thời gian di chuyển về Home (giây)
MOVE_DURATION_SEC = 2.5

# Tần suất gửi điểm (Hz) — 15Hz phù hợp HC10DTP
POINT_RATE_HZ = 20.0


class GoHomeNode(Node):
    def __init__(self):
        super().__init__('go_home_node')
        self._current_joints = None

        self._js_sub = self.create_subscription(
            JointState, '/joint_states',
            self._on_js, 10)

    def _on_js(self, msg):
        if self._current_joints is None:
            try:
                joints = []
                for name in JOINT_NAMES:
                    idx = msg.name.index(name)
                    joints.append(msg.position[idx])
                self._current_joints = joints
            except ValueError:
                pass

    def call_service_sync(self, client, request, name, timeout=5.0):
        """Gọi service đồng bộ."""
        if not client.wait_for_service(timeout_sec=3.0):
            self.get_logger().error(f'Service {name} KHÔNG khả dụng!')
            return None
        future = client.call_async(request)
        start = time.time()
        while rclpy.ok() and not future.done():
            rclpy.spin_once(self, timeout_sec=0.05)
            if time.time() - start > timeout:
                self.get_logger().error(f'Service {name} TIMEOUT!')
                return None
        return future.result()

    def run(self):
        # ── Bước 1: Chờ joint_states ──────────────────────────────
        self.get_logger().info('Đang chờ /joint_states...')
        start = time.time()
        while rclpy.ok() and self._current_joints is None:
            rclpy.spin_once(self, timeout_sec=0.1)
            if time.time() - start > 10.0:
                self.get_logger().error('TIMEOUT: Không nhận được /joint_states!')
                return
        self.get_logger().info(
            f'Joints hiện tại: {[f"{j:.4f}" for j in self._current_joints]}')

        # ── Bước 2: Stop mode cũ ─────────────────────────────────
        self.get_logger().info('Gọi stop_traj_mode...')
        cli = self.create_client(Trigger, '/stop_traj_mode')
        self.call_service_sync(cli, Trigger.Request(), 'stop_traj_mode')
        time.sleep(0.5)

        # ── Bước 3: Reset error ───────────────────────────────────
        self.get_logger().info('Gọi reset_error...')
        cli = self.create_client(ResetError, '/reset_error')
        self.call_service_sync(cli, ResetError.Request(), 'reset_error')
        time.sleep(0.5)

        # ── Bước 4: Start Point Queue Mode ────────────────────────
        self.get_logger().info('Gọi start_point_queue_mode...')
        cli = self.create_client(
            StartPointQueueMode, '/start_point_queue_mode')
        res = self.call_service_sync(
            cli, StartPointQueueMode.Request(), 'start_point_queue_mode')
        if not res or res.result_code.value not in (0, 1):
            self.get_logger().error('start_point_queue_mode FAILED!')
            return
        self.get_logger().info('✓ Point Queue Mode ACTIVE — Servo ON!')
        time.sleep(1.5)  # Đợi servo ổn định

        # ── Bước 5: Gửi seed point ───────────────────────────────
        self.get_logger().info('Gửi seed point...')
        queue_cli = self.create_client(QueueTrajPoint, '/queue_traj_point')
        if not queue_cli.wait_for_service(timeout_sec=3.0):
            self.get_logger().error('/queue_traj_point KHÔNG khả dụng!')
            return

        req = QueueTrajPoint.Request()
        req.joint_names = JOINT_NAMES
        seed = JointTrajectoryPoint()
        seed.positions = list(self._current_joints)
        seed.velocities = [0.0] * 6
        seed.time_from_start = Duration(sec=0, nanosec=0)
        req.point = seed
        res = self.call_service_sync(queue_cli, req, 'seed_point')
        if not res or res.result_code.value not in (0, 1):
            self.get_logger().error('Seed point bị từ chối!')
            return
        self.get_logger().info('✓ Seed point accepted.')
        time.sleep(0.3)

        # ── Bước 6: Nội suy và gửi motion points ─────────────────
        dt = 1.0 / POINT_RATE_HZ
        num_points = int(MOVE_DURATION_SEC * POINT_RATE_HZ)
        cumulative_ns = 0
        dt_ns = int(dt * 1e9)
        start_joints = list(self._current_joints)

        self.get_logger().info(
            f'Di chuyển về Home trong {MOVE_DURATION_SEC:.1f}s '
            f'({num_points} points @ {POINT_RATE_HZ:.0f}Hz)...')

        accepted = 0
        for i in range(num_points):
            # Nội suy tuyến tính từ vị trí hiện tại → Home
            alpha = (i + 1) / num_points
            joints = [
                s + alpha * (h - s)
                for s, h in zip(start_joints, HOME_JOINTS)
            ]

            cumulative_ns += dt_ns
            total_sec = cumulative_ns // 1_000_000_000
            total_nsec = cumulative_ns % 1_000_000_000

            req = QueueTrajPoint.Request()
            req.joint_names = JOINT_NAMES
            point = JointTrajectoryPoint()
            point.positions = [float(j) for j in joints]

            # Tính velocity
            vel = [(h - s) / MOVE_DURATION_SEC for s, h in zip(start_joints, HOME_JOINTS)]
            point.velocities = vel
            point.time_from_start = Duration(
                sec=int(total_sec), nanosec=int(total_nsec))
            req.point = point

            res = self.call_service_sync(queue_cli, req, f'point_{i+1}', timeout=2.0)
            if res:
                code = res.result_code.value if hasattr(res, 'result_code') else -1
                if code in (0, 1):
                    accepted += 1
                elif code == 4:  # BUSY → retry
                    time.sleep(0.05)
                    res2 = self.call_service_sync(queue_cli, req, f'retry_{i+1}', timeout=2.0)
                    if res2 and res2.result_code.value in (0, 1):
                        accepted += 1
                else:
                    self.get_logger().warn(
                        f'Point {i+1} rejected: code={code}')

            time.sleep(0.03)  # Pacing

        # Gửi điểm cuối cùng với velocity = 0 để dừng
        cumulative_ns += dt_ns
        total_sec = cumulative_ns // 1_000_000_000
        total_nsec = cumulative_ns % 1_000_000_000
        req = QueueTrajPoint.Request()
        req.joint_names = JOINT_NAMES
        final = JointTrajectoryPoint()
        final.positions = [float(h) for h in HOME_JOINTS]
        final.velocities = [0.0] * 6
        final.time_from_start = Duration(
            sec=int(total_sec), nanosec=int(total_nsec))
        req.point = final
        self.call_service_sync(queue_cli, req, 'final_point')

        self.get_logger().info(
            f'✓ Đã gửi {accepted}/{num_points} points. '
            f'Robot đang di chuyển về Home...')

        # Đợi robot hoàn thành
        time.sleep(MOVE_DURATION_SEC + 1.0)

        # ── Graceful shutdown: thoát Point Queue Mode sạch sẽ ──────
        self.get_logger().info('Thoát Point Queue Mode (stop_traj_mode)...')
        stop_cli = self.create_client(Trigger, '/stop_traj_mode')
        if stop_cli.wait_for_service(timeout_sec=2.0):
            stop_res = self.call_service_sync(stop_cli, Trigger.Request(), 'stop_traj_mode')
            if stop_res:
                self.get_logger().info('✓ stop_traj_mode thành công. Tủ điện sạch sẽ.')
            else:
                self.get_logger().warn('⚠ stop_traj_mode không có phản hồi.')
        else:
            self.get_logger().warn('⚠ /stop_traj_mode service không sẵn sàng.')

        self.get_logger().info('✓ Đã về Home an toàn! Controller đã thoát queue mode.')


def main(args=None):
    rclpy.init(args=args)
    node = GoHomeNode()
    try:
        node.run()
    except KeyboardInterrupt:
        node.get_logger().info('Interrupted! Đang dọn dẹp...')
        # Cố gắng gọi stop_traj_mode ngay cả khi bị Ctrl+C
        try:
            stop_cli = node.create_client(Trigger, '/stop_traj_mode')
            if stop_cli.wait_for_service(timeout_sec=1.0):
                node.call_service_sync(stop_cli, Trigger.Request(), 'emergency_stop')
                node.get_logger().info('✓ stop_traj_mode gửi thành công.')
        except Exception:
            pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
