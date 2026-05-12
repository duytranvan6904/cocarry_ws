#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import yaml
import re
import os

class CaptureHomeNode(Node):
    def __init__(self):
        super().__init__('capture_home_node')
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.listener_callback,
            10)
        self.get_logger().info('Đang chờ dữ liệu từ /joint_states để lưu làm vị trí Home...')

    def listener_callback(self, msg):
        self.get_logger().info('Đã nhận được tọa độ hiện tại! Đang tiến hành lưu...')
        
        # Lấy giá trị từng khớp
        joint_names = ['joint_1_s', 'joint_2_l', 'joint_3_u', 'joint_4_r', 'joint_5_b', 'joint_6_t']
        values = []
        for name in joint_names:
            if name in msg.name:
                idx = msg.name.index(name)
                values.append(msg.position[idx])
            else:
                self.get_logger().error(f'Không tìm thấy {name} trong /joint_states!')
                return

        # 1. Cập nhật initial_positions.yaml
        ws_path = '/home/duy/cocarry_ws'
        init_yaml = f'{ws_path}/src/hc10dtp_moveit_config/config/initial_positions.yaml'
        try:
            with open(init_yaml, 'w') as f:
                f.write('# Tự động tạo bởi capture_home.py\n\ninitial_positions:\n')
                for name, val in zip(joint_names, values):
                    f.write(f'  {name}: {val:.6f}\n')
            self.get_logger().info(f'Đã cập nhật: {init_yaml}')
        except Exception as e:
            self.get_logger().error(f'Lỗi lưu yaml: {e}')

        # 2. Cập nhật motoman_hc10dtp.srdf
        srdf_path = f'{ws_path}/src/hc10dtp_moveit_config/config/motoman_hc10dtp.srdf'
        try:
            with open(srdf_path, 'r') as f:
                content = f.read()

            for name, val in zip(joint_names, values):
                # Regex tìm pattern: <joint name="joint_1_s" value="0"/>
                pattern = r'(<group_state name="home" group="hc10dtp_arm">.*?<joint name="' + name + r'" value=")([^"]+)("/>)'
                content = re.sub(pattern, r'\g<1>' + f'{val:.6f}' + r'\g<3>', content, flags=re.DOTALL)

            with open(srdf_path, 'w') as f:
                f.write(content)
            self.get_logger().info(f'Đã cập nhật SRDF: {srdf_path}')
        except Exception as e:
            self.get_logger().error(f'Lỗi lưu srdf: {e}')

        # 3. Cập nhật go_home.py
        go_home_path = f'{ws_path}/src/hc10dtp_bringup/scripts/go_home.py'
        try:
            with open(go_home_path, 'r') as f:
                go_home_content = f.read()

            new_positions = f'[{", ".join([f"{v:.6f}" for v in values])}]'
            go_home_content = re.sub(
                r'HOME_JOINTS = \[.*?\]',
                f'HOME_JOINTS = {new_positions}',
                go_home_content,
                flags=re.DOTALL
            )
            with open(go_home_path, 'w') as f:
                f.write(go_home_content)
            self.get_logger().info(f'Đã cập nhật go_home.py: {go_home_path}')
        except Exception as e:
            self.get_logger().error(f'Lỗi lưu go_home: {e}')

        self.get_logger().info('\n=== LƯU THÀNH CÔNG ===\nHãy chạy colcon build và khởi động lại launch file để áp dụng!')
        
        # Tắt node sau khi hoàn thành
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = CaptureHomeNode()
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
