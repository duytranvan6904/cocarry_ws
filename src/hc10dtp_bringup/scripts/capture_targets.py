#!/usr/bin/env python3
"""
capture_targets.py
──────────────────
Capture vị trí EE (Cartesian) tại các mốc đích T1/T2/T3 cho tính năng
Target Zone Auto-Snap.

Quy trình sử dụng:
  1. Di chuyển robot (bằng tay hoặc Teach Pendant) đến chính xác vị trí T1.
  2. Chạy:  python3 capture_targets.py T1
  3. Lặp lại cho T2, T3.
  4. Sau khi capture đủ 3 mốc, chạy colcon build lại.

Cách dùng:
    export ROS_DOMAIN_ID=10
    source ~/cocarry_ws/install/setup.bash
    python3 src/hc10dtp_bringup/scripts/capture_targets.py T1
    python3 src/hc10dtp_bringup/scripts/capture_targets.py T2
    python3 src/hc10dtp_bringup/scripts/capture_targets.py T3
    python3 src/hc10dtp_bringup/scripts/capture_targets.py --show
"""

import sys
import os
import re
import yaml
import argparse

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

# Import local FK solver (cùng thư mục)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_ik_solver import LocalIKSolver

JOINT_NAMES = [
    'joint_1_s', 'joint_2_l', 'joint_3_u',
    'joint_4_r', 'joint_5_b', 'joint_6_t'
]

WS_PATH = '/home/duy/cocarry_ws'
YAML_PATH = f'{WS_PATH}/src/coord_transform/config/transform_params.yaml'

VALID_TARGETS = ['T1', 'T2', 'T3']


class CaptureTargetNode(Node):
    def __init__(self, target_name: str):
        super().__init__('capture_target_node')
        self._target_name = target_name.upper()
        self._fk_solver = LocalIKSolver()

        self._sub = self.create_subscription(
            JointState, '/joint_states',
            self._on_joint_state, 10)
        self.get_logger().info(
            f'Đang chờ /joint_states để capture vị trí {self._target_name}...')

    def _on_joint_state(self, msg: JointState):
        # Lấy giá trị từng khớp
        values = []
        for name in JOINT_NAMES:
            if name in msg.name:
                idx = msg.name.index(name)
                values.append(msg.position[idx])
            else:
                self.get_logger().error(f'Không tìm thấy {name} trong /joint_states!')
                return

        # Giải FK → lấy tọa độ EE (x, y, z) trong base_link
        pos, quat = self._fk_solver.fk_pose(values)
        x, y, z = float(pos[0]), float(pos[1]), float(pos[2])

        self.get_logger().info(
            f'\n╔══════════════════════════════════════════════╗\n'
            f'║  {self._target_name} — Capture thành công!              ║\n'
            f'╠══════════════════════════════════════════════╣\n'
            f'║  Joint values:                               ║\n'
            f'║    [{", ".join(f"{v:.6f}" for v in values)}]  ║\n'
            f'║  EE Position (base_link):                    ║\n'
            f'║    X = {x:+.6f} m                           ║\n'
            f'║    Y = {y:+.6f} m                           ║\n'
            f'║    Z = {z:+.6f} m                           ║\n'
            f'╚══════════════════════════════════════════════╝'
        )

        # Cập nhật transform_params.yaml
        self._update_yaml(x, y, z)

        self.get_logger().info(
            f'✓ Đã lưu {self._target_name} vào {YAML_PATH}\n'
            f'  Hãy chạy: colcon build --packages-select coord_transform\n'
            f'  Sau đó source install/setup.bash và restart node.')

        rclpy.shutdown()

    def _update_yaml(self, x: float, y: float, z: float):
        """Cập nhật tọa độ target trong transform_params.yaml."""
        target_key = self._target_name.lower()  # t1, t2, t3

        try:
            with open(YAML_PATH, 'r') as f:
                content = f.read()

            # Regex pattern cho mỗi trục: target_zones.t1_x: 0.0
            for axis, val in [('x', x), ('y', y), ('z', z)]:
                key = f'target_zones.{target_key}_{axis}'
                pattern = rf'({re.escape(key)}:\s*)[\-\d\.]+'
                replacement = f'\\g<1>{val:.6f}'

                if re.search(pattern, content):
                    content = re.sub(pattern, replacement, content)
                else:
                    self.get_logger().warn(
                        f'Không tìm thấy key "{key}" trong YAML. '
                        f'Hãy chắc chắn đã thêm section target_zones vào file.')

            with open(YAML_PATH, 'w') as f:
                f.write(content)

        except Exception as e:
            self.get_logger().error(f'Lỗi cập nhật YAML: {e}')


def show_current_targets():
    """Hiển thị tọa độ các target đã lưu."""
    try:
        with open(YAML_PATH, 'r') as f:
            content = f.read()

        print('\n╔══════════════════════════════════════════════╗')
        print('║  Target Zone Positions (base_link)           ║')
        print('╠══════════════════════════════════════════════╣')

        for t in ['t1', 't2', 't3']:
            coords = {}
            for axis in ['x', 'y', 'z']:
                key = f'target_zones.{t}_{axis}'
                match = re.search(rf'{re.escape(key)}:\s*([\-\d\.]+)', content)
                if match:
                    coords[axis] = float(match.group(1))
                else:
                    coords[axis] = None

            if all(v is not None for v in coords.values()):
                print(f'║  {t.upper()}: ({coords["x"]:+.4f}, {coords["y"]:+.4f}, {coords["z"]:+.4f})  ║')
            else:
                print(f'║  {t.upper()}: (chưa capture)                        ║')

        print('╚══════════════════════════════════════════════╝\n')

    except FileNotFoundError:
        print(f'File không tồn tại: {YAML_PATH}')


def main():
    parser = argparse.ArgumentParser(
        description='Capture vị trí EE tại các mốc đích T1/T2/T3.')
    parser.add_argument(
        'target', nargs='?', default=None,
        help='Tên target: T1, T2, hoặc T3')
    parser.add_argument(
        '--show', action='store_true',
        help='Hiển thị tọa độ các target đã capture')

    args = parser.parse_args()

    if args.show:
        show_current_targets()
        return

    if args.target is None:
        parser.print_help()
        print('\nVí dụ:')
        print('  python3 capture_targets.py T1    # Capture vị trí T1')
        print('  python3 capture_targets.py T2    # Capture vị trí T2')
        print('  python3 capture_targets.py T3    # Capture vị trí T3')
        print('  python3 capture_targets.py --show # Xem tọa độ đã lưu')
        return

    target = args.target.upper()
    if target not in VALID_TARGETS:
        print(f'Lỗi: Target phải là T1, T2, hoặc T3. Nhận được: {args.target}')
        sys.exit(1)

    rclpy.init()
    node = CaptureTargetNode(target)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()


if __name__ == '__main__':
    main()
