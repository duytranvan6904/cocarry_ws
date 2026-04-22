# HRC Co-Carrying Robot Project — Agent Task Instructions

## Tổng quan dự án

Đây là tài liệu hướng dẫn cho AI agents thực hiện việc tích hợp hai repo thành một workspace hoàn chỉnh cho bài toán **Human-Robot Co-Carrying** (người và robot cùng mang vật). Hệ thống theo dõi tay người qua camera, dự đoán quỹ đạo tương lai bằng deep learning, rồi stream tọa độ đặt real-time xuống robot cộng tác Yaskawa HC10DTP.

---

## Thông tin repo nguồn

### Repo 1 — `hrc_ws` (Experiment workspace)

**Vị trí:** `~/hrc_ws/`

**Packages hiện có:**
- `hrc_bringup` — launch files và config tổng (`full_pipeline.launch.py`, `all_params.yaml`)
- `human_hand_msgs` — custom ROS 2 messages: `HandState`, `HandPrediction`
- `realsense_tracker` — đọc Intel RealSense D-series + MediaPipe pose landmark → publish tọa độ 3D cổ tay người dùng topic `/hand_position` (msg type: `HandState`)
- `trajectory_predictor` — chạy inference GRU/LSTM/RNN trong subprocess tách biệt, subscribe `/hand_position`, publish `/ml/predicted_position` (msg type: `HandPrediction`)
- `experiment_logger` — tính MAE real-time, ghi CSV log
- `predictor_ui` — dashboard PyQtGraph hiển thị trajectory thực tế vs dự đoán theo 3 trục X/Y/Z

**Stack:** Python 3.10, ROS 2 Humble, TensorFlow, MediaPipe, PyQt5, pyrealsense2

---

### Repo 2 — `gp4_ws` (Robot Controller workspace)

**Vị trí:** `~/gp4_ws/`

**Packages hiện có:**
- `hc10dtp_bringup` — launch files cho HC10DTP, chứa `cartesian_streamer_hc10dtp.py` và `restamp_joint_states.py`
- `hc10dtp_moveit_config` — URDF (dùng `motoman_hc10dtp_support`), SRDF, kinematics (TRAC-IK), MoveIt controllers config, launch `hc10dtp_start.launch.py`
- `cpp_pubsub` — C++ nodes cho trajectory action client, joint state monitor (giữ nguyên, không cần sửa)

**Stack:** C++14, Python 3, ROS 2 Humble, MoveIt2, MotoROS2, motoros2_interfaces

**Robot:** Yaskawa HC10DTP collaborative robot, controller YRC1000micro, MotoROS2 driver expose `/yaskawa/*` services

**Kiến trúc quan trọng:**
- MotoROS2 driver chạy trực tiếp trên YRC1000micro, **không** dùng `ros2_control`
- `cartesian_streamer_hc10dtp.py` dùng Point Queue Mode (`/yaskawa/start_point_queue_mode` + `/yaskawa/queue_traj_point`)
- Stream rate: 20 Hz, queue_dt: 0.05s, SMOOTH_ALPHA: 0.4, MAX_JOINT_DELTA: 0.3 rad
- IK solver: TRAC-IK qua `/compute_ik` service (MoveIt move_group)
- Joint names: `joint_1_s, joint_2_l, joint_3_u, joint_4_r, joint_5_b, joint_6_t`
- MoveIt group: `hc10dtp_arm`, EE link: `tool0`, base frame: `base_link`

---

## Workspace mới cần tạo

**Tên:** `cocarry_ws`
**Vị trí:** `~/cocarry_ws/`

### Cấu trúc thư mục mục tiêu

```
cocarry_ws/
├── src/
│   ├── hrc_bringup/           (copy từ hrc_ws, SẼ ĐƯỢC SỬA)
│   ├── human_hand_msgs/       (copy từ hrc_ws, SẼ ĐƯỢC SỬA)
│   ├── realsense_tracker/     (copy từ hrc_ws, giữ nguyên)
│   ├── trajectory_predictor/  (copy từ hrc_ws, giữ nguyên)
│   ├── experiment_logger/     (copy từ hrc_ws, giữ nguyên)
│   ├── predictor_ui/          (copy từ hrc_ws, giữ nguyên)
│   ├── coord_transform/       ← TẠO MỚI HOÀN TOÀN
│   ├── hc10dtp_bringup/       (copy từ gp4_ws, giữ nguyên)
│   └── hc10dtp_moveit_config/ (copy từ gp4_ws, giữ nguyên)
└── README.md                  ← TẠO MỚI
```

---

## Task 1 — Tạo workspace và copy source

**Ưu tiên:** P0 (làm đầu tiên)

**Mô tả:** Khởi tạo workspace `cocarry_ws` và copy toàn bộ packages từ 2 repo nguồn.

**Các lệnh cần thực thi:**

```bash
# Tạo workspace
mkdir -p ~/cocarry_ws/src

# Copy từ hrc_ws
cp -r ~/hrc_ws/src/hrc_bringup        ~/cocarry_ws/src/
cp -r ~/hrc_ws/src/human_hand_msgs    ~/cocarry_ws/src/
cp -r ~/hrc_ws/src/realsense_tracker  ~/cocarry_ws/src/
cp -r ~/hrc_ws/src/trajectory_predictor ~/cocarry_ws/src/
cp -r ~/hrc_ws/src/experiment_logger  ~/cocarry_ws/src/
cp -r ~/hrc_ws/src/predictor_ui       ~/cocarry_ws/src/

# Copy từ gp4_ws
cp -r ~/gp4_ws/src/hc10dtp_bringup        ~/cocarry_ws/src/
cp -r ~/gp4_ws/src/hc10dtp_moveit_config  ~/cocarry_ws/src/

# Build thử để xác nhận không có conflict
cd ~/cocarry_ws
colcon build --symlink-install 2>&1 | tail -30
source install/setup.bash
```

**Điều kiện thành công:** `colcon build` hoàn thành không có lỗi (warning là chấp nhận được).

---

## Task 2 — Cập nhật `HandPrediction` message để hỗ trợ multi-step prediction

**Ưu tiên:** P0

**File cần sửa:** `~/cocarry_ws/src/human_hand_msgs/msg/HandPrediction.msg`

**Nội dung file mới (thay thế hoàn toàn):**

```
# HandPrediction.msg
# Kết quả dự đoán quỹ đạo từ trajectory_predictor node

string model_name
float32 inference_time_ms
int32 buffer_size

# Multi-step prediction: mảng tọa độ cho N bước tương lai
# Index 0 = hiện tại, index N-1 = xa nhất trong tương lai
# Đơn vị: meters, trong camera frame
float32[] pred_x
float32[] pred_y
float32[] pred_z

# Thời gian giữa mỗi bước dự đoán (seconds)
float32 dt_per_step

# Backward compatibility: tọa độ của bước gần nhất (= pred_x[0], pred_y[0], pred_z[0])
float32 x
float32 y
float32 z
```

**Sau khi sửa file:** Rebuild package `human_hand_msgs`:

```bash
cd ~/cocarry_ws
colcon build --packages-select human_hand_msgs --symlink-install
```

**Lưu ý cho agent:** Sau khi sửa message, cần kiểm tra xem `trajectory_predictor` và `predictor_ui` có dùng field `x, y, z` trực tiếp không. Nếu có, chúng vẫn hoạt động vì ta giữ backward compatibility. Tuy nhiên, cần cập nhật `trajectory_predictor` để publish thêm mảng `pred_x, pred_y, pred_z` nếu model output multi-step.

---

## Task 3 — Tạo package `coord_transform` (TASK QUAN TRỌNG NHẤT)

**Ưu tiên:** P0

**Mô tả:** Tạo mới hoàn toàn package Python ROS 2 làm cầu nối giữa prediction output và robot streamer. Package này thực hiện 3 việc:
1. Thêm **object offset**: bù trừ khoảng cách từ wrist landmark của MediaPipe đến điểm gắn robot trên vật co-carry
2. **Transform hệ tọa độ**: chuyển từ camera frame (RealSense, Z hướng ra trước, Y hướng xuống) sang robot base frame (`base_link`)
3. **Safety clamp**: giới hạn tọa độ trong workspace an toàn của robot

### Task 3.1 — Tạo cấu trúc package

```bash
cd ~/cocarry_ws/src
mkdir -p coord_transform/coord_transform
mkdir -p coord_transform/config
mkdir -p coord_transform/scripts
touch coord_transform/coord_transform/__init__.py
```

### Task 3.2 — Tạo `package.xml`

**File:** `~/cocarry_ws/src/coord_transform/package.xml`

```xml
<?xml version="1.0"?>
<package format="3">
  <name>coord_transform</name>
  <version>0.1.0</version>
  <description>
    Coordinate transform node for HRC co-carrying:
    transforms predicted hand position from camera frame to robot base frame,
    applies object offset, and publishes PoseStamped for cartesian_streamer.
  </description>
  <maintainer email="duy@example.com">Duy Tran</maintainer>
  <license>Apache-2.0</license>

  <buildtool_depend>ament_python</buildtool_depend>

  <depend>rclpy</depend>
  <depend>geometry_msgs</depend>
  <depend>std_msgs</depend>
  <depend>human_hand_msgs</depend>
  <depend>tf2_ros</depend>
  <depend>tf2_geometry_msgs</depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

### Task 3.3 — Tạo `setup.py`

**File:** `~/cocarry_ws/src/coord_transform/setup.py`

```python
from setuptools import setup
import os
from glob import glob

package_name = 'coord_transform'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'scripts'), glob('scripts/*.py')),
    ],
    install_requires=['setuptools', 'numpy', 'scipy'],
    zip_safe=True,
    maintainer='Duy Tran',
    maintainer_email='duy@example.com',
    description='Coordinate transform for HRC co-carrying',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'transform_node = coord_transform.transform_node:main',
        ],
    },
)
```

Tạo resource marker:
```bash
mkdir -p ~/cocarry_ws/src/coord_transform/resource
touch ~/cocarry_ws/src/coord_transform/resource/coord_transform
```

### Task 3.4 — Tạo `transform_node.py` (node chính)

**File:** `~/cocarry_ws/src/coord_transform/coord_transform/transform_node.py`

```python
#!/usr/bin/env python3
"""
transform_node.py
─────────────────
Node cầu nối giữa trajectory_predictor và cartesian_streamer.

Pipeline:
  /ml/predicted_position (HandPrediction, camera frame)
    → [object offset] → [cam→base transform] → [safety clamp]
  → /cartesian_streamer/target_pose (PoseStamped, robot base frame)

Cách chạy độc lập để test:
  ros2 run coord_transform transform_node --ros-args \
    --params-file /path/to/transform_params.yaml
"""

import numpy as np
from scipy.spatial.transform import Rotation

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Point, Quaternion
from std_msgs.msg import String
from human_hand_msgs.msg import HandPrediction


class CoordTransformNode(Node):

    def __init__(self):
        super().__init__('coord_transform')
        self._declare_all_params()
        self._load_params()
        self._setup_pubsub()
        self.get_logger().info(
            'CoordTransformNode khởi động.\n'
            f'  Object offset (cam frame): {self._obj_offset}\n'
            f'  Translation cam→base:      {self._t_cam_to_base}\n'
            f'  EE orientation (xyzw):     {self._ee_orient}\n'
            f'  Prediction step:           {self._pred_step}\n'
            f'  Workspace X: {self._ws_x}, Y: {self._ws_y}, Z: {self._ws_z}'
        )

    # ─── Parameter declarations ──────────────────────────────────────────

    def _declare_all_params(self):
        # Object offset: từ wrist landmark → điểm gắn robot trên vật (meters, camera frame)
        self.declare_parameter('object_offset_x', 0.0)
        self.declare_parameter('object_offset_y', 0.0)
        self.declare_parameter('object_offset_z', 0.0)

        # Rotation camera frame → robot base frame (quaternion xyzw)
        # Xác định bằng calibration script
        self.declare_parameter('cam_to_base_qx', 0.0)
        self.declare_parameter('cam_to_base_qy', 0.0)
        self.declare_parameter('cam_to_base_qz', 0.0)
        self.declare_parameter('cam_to_base_qw', 1.0)

        # Translation: vị trí origin camera trong robot base frame (meters)
        self.declare_parameter('cam_to_base_tx', 0.5)
        self.declare_parameter('cam_to_base_ty', 0.0)
        self.declare_parameter('cam_to_base_tz', 1.2)

        # EE orientation mặc định cho robot khi co-carrying (quaternion xyzw)
        # Default: EE hướng xuống (phù hợp với co-carrying ngang)
        self.declare_parameter('ee_orient_x', 0.0)
        self.declare_parameter('ee_orient_y', 1.0)
        self.declare_parameter('ee_orient_z', 0.0)
        self.declare_parameter('ee_orient_w', 0.0)

        # Dùng bước dự đoán thứ mấy (0=hiện tại, N=lookahead xa hơn)
        # Tăng để bù đắp độ trễ pipeline: camera latency + IK + queue buffer
        self.declare_parameter('prediction_step', 3)

        # Workspace safety bounds (robot base frame, meters)
        self.declare_parameter('workspace_x_min', -1.0)
        self.declare_parameter('workspace_x_max',  1.0)
        self.declare_parameter('workspace_y_min', -1.0)
        self.declare_parameter('workspace_y_max',  1.0)
        self.declare_parameter('workspace_z_min',  0.05)
        self.declare_parameter('workspace_z_max',  1.5)

    def _load_params(self):
        # Object offset
        self._obj_offset = np.array([
            self.get_parameter('object_offset_x').value,
            self.get_parameter('object_offset_y').value,
            self.get_parameter('object_offset_z').value,
        ])

        # Rotation matrix từ quaternion
        qx = self.get_parameter('cam_to_base_qx').value
        qy = self.get_parameter('cam_to_base_qy').value
        qz = self.get_parameter('cam_to_base_qz').value
        qw = self.get_parameter('cam_to_base_qw').value
        self._R_cam_to_base = Rotation.from_quat([qx, qy, qz, qw]).as_matrix()

        # Translation
        self._t_cam_to_base = np.array([
            self.get_parameter('cam_to_base_tx').value,
            self.get_parameter('cam_to_base_ty').value,
            self.get_parameter('cam_to_base_tz').value,
        ])

        # EE orientation
        self._ee_orient = [
            self.get_parameter('ee_orient_x').value,
            self.get_parameter('ee_orient_y').value,
            self.get_parameter('ee_orient_z').value,
            self.get_parameter('ee_orient_w').value,
        ]

        self._pred_step = int(self.get_parameter('prediction_step').value)

        # Workspace bounds
        self._ws_x = (
            self.get_parameter('workspace_x_min').value,
            self.get_parameter('workspace_x_max').value,
        )
        self._ws_y = (
            self.get_parameter('workspace_y_min').value,
            self.get_parameter('workspace_y_max').value,
        )
        self._ws_z = (
            self.get_parameter('workspace_z_min').value,
            self.get_parameter('workspace_z_max').value,
        )

    def _setup_pubsub(self):
        # Subscribe: tọa độ dự đoán từ trajectory_predictor
        self._pred_sub = self.create_subscription(
            HandPrediction,
            '/ml/predicted_position',
            self._on_prediction,
            10,
        )

        # Publish: target pose cho cartesian_streamer
        self._target_pub = self.create_publisher(
            PoseStamped,
            '/cartesian_streamer/target_pose',
            10,
        )

        # Publish: debug pose (để kiểm tra trong RViz)
        self._debug_pub = self.create_publisher(
            PoseStamped,
            '/coord_transform/debug_pose',
            10,
        )

        # Publish: trạng thái node (để UI theo dõi)
        self._status_pub = self.create_publisher(
            String,
            '/coord_transform/status',
            10,
        )

    # ─── Callback ────────────────────────────────────────────────────────

    def _on_prediction(self, msg: HandPrediction):
        """
        Xử lý HandPrediction, transform sang robot base frame,
        rồi publish PoseStamped.
        """
        # Lấy tọa độ theo prediction_step
        # Nếu msg có mảng pred_x (multi-step), dùng step được chọn
        # Nếu chỉ có x,y,z scalar (backward compat), dùng trực tiếp
        if hasattr(msg, 'pred_x') and len(msg.pred_x) > 0:
            step = min(self._pred_step, len(msg.pred_x) - 1)
            p_cam = np.array([msg.pred_x[step], msg.pred_y[step], msg.pred_z[step]])
        else:
            p_cam = np.array([msg.x, msg.y, msg.z])

        # Bước 1: Kiểm tra tọa độ hợp lệ (không phải NaN/Inf)
        if not np.all(np.isfinite(p_cam)):
            self.get_logger().warn(
                f'Tọa độ dự đoán không hợp lệ: {p_cam}',
                throttle_duration_sec=1.0,
            )
            return

        # Bước 2: Thêm object offset (trong camera frame)
        # Đây là vector từ wrist landmark đến điểm gắn robot trên vật
        p_cam_obj = p_cam + self._obj_offset

        # Bước 3: Transform sang robot base frame
        # Phép biến đổi: p_base = R * p_cam_obj + t
        p_base = self._R_cam_to_base @ p_cam_obj + self._t_cam_to_base

        # Bước 4: Safety clamp — giới hạn trong workspace robot
        p_clamped, was_clamped = self._clamp_to_workspace(p_base)
        if was_clamped:
            self.get_logger().warn(
                f'Tọa độ bị clamp: {p_base} → {p_clamped}',
                throttle_duration_sec=1.0,
            )

        # Bước 5: Tạo và publish PoseStamped
        target = PoseStamped()
        target.header.frame_id = 'base_link'
        target.header.stamp = self.get_clock().now().to_msg()
        target.pose.position.x = float(p_clamped[0])
        target.pose.position.y = float(p_clamped[1])
        target.pose.position.z = float(p_clamped[2])
        target.pose.orientation.x = float(self._ee_orient[0])
        target.pose.orientation.y = float(self._ee_orient[1])
        target.pose.orientation.z = float(self._ee_orient[2])
        target.pose.orientation.w = float(self._ee_orient[3])

        self._target_pub.publish(target)
        self._debug_pub.publish(target)

        self.get_logger().info(
            f'Transform: cam{p_cam.round(3)} → base{p_clamped.round(3)}',
            throttle_duration_sec=1.0,
        )

    def _clamp_to_workspace(self, p: np.ndarray):
        """Clamp điểm vào workspace an toàn. Trả về (p_clamped, was_clamped)."""
        p_c = np.array([
            np.clip(p[0], self._ws_x[0], self._ws_x[1]),
            np.clip(p[1], self._ws_y[0], self._ws_y[1]),
            np.clip(p[2], self._ws_z[0], self._ws_z[1]),
        ])
        was_clamped = not np.allclose(p, p_c)
        return p_c, was_clamped


def main(args=None):
    rclpy.init(args=args)
    node = CoordTransformNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Task 3.5 — Tạo file config mặc định

**File:** `~/cocarry_ws/src/coord_transform/config/transform_params.yaml`

```yaml
# transform_params.yaml
# Các tham số này là GIÁ TRỊ MẶC ĐỊNH — cần cập nhật sau khi chạy calibration script

coord_transform:
  ros__parameters:

    # ── Object offset (camera frame, meters) ─────────────────────────────
    # Vector từ wrist landmark của MediaPipe đến điểm gắn robot trên vật
    # Đo bằng thước từ cổ tay người đến điểm gắn flange robot
    # Điều chỉnh theo thiết kế cụ thể của jig/handle co-carrying
    object_offset_x: 0.05    # 5cm theo trục X camera (sang phải)
    object_offset_y: 0.0     # 0cm theo trục Y camera
    object_offset_z: 0.10    # 10cm theo trục Z camera (xa hơn về phía trước)

    # ── Camera → Robot Base transform ────────────────────────────────────
    # XÁC ĐỊNH BẰNG CALIBRATION SCRIPT (Task 4)
    # Sau khi chạy calibrate_camera_to_robot.py, copy kết quả vào đây

    # Quaternion rotation (xyzw format)
    cam_to_base_qx: 0.0
    cam_to_base_qy: 0.0
    cam_to_base_qz: 0.0
    cam_to_base_qw: 1.0    # Identity rotation — PHẢI cập nhật sau calibration

    # Translation: vị trí origin camera trong robot base frame (meters)
    cam_to_base_tx: 0.5    # Camera đặt cách robot 0.5m theo X
    cam_to_base_ty: 0.0
    cam_to_base_tz: 1.2    # Camera treo cao 1.2m

    # ── End-effector orientation ─────────────────────────────────────────
    # Hướng EE của robot khi co-carrying
    # Default (0, 1, 0, 0) = hướng xuống (tool0 pointing down)
    # Điều chỉnh theo hướng gắn handle thực tế
    ee_orient_x: 0.0
    ee_orient_y: 1.0
    ee_orient_z: 0.0
    ee_orient_w: 0.0

    # ── Prediction lookahead ─────────────────────────────────────────────
    # Dùng bước dự đoán thứ mấy (0 = hiện tại, 3 ≈ 0.2s lookahead)
    # Tăng để bù đắp pipeline latency (camera→predict→IK→queue≈150-300ms)
    prediction_step: 3

    # ── Workspace safety bounds (robot base frame, meters) ───────────────
    # HC10DTP có tầm với 1.2m — giới hạn theo môi trường thực nghiệm
    workspace_x_min: -1.0
    workspace_x_max:  1.0
    workspace_y_min: -1.0
    workspace_y_max:  1.0
    workspace_z_min:  0.05   # Không cho robot đâm xuống sàn
    workspace_z_max:  1.5
```

### Task 3.6 — Build package

```bash
cd ~/cocarry_ws
colcon build --packages-select coord_transform --symlink-install
source install/setup.bash
```

---

## Task 4 — Tạo calibration script

**Ưu tiên:** P0 (cần thiết trước khi chạy thực nghiệm)

**Mô tả:** Script này giúp xác định chính xác transform từ camera frame sang robot base frame bằng cách khớp các cặp điểm tương ứng đo được từ cả hai hệ tọa độ.

**File:** `~/cocarry_ws/src/coord_transform/scripts/calibrate_camera_to_robot.py`

```python
#!/usr/bin/env python3
"""
calibrate_camera_to_robot.py
──────────────────────────────
Tính ma trận transform từ camera frame (RealSense) → robot base frame.

QUY TRÌNH THỰC NGHIỆM:
  1. In ra hoặc tạo 6-8 marker vật lý (ArUco marker hoặc điểm màu nổi bật)
  2. Đặt từng marker tại vị trí cố định trong không gian làm việc
  3. Dùng robot teach pendant di chuyển TCP đến từng marker, đọc tọa độ XYZ
     (đây là tọa độ trong robot base frame)
  4. Giữ nguyên vị trí marker, đọc tọa độ XYZ từ RealSense + MediaPipe
     hoặc dùng depth point cloud để lấy tọa độ
  5. Điền cả hai bộ tọa độ vào POINTS_CAM và POINTS_ROBOT bên dưới
  6. Chạy script này để tính transform

CHẠY:
  python3 calibrate_camera_to_robot.py
  python3 calibrate_camera_to_robot.py --output ../config/transform_params.yaml

YÊU CẦU:
  pip install numpy scipy pyyaml
"""

import numpy as np
from scipy.spatial.transform import Rotation
import yaml
import argparse
import sys


# ══════════════════════════════════════════════════════════════════════════════
# NHẬP DỮ LIỆU ĐO ĐẠC (điền vào sau khi đo thực tế)
# ══════════════════════════════════════════════════════════════════════════════

# Tọa độ các điểm marker đo từ camera RealSense (camera frame, meters)
# Thứ tự: [x, y, z] — phải khớp 1-1 với POINTS_ROBOT bên dưới
POINTS_CAM = np.array([
    # Ví dụ (thay bằng số đo thực):
    # [x_cam,  y_cam,  z_cam ]
    [ 0.10,   0.05,   0.82  ],
    [ 0.30,   0.08,   0.91  ],
    [-0.12,  -0.03,   0.85  ],
    [ 0.05,   0.18,   0.76  ],
    [ 0.22,  -0.10,   0.88  ],
    [-0.05,   0.12,   0.79  ],
])

# Tọa độ các điểm marker đọc từ robot teach pendant (robot base frame, meters)
# Thứ tự: [x, y, z] — phải khớp 1-1 với POINTS_CAM bên trên
POINTS_ROBOT = np.array([
    # Ví dụ (thay bằng số đọc từ teach pendant):
    # [x_base, y_base, z_base]
    [ 0.50,   0.12,   0.38  ],
    [ 0.62,  -0.08,   0.35  ],
    [ 0.42,   0.15,   0.40  ],
    [ 0.52,  -0.04,   0.48  ],
    [ 0.58,   0.20,   0.36  ],
    [ 0.44,   0.08,   0.45  ],
])

# ══════════════════════════════════════════════════════════════════════════════


def solve_rigid_transform(points_src: np.ndarray, points_dst: np.ndarray):
    """
    Tìm R, t sao cho: points_dst ≈ R @ points_src + t

    Sử dụng SVD decomposition (phương pháp Kabsch algorithm).
    Đây là least-squares solution tối ưu cho rigid body transform.

    Returns:
        R: (3,3) rotation matrix
        t: (3,) translation vector
        quat: (4,) quaternion [x, y, z, w]
        rmse_mm: residual error in mm
    """
    assert points_src.shape == points_dst.shape, "Số điểm phải bằng nhau"
    assert points_src.shape[0] >= 3, "Cần ít nhất 3 điểm"

    n = points_src.shape[0]

    # Tính centroid
    c_src = points_src.mean(axis=0)
    c_dst = points_dst.mean(axis=0)

    # Center về centroid
    A = points_src - c_src
    B = points_dst - c_dst

    # Covariance matrix
    H = A.T @ B

    # SVD
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T

    # Sửa reflection nếu det(R) < 0 (đảm bảo proper rotation)
    if np.linalg.det(R) < 0:
        Vt[-1, :] *= -1
        R = Vt.T @ U.T

    # Translation
    t = c_dst - R @ c_src

    # Tính residual RMSE
    transformed = (R @ points_src.T).T + t
    residuals = np.linalg.norm(transformed - points_dst, axis=1)
    rmse_mm = residuals.mean() * 1000.0

    # Chuyển sang quaternion [x, y, z, w]
    quat = Rotation.from_matrix(R).as_quat()

    return R, t, quat, rmse_mm


def print_results(R, t, quat, rmse_mm):
    print('\n' + '═' * 60)
    print('  KẾT QUẢ CALIBRATION')
    print('═' * 60)
    print(f'\nResidual RMSE: {rmse_mm:.2f} mm')
    if rmse_mm > 20:
        print('  ⚠  RMSE > 20mm — kiểm tra lại dữ liệu đo đạc!')
    elif rmse_mm > 10:
        print('  ⚠  RMSE > 10mm — có thể chấp nhận nhưng nên đo thêm')
    else:
        print('  ✓  RMSE tốt (< 10mm)')

    print(f'\nRotation matrix R:')
    for row in R:
        print(f'  [{row[0]:+.6f}  {row[1]:+.6f}  {row[2]:+.6f}]')

    print(f'\nQuaternion (x, y, z, w):')
    print(f'  x = {quat[0]:+.8f}')
    print(f'  y = {quat[1]:+.8f}')
    print(f'  z = {quat[2]:+.8f}')
    print(f'  w = {quat[3]:+.8f}')

    print(f'\nTranslation (meters):')
    print(f'  tx = {t[0]:+.6f}')
    print(f'  ty = {t[1]:+.6f}')
    print(f'  tz = {t[2]:+.6f}')
    print()


def write_yaml(output_path: str, quat, t, current_yaml_path=None):
    """Ghi kết quả vào file YAML params."""

    # Đọc YAML hiện tại nếu có
    if current_yaml_path:
        try:
            with open(current_yaml_path) as f:
                data = yaml.safe_load(f)
        except FileNotFoundError:
            data = {}
    else:
        data = {}

    # Cập nhật các field calibration
    if 'coord_transform' not in data:
        data['coord_transform'] = {}
    if 'ros__parameters' not in data['coord_transform']:
        data['coord_transform']['ros__parameters'] = {}

    params = data['coord_transform']['ros__parameters']
    params['cam_to_base_qx'] = float(quat[0])
    params['cam_to_base_qy'] = float(quat[1])
    params['cam_to_base_qz'] = float(quat[2])
    params['cam_to_base_qw'] = float(quat[3])
    params['cam_to_base_tx'] = float(t[0])
    params['cam_to_base_ty'] = float(t[1])
    params['cam_to_base_tz'] = float(t[2])

    with open(output_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    print(f'✓ Đã ghi kết quả vào: {output_path}')


def main():
    parser = argparse.ArgumentParser(
        description='Calibrate camera-to-robot base transform')
    parser.add_argument(
        '--output', type=str, default=None,
        help='Path to output YAML file (e.g. ../config/transform_params.yaml)')
    parser.add_argument(
        '--update', type=str, default=None,
        help='Path to existing YAML to update (keeps other params)')
    args = parser.parse_args()

    if len(POINTS_CAM) < 4:
        print('LỖI: Cần ít nhất 4 cặp điểm. Điền thêm vào POINTS_CAM và POINTS_ROBOT.')
        sys.exit(1)

    print(f'Số cặp điểm: {len(POINTS_CAM)}')
    R, t, quat, rmse_mm = solve_rigid_transform(POINTS_CAM, POINTS_ROBOT)
    print_results(R, t, quat, rmse_mm)

    if args.output:
        write_yaml(args.output, quat, t, current_yaml_path=args.update)
    else:
        print('Dùng --output <file.yaml> để lưu kết quả.')


if __name__ == '__main__':
    main()
```

**Cách dùng sau khi đo thực tế:**

```bash
# Sau khi điền POINTS_CAM và POINTS_ROBOT:
cd ~/cocarry_ws/src/coord_transform/scripts
python3 calibrate_camera_to_robot.py \
  --output ../config/transform_params.yaml \
  --update ../config/transform_params.yaml
```

---

## Task 5 — Tạo launch file tích hợp

**Ưu tiên:** P1

**File:** `~/cocarry_ws/src/hrc_bringup/launch/cocarry_full.launch.py`

```python
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
            'auto_start': True,         # Tự động bắt đầu dự đoán
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
```

---

## Task 6 — Tạo README.md cho workspace mới

**Ưu tiên:** P2

**File:** `~/cocarry_ws/README.md`

```markdown
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
```

---

## Task 7 — Kiểm tra tích hợp end-to-end

**Ưu tiên:** P1 (thực hiện sau khi hoàn thành Task 1-6)

**Mô tả:** Kiểm tra từng bước trong chuỗi pipeline.

### Bước 7.1 — Test build toàn bộ

```bash
cd ~/cocarry_ws
colcon build --symlink-install
source install/setup.bash
```

Kết quả mong đợi: tất cả packages build thành công.

### Bước 7.2 — Test coord_transform node độc lập

```bash
# Terminal 1: Chạy node
ros2 run coord_transform transform_node \
  --ros-args --params-file ~/cocarry_ws/src/coord_transform/config/transform_params.yaml

# Terminal 2: Publish test message
ros2 topic pub /ml/predicted_position human_hand_msgs/msg/HandPrediction \
  '{x: 0.1, y: 0.05, z: 0.8, model_name: "test", inference_time_ms: 5.0}'

# Terminal 3: Xem output
ros2 topic echo /cartesian_streamer/target_pose
ros2 topic echo /coord_transform/debug_pose
```

### Bước 7.3 — Test full pipeline không có robot

```bash
# Terminal 1: MoveIt (giả lập, không kết nối robot thật)
ros2 launch hc10dtp_moveit_config hc10dtp_start.launch.py

# Terminal 2: Pipeline với demo pattern (không cần camera hay robot thật)
# Chạy cartesian_streamer với demo để kiểm tra IK hoạt động
cd ~/cocarry_ws
source install/setup.bash
python3 src/hc10dtp_bringup/scripts/cartesian_streamer_hc10dtp.py --demo line
```

### Bước 7.4 — Test full pipeline với robot thật

```bash
# Đảm bảo: robot ở AUTO mode, E-stop released, MotoROS2 driver chạy

# Terminal 1:
ros2 launch hc10dtp_moveit_config hc10dtp_start.launch.py

# Terminal 2:
ros2 launch hrc_bringup cocarry_full.launch.py \
  model_dir:=~/Downloads/GRU-Model-main

# Kiểm tra topics:
ros2 topic hz /ml/predicted_position     # Phải ~20-25 Hz
ros2 topic hz /cartesian_streamer/target_pose  # Phải ~20-25 Hz
ros2 topic hz /yaskawa/joint_states      # Phải ~50 Hz
```

---

## Checklist hoàn thành

Đánh dấu `[x]` khi mỗi task hoàn thành:

- [ ] **Task 1** — Tạo workspace `cocarry_ws`, copy packages, build thành công
- [ ] **Task 2** — Cập nhật `HandPrediction.msg` với multi-step fields
- [ ] **Task 3** — Tạo package `coord_transform` (node + config + setup)
- [ ] **Task 4** — Tạo và chạy calibration script với dữ liệu đo thực tế
- [ ] **Task 5** — Tạo `cocarry_full.launch.py`
- [ ] **Task 6** — Tạo README.md
- [ ] **Task 7.1** — Build toàn bộ workspace không lỗi
- [ ] **Task 7.2** — Test `coord_transform` node độc lập
- [ ] **Task 7.3** — Test pipeline với MoveIt giả lập
- [ ] **Task 7.4** — Test end-to-end với robot thật

---

## Lưu ý kỹ thuật quan trọng

### Về MotoROS2 / HC10DTP
- **KHÔNG** dùng `ros2_control` hay `real_robot.launch.py` — sẽ tạo xung đột với MotoROS2
- MotoROS2 tự expose `/yaskawa/*` services khi driver chạy trên YRC1000micro
- Point Queue Mode yêu cầu: (1) `start_point_queue_mode` → (2) gửi seed point (t=0) → (3) stream cumulative timestamps
- `time_from_start` phải LUÔN tăng lũy tiến (cumulative), không phải delta

### Về coordinate frames
- Camera RealSense: Z hướng ra phía trước, Y hướng xuống, X sang phải
- Robot base frame (`base_link`): theo chuẩn REP-103, Z hướng lên, X hướng ra trước
- Calibration cần ít nhất 6 cặp điểm, phân bố đều trong workspace để giảm sai số
- RMSE < 10mm là tốt, 10-20mm chấp nhận được, > 20mm cần đo lại

### Về prediction lookahead
- Mỗi step dự đoán ≈ `window_step` giây (thường 0.04-0.067s với 15-25Hz)
- `prediction_step=3` ≈ 0.12-0.2s lookahead
- Pipeline latency ước tính: camera→MediaPipe (~50ms) + GRU inference (~10ms) + IK (~50ms) + queue buffer (~100ms) = ~200-300ms tổng
- Nên set `prediction_step` sao cho `step × dt ≈ 200-300ms`

### Về safety
- `MAX_JOINT_DELTA=0.3 rad` trong `cartesian_streamer_hc10dtp.py` — đây là hard safety limit
- `SMOOTH_ALPHA=0.4` kiểm soát tốc độ đuổi theo target — giảm để mượt hơn
- Workspace bounds trong `transform_params.yaml` là lớp safety thứ hai
- HC10DTP có collaborative safety built-in (force limiting) — nhưng software limits vẫn quan trọng
```
