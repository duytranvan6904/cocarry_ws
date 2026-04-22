#!/usr/bin/env python3
"""
cocarry_full.launch.py
──────────────────────
Launch file tích hợp toàn bộ pipeline co-carrying.

Kiến trúc 2 terminal:
  Terminal 1 (MoveIt stack):
    ros2 launch hc10dtp_moveit_config hc10dtp_start.launch.py

  Terminal 2 (Co-carry pipeline):
    ros2 launch hrc_bringup cocarry_full.launch.py

Pipeline data flow:
  RealSense → realsense_tracker → /hand_position
    → trajectory_predictor → /ml/predicted_position
    → coord_transform → /cartesian_streamer/target_pose
    → cartesian_streamer_hc10dtp → /yaskawa/queue_traj_point
    → HC10DTP robot
"""

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # ── Environment fix (TensorFlow + protobuf conflict) ─────────────────
    env_fix = SetEnvironmentVariable(
        'PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION', 'python')

    # ── Launch arguments ──────────────────────────────────────────────────
    model_dir_arg = DeclareLaunchArgument(
        'model_dir',
        default_value=os.path.expanduser('~/Downloads/GRU-Model-main'),
        description='Path to directory containing .h5 models and .pkl scalers')

    log_dir_arg = DeclareLaunchArgument(
        'log_dir',
        default_value=os.path.expanduser('~/cocarry_logs'),
        description='Directory for experiment CSV logs')

    # ── Config paths ──────────────────────────────────────────────────────
    rs_model_path = os.path.join(
        get_package_share_directory('realsense_tracker'),
        'models', 'pose_landmarker_full.task')

    transform_params = os.path.join(
        get_package_share_directory('coord_transform'),
        'config', 'transform_params.yaml')

    # ── Nodes ─────────────────────────────────────────────────────────────

    # 1. Camera tracking node
    realsense_node = Node(
        package='realsense_tracker',
        executable='realsense_node',
        name='realsense_tracker',
        output='screen',
        parameters=[{
            'model_path': rs_model_path,
            'offset_x': 0.0,
            'offset_y': 0.0,
            'offset_z': 0.0,
        }])

    # 2. Trajectory prediction node
    predictor_node = Node(
        package='trajectory_predictor',
        executable='predictor_node',
        name='trajectory_predictor',
        output='screen',
        parameters=[{
            'model_dir': LaunchConfiguration('model_dir'),
            'default_model': 'gru',
            'auto_start': True,
            'window_size': 20,
            'num_features': 3,
            'scaler_x_file': 'scaler_x.pkl',
            'scaler_y_file': 'scaler_y.pkl',
            'clear_on_tracking_lost': 1.0,
            'model_files.gru': 'gru_velocity_3_layers.h5',
            'model_files.lstm': 'lstm_velocity_3_layers.h5',
            'model_files.rnn': 'rnn_velocity_3_layers.h5',
        }])

    # 3. Coordinate transform node (cầu nối giữa 2 repo)
    transform_node = Node(
        package='coord_transform',
        executable='transform_node',
        name='coord_transform',
        output='screen',
        parameters=[transform_params])

    # 4. Cartesian streamer (kết nối robot)
    streamer_node = Node(
        package='hc10dtp_bringup',
        executable='cartesian_streamer_hc10dtp.py',
        name='cartesian_streamer',
        output='screen')

    # 5. Experiment logger
    logger_node = Node(
        package='experiment_logger',
        executable='logger_node',
        name='experiment_logger',
        output='screen',
        parameters=[{
            'log_dir': LaunchConfiguration('log_dir'),
            'auto_start': True,
        }])

    # 6. UI dashboard
    ui_node = Node(
        package='predictor_ui',
        executable='ui_node',
        name='predictor_ui',
        output='screen')

    return LaunchDescription([
        env_fix,
        model_dir_arg,
        log_dir_arg,
        realsense_node,
        predictor_node,
        transform_node,
        streamer_node,
        logger_node,
        ui_node,
    ])
