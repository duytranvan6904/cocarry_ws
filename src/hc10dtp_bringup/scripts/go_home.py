#!/usr/bin/env python3
"""
go_home.py
──────────
Đưa robot HC10DTP về vị trí ban đầu (tất cả các khớp = 0) hoặc vị trí 'ready'.
Script này sử dụng Action Client gọi trực tiếp controller của robot
(áp dụng cho cả Simulation và Robot thật).

Lưu ý: Bạn CẦN phải tắt (Ctrl+C) cartesian_streamer.py trước khi chạy lệnh này
để nhả quyền điều khiển controller.

Cách dùng:
    python3 go_home.py
"""

import rclpy
from rclpy.node import Node
import time
from rclpy.action import ActionClient
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from builtin_interfaces.msg import Duration
from std_srvs.srv import Trigger

class GoHomeNode(Node):
    def __init__(self):
        super().__init__('go_home_node')

        # Dùng hc10dtp_arm_controller/follow_joint_trajectory cho simulation/ros2_control
        # Nếu robot thật sử dụng /follow_joint_trajectory, hãy đổi tên action
        self._action_client = ActionClient(self, FollowJointTrajectory, '/follow_joint_trajectory')
        
        # Tắt point queue mode nếu nó đang chạy ngầm
        self._stop_cli = self.create_client(Trigger, '/stop_traj_mode')
        if self._stop_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Đang gửi lệnh tắt chế độ Stream (Point Queue Mode)...')
            req = Trigger.Request()
            self._stop_cli.call_async(req)
            time.sleep(0.5)

        # Bật servo_on trước và đợi
        self._servo_cli = self.create_client(Trigger, '/servo_on')
        if self._servo_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Đang gửi lệnh bật Servo...')
            req = Trigger.Request()
            self._servo_cli.call_async(req)
            self.get_logger().info('Đợi 2 giây để Servo kịp khởi động...')
            time.sleep(2.0)
            
        # Bật Traj Mode để nhận follow_joint_trajectory
        self._start_traj_cli = self.create_client(Trigger, '/start_traj_mode')
        if self._start_traj_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Đang gửi lệnh bật TRAJ MODE...')
            req = Trigger.Request()
            self._start_traj_cli.call_async(req)
            time.sleep(0.5)

    def send_goal(self):
        self.get_logger().info('Đang chờ action server /hc10dtp_arm_controller/follow_joint_trajectory...')
        self._action_client.wait_for_server()

        goal_msg = FollowJointTrajectory.Goal()
        goal_msg.trajectory.joint_names = [
            'joint_1_s', 'joint_2_l', 'joint_3_u',
            'joint_4_r', 'joint_5_b', 'joint_6_t'
        ]

        point = JointTrajectoryPoint()
        # Vị trí Home đã được capture
        point.positions = [0.000000, 0.000000, -1.571269, 0.000000, 0.000011, 0.000011]
        point.time_from_start = Duration(sec=3, nanosec=0)  # Mất 3 giây để về nhà

        goal_msg.trajectory.points = [point]

        self.get_logger().info('Đang gửi lệnh về Home mới đã capture...')
        self._send_goal_future = self._action_client.send_goal_async(goal_msg)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Lệnh về Home bị từ chối!')
            return

        self.get_logger().info('Robot đang di chuyển về Home...')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Đã về Home an toàn. Mã kết quả: {result.error_code}')
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    action_client = GoHomeNode()
    action_client.send_goal()
    rclpy.spin(action_client)

if __name__ == '__main__':
    main()
