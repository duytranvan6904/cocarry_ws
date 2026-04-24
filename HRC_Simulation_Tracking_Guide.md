# Hướng Dẫn Thử Nghiệm Mô Phỏng Co-Carrying (Camera Thật + Robot Ảo)

Tài liệu này hướng dẫn cách chạy hệ thống **Human-Robot Co-Carrying** một cách an toàn nhất: Dùng Camera RealSense thu nhận cử động thực tế của người, nhưng điều khiển Robot trên môi trường ảo (RViz/Gazebo) thay vì robot thật.

## 🌟 Tổng quan Kiến trúc Thử nghiệm

1. **RealSense Node**: Lấy ảnh từ camera thực, chạy AI MediaPipe tìm tọa độ tay người.
2. **Transform Node**: Đồng bộ tọa độ, bù trừ khoảng cách, tính toán tọa độ đích tương đối cho robot.
3. **Cartesian Streamer**: Nhận tọa độ đích, tính IK (động học ngược) để sinh quỹ đạo liên tục.
4. **MotoROS2 Mock & MoveIt (Simulation)**: Đóng giả phần cứng tủ điện YRC1000, nhận quỹ đạo và vẽ robot chuyển động trên RViz.

---

## 🚀 Các Bước Chạy Thử Nghiệm

Ưu tiên chạy theo profile mới để giảm số terminal. Ở mỗi terminal, đảm bảo bạn đã source không gian làm việc:
```bash
cd ~/cocarry_ws
source install/setup.bash
```

### Cách khuyến nghị (1 terminal cho simulation)
Chạy toàn bộ pipeline simulation + GUI trong một lệnh:
```bash
ros2 launch hrc_bringup cocarry_sim_gui.launch.py
```
Lệnh này sẽ tự gom:
- Môi trường mô phỏng (MoveIt + fake hardware + MotoROS2 mock)
- Camera tracking + predictor + transform + cartesian streamer
- GUI dashboard/control panel

### Cách cũ (4 terminal) — giữ lại để debug chi tiết
### Terminal 1: Khởi động Môi trường Mô phỏng
```bash
ros2 launch hc10dtp_simulation sim_start.launch.py
```

### Terminal 2: Bật Camera và AI Tracking
Bật camera RealSense thật và bắt đầu nhận diện khung xương:
```bash
ros2 run realsense_tracker realsense_node
```
*(Đứng vào khung hình để đảm bảo camera nhận ra tay phải của bạn).*

### Terminal 3: Khởi chạy Bộ Xử lý Tọa độ
Node chuyển đổi tọa độ từ Camera sang Robot (dùng hệ quy chiếu tương đối `Relative Displacement` đã cấu hình):
```bash
ros2 run coord_transform transform_node
```

### Terminal 4: Bật Trình Điều khiển Robot (Streamer)
Kết nối luồng tọa độ vào Robot ảo:
```bash
python3 src/hc10dtp_bringup/scripts/cartesian_streamer_hc10dtp.py
```

---

## 🛠 Cách Thao tác Trong Lúc Chạy

Để đảm bảo robot di chuyển đúng theo tọa độ người thật một cách an toàn và đúng trục, bạn bắt buộc phải tuân theo trình tự sau:

1. Đứng vào vị trí chuẩn bị trước Camera, giữ tay ở tư thế tự nhiên.
2. Trên GUI, bấm **`⌖ Calibrate Camera`** (Thiết lập gốc tọa độ của người).
3. Trên GUI, bấm **`📌 Capture Init Pose`** (Chốt vị trí EE hiện tại của robot làm mốc tương đối).
4. Chọn chế độ quỹ đạo: **`📍 Ground Truth`** (tọa độ thực) hoặc **`🧠 Prediction`** (tọa độ dự đoán từ AI).
5. Bấm **`⚡ Enable Robot`**. Robot sẽ chuyển sang trạng thái chờ nhận lệnh (bật Point Queue Mode). *Lưu ý: Nút này sẽ báo lỗi nếu bạn chưa làm bước 2 và 3.*
6. Bấm **`▶ Start Run`**. Dữ liệu sẽ bắt đầu stream xuống robot và được ghi log lại. Di chuyển tay, robot sẽ đi theo bạn. (Lưu ý: Tọa độ camera trục X, Y đã được tự động map chéo sang trục Y, X của robot để khớp với workspace thực tế).
7. Khi cần dừng stream: bấm **`⏸ Stop Run`**. Đồ thị vẫn tiếp tục vẽ nhưng robot sẽ dừng nhận tọa độ.
8. Khi thử nghiệm xong hoặc muốn reset: bấm **`⛔ Disable Robot`** (để thoát Point Queue Mode an toàn).

---

## 🏠 Lệnh Đưa Robot Về Gốc (Go Home)

Sau khi thử nghiệm xong, tay bạn có thể ở vị trí bất kỳ khiến robot bị kẹt ở góc khó. Để đưa robot ảo trở về tư thế thẳng đứng nguyên bản (tất cả khớp = 0), hãy làm theo 2 bước:

Ưu tiên dùng nút `Go Home` trên GUI.

Nếu cần fallback bằng terminal:
```bash
python3 src/hc10dtp_bringup/scripts/go_home.py
```
Robot trên RViz sẽ mượt mà xoay lại tư thế Home (0,0,0,0,0,0).
