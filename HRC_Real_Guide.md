# 📘 Hướng dẫn Vận hành & Kiểm thử Robot HC10DTP Thực Tế (HRC Co-carry)

Tài liệu này hướng dẫn chi tiết quy trình kiểm thử và vận hành hệ thống Human-Robot Co-carrying trên tay máy Yaskawa HC10DTP thực tế. Chúng ta sẽ đi qua 3 bài test từ cơ bản đến nâng cao để đảm bảo an toàn tuyệt đối.

**⚠️ QUY TẮC AN TOÀN TỐI THƯỢNG:**
- Luôn giữ tay ở nút E-Stop (Dừng khẩn cấp) trên Teach Pendant.
- Tốc độ robot trên Teach Pendant không được vượt quá **10-15%** trong các bài test đầu tiên.
- Đảm bảo khu vực xung quanh robot không có chướng ngại vật trước khi bắt đầu.
- Tất cả terminal kết nối với robot phải được set `export ROS_DOMAIN_ID=10`.
- **Mới:** Hệ thống đã tích hợp giới hạn tốc độ (0.15m/s) và gia tốc an toàn tự động.

---

## 🛠️ Chuẩn bị chung (Áp dụng cho mọi bài test)

Chạy docker microros-agent trước khi mở các terminal khác bằng script tự động restart để tránh crash:
Mở **Terminal 0**:
```bash
cd ~/cocarry_ws
./start_microros.sh
```

Mở **Terminal 1** và khởi động MoveIt Stack cùng RViz để theo dõi trạng thái robot:
```bash
export ROS_DOMAIN_ID=10
cd ~/cocarry_ws
source install/setup.bash
ros2 launch hc10dtp_moveit_config hc10dtp_start.launch.py
```
> **Output mong muốn:** Cửa sổ RViz mở ra, hiển thị mô hình tay máy HC10DTP, sa bàn (safety cage) và cái bàn làm việc. Vị trí khớp trên RViz phải giống hệt vị trí thực tế của robot.

---

## 🧪 Test 1: Kiểm tra tính năng "Go Home" (Trở về vị trí chuẩn bị)

Tính năng này giúp robot tự động di chuyển mượt mà về vị trí Home (vị trí đã được hiệu chỉnh để vươn thẳng theo trục +Y ra giữa bàn làm việc).

**Cách chạy:**
Mở **Terminal 2**:
```bash
export ROS_DOMAIN_ID=10
cd ~/cocarry_ws
source install/setup.bash
python3 src/hc10dtp_bringup/scripts/go_home.py
```

**Quy trình & Output mong muốn:**
1. Terminal in ra: `✓ Kích hoạt StartPointQueueMode thành công. Servo ON!`
2. Robot di chuyển chậm (2.5 giây) về vị trí Home.
3. Khi đến nơi, terminal in ra: `✓ stop_traj_mode thành công. Tủ điện sạch sẽ.` và `✓ Đã về Home an toàn!`.
4. **Lưu ý:** Robot tự động thoát Queue Mode, bạn có thể chạy lại lệnh ngay mà không cần restart tủ điện.

---

## 🧪 Test 2: Kiểm tra Cartesian Streamer với Demo Pattern

Bài test này đánh giá khả năng giải Inverse Kinematics (IK) liên tục và đẩy quỹ đạo xuống robot với các giới hạn an toàn mới.

**Cách chạy:**
Mở **Terminal 2**:
```bash
export ROS_DOMAIN_ID=10
cd ~/cocarry_ws
source install/setup.bash
# Chạy mặc định (v=0.15m/s)
python3 src/hc10dtp_bringup/scripts/cartesian_streamer_hc10dtp.py --demo line

# HOẶC chạy cực chậm để kiểm tra an toàn (v=0.05m/s)
python3 src/hc10dtp_bringup/scripts/cartesian_streamer_hc10dtp.py --demo line --max-vel 0.05 --smooth-alpha 0.1
```

**Quy trình & Output mong muốn:**
1. Robot di chuyển tịnh tiến cực kỳ mượt mà nhờ bộ lọc gia tốc và vận tốc mới.
2. Terminal liên tục in ra toạ độ và trạng thái stream.
3. **Quan trọng:** Bấm `Ctrl+C` để dừng. Terminal sẽ báo: `✓ stop_traj_mode thành công. Controller sạch sẽ.`
4. **Kết quả:** Tủ điện không bị báo lỗi (Alarm), bạn có thể chạy tiếp bài test khác ngay lập tức.

---

## 🧪 Test 3: Vận hành toàn bộ hệ thống HRC (AI + Camera + Robot)

Tích hợp AI Predictor và Camera. Hệ thống sẽ bám theo tay người với tốc độ được kiểm soát an toàn.

**Cách chạy:**
Đảm bảo đã tắt hết các terminal cũ (chỉ giữ lại Terminal 1).
Mở **Terminal 2**:
```bash
export ROS_DOMAIN_ID=10
cd ~/cocarry_ws
colcon build --symlink-install --packages-select predictor_ui
source install/setup.bash
ros2 launch hrc_bringup cocarry_full.launch.py
```

**Quy trình thao tác trên Dashboard UI:**
1. **Calibrate & Capture:** Thực hiện như hướng dẫn cũ để đồng bộ tọa độ tay và robot.
2. **Enable & Start Run:** Bấm **[Enable Robot]** rồi **[▶ Start Run]**.
3. **Di chuyển:** Tay người di chuyển, robot sẽ bám theo. Nhờ giới hạn `max-vel` và `max-accel` mới, robot sẽ không còn bị giật cục kể cả khi tay người di chuyển nhanh hoặc đột ngột.
4. **Dừng an toàn:** Bấm nút **[🏠 Go Home]** trên UI. Nút này đã được fix để gọi script an toàn, đảm bảo tủ điện không bị Alarm sau khi thoát.

**Output mong muốn:**
- Robot bám tay mượt mà, không giật, không gây nguy hiểm.
- Khi dừng chương trình hoặc bấm Go Home, tủ điện YRC1000 trạng thái vẫn xanh (Normal), không cần khởi động lại.
