# Human-Robot Collaboration (HRC) Workspace

## 1. Giới thiệu
Dự án HRC Workspace là một hệ thống ROS 2 tích hợp nhằm theo dõi và dự đoán quỹ đạo chuyển động của cánh tay người dùng (Skeleton Tracking), phục vụ cho nghiên cứu tương tác người - máy (Human-Robot Collaboration). Hệ thống sử dụng camera **Intel RealSense** kết hợp với mô hình **MediaPipe** để lấy tọa độ 3D theo thời gian thực, đồng thời áp dụng mô hình mạng nơ-ron (TensorFlow) để dự đoán quỹ đạo tiếp theo và được hiển thị chi tiết qua giao diện phân tích đồ thị.

## 2. Danh sách các Packages trong Project
Workspace này bao gồm các ROS 2 packages sau:
- **`hrc_bringup`**: Chứa các file cấu hình (`all_params.yaml`) và file khởi chạy (`full_pipeline.launch.py`) để chạy toàn bộ các thành phần của hệ thống cùng lúc.
- **`human_hand_msgs`**: Package chứa định nghĩa các custom messages và services (ví dụ: `HandState`, `HandPrediction`, `SystemStatus`).
- **`realsense_tracker`**: Node đọc dữ liệu thô (ảnh và chiều sâu) từ camera RealSense, sử dụng thư viện MediaPipe (Vision Tasks) để trích xuất và công bố tọa độ 3D của tay người.
- **`trajectory_predictor`**: Chạy inference model dự đoán (TensorFlow) trong một tiến trình tách biệt để không ảnh hưởng đến tần số vòng lặp ROS, đồng thời xử lý lọc nhiễu (như Savitzky-Golay).
- **`experiment_logger`**: Thực hiện nhiệm vụ tính toán sai số thời gian thực (MAE) và ghi log dữ liệu tay thô, dữ liệu dự đoán ra file CSV để phân tích sau thực nghiệm.
- **`predictor_ui`**: Cung cấp giao diện đồ họa (GUI) dựa trên PyQtGraph, cho phép kỹ sư/nhà nghiên cứu giám sát trạng thái kết nối, biểu đồ quỹ đạo 3 trục X, Y, Z và điều khiển hệ thống (Bắt đầu/Dừng dự đoán, ghi log).

## 3. Các yêu cầu (Dependencies) cần thiết
Để dự án hoạt động trơn tru, bạn cần cài đặt đầy đủ các thư viện và môi trường sau:

### 3.1. Hệ điều hành và Framework chính
- **OS**: Ubuntu 22.04 LTS
- **ROS 2**: Humble Hawksbill
- **Ngôn ngữ**: Python 3.10+

### 3.2. ROS 2 Dependencies
Đảm bảo đã cài đặt các gói ROS tiêu chuẩn:
```bash
sudo apt update
sudo apt install ros-humble-cv-bridge \
                 ros-humble-rosidl-default-generators \
                 ros-humble-sensor-msgs \
                 ros-humble-std-msgs \
                 ros-humble-std-srvs
```

### 3.3. Python Dependencies
Cài đặt các gói thư viện Python yêu cầu bằng `pip`:
```bash
pip install numpy \
            opencv-python \
            pyrealsense2 \
            mediapipe \
            pyqtgraph \
            PyQt5 \
            tensorflow \
            scipy \
            pyyaml
```

## 4. Hướng dẫn cài đặt và Build

**Bước 1: Di chuyển tới workspace**
```bash
cd ~/Experiment/hrc_ws
```

**Bước 2: Cài đặt phụ thuộc thông qua rosdep (Tùy chọn)**
```bash
rosdep update
rosdep install --from-paths src --ignore-src -r -y
```

**Bước 3: Build dự án**
```bash
colcon build --symlink-install
```

**Bước 4: Source môi trường**
Thêm lệnh source vào `~/.bashrc` hoặc chạy trực tiếp trong terminal hiện tại:
```bash
source install/setup.bash
```

## 5. Hướng dẫn chạy chương trình (Run)

Để khởi chạy toàn bộ pipeline (Tracker, Predictor, Logger, và UI) cùng một lúc, hãy sử dụng file launch được cung cấp sẵn:

```bash
ros2 launch hrc_bringup full_pipeline.launch.py
```

**Lưu ý:**
- Bạn có thể tùy chỉnh các cấu hình chung (topics, namespace, model path, v.v...) trực tiếp trong file: `src/hrc_bringup/config/all_params.yaml`.
- Đảm bảo camera **Intel RealSense** đã được kết nối với cổng USB 3.0 của máy tính trước khi khởi chạy để tránh lỗi timeout.
