# Hướng Dẫn Thử Nghiệm Mô Phỏng Co-Carrying (Camera Thật + Robot Ảo)

Tài liệu này hướng dẫn cách chạy hệ thống **Human-Robot Co-Carrying** một cách an toàn nhất: Dùng Camera RealSense thu nhận cử động thực tế của người, nhưng điều khiển Robot trên môi trường ảo (RViz/Gazebo) thay vì robot thật.

## 🌟 Tổng quan Kiến trúc Thử nghiệm

1. **RealSense Node**: Lấy ảnh từ camera thực, chạy AI MediaPipe tìm tọa độ tay người.
2. **Transform Node**: Đồng bộ tọa độ, bù trừ khoảng cách, tính toán tọa độ đích tương đối cho robot.
3. **Cartesian Streamer**: Nhận tọa độ đích, tính IK (động học ngược) để sinh quỹ đạo liên tục.
4. **MotoROS2 Mock & MoveIt (Simulation)**: Đóng giả phần cứng tủ điện YRC1000, nhận quỹ đạo và vẽ robot chuyển động trên RViz.

---

## 🚀 Các Bước Chạy Thử Nghiệm

Mở **4 Terminal** khác nhau. Ở mỗi Terminal, đảm bảo bạn đã source không gian làm việc:
```bash
cd ~/cocarry_ws
source install/setup.bash
```

### Terminal 1: Khởi động Môi trường Mô phỏng
Kích hoạt Robot Ảo và hệ thống giả lập MotoROS2:
```bash
ros2 launch hc10dtp_simulation sim_start.launch.py
```
*(Cửa sổ RViz sẽ mở ra hiển thị robot và lồng an toàn).*

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

Trình tự chuẩn để robot ảo đi theo tay bạn:

1. Đứng vào vị trí chuẩn bị trước Camera, giữ tay ở tư thế tự nhiên.
2. **Reset Gốc Camera**: Để đồng bộ gốc camera với vị trí tay hiện tại, mở Terminal thứ 5 và gõ:
   ```bash
   ros2 service call /realsense/calibrate_origin std_srvs/srv/Trigger
   ```
3. **Khởi tạo Gốc Robot**: Để ghi nhớ tư thế bắt đầu của robot ảo (làm mốc cho chuyển động tương đối):
   ```bash
   ros2 service call /coord_transform/capture_init_pose std_srvs/srv/Trigger
   ```
4. **Bắt đầu di chuyển**: 
   Khi bạn di chuyển tay lên/xuống, trái/phải, `transform_node` sẽ tính độ dời và gửi cho `cartesian_streamer`. Bạn sẽ thấy con robot trong RViz (Terminal 1) bám sát theo chuyển động tay của bạn ngoài đời thực!

---

## 🏠 Lệnh Đưa Robot Về Gốc (Go Home)

Sau khi thử nghiệm xong, tay bạn có thể ở vị trí bất kỳ khiến robot bị kẹt ở góc khó. Để đưa robot ảo trở về tư thế thẳng đứng nguyên bản (tất cả khớp = 0), hãy làm theo 2 bước:

**Bước 1:** Bấm `Ctrl+C` tại **Terminal 4** để tắt `cartesian_streamer.py` (giải phóng quyền điều khiển).

**Bước 2:** Chạy lệnh Go Home:
```bash
python3 src/hc10dtp_bringup/scripts/go_home.py
```
Robot trên RViz sẽ mượt mà xoay lại tư thế Home (0,0,0,0,0,0).
