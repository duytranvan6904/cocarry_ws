# Hướng Dẫn Thử Nghiệm Co-Carrying Trên Robot Thật (Yaskawa HC10DTP)

Tài liệu này hướng dẫn cách chạy hệ thống **Human-Robot Co-Carrying** trực tiếp với robot thật Yaskawa HC10DTP thông qua giao thức MotoROS2 và Micro-ROS. 

> [!WARNING]
> **AN TOÀN LÀ TRÊN HẾT**: Khi chạy trên robot thật, luôn giữ tay ở gần nút E-Stop (Dừng khẩn cấp). Trong lần chạy đầu tiên, hãy giới hạn tốc độ (Speed override) trên Teach Pendant ở mức thấp (ví dụ: 10-20%) để đảm bảo an toàn.

---

## 🌟 Tổng quan Kiến trúc

1. **Micro-ROS Agent**: Cầu nối mạng UDP giữa tủ điện YRC1000 và máy tính ROS 2.
2. **RealSense Node**: Lấy ảnh từ camera thực, chạy AI MediaPipe tìm tọa độ tay người.
3. **Transform Node**: Đồng bộ tọa độ, bù trừ khoảng cách, tính toán tọa độ đích tương đối cho robot.
4. **Cartesian Streamer**: Nhận tọa độ đích, tính IK và stream quỹ đạo liên tục xuống robot thật qua MotoROS2 Point Queue Mode (15Hz).
5. **MotoROS2 (Robot)**: Chạy trực tiếp trên tủ điện, nhận lệnh và điều khiển các khớp.

---

## 🚀 Các Bước Khởi Động

### Bước 1: Bật kết nối Micro-ROS Agent (Bắt buộc)
Trước khi kết nối với robot, máy tính cần chạy Agent để nhận luồng dữ liệu UDP từ tủ điện.
Mở một terminal và chạy lệnh Docker sau:
```bash
docker run -it --rm --net=host --user=$(id -u):$(id -g) microros/micro-ros-agent:humble udp4 --port 8888
```
*(Giữ terminal này chạy ngầm trong suốt quá trình thử nghiệm)*

### Bước 2: Chuẩn bị Robot (Teach Pendant)
1. Bật nguồn tủ điện YRC1000.
2. Chuyển chìa khóa sang chế độ **REMOTE**.
3. Khởi động ứng dụng/job **MotoROS2** trên Teach Pendant.
4. *(Tùy chọn nhưng khuyến nghị)*: Hạ tốc độ Play Speed xuống mức thấp.

### Bước 3: Khởi chạy toàn bộ Pipeline + GUI
Mở terminal mới (đã source workspace) và chạy lệnh launch được thiết kế riêng cho robot thật:
```bash
cd ~/cocarry_ws
source install/setup.bash
ros2 launch hrc_bringup cocarry_real_gui.launch.py
```
Lệnh này sẽ khởi động:
- MoveIt & RViz (hiển thị trạng thái thực của robot)
- Camera tracking + AI Predictor + Transform Node
- Cartesian Streamer (kết nối trực tiếp `/yaskawa/queue_traj_point`)
- GUI Dashboard điều khiển
- Experiment Logger (ghi file CSV)

---

## 🛠 Cách Thao tác Trong Lúc Chạy (Trên GUI)

Quy trình thao tác hoàn toàn tương tự như khi mô phỏng, nhưng áp dụng thẳng lên robot vật lý:

1. Đứng vào vị trí chuẩn bị trước Camera, giữ tay ở tư thế tự nhiên.
2. Trên GUI, bấm **`⌖ Calibrate Camera`** (Thiết lập gốc tọa độ của người).
3. Trên GUI, bấm **`📌 Capture Init Pose`** (Chốt vị trí End-Effector hiện tại của robot thật làm mốc tương đối).
4. Chọn chế độ quỹ đạo: **`📍 Ground Truth`** hoặc **`🧠 Prediction`**.
5. Bấm **`⚡ Enable Robot`**. 
   - Hệ thống sẽ tự động gửi lệnh Reset Error → Servo ON → Start Point Queue Mode.
   - Bạn sẽ nghe thấy tiếng "Tạch" (Servo bật) từ robot.
   - Lúc này robot đang gửi Hold-Points để giữ nguyên vị trí hiện tại.
6. Khi đã sẵn sàng, bấm **`▶ Start Run`**. 
   - Dữ liệu tọa độ bắt đầu stream xuống robot. Robot sẽ bám theo chuyển động tay của bạn.
   - Dữ liệu thử nghiệm (Time, Error, Jerk...) đang được ghi lại vào CSV.
7. Khi cần dừng stream (hoặc có nguy hiểm): bấm **`⏸ Stop Run`**. Robot sẽ dừng lại tại chỗ (ngừng nhận tọa độ mới).
8. Khi thử nghiệm xong: bấm **`⛔ Disable Robot`** để tắt Point Queue Mode an toàn.

---

## 🛑 Xử lý Sự cố & An toàn

- **E-Stop**: Bất cứ khi nào robot có dấu hiệu đi quá giới hạn hoặc quá nhanh, **NHẤN E-STOP NGAY LẬP TỨC**.
- **Soft Stop**: Trên GUI có nút `🛑 Soft Stop` (gửi lệnh `/yaskawa/stop_traj_mode`). Dùng nút này để robot giảm tốc và dừng lại một cách mượt mà hơn E-Stop khi không quá khẩn cấp.
- **Go Home**: 
  - Nếu muốn đưa robot về lại tư thế chuẩn bị (Home), hãy đảm bảo không có vật cản xung quanh.
  - Bấm nút **`🏠 Go Home`** trên GUI (chỉ thực hiện được khi đã Disable Robot).
  - Hoặc chạy lệnh thủ công: `python3 src/hc10dtp_bringup/scripts/go_home.py`
- **Mất kết nối Micro-ROS**: Nếu terminal chạy Docker báo lỗi hoặc dừng cập nhật, robot sẽ tự động ngắt kết nối an toàn. Khởi động lại Docker Agent và chạy lại Launch file.
