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
    
    # ──── Disable VAAPI for libfreenect2 (Fixes corrupt RGB image) ────
    libfreenect2_fix = SetEnvironmentVariable('LIBFREENECT2_PIPELINE', 'cpu')

    # ──── Launch arguments ────
    model_dir_arg = DeclareLaunchArgument(
        'model_dir',
        default_value=os.path.expanduser('~/Downloads/GRU-Model-main'),
        description='Path to directory containing .h5 models and .pkl scalers'
    )

    from ament_index_python.packages import get_package_share_directory

    kinect_model_arg = DeclareLaunchArgument(
        'kinect_model_path',
        default_value=os.path.join(get_package_share_directory('kinect_tracker'), 'models', 'pose_landmarker_full.task'),
        description='Path to MediaPipe pose landmarker model'
    )

    log_dir_arg = DeclareLaunchArgument(
        'log_dir',
        default_value=os.path.expanduser('~/hrc_logs'),
        description='Directory for experiment CSV logs'
    )

    # ──── Nodes ────

    kinect_bridge_node = Node(
        package='kinect2_bridge',
        executable='kinect2_bridge_node',
        name='kinect2_bridge',
        output='screen',
        parameters=[{
            'fps_limit': 30.0,
            'depth_method': 'cpu',
            'reg_method': 'default'
        }],
    )

    kinect_tracker_node = Node(
        package='kinect_tracker',
        executable='kinect_node',
        name='kinect_tracker',
        output='screen',
        parameters=[{
            'model_path': LaunchConfiguration('kinect_model_path'),
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
        libfreenect2_fix,
        model_dir_arg,
        kinect_model_arg,
        log_dir_arg,
        kinect_bridge_node,
        kinect_tracker_node,
        predictor_node,
        logger_node,
        ui_node,
    ])
