"""
sim_start.launch.py
───────────────────
Launch mô phỏng HOÀN CHỈNH cho HC10DTP co-carrying experiments.

Kiến trúc:
  ┌────────────────────┐
  │  MoveIt move_group  │  ← IK solver, planning scene
  │  (fake hardware)    │
  └──────────┬─────────┘
             │
  ┌──────────▼─────────┐
  │  ros2_control       │  ← GenericSystem (mock hardware)
  │  + JTC + JSB        │     publish /joint_states
  └──────────┬─────────┘
             │
  ┌──────────▼─────────┐
  │  motoros2_mock_node  │  ← relay /joint_states → /yaskawa/joint_states
  │                     │     mock /yaskawa/* services
  │                     │     forward queue points → JTC
  └─────────────────────┘

Cách dùng:
  Terminal 1: ros2 launch hc10dtp_simulation sim_start.launch.py
  Terminal 2: python3 cartesian_streamer_hc10dtp.py --demo line

LƯU Ý: File này KHÔNG thay đổi bất kỳ file nào trong hc10dtp_moveit_config.
        Nó sử dụng tham số use_fake_hardware:=true đã có sẵn trong URDF xacro.
"""

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():

    # ── MoveIt config (dùng fake hardware) ───────────────────────────
    moveit_config = (
        MoveItConfigsBuilder("motoman_hc10dtp", package_name="hc10dtp_moveit_config")
        .robot_description(
            file_path="config/motoman_hc10dtp.urdf.xacro",
            mappings={"use_fake_hardware": "true"},
        )
        .robot_description_semantic(file_path="config/motoman_hc10dtp.srdf")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .planning_pipelines(pipelines=["ompl"])
        .to_moveit_configs()
    )

    planning_scene_monitor_parameters = {
        "publish_planning_scene": True,
        "publish_geometry_updates": True,
        "publish_state_updates": True,
        "publish_transforms_updates": True,
        "publish_robot_description": True,
        "publish_robot_description_semantic": True,
        "provide_planning_scene_service": True,
    }

    # ── Static TF (world -> base_link) ───────────────────────────────
    static_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="static_transform_publisher",
        output="log",
        arguments=["0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "world", "base_link"],
    )

    # ── Robot State Publisher ────────────────────────────────────────
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="both",
        parameters=[moveit_config.robot_description],
    )

    # ── ros2_control controller_manager (fake hardware) ──────────────
    ros2_controllers_path = os.path.join(
        get_package_share_directory("hc10dtp_moveit_config"),
        "config",
        "ros2_controllers.yaml",
    )

    ros2_control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            moveit_config.robot_description,
            ros2_controllers_path,
        ],
        output="screen",
    )

    # Spawn controllers (chờ controller_manager sẵn sàng trước)
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ],
        output="screen",
    )

    arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "hc10dtp_arm_controller",
            "--controller-manager",
            "/controller_manager",
        ],
        output="screen",
    )

    # ── MoveIt move_group ────────────────────────────────────────────
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_config.to_dict(),
            planning_scene_monitor_parameters,
        ],
    )

    # ── RViz ─────────────────────────────────────────────────────────
    rviz_config_path = os.path.join(
        get_package_share_directory("hc10dtp_moveit_config"),
        "config",
        "moveit.rviz",
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_path],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.planning_pipelines,
            moveit_config.robot_description_kinematics,
        ],
    )

    # ── MotoROS2 Mock Node ───────────────────────────────────────────
    # Chờ 3 giây để ros2_control + controller khởi động xong
    motoros2_mock_node = TimerAction(
        period=3.0,
        actions=[
            Node(
                package="hc10dtp_simulation",
                executable="motoros2_mock_node.py",
                name="motoros2_mock",
                output="screen",
            ),
        ],
    )

    return LaunchDescription(
        [
            static_tf,
            robot_state_publisher,
            ros2_control_node,
            joint_state_broadcaster_spawner,
            arm_controller_spawner,
            move_group_node,
            rviz_node,
            motoros2_mock_node,
        ]
    )
