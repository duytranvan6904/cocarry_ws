#!/bin/bash
export ROS_LOG_DIR=/home/duy/cocarry_ws/cocarry_logs/ros_log
mkdir -p /home/duy/cocarry_ws/cocarry_logs/ros_log

echo "[SHELL] Cleaning up previous processes..."
pkill -f ros2
pkill -f python3
pkill -f transform_node
pkill -f streamer
pkill -f logger

echo "[SHELL] Launching full pipeline..."
source /opt/ros/humble/setup.bash
source /home/duy/cocarry_ws/install/setup.bash
ros2 launch hrc_bringup cocarry_full.launch.py > /home/duy/cocarry_ws/cocarry_logs/launch.log 2>&1 &
LAUNCH_PID=$!

echo "[SHELL] Sleeping 15 seconds for ML model and ROS 2 setup to initialize..."
sleep 15

echo "[SHELL] Running diagnostic tester..."
python3 /home/duy/cocarry_ws/cocarry_logs/test_pipeline_flow.py

echo "[SHELL] Cleaning up background launch (PID $LAUNCH_PID)..."
kill $LAUNCH_PID
pkill -f ros2
pkill -f python3
pkill -f transform_node
pkill -f streamer
pkill -f logger
echo "[SHELL] Complete!"
