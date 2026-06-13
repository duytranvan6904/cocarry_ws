# Hướng dẫn thu thập dữ liệu (Data Collection Workflow)

Tài liệu này hướng dẫn các bước chi tiết để vận hành công cụ `data_collection_gui.py` mới được tạo ra nhằm thu thập dữ liệu quỹ đạo chuyển động tay.

---

## 1. Khởi động hệ thống

Bạn cần 3 cửa sổ terminal độc lập.

**Terminal 0: Micro-ROS Agent:**
```bash
cd ~/cocarry_ws && ./start_microros.sh
```

**Terminal 1 (Pipeline chính):**
Chạy pipeline chứa các node lấy dữ liệu từ RealSense và xử lý toạ độ.
```bash
export ROS_DOMAIN_ID=10
source ~/cocarry_ws/install/setup.bash
ros2 launch hrc_bringup cocarry_full.launch.py
```
> [!IMPORTANT]
> Chờ cho node camera báo ready và topic `/transformed_hand_pose` bắt đầu có data.

**Terminal 2 (Giao diện Data Collection):**  
Chạy riêng tool ghi hình, không cần attach vào launch file.
```bash
export ROS_DOMAIN_ID=10
source ~/cocarry_ws/install/setup.bash
python3 ~/cocarry_ws/src/data_collection_gui.py
```

---

## 2. Cấu trúc Giao diện

Khi chạy tool, sẽ có **2 cửa sổ** hiện lên:
1. **Control Panel (Cửa sổ nhỏ):** Dành cho người điều hành (nhập ID, setup thời gian, chọn kịch bản, ấn Start). Bạn có thể để cửa sổ này ở màn hình của bạn.
2. **Participant Display (Cửa sổ lớn màu đen):** Dành cho người tham gia. Bạn có thể kéo cửa sổ này sang màn hình phụ và ấn phím `F11` để bật Fullscreen. Nhấn `Esc` để thoát Fullscreen.

---

## 3. Các bước tiến hành trên GUI

1. **Nhập thông tin ban đầu:**
   - Tại ô **Participant ID**, nhập mã người tham gia (ví dụ: `p01`). Mọi file CSV lưu ra sẽ được gom vào chung folder.
   - Tại ô **Duration (s)**, xác nhận độ dài quỹ đạo. Mặc định là **8.0s**.
   - Tại ô **Y-Threshold (m)**, đặt giới hạn khoảng cách (trên trục Y) để kích hoạt sự kiện đổi Target. Mặc định là **0.6m**.
   - Tick vào ô **Random Mode** nếu muốn thứ tự 9 quỹ đạo được trộn ngẫu nhiên. Nếu bỏ tick, bạn có thể tự chọn quỹ đạo bằng ô **Manual Scenario**.

2. **Chạy Trial (Scenario):**
   - Người tham gia đặt tay ở vị trí màu xanh lá (vùng **START** trên màn hình phụ).
   - Giải thích cho người tham gia về mục tiêu:
     - Nếu đang ở `Mode: Free`: "Đưa tay thẳng từ Start đến đích hiển thị màu vàng và giữ nguyên tay ở đó."
     - Nếu đang ở `Mode: Change`: "Đưa tay về đích hiển thị màu vàng. Ngay khi vượt qua vạch cảnh báo (Trigger Y) và nghe tiếng máy tính phát ra tiếng **BÍP**, hãy lập tức chuyển hướng đưa tay tới đích màu vàng mới hiện lên."
   - Bấm nút **START TRIAL** ở bảng điều khiển.
   - Máy sẽ hiển thị dòng chữ nhấp nháy `🔴 RECORDING`, thanh đếm ngược bắt đầu. Dữ liệu tay được âm thầm lưu lại trên RAM với tốc độ cố định 16Hz.

3. **Kết thúc 1 Trial:**
   - Khi thanh đếm ngược chạy hết 8s. Giao diện sẽ phát 2 tiếng beep nhỏ.
   - Tệp CSV sẽ được lưu tự động ra ổ cứng ở `cocarry_logs/data_collection/pXX/`
   - Giao diện tự động chuyển Scenario kế tiếp, và nút **START TRIAL** sáng lại.

4. **Lặp lại:**
   - Cứ thế thực hiện cho tới khi `Progress` báo hoàn thành đủ số quỹ đạo cần thiết.

---

## 4. Các lưu ý quan trọng

> [!WARNING]
> Mọi file log tự động đều mang tên dạng `p01_SCC3_r01_20260527_103000.csv` với đầy đủ tham số tần số, mode, target bên trong phần header.

> [!TIP]
> Bạn có thể bấm **Reset Queue** nếu như đang thu mà phát hiện làm sai kịch bản hoặc muốn thu lại toàn bộ tập dataset ngẫu nhiên từ đầu.

> [!NOTE]
> Giao diện sẽ phát một tiếng Bíp khi tọa độ tay người vượt qua vạch đứt màu vàng trên màn hình Participant Display (tương đương với Y-Threshold đã cài). Đảm bảo loa đang bật để người tham gia nghe thấy.
