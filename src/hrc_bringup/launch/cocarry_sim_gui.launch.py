#!/usr/bin/env python3
import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    model_dir_arg = DeclareLaunchArgument(
        'model_dir',
        default_value=os.path.expanduser('~/Downloads/GRU-Model-main'),
        description='Path to directory containing .h5 models and .pkl scalers',
    )
    log_dir_arg = DeclareLaunchArgument(
        'log_dir',
        default_value=os.path.expanduser('~/cocarry_logs'),
        description='Directory for experiment CSV logs',
    )

    sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('hc10dtp_simulation'),
                'launch',
                'sim_start.launch.py',
            )
        )
    )

    cocarry_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('hrc_bringup'),
                'launch',
                'cocarry_full.launch.py',
            )
        ),
        launch_arguments={
            'model_dir': LaunchConfiguration('model_dir'),
            'log_dir': LaunchConfiguration('log_dir'),
        }.items(),
    )

    return LaunchDescription([
        model_dir_arg,
        log_dir_arg,
        sim_launch,
        cocarry_launch,
    ])
