#!/usr/bin/env python3
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    # ──── Global Environment Fix for TensorFlow/ROS conflict ────
    # Forces python-based protobuf to avoid C++ descriptor database crashes
    env_fix = SetEnvironmentVariable('PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION', 'python')

    # ──── Launch arguments ────
    model_dir_arg = DeclareLaunchArgument(
        'model_dir',
        default_value=os.path.expanduser('~/Downloads/GRU-Model-main'),
        description='Path to directory containing .h5 models and .pkl scalers'
    )

    from ament_index_python.packages import get_package_share_directory

    rs_model_arg = DeclareLaunchArgument(
        'rs_model_path',
        default_value=os.path.join(get_package_share_directory('realsense_tracker'), 'models', 'pose_landmarker_full.task'),
        description='Path to MediaPipe pose landmarker model'
    )

    log_dir_arg = DeclareLaunchArgument(
        'log_dir',
        default_value=os.path.expanduser('~/hrc_logs'),
        description='Directory for experiment CSV logs'
    )

    # ──── Nodes ────

    realsense_node = Node(
        package='realsense_tracker',
        executable='realsense_node',
        name='realsense_tracker',
        output='screen',
        parameters=[{
            'model_path': LaunchConfiguration('rs_model_path'),
            'offset_x': 0.0,
            'offset_y': 0.0,
            'offset_z': 0.0,
        }],
    )

    predictor_node = Node(
        package='trajectory_predictor',
        executable='predictor_node',
        name='trajectory_predictor',
        output='screen',
        parameters=[{
            'model_dir': LaunchConfiguration('model_dir'),
            'default_model': 'gru',
            'scaler_x_file': 'scaler_x.pkl',
            'scaler_y_file': 'scaler_y.pkl',
            'window_size': 20,
            'num_features': 3,
            'auto_start': False,
            'clear_on_tracking_lost': 1.0,
            'model_files.rnn': 'rnn_velocity_3_layers.h5',
            'model_files.gru': 'gru_velocity_3_layers.h5',
            'model_files.lstm': 'lstm_velocity_3_layers.h5',
        }],
    )

    ui_node = Node(
        package='predictor_ui',
        executable='ui_node',
        name='predictor_ui',
        output='screen',
    )

    logger_node = Node(
        package='experiment_logger',
        executable='logger_node',
        name='experiment_logger',
        output='screen',
        parameters=[{
            'log_dir': LaunchConfiguration('log_dir'),
            'auto_start': True,
            'default_model': 'gru',
        }],
    )

    return LaunchDescription([
        env_fix,
        model_dir_arg,
        rs_model_arg,
        log_dir_arg,
        realsense_node,
        predictor_node,
        logger_node,
        ui_node,
    ])
