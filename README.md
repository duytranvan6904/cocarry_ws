# HRC Co-Carrying Robot Workspace

## Tổng quan

Workspace tích hợp hệ thống **Human-Robot Co-Carrying** sử dụng robot cộng tác Yaskawa HC10DTP.
Người và robot cùng mang một vật, robot dự đoán quỹ đạo chuyển động của tay người
và stream tọa độ đặt real-time để phối hợp chuyển động mượt mà.

## Kiến trúc hệ thống

```
RealSense D-series
      ↓ depth + RGB
realsense_tracker (MediaPipe)
      ↓ /hand_position (HandState)
trajectory_predictor (GRU/LSTM)
      ↓ /ml/predicted_position (HandPrediction)
coord_transform ← transform_params.yaml
      ↓ /cartesian_streamer/target_pose (PoseStamped, robot base frame)
cartesian_streamer_hc10dtp (IK + Point Queue)
      ↓ /yaskawa/queue_traj_point
HC10DTP cobot (YRC1000micro + MotoROS2)
```

## Packages

| Package | Mô tả |
|---|---|
| `realsense_tracker` | Đọc camera, detect wrist landmark 3D |
| `trajectory_predictor` | GRU/LSTM inference, dự đoán N bước tương lai |
| `coord_transform` | Transform tọa độ camera → robot base |
| `hc10dtp_bringup` | Cartesian streamer, launch files robot |
| `hc10dtp_moveit_config` | URDF, SRDF, TRAC-IK, MoveIt config |
| `experiment_logger` | Ghi CSV log, tính MAE |
| `predictor_ui` | PyQtGraph dashboard real-time |
| `human_hand_msgs` | Custom ROS 2 messages |

## Cài đặt

```bash
# Dependencies
sudo apt install ros-humble-moveit ros-humble-tf2-tools
pip install numpy scipy pyrealsense2 mediapipe tensorflow pyqtgraph PyQt5 pyyaml

# Build
cd ~/cocarry_ws
colcon build --symlink-install
source install/setup.bash
```

## Cách chạy

### Terminal 1 — MoveIt stack (bắt buộc chạy trước)
```bash
source ~/cocarry_ws/install/setup.bash
ros2 launch hc10dtp_moveit_config hc10dtp_start.launch.py
```

### Terminal 2 — Co-carry pipeline
```bash
source ~/cocarry_ws/install/setup.bash
ros2 launch hrc_bringup cocarry_full.launch.py \
  model_dir:=~/Downloads/GRU-Model-main
```

## Calibration (bắt buộc trước thực nghiệm)

```bash
cd ~/cocarry_ws/src/coord_transform/scripts
# 1. Điền dữ liệu đo đạc vào POINTS_CAM và POINTS_ROBOT
nano calibrate_camera_to_robot.py

# 2. Chạy script
python3 calibrate_camera_to_robot.py \
  --output ../config/transform_params.yaml \
  --update ../config/transform_params.yaml
```

## Topics quan trọng

| Topic | Type | Mô tả |
|---|---|---|
| `/hand_position` | `HandState` | Tọa độ wrist real-time từ camera |
| `/ml/predicted_position` | `HandPrediction` | Dự đoán quỹ đạo tương lai |
| `/cartesian_streamer/target_pose` | `PoseStamped` | Target pose cho robot |
| `/cartesian_streamer/current_pose` | `PoseStamped` | EE pose phản hồi từ robot |
| `/coord_transform/debug_pose` | `PoseStamped` | Debug transform (xem trong RViz) |
| `/yaskawa/joint_states` | `JointState` | Trạng thái khớp robot |

## Tuning parameters

Sau khi calibration, điều chỉnh trong `transform_params.yaml`:

- `prediction_step`: Tăng (3→5) nếu robot phản ứng chậm so với tay người
- `object_offset_*`: Điều chỉnh theo vị trí gắn handle thực tế
- `workspace_*`: Giới hạn theo không gian làm việc thực nghiệm

Trong `cartesian_streamer_hc10dtp.py`:

- `SMOOTH_ALPHA`: Giảm (0.4→0.2) để chuyển động mượt hơn
- `MAX_JOINT_DELTA`: Giảm (0.3→0.2 rad) cho safety cao hơn
- `DEFAULT_STREAM_HZ`: 15 Hz là ổn định cho HC10DTP
