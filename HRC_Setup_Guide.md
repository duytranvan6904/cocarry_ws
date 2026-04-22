# Hướng Dẫn Cài Đặt và Chuẩn Hóa Tọa Độ Co-Carrying (Relative Displacement)

Tài liệu này hướng dẫn cách bố trí camera, quy ước các trục tọa độ và các bước thực hiện calib để hệ thống tracking chuyển động tay người và đồng bộ với cánh tay robot HC10DTP.

---

## 1. Phương pháp Relative Displacement (Dịch chuyển tương đối)

Thay vì phải đo đạc chính xác khoảng cách 38cm giữa hai tay cầm của vật thể và gán tọa độ tuyệt đối, hệ thống đã được cập nhật để sử dụng phương pháp **Dịch chuyển tương đối**:
- **Nguyên lý:** Vật thể (hộp 30x20x10) là một vật rắn. Khi tay người di chuyển một đoạn `(dx, dy, dz)`, tay máy của robot cũng sẽ phải di chuyển chính xác một đoạn `(dx, dy, dz)` tương ứng.
- **Cách hoạt động:** Khi bắt đầu, robot đang cầm vật ở một vị trí bất kỳ (gọi là `P_init`). Cùng lúc đó, camera calib điểm gốc `(0,0,0)` tại vị trí tay phải của người. Bất cứ chuyển động nào của tay người sau đó sẽ được cộng trực tiếp vào `P_init` để điều khiển robot.

---

## 2. Bố trí Camera trong thực tế (Để R = Identity)

Trục tọa độ của Yaskawa HC10DTP tại `base_link` theo chuẩn ROS:
- **Trục X+:** Hướng thẳng ra phía trước robot.
- **Trục Y+:** Hướng sang bên trái của robot.
- **Trục Z+:** Hướng thẳng đứng lên trên.

Trong mã nguồn `realsense_node.py`, tọa độ trả về đã được quy ước lại thành `(x_ws, y_ws, z_ws)`:
- `x_ws`: Hướng sang phải của ảnh camera.
- `y_ws`: Hướng về phía camera (ngược chiều nhìn của camera).
- `z_ws`: Hướng thẳng đứng lên trên (ngược với chiều rơi của trọng lực).

> [!TIP]
> **Vị trí đặt Camera tối ưu nhất:**
> Đặt camera ở **BÊN TRÁI robot** (khi đứng từ phía sau robot nhìn tới), camera hướng ngang sang phải, vuông góc với trục X của robot.
>
> **Lý do:** Khi đặt như vậy, các trục của camera sẽ trùng khớp hoàn toàn với trục của robot:
> - Sang phải của camera (`x_ws`) ≡ Đi tới phía trước của robot (`Trục X`).
> - Hướng về phía camera (`y_ws`) ≡ Sang trái của robot (`Trục Y`).
> - Hướng lên trên (`z_ws`) ≡ Hướng lên trên của robot (`Trục Z`).
>
> Với cách đặt này, Rotation Quaternion `cam_to_base_q*` trong file config sẽ chỉ đơn giản là `[0, 0, 0, 1]` (Identity Matrix). Không cần phải tính toán xoay hệ tọa độ phức tạp!

---

## 3. Quy trình Calib Thực Tế (Mỗi lần chạy thử nghiệm)

Thực hiện theo các bước sau để đảm bảo an toàn và tọa độ đồng bộ chính xác:

### Bước 1: Khởi động hệ thống
1. Chạy MoveIt và ROS2 driver của HC10DTP.
2. Chạy node `cartesian_streamer_hc10dtp.py`.
3. Chạy `realsense_node.py` và `transform_node.py`.

### Bước 2: Setup vật lý
1. Di chuyển robot bằng tay (Teach Pendant) đến vị trí cầm bên trái của vật thể.
2. Người thí nghiệm cầm vào bên phải của vật thể (với tay phải tại vị trí tay cầm). Đứng cố định tại vị trí chuẩn bị.

### Bước 3: Capture Initial Pose & Calibrate
Khi cả người và robot đã giữ chặt vật thể ở tư thế chuẩn bị, mở một Terminal mới và chạy 2 lệnh sau (có thể gộp vào 1 file `bash` script cho nhanh):

```bash
# 1. Reset điểm gốc camera về vị trí tay phải hiện tại của người
ros2 service call /realsense/calibrate_origin std_srvs/srv/Trigger

# 2. Lưu vị trí hiện tại của tay máy robot làm điểm gốc (P_init)
ros2 service call /coord_transform/capture_init_pose std_srvs/srv/Trigger
```

> [!IMPORTANT]
> **Xác nhận kết quả:**
> Terminal chạy `transform_node` sẽ in ra dòng chữ: `Captured Init Pose! P_init=(x, y, z)...`
> Từ thời điểm này, bất kỳ di chuyển nào của tay người sẽ lập tức khiến robot di chuyển theo.

### Bước 4: Bắt đầu Co-Carrying
Bây giờ hệ thống Tracking đã sẵn sàng dự đoán. Khi bạn bước đi và dịch chuyển tay, vector dịch chuyển sẽ được truyền vào `transform_node` và robot sẽ đi theo.

---

## 4. Xử lý sự cố (Troubleshooting)

- **Robot đi ngược hướng:** Khả năng cao là camera đặt không đúng góc 90 độ, hoặc bạn đang đặt camera ở bên phải robot thay vì bên trái. Nếu đặt ở bên phải robot, trục X và Y sẽ bị ngược, bạn sẽ cần phải cấu hình lại `cam_to_base_q*` trong yaml file (xoay 180 độ quanh trục Z).
- **Robot không di chuyển khi đã calib:** Kiểm tra xem `cartesian_streamer` đã hiển thị dòng chữ `Sẵn sàng stream` chưa, và bạn đã trigger prediction model chưa.
- **Vật thể bị xoay:** Hệ thống hiện tại sử dụng chế độ "Cartesian Streaming" với orientation cố định. Trong lúc di chuyển, hãy cố gắng giữ vật thể song song với mặt đất. Gốc tay cầm của robot sẽ duy trì tư thế ngang ban đầu.
