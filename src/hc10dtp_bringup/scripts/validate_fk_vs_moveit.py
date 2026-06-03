#!/usr/bin/env python3
"""
validate_fk_vs_moveit.py
────────────────────────
Script cross-validate local FK vs MoveIt! /compute_fk.
Chạy khi có ROS 2 và MoveIt! đang hoạt động.

Cách dùng:
  # Terminal 1: khởi động MoveIt!
  ros2 launch hc10dtp_moveit_config hc10dtp_start.launch.py

  # Terminal 2: chạy validation
  python3 validate_fk_vs_moveit.py
"""

import sys
import os
import math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_ik_solver import LocalIKSolver

import rclpy
from rclpy.node import Node
from moveit_msgs.srv import GetPositionFK
from moveit_msgs.msg import RobotState
from geometry_msgs.msg import PoseStamped
import threading


JOINT_NAMES = [
    'joint_1_s', 'joint_2_l', 'joint_3_u',
    'joint_4_r', 'joint_5_b', 'joint_6_t'
]

# Tư thế co-carry home
HOME_JOINTS = [1.5705, 0.0748, -1.0491, -0.0304, -0.5231, -0.0017]


class FKValidator(Node):
    def __init__(self):
        super().__init__('fk_validator')
        self._fk_cli = self.create_client(GetPositionFK, '/compute_fk')
        self._solver = LocalIKSolver()

    def solve_moveit_fk(self, joints):
        """Gọi MoveIt! /compute_fk."""
        if not self._fk_cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().error('/compute_fk service not available!')
            return None

        req = GetPositionFK.Request()
        req.header.frame_id = 'base_link'
        req.header.stamp = self.get_clock().now().to_msg()
        req.fk_link_names = ['tool0']

        seed = RobotState()
        seed.joint_state.name = JOINT_NAMES
        seed.joint_state.position = joints
        req.robot_state = seed

        event = threading.Event()
        result_holder = [None]

        def _done(f):
            result_holder[0] = f
            event.set()

        fut = self._fk_cli.call_async(req)
        fut.add_done_callback(_done)
        if not event.wait(timeout=5.0):
            return None

        res = result_holder[0].result()
        if res and res.pose_stamped:
            p = res.pose_stamped[0].pose
            return {
                'pos': [p.position.x, p.position.y, p.position.z],
                'quat': [p.orientation.x, p.orientation.y, p.orientation.z, p.orientation.w],
            }
        return None

    def run_validation(self, n_random=50):
        print("=" * 70)
        print("FK Cross-Validation: Local FK vs MoveIt! /compute_fk")
        print("=" * 70)

        # Test configurations
        test_configs = []

        # 1) Home (zeros)
        test_configs.append(('Home (q=0)', [0.0] * 6))

        # 2) Co-carry home
        test_configs.append(('Co-carry home', HOME_JOINTS))

        # 3) Random configs trong soft limits
        rng = np.random.default_rng(42)
        soft_limits = [
            (0.00, 3.14), (-0.80, 1.20), (-2.00, 1.05),
            (-1.05, 1.05), (-2.09, 0.52), (-1.05, 1.05),
        ]
        for i in range(n_random):
            q = [rng.uniform(lo, hi) for lo, hi in soft_limits]
            test_configs.append((f'Random #{i+1}', q))

        max_pos_err = 0.0
        max_ori_err = 0.0
        errors = []

        for name, q in test_configs:
            # Local FK
            pos_local, quat_local = self._solver.fk_pose(q)

            # MoveIt! FK
            result = self.solve_moveit_fk(q)
            if result is None:
                print(f"  [{name}] MoveIt! FK FAILED — skipping")
                continue

            pos_moveit = np.array(result['pos'])
            quat_moveit = np.array(result['quat'])

            # Position error
            pos_err = np.linalg.norm(pos_local - pos_moveit)
            pos_err_mm = pos_err * 1000

            # Orientation error (quaternion dot product)
            dot = abs(np.dot(quat_local, quat_moveit))
            ori_err_deg = math.degrees(2 * math.acos(min(1.0, dot))) if dot < 1.0 else 0.0

            errors.append((pos_err_mm, ori_err_deg))
            max_pos_err = max(max_pos_err, pos_err_mm)
            max_ori_err = max(max_ori_err, ori_err_deg)

            # Print chỉ nếu error lớn hoặc là named test
            if pos_err_mm > 0.1 or not name.startswith('Random'):
                print(f"  [{name}]")
                print(f"    Local:  pos=({pos_local[0]:.5f}, {pos_local[1]:.5f}, {pos_local[2]:.5f})")
                print(f"    MoveIt: pos=({pos_moveit[0]:.5f}, {pos_moveit[1]:.5f}, {pos_moveit[2]:.5f})")
                print(f"    Error:  pos={pos_err_mm:.4f}mm, ori={ori_err_deg:.4f}°")

        print("\n" + "─" * 70)
        if errors:
            pos_errs = [e[0] for e in errors]
            ori_errs = [e[1] for e in errors]
            print(f"  Total tests:     {len(errors)}")
            print(f"  Position error:  max={max(pos_errs):.4f}mm, mean={np.mean(pos_errs):.4f}mm")
            print(f"  Orient. error:   max={max(ori_errs):.4f}°, mean={np.mean(ori_errs):.4f}°")
            passed = max_pos_err < 1.0  # < 1mm
            print(f"\n  Result: {'✓ PASSED' if passed else '✗ FAILED'} (threshold: 1.0mm)")
        else:
            print("  No tests completed!")
        print("=" * 70)


def main():
    rclpy.init()
    node = FKValidator()
    executor = rclpy.executors.MultiThreadedExecutor(num_threads=2)
    executor.add_node(node)

    # Spin trong thread riêng
    spin_thread = threading.Thread(target=executor.spin, daemon=True)
    spin_thread.start()

    try:
        node.run_validation(n_random=50)
    finally:
        executor.shutdown()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
