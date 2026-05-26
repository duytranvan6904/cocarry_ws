# Human-Robot Co-Carrying Workspace (HC10DTP)

## Tổng quan (Overview)
Dự án này là một hệ thống **Human-Robot Collaborative (HRC) Co-Carrying** sử dụng cánh tay robot cộng tác Yaskawa HC10DTP. Hệ thống cho phép người và robot cùng khiêng một vật thể. Dựa vào dữ liệu hình ảnh 3D từ camera chiều sâu, hệ thống theo dõi chuyển động tay của người, đưa qua mạng nơ-ron hồi quy (GRU/LSTM) để dự đoán quỹ đạo (trajectory prediction) trong tương lai gần (multi-step prediction `Ts=3`), tự động bù trễ hệ thống, và liên tục nội suy tọa độ để điều khiển robot bám sát quỹ đạo phối hợp mượt mà ở tần số cao.

## Yêu cầu Hệ thống (System Requirements)

### Phần cứng (Hardware)
1. **Robot:** Yaskawa HC10DTP Collaborative Robot.
2. **Controller:** YRC1000micro Controller, đã kích hoạt và cài đặt **MotoROS2**.
3. **Camera:** Camera Depth RGB-D (Hỗ trợ Kinect V2, Intel RealSense D-series).
4. **Máy tính:** PC/Laptop chạy Linux (Khuyến nghị có GPU rời để xử lý AI real-time mượt mà, nhưng hệ thống vẫn tương thích hoàn toàn khi chạy bằng CPU do kiến trúc GRU 1-layer đã được tối ưu).

### Phần mềm & Thư viện (Software & Libraries)
1. **Hệ điều hành:** Ubuntu 22.04 LTS
2. **Middle-ware:** ROS 2 Humble Hawksbill
3. **Ngôn ngữ:** Python 3.10+
4. **Thư viện Python Core:**
   - `numpy`, `scipy`, `pyyaml` (Toán học, Lọc nhiễu & Config)
   - `tensorflow`, `keras`, `scikit-learn` (AI Model Inference & Data Scaling)
   - `mediapipe` / `pyrealsense2` (Computer Vision & Hand Tracking)
   - `PyQt5`, `pyqtgraph` (Giao diện UI Dashboard Real-time)
5. **ROS 2 Packages:** `ros-humble-moveit`, `ros-humble-tf2-tools`
6. **Drivers:** Thư viện `motoros2_interfaces` (Dành cho Yaskawa MotoROS2).

---

## Cấu trúc Packages trong Workspace

| Tên Package | Vai trò & Chức năng |
|---|---|
| `realsense_tracker` | Đọc dữ liệu từ Camera, sử dụng MediaPipe trích xuất tọa độ 3D của cổ tay người (Wrist Landmark) ở tần số 16Hz-30Hz. |
| `trajectory_predictor` | Node AI chứa logic dự đoán và tải mô hình Machine Learning (`gru_model_Ts3.h5`). Lấy chuỗi lịch sử XYZ và vận tốc để suy luận (Inference) ra vị trí tay N bước trong tương lai theo thời gian thực. |
| `coord_transform` | Chuyển đổi tọa độ không gian: Mapping từ hệ trục Camera (Camera Frame) sang hệ trục gốc của Robot (Base Link Frame) bao gồm lật trục tọa độ theo hướng người đứng. |
| `hc10dtp_bringup` | Chứa script điều khiển trung tâm `cartesian_streamer_hc10dtp.py`. Nhận tọa độ Cartesian, liên tục giải Inverse Kinematics (IK), và stream Joint Angles xuống bộ điều khiển MotoROS2 (qua `QueueTrajPoint`) với tần số **25Hz**. |
| `hc10dtp_moveit_config` | Cấu hình MoveIt 2 (SRDF, URDF, TRAC-IK) dùng cho giả lập, collision checking và giải động học nghịch. |
| `hc10dtp_simulation` | Môi trường giả lập tích hợp Gazebo/ROS Control. Bao gồm script `motoros2_mock_node.py` để giả lập các tín hiệu Service của MotoROS2 driver cho phép code streamer chạy mô phỏng 100% y như robot thật. |
| `experiment_logger` | Lưu tọa độ thực tế của người, tọa độ dự đoán của AI, và dữ liệu khớp robot ra file `.csv`. Cung cấp báo cáo phân tích độ chính xác (MAE, MSE), tính toán thời gian phản hồi và độ giật (Jerk) sau mỗi lần thử. |
| `predictor_ui` | Giao diện Dashboard (PyQtGraph) giám sát quỹ đạo đa trục X-Y-Z real-time. Cung cấp các nút điều khiển luồng thử nghiệm một cách an toàn và trực quan. |
| `hrc_bringup` | Chứa các file `launch` chính liên kết tất cả các node của hệ thống với nhau (`cocarry_full.launch.py`, `cocarry_sim_gui.launch.py`). |
| `GRU-Model` | Thư mục Jupyter Notebook chứa source code quá trình Offline Training, đánh giá Ablation Studies và lưu trữ các file mô hình (`.h5`) cùng scaler (`.pkl`). |

---

## Hướng dẫn Cài đặt (Installation)

1. **Cài đặt ROS 2 Dependencies và Python libs:**
```bash
sudo apt update
sudo apt install ros-humble-moveit ros-humble-tf2-tools
pip3 install numpy scipy mediapipe tensorflow scikit-learn pyqtgraph PyQt5 pyyaml
```
*(Lưu ý: Cài đặt thêm `pyrealsense2` nếu sử dụng camera Intel RealSense).*

2. **Build Workspace:**
```bash
cd ~/cocarry_ws
colcon build --symlink-install
source install/setup.bash
```

---

## Quy trình Thực thi (Execution Workflow)

### Bước 0: Calibrate Camera - Robot (Bắt buộc trước khi thao tác lần đầu)

Hệ thống cần biết Camera đang được đặt ở đâu và góc quay ra sao so với Robot để scale/transform quỹ đạo cho chính xác.
1. Đo tọa độ của ít nhất 3 điểm chuẩn trên sàn thực tế (trong không gian Camera và không gian Base Robot).
2. Nhập các thông số đo được vào biến `POINTS_CAM` và `POINTS_ROBOT` trong script `calibrate_camera_to_robot.py`.
3. Chạy lệnh sinh file Config:
```bash
cd ~/cocarry_ws/src/coord_transform/scripts
python3 calibrate_camera_to_robot.py \
  --output ../config/transform_params.yaml \
  --update ../config/transform_params.yaml
```

---

### Tùy chọn A: Chạy Mô Phỏng (Simulation) - Đề xuất cho Dev/Test

Mô phỏng sử dụng Camera thật (RealSense/Kinect) để thu nhận cử động người nhưng điều khiển Robot trên môi trường ảo (RViz/Gazebo). Hệ thống ảo hóa hoàn toàn MotoROS2 driver.

1. **Khởi chạy Hệ thống Simulation:**
Mở Terminal 1:
```bash
source ~/cocarry_ws/install/setup.bash
ros2 launch hrc_bringup cocarry_sim_gui.launch.py
```
*(Lệnh này tự động gom: MoveIt, fake hardware, MotoROS2 mock, Camera tracking, Predictor, Transform và Dashboard UI).*

2. **Thao tác trên UI Dashboard:**
   - Đứng trước Camera ở tư thế tự nhiên.
   - Bấm **"⌖ Calibrate Camera"** (Thiết lập gốc tọa độ người).
   - Bấm **"📌 Capture Init Pose"** (Chốt vị trí EE hiện tại làm mốc tương đối).
   - Chọn chế độ: **"📍 Ground Truth"** (Trực tiếp) hoặc **"🧠 Prediction"** (AI Dự đoán).
   - Bấm **"⚡ Enable Robot"** (Bật Point Queue Mode giả lập).
   - Bấm **"▶ Start Run"** (Bắt đầu stream và ghi log CSV). Di chuyển tay, robot ảo sẽ bám theo.
   - Kết thúc: Bấm **"⏸ Stop Run"** -> **"⛔ Disable Robot"** -> **"🏠 Go Home"**.

---

### Tùy chọn B: Chạy Thực Tế (Real HC10DTP Cobot)

**⚠️ QUY TẮC AN TOÀN:** Luôn giữ tay ở nút **Emergency Stop**. Tốc độ robot trên Teach Pendant không quá **10-15%** cho lần test đầu. Đảm bảo robot ở chế độ **REMOTE**.

1. **Terminal 0: Micro-ROS Agent (Nếu có cảm biến/gripper):**
```bash
cd ~/cocarry_ws && ./start_microros.sh
```

2. **Terminal 1: Khởi động MoveIt & Connect Robot:**
```bash
export ROS_DOMAIN_ID=10
source ~/cocarry_ws/install/setup.bash
ros2 launch hc10dtp_moveit_config hc10dtp_start.launch.py
```

3. **Terminal 2: Khởi động Co-Carry Pipeline & UI:**
```bash
export ROS_DOMAIN_ID=10
source ~/cocarry_ws/install/setup.bash
ros2 launch hrc_bringup cocarry_full.launch.py
```

4. **Các bài thử nghiệm khuyến nghị:**
   - **Test 1 (Go Home):** Chạy `python3 src/hc10dtp_bringup/scripts/go_home.py` để kiểm tra kết nối.
   - **Test 2 (Demo Pattern):** Chạy `python3 src/hc10dtp_bringup/scripts/cartesian_streamer_hc10dtp.py --demo line` để kiểm tra độ mượt.
   - **Test 3 (HRC Full):** Thao tác trên UI: **Calibrate** -> **Capture Init Pose** -> **Enable Robot** -> **Start Run**.

5. **Dừng an toàn:** Bấm nút **"🏠 Go Home"** trên UI hoặc Terminal 2 để robot về vị trí nghỉ và thoát Queue Mode sạch sẽ.

---

### Tùy chọn C: Điều khiển qua CLI (Headless/No-GUI Mode)

Nếu giao diện UI Dashboard gặp lỗi đồ họa (ví dụ: lỗi thư viện X11/XCB trong môi trường ảo hóa Docker/SSH), bạn hoàn toàn có thể điều khiển toàn bộ quy trình thực nghiệm (Calibrate, Capture Init Pose, Mode Switch, Enable, Run) trực tiếp bằng dòng lệnh ROS 2 CLI:

1. **Khởi chạy Hệ thống Simulation (Không có UI):**
```bash
ros2 launch hrc_bringup cocarry_sim_gui.launch.py
```
*(Nếu UI bị crash, các node xử lý nền như predictor, transform, cartesian_streamer, và realsense_tracker vẫn tiếp tục hoạt động bình thường).*

2. **Bước 1: Thiết lập gốc tọa độ người (Calibrate Camera):**
```bash
ros2 service call /coord_transform/calibrate std_srvs/srv/Trigger "{}"
```

3. **Bước 2: Chốt vị trí ban đầu của robot (Capture Init Pose):**
```bash
ros2 service call /coord_transform/capture_init_pose std_srvs/srv/Trigger "{}"
```

4. **Bước 3: Chọn chế độ quỹ đạo (Mode Switch):**
- Chế độ dự đoán AI (Prediction Mode):
  ```bash
  ros2 topic pub /trajectory_mode std_msgs/msg/String "{data: 'prediction'}" --once
  ```
  *(Khi chuyển sang chế độ này, bộ dự đoán `trajectory_predictor` sẽ tự động kích hoạt model GRU và bắt đầu xuất kết quả dự đoán).*
- Chế độ trực tiếp (Ground Truth Mode):
  ```bash
  ros2 topic pub /trajectory_mode std_msgs/msg/String "{data: 'ground_truth'}" --once
  ```

5. **Bước 4: Kích hoạt điều khiển robot (Enable Streamer):**
```bash
ros2 service call /cartesian_streamer/enable std_srvs/srv/SetBool "{data: true}"
```

6. **Bước 5: Bắt đầu truyền dữ liệu và ghi log (Start Run):**
```bash
ros2 topic pub /run_status std_msgs/msg/Bool "{data: true}" --once
ros2 service call /logger/toggle std_srvs/srv/SetBool "{data: true}"
```

7. **Bước 6: Dừng chương trình an toàn (Stop Run & Disable):**
- Dừng truyền dữ liệu và tắt logger:
  ```bash
  ros2 topic pub /run_status std_msgs/msg/Bool "{data: false}" --once
  ros2 service call /logger/toggle std_srvs/srv/SetBool "{data: false}"
  ```
- Tắt điều khiển streamer:
  ```bash
  ros2 service call /cartesian_streamer/enable std_srvs/srv/SetBool "{data: false}"
  ```
- Đưa robot về vị trí Home:
  ```bash
  python3 src/hc10dtp_bringup/scripts/go_home.py
  ```

---

## Kiến trúc Luồng Dữ Liệu (Data Pipeline)

Hệ thống được thiết kế để bù đắp các độ trễ từ Mạng nội bộ, Camera, và Quá trình giải IK, giúp robot bắt kịp với người ở thời gian thực `(Total system latency ≈ 165ms)`.

1. Camera thu thập tọa độ thô `XYZ` của tay người `(~16Hz)`.
2. Tọa độ `/hand_position` được đẩy vào buffer cửa sổ trượt của node `trajectory_predictor`.
3. Node suy luận (TensorFlow Backend) sử dụng mô hình `gru_model_Ts3.h5` và bộ Scaler đã được train với Vector Vận Tốc, đưa ra dự đoán trước `Ts=3` frame (tương đương `+187.5ms` trong tương lai).
4. Node `coord_transform` nội suy vị trí điểm bù trừ End-Effector, áp dụng bộ lọc Tín Hiệu (EMA) loại bỏ nhiễu rung (Jitter).
5. Output được phát sóng lên `/cartesian_streamer/target_pose` tới script `cartesian_streamer_hc10dtp.py`.
6. Streamer kích hoạt MoveIt giải ngược Inverse Kinematics liên tục, gài các bộ Constraint vận tốc/vị trí khớp để đảm bảo Safety ISO Limits.
7. Gửi danh sách góc khớp thành công dưới dạng `QueueTrajPoint` xuống bộ điều khiển Yaskawa với khoảng ngắt thời gian là `0.04s` (**Tần số 25Hz**) để làm mượt hoàn toàn các bước giật của chuyển động khung hình chuẩn.

---

## Đo lường & Phân tích Độ trễ Hệ thống (System Latency Measurement & Analysis)

Để tối ưu hóa độ trễ phản hồi của robot mà không gây thêm bất kỳ overhead nào trong quá trình vận hành thời gian thực (real-time), hệ thống sử dụng cơ chế **đệm ghi nhớ (in-memory buffer)** và công cụ **phân tích offline tương quan chéo (cross-correlation analysis)**.

### 1. Cơ chế Logging Không Trễ (Zero-Overhead Logging)
* Thay vì ghi file CSV trực tiếp từng frame xuống đĩa gây ra micro-stutters/jitter, dữ liệu thực nghiệm được lưu tạm trên RAM (`self._log_buffer`).
* Khi dừng thực nghiệm (gọi service stop hoặc nhận lệnh dừng từ Windows), toàn bộ đệm dữ liệu được xuất hàng loạt xuống đĩa (`experiment_*.csv`) và tự động tính toán các chỉ số cơ bản (MAE, MSE, Jerk).

### 2. Quy trình Đo & Phân tích Độ trễ (Offline Analysis Workflow)

#### Bước 1: Thu thập dữ liệu thực nghiệm
1. Chạy đầy đủ pipeline thực tế hoặc giả lập (Tùy chọn A hoặc B).
2. Kích hoạt ghi log thông qua UI Dashboard hoặc gọi service:
   ```bash
   ros2 service call /logger/toggle std_srvs/srv/SetBool "{data: true}"
   ```
3. Đứng trước camera thực hiện chuyển động tay **lặp đi lặp lại nhịp nhàng (sinusoidal motion)** hoặc **di chuyển đột ngột (step input)** trên một trục (ví dụ trục Y hoặc Z) trong khoảng 15-30 giây.
4. Dừng ghi log để kết xuất dữ liệu ra đĩa:
   ```bash
   ros2 service call /logger/toggle std_srvs/srv/SetBool "{data: false}"
   ```

#### Bước 2: Chạy phân tích offline
Chạy công cụ phân tích tương quan chéo trên file log vừa tạo để tìm độ lệch thời gian chính xác:
```bash
# Tự động quét và phân tích file log mới nhất trong thư mục ~/hrc_logs hoặc ~/cocarry_logs
ros2 run experiment_logger analyze_latency

# Hoặc chỉ định chính xác file log cần phân tích
ros2 run experiment_logger analyze_latency --csv /home/duy/cocarry_ws/cocarry_logs/experiment_GROUND_TRUTH_20260525_121439.csv
```

#### Kết quả phân tích (Ví dụ):
```text
============================================================
     LATENCY MEASUREMENT — Onset Detection Method
============================================================
Total samples: 2168 | Duration: 21.7s | Rate: 100 Hz
Movement bursts detected: 9
Thresholds — Hand: 355.9 mm/s | Robot: 142.3 mm/s | Pred: 355.9 mm/s
------------------------------------------------------------
Burst | Hand onset | Robot onset | H→R Delay | H→P Delay | P→R Delay
------------------------------------------------------------
  #  1 |      0.48s |       2.45s |   1970 ms |   -410 ms |   2380 ms
  #  2 |      1.53s |       2.45s |    920 ms |      0 ms |    920 ms
  #  3 |      3.82s |       3.82s |      0 ms |   -390 ms |    390 ms
...
============================================================

── SUMMARY STATISTICS ──

  1. Hand → Robot (Total End-to-End Delay) (9 samples):
    Mean:        467 ms
    Median:       50 ms
...
```
*(Nếu chạy có truyền tham số `--plot`, script sẽ tự động tạo biểu đồ phân tích phân rã các đợt chuyển động và lưu vào thư mục chứa log).*

### 3. Giải thích ý nghĩa các thông số kết quả (Onset Detection)
Thay vì sử dụng phương pháp tương quan chéo (Cross-Correlation) vốn dễ bị nhiễu bởi các khoảng thời gian đứng yên, công cụ đo lường đã nâng cấp sang phương pháp **Onset Detection** đáng tin cậy hơn. Thuật toán tự động cô lập các "đợt chuyển động" (Burst) rõ ràng của tay người, sau đó đo thời điểm bắt đầu chuyển động (Onset) của mô hình dự đoán và của cánh tay robot tương ứng trong từng đợt.

* **Total samples / Duration:** Tổng số lượng điểm dữ liệu và thời lượng của toàn bộ file log (tính bằng giây).
* **Movement bursts detected:** Số lần hệ thống phát hiện ra tay người bắt đầu di chuyển (tăng tốc đột ngột). Mỗi đợt này cung cấp 1 mẫu đo lường độ trễ độc lập.
* **Thresholds:** Ngưỡng vận tốc (mm/s) để thuật toán xác định là "bắt đầu chuyển động". (Ngưỡng của robot thường thấp hơn do robot di chuyển mượt và chậm hơn tay người).
* **Bảng chi tiết từng đợt (Per-burst):**
  * `Hand onset` / `Robot onset`: Dấu mốc thời gian (s) khi tay/robot vượt ngưỡng vận tốc.
  * `H→R`, `H→P`, `P→R Delay`: Các độ trễ tương ứng đo được trong đợt chuyển động đó.
* **SUMMARY STATISTICS (Thống kê tổng hợp):** Cung cấp bức tranh toàn cảnh (Mean, Median, Std) từ tất cả các đợt chuyển động. *(Lưu ý: Mức trung vị **Median** thường là thước đo chính xác nhất về trải nghiệm thực tế do nó tự động loại bỏ các điểm nhiễu bất thường)*.
  * **1. Hand → Robot (Total End-to-End Delay):** Độ trễ tổng hợp từ lúc tay bạn chuyển động đến khi cánh tay cơ khí thực sự nhúc nhích theo (bao gồm tất cả trễ camera, mạng, AI, và quán tính cơ khí).
  * **2. Hand → Predictor (Model Phase Shift):** Khoảng thời gian mô hình AI đi trước (mang dấu âm, ví dụ `-400ms`) hoặc đi sau (dương) chuyển động của người. Giá trị âm càng sâu chứng tỏ AI đang làm rất tốt việc phóng pha bù trễ về tương lai.
  * **3. Predictor → Robot (Tracking Delay):** Độ trễ cố hữu từ lúc Controller nhận tọa độ đích đến lúc robot vật lý lấy đà và bám theo (do giới hạn an toàn động cơ và hàm làm mượt). Mạng AI lý tưởng cần tạo ra pha âm ở bước 2 để triệt tiêu hoàn toàn độ trễ bước 3 này.

---

## Các Tuning Parameters Đáng Lưu Ý
Khi thực nghiệm trong môi trường mới, nếu robot phản hồi quá chậm hoặc hơi giật, hãy tinh chỉnh các chỉ số sau trong source code:

* **Trong `hc10dtp_bringup/scripts/cartesian_streamer_hc10dtp.py`:**
  * `DEFAULT_STREAM_HZ = 25` và `QUEUE_DT_SEC = 0.04`: Đây là tần suất giao tiếp 25Hz, phù hợp với giới hạn băng thông dịch vụ (Service Call) thực tế của robot.
  * `SMOOTH_ALPHA = 0.5`: Hệ số làm mượt (Lọc hàm mũ). Điều chỉnh từ `0.1` (rất êm nhưng bám chậm) đến `1.0` (bám gắt nhưng dễ giật cục).
  * `MAX_JOINT_DELTA_PER_AXIS`: Góc quay tối đa cho phép mỗi chu kì (Chống lật khớp khuỷu/cổ tay).
* **Trong `hrc_bringup/config/transform_params.yaml`:**
  * `prediction_step`: Số frame ngoại suy thêm (fallback nếu ML model delay).
  * `workspace_limits`: Giới hạn lồng giam không gian 3D ngăn robot đập vào tường.
* **Đổi Model AI Mới:** 
  * Cập nhật lại các tham số Default Param trong `trajectory_predictor/predictor_node.py` để trỏ vào đúng bộ `weights (.h5)` và `scalers (.pkl)` mới của bạn trong file config tương ứng.

---

## Giám sát & Chẩn đoán hệ thống (Diagnostics)

Trong quá trình robot chạy (Streaming), script `cartesian_streamer_hc10dtp.py` sẽ in log định kỳ mỗi 5 giây về tình trạng thực tế của luồng dữ liệu. Người vận hành cần chú ý các thông số sau để đảm bảo an toàn:

### Ý nghĩa các thông số log:
*   **`tick_hz` (~50Hz):** Tần suất vòng lặp điều khiển. Nếu < 45Hz, cần kiểm tra tải CPU.
*   **`queue_send_hz` & `ack_hz`:** Tốc độ gửi và nhận phản hồi từ robot. Lý tưởng nhất là 48-50Hz.
*   **`inter_ack_ms` (~20ms):** Độ trễ phản hồi. Nếu > 50ms, kết nối mạng LAN có vấn đề hoặc bị nhiễu.
*   **`busy_hz` (Nên là 0):** Nếu > 0, robot đang bị "nghẽn" hàng đợi (Queue Full). Hệ thống sẽ tự động retry nhưng chuyển động có thể bị khựng.
*   **`retry_count` / `reject_count`:** Số lần gửi lại hoặc số điểm bị từ chối do lỗi IK/Giới hạn an toàn. Nếu các số này tăng nhanh, cần kiểm tra lại vùng làm việc (Workspace) hoặc vật cản.
*   **`max_joint_delta`:** Độ thay đổi khớp lớn nhất mỗi tick. Robot sẽ tự động CLAMP (kìm hãm) nếu giá trị này vượt ngưỡng cấu hình để tránh rung lắc mạnh.

### Cách kiểm tra nhanh:
Nếu robot di chuyển không mượt, hãy kiểm tra log:
1. Nếu `ack_hz` thấp nhưng `tick_hz` cao -> Lỗi mạng hoặc controller quá tải.
2. Nếu `reject_count` tăng -> Tọa độ mục tiêu nằm ngoài tầm với hoặc gây lật khớp (Singularity).
3. Nếu `hold_count` tăng cao -> AI Predictor node đang bị chậm, không cung cấp kịp tọa độ.

---
*Developed & Optimized for Human-Robot Collaboration Research.*
