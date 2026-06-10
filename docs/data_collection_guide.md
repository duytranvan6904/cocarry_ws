# Hướng dẫn thu thập dữ liệu tọa độ tay người

## Tổng quan

Thu thập tọa độ cổ tay (wrist) 3D (x, y, z) qua camera RealSense + MediaPipe, ghi vào CSV với tần số 16Hz, thời lượng mỗi trial 8s. Hỗ trợ 9 kịch bản (3 Free + 6 Change), mỗi kịch bản lặp 4 lần.

---

## Pipeline dữ liệu

```
RealSense Camera (30fps)
  → realsense_tracker → /hand_position (HandState)
    → coord_transform → /transformed_hand_pose (PoseStamped) ⚠️ CHƯA TỒN TẠI
    → data_collection_gui.py (subscribe + ghi CSV)
```

---

## Thứ tự chạy

### Bước 1: Build workspace

```bash
cd ~/cocarry_ws
colcon build --symlink-install --packages-select \
  human_hand_msgs realsense_tracker coord_transform hrc_bringup
source install/setup.bash
```

### Bước 2: Chạy camera tracker

```bash
# Terminal 1
ros2 run realsense_tracker realsense_node \
  --ros-args -p model_path:=$(ros2 pkg prefix realsense_tracker)/share/realsense_tracker/models/pose_landmarker_full.task
```

Node này publish: `/hand_position` (msg type: `HandState` với `x, y, z`)

### Bước 3: Chạy GUI thu thập dữ liệu

```bash
# Terminal 2
cd ~/cocarry_ws && source install/setup.bash
python3 src/data_collection_gui.py
```

### Bước 4: Thao tác trên GUI

1. Nhập **Participant ID** (vd: `p01`)
2. Điều chỉnh **Duration** (mặc định 8s) và **Y-Threshold** (mặc định 0.60m)
3. Nhấn **START TRIAL** → GUI bắt đầu ghi dữ liệu
4. Sau khi hết thời gian → tự động lưu CSV và chuyển scenario tiếp theo

---

## ⚠️ Phân tích kết nối: `data_collection_gui.py` và trục Y

### Kết quả kiểm tra: **CÓ VẤN ĐỀ VỀ TOPIC**

| Hạng mục | Chi tiết |
|---|---|
| **Topic subscribe** | `/transformed_hand_pose` (`PoseStamped`) — dòng 91 |
| **Topic có sẵn** | `/hand_position` (`HandState`) — do `realsense_tracker` publish |
| **Vấn đề** | **KHÔNG CÓ NODE NÀO** publish topic `/transformed_hand_pose` |

### Chi tiết vấn đề

`data_collection_gui.py` subscribe topic `/transformed_hand_pose` (kiểu `PoseStamped`):

```python
# Dòng 89-94
self.sub_pose = self.create_subscription(
    PoseStamped,
    '/transformed_hand_pose',    # ← TOPIC NÀY KHÔNG TỒN TẠI
    self.pose_callback,
    10
)
```

Trong khi pipeline thực tế chỉ có:
- `realsense_tracker` → publish `/hand_position` (kiểu `HandState`)
- `coord_transform` → publish `/coord_transform/filtered_hand_position` (kiểu `PointStamped`)
- `coord_transform` → publish `/cartesian_streamer/target_pose` (kiểu `PoseStamped`, nhưng đây là tọa độ robot, KHÔNG phải tay)

**→ GUI sẽ KHÔNG nhận được dữ liệu tọa độ tay. `latest_pose` luôn = `None`.**

### Logic Y-threshold (nếu có dữ liệu)

Logic đọc trục Y và đổi target **đã được implement đầy đủ** tại `App.update_loop()` (dòng 547-576):

```python
# Dòng 551-558
if self.manager.current_scenario.is_change_scenario() and not self.manager.change_triggered:
    if self.ros_node.latest_pose is not None:
        _, current_y, _ = self.ros_node.latest_pose     # Đọc Y
        if current_y >= self.manager.y_threshold:        # So sánh threshold
            self.manager.change_triggered = True         # Kích hoạt đổi target
            self.bell()
```

**Kết luận**: Logic threshold **đúng**, nhưng **không bao giờ chạy** vì `latest_pose` luôn `None` do sai topic.

---

## 🔧 Cách sửa

Có 2 phương án:

### Phương án A: Đổi GUI subscribe `/hand_position` (HandState) — **Khuyến nghị**

Không cần `coord_transform`, GUI nhận trực tiếp tọa độ thô từ camera:

```python
# Thay đổi trong class HandPoseSubscriber:

from human_hand_msgs.msg import HandState   # Thêm import

# Đổi subscription:
self.sub_pose = self.create_subscription(
    HandState,
    '/hand_position',
    self.pose_callback,
    10
)

# Đổi callback:
def pose_callback(self, msg):
    if msg.is_tracked:
        self.latest_pose = (msg.x, msg.y, msg.z)
```

### Phương án B: Đổi GUI subscribe `/coord_transform/filtered_hand_position` (PointStamped)

Nhận tọa độ đã lọc, cần chạy thêm `coord_transform`:

```python
from geometry_msgs.msg import PointStamped

self.sub_pose = self.create_subscription(
    PointStamped,
    '/coord_transform/filtered_hand_position',
    self.pose_callback,
    10
)

def pose_callback(self, msg):
    self.latest_pose = (msg.point.x, msg.point.y, msg.point.z)
```

---

## Cấu trúc dữ liệu đầu ra

```
~/cocarry_ws/cocarry_logs/data_collection/
└── p01/
    ├── p01_SCF1_r01_20260604_090000.csv
    ├── p01_SCF1_r02_20260604_090100.csv
    └── ...
```

**Header CSV:**
```
# participant_id: p01
# scenario_id: SCF1
# mode: Free
# initial_target: 1
# final_target: 1
# sample_rate_hz: 16.0
# trial_duration_s: 8.0
# y_threshold_trigger: 0.6
timestamp_s, x, y, z
```

---

## 9 Kịch bản

| ID | Mode | Initial → Final Target |
|---|---|---|
| SCF1 | Free | T1 → T1 |
| SCF2 | Free | T2 → T2 |
| SCF3 | Free | T3 → T3 |
| SCC1 | Change | T1 → T2 |
| SCC2 | Change | T2 → T1 |
| SCC3 | Change | T1 → T3 |
| SCC4 | Change | T2 → T3 |
| SCC5 | Change | T3 → T1 |
| SCC6 | Change | T3 → T2 |

**Tổng**: 9 scenarios × 4 repeats = **36 trials / participant**
