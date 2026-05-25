#!/usr/bin/env python3
"""
test_queue_diagnostic.py
────────────────────────
Script chẩn đoán tối giản: test trực tiếp MotoROS2 Point Queue Mode
trên HC10DTP hardware KHÔNG qua cartesian_streamer.

Chạy:
  export ROS_DOMAIN_ID=10
  source ~/cocarry_ws/install/setup.bash
  python3 src/hc10dtp_bringup/scripts/test_queue_diagnostic.py
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


class QueueDiagnostic(Node):
    def __init__(self):
        super().__init__('queue_diagnostic')
        self._current_joints = None

        self._js_sub = self.create_subscription(
            JointState, '/joint_states',
            self._on_js, 10)

        self.get_logger().info('='*60)
        self.get_logger().info('  HC10DTP Queue Diagnostic Tool')
        self.get_logger().info('='*60)

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

    def wait_for_joints(self, timeout=10.0):
        self.get_logger().info('[1/6] Đang chờ /joint_states...')
        start = time.time()
        while rclpy.ok() and self._current_joints is None:
            rclpy.spin_once(self, timeout_sec=0.1)
            if time.time() - start > timeout:
                self.get_logger().error('TIMEOUT: Không nhận được /joint_states!')
                return False
        self.get_logger().info(
            f'  ✓ Nhận được joints: '
            f'{[f"{j:.4f}" for j in self._current_joints]}')
        return True

    def call_service_sync(self, client, request, name, timeout=5.0):
        """Gọi service đồng bộ và trả về response."""
        if not client.wait_for_service(timeout_sec=3.0):
            self.get_logger().error(f'  ✗ Service {name} KHÔNG khả dụng!')
            return None
        future = client.call_async(request)
        start = time.time()
        while rclpy.ok() and not future.done():
            rclpy.spin_once(self, timeout_sec=0.05)
            if time.time() - start > timeout:
                self.get_logger().error(f'  ✗ Service {name} TIMEOUT!')
                return None
        return future.result()

    def step_stop_traj(self):
        self.get_logger().info('[2/6] Gọi /stop_traj_mode...')
        cli = self.create_client(Trigger, '/stop_traj_mode')
        res = self.call_service_sync(cli, Trigger.Request(), 'stop_traj_mode')
        if res:
            self.get_logger().info(
                f'  → success={res.success}, message="{res.message}"')
        time.sleep(0.5)

    def step_reset_error(self):
        self.get_logger().info('[3/6] Gọi /reset_error (ResetError type)...')
        cli = self.create_client(ResetError, '/reset_error')
        res = self.call_service_sync(cli, ResetError.Request(), 'reset_error')
        if res:
            self.get_logger().info(
                f'  → result_code={res.result_code.value}, '
                f'message="{res.message}"')
        time.sleep(0.5)

    def step_start_queue(self):
        self.get_logger().info('[4/6] Gọi /start_point_queue_mode...')
        cli = self.create_client(
            StartPointQueueMode, '/start_point_queue_mode')
        res = self.call_service_sync(
            cli, StartPointQueueMode.Request(), 'start_point_queue_mode')
        if res:
            self.get_logger().info(
                f'  → result_code={res.result_code.value}, '
                f'message="{res.message}"')
            if res.result_code.value in (0, 1):
                self.get_logger().info('  ✓ Point Queue Mode ACTIVE!')
                return True
            else:
                self.get_logger().error('  ✗ Point Queue Mode FAILED!')
                return False
        return False

    def step_send_seed(self):
        self.get_logger().info('[5/6] Gửi SEED point (joints hiện tại, t=0, v=0)...')
        cli = self.create_client(QueueTrajPoint, '/queue_traj_point')
        if not cli.wait_for_service(timeout_sec=3.0):
            self.get_logger().error('  ✗ Service /queue_traj_point KHÔNG khả dụng!')
            # Thử /queue_point
            cli = self.create_client(QueueTrajPoint, '/queue_point')
            if not cli.wait_for_service(timeout_sec=3.0):
                self.get_logger().error(
                    '  ✗ Service /queue_point CŨNG KHÔNG khả dụng!')
                return False, None
            self.get_logger().info('  → Dùng /queue_point thay thế.')

        req = QueueTrajPoint.Request()
        req.joint_names = JOINT_NAMES

        point = JointTrajectoryPoint()
        point.positions = list(self._current_joints)
        point.velocities = [0.0] * 6
        point.time_from_start = Duration(sec=0, nanosec=0)
        req.point = point

        res = self.call_service_sync(cli, req, 'queue_traj_point (seed)')
        if res:
            code = res.result_code.value if hasattr(res, 'result_code') else 'N/A'
            msg = res.message if hasattr(res, 'message') else ''
            self.get_logger().info(
                f'  → result_code={code}, message="{msg}"')
            if code in (0, 1):
                self.get_logger().info('  ✓ Seed point ACCEPTED!')
                return True, cli
            else:
                self.get_logger().error(f'  ✗ Seed point REJECTED! code={code}')
                return False, cli
        return False, None

    def step_send_motion_points(self, cli, num_points=10):
        self.get_logger().info(
            f'[6/6] Gửi {num_points} motion points '
            f'(joint_1 oscillation ±0.02 rad)...')

        cumulative_ns = 0
        dt_ns = 67_000_000  # 67ms = ~15Hz (giống GP4)
        accepted = 0
        rejected = 0

        for i in range(num_points):
            cumulative_ns += dt_ns
            total_sec = cumulative_ns // 1_000_000_000
            total_nsec = cumulative_ns % 1_000_000_000

            # Tạo chuyển động nhỏ trên joint_1 (±0.02 rad sine)
            delta = 0.02 * math.sin(2.0 * math.pi * i / num_points)
            joints = list(self._current_joints)
            joints[0] += delta

            req = QueueTrajPoint.Request()
            req.joint_names = JOINT_NAMES

            point = JointTrajectoryPoint()
            point.positions = [float(j) for j in joints]
            # Tính velocity
            if i == 0:
                point.velocities = [0.0] * 6
            else:
                dt = dt_ns / 1e9
                point.velocities = [delta / dt] + [0.0] * 5
            point.time_from_start = Duration(
                sec=int(total_sec), nanosec=int(total_nsec))
            req.point = point

            res = self.call_service_sync(
                cli, req, f'motion_point_{i+1}', timeout=2.0)
            if res:
                code = res.result_code.value if hasattr(res, 'result_code') else -1
                msg = res.message if hasattr(res, 'message') else ''
                t_sec = total_sec + total_nsec / 1e9
                if code in (0, 1):
                    accepted += 1
                    self.get_logger().info(
                        f'  Point {i+1}/{num_points}: ACCEPTED '
                        f'(t={t_sec:.3f}s, j1_delta={delta:.4f})')
                elif code == 4:
                    self.get_logger().warn(
                        f'  Point {i+1}/{num_points}: BUSY '
                        f'(t={t_sec:.3f}s) — retrying...')
                    time.sleep(0.05)
                    # retry once
                    res2 = self.call_service_sync(
                        cli, req, f'retry_{i+1}', timeout=2.0)
                    if res2 and res2.result_code.value in (0, 1):
                        accepted += 1
                    else:
                        rejected += 1
                else:
                    rejected += 1
                    self.get_logger().error(
                        f'  Point {i+1}/{num_points}: REJECTED '
                        f'code={code}, msg="{msg}"')
            else:
                rejected += 1
                self.get_logger().error(
                    f'  Point {i+1}/{num_points}: NO RESPONSE')

            time.sleep(0.05)  # small gap between points

        self.get_logger().info('='*60)
        self.get_logger().info(
            f'  KẾT QUẢ: {accepted} accepted, {rejected} rejected '
            f'/ {num_points} total')
        if accepted > 0:
            self.get_logger().info(
                '  ✓ Robot CÓ THỂ nhận điểm — '
                'nếu không thấy di chuyển, kiểm tra biên độ hoặc timing.')
        else:
            self.get_logger().error(
                '  ✗ KHÔNG có điểm nào được chấp nhận — '
                'kiểm tra firmware/config MotoROS2.')
        self.get_logger().info('='*60)

    def run_diagnostic(self):
        if not self.wait_for_joints():
            return

        self.step_stop_traj()
        self.step_reset_error()

        if not self.step_start_queue():
            return

        time.sleep(1.5)  # Đợi servo ổn định

        success, cli = self.step_send_seed()
        if not success:
            return

        time.sleep(0.5)

        self.step_send_motion_points(cli, num_points=20)


def main():
    rclpy.init()
    node = QueueDiagnostic()
    node.run_diagnostic()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
