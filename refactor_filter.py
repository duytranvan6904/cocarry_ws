import re

with open('src/coord_transform/coord_transform/transform_node.py', 'r') as f:
    content = f.read()

# Add CameraFilterState class
class_def = """
class CameraFilterState:
    def __init__(self, median_size):
        from collections import deque
        self.last_raw_p_cam = None
        self.outlier_count = 0
        self.median_buffer_y = deque(maxlen=median_size)
        self.recent_buffer = deque(maxlen=15)
        self.smoothed_p_cam = None
        self.is_holding_position = False
        self.hold_p_cam = None
        self.stationary_counter = 0
        self.last_moving_p_cam = None

    def reset(self):
        self.last_raw_p_cam = None
        self.outlier_count = 0
        self.median_buffer_y.clear()
        self.recent_buffer.clear()
        self.smoothed_p_cam = None
        self.is_holding_position = False
        self.hold_p_cam = None
        self.stationary_counter = 0
        self.last_moving_p_cam = None

class CoordTransformNode(Node):
"""
content = content.replace("class CoordTransformNode(Node):", class_def)

# Replace state variables initialization
state_init_old = """        self._hold_p_cam = None
        self._smoothed_p_cam = None
        self._last_raw_p_cam = None
        self._outlier_count = 0
        # Kích thước median buffer được load từ YAML
        self._median_buffer_y = deque(maxlen=self._filter_median_size_y)
        self._moving_deadzone_tol = self._filter_deadband_depth_tol
        # Moving deadband: theo dõi vị trí hiện tại (không chỉ vị trí ban đầu)
        self._stationary_counter = 0
        self._stationary_threshold = self._filter_stationary_threshold
        self._last_moving_p_cam = None  # Vị trí cuối cùng khi đang di chuyển"""

state_init_new = """        self._moving_deadzone_tol = self._filter_deadband_depth_tol
        self._stationary_threshold = self._filter_stationary_threshold
        
        # Tạo 2 filter state riêng biệt cho ground_truth (UI vẽ) và prediction (robot chạy)
        self._actual_filter = CameraFilterState(self._filter_median_size_y)
        self._pred_filter = CameraFilterState(self._filter_median_size_y)"""

content = content.replace(state_init_old, state_init_new)

# Modify reset logic in _on_mode
reset_old = """            self._smoothed_p_cam = None
            self._median_buffer_y.clear()
            self._stationary_counter = 0
            self._last_moving_p_cam = None
            # QUAN TRỎNG: Không giữ hold state cũ khi đổi mode
            # (tránh prediction mode bị lock ở giá trị ground_truth cũ → ramp chậm)
            self._is_holding_position = False
            self._hold_p_cam = None"""

reset_new = """            self._actual_filter.reset()
            self._pred_filter.reset()"""

content = content.replace(reset_old, reset_new)

# Modify _on_hand_state and _on_prediction
cb_old = """    def _on_hand_state(self, msg: HandState):
        \"\"\"Xử lý HandState khi mode = ground_truth\"\"\"
        if self._mode != 'ground_truth':
            return
        if not msg.is_tracked:
            return
            
        p_cam = np.array([msg.x, msg.y, msg.z])
        self._last_p_cam = p_cam
        self._calib_buffer.append(p_cam)
        
        # Luôn chạy _process_and_publish để lọc dữ liệu và publish lên UI vẽ,
        # bất kể self._running hay self._p_cam_init có bằng None hay không
        self._process_and_publish(p_cam)

    def _on_prediction(self, msg: HandPrediction):
        \"\"\"Xử lý HandPrediction khi mode = prediction\"\"\"
        if self._mode != 'prediction':
            return

        # Lấy tọa độ theo prediction_step
        if hasattr(msg, 'pred_x') and len(msg.pred_x) > 0:
            step = min(self._pred_step, len(msg.pred_x) - 1)
            p_cam = np.array([msg.pred_x[step], msg.pred_y[step], msg.pred_z[step]])
        else:
            p_cam = np.array([msg.x, msg.y, msg.z])
            
        self._last_p_cam = p_cam
        self._calib_buffer.append(p_cam)
        
        # Luôn chạy _process_and_publish để lọc dữ liệu và publish lên UI vẽ,
        # bất kể self._running hay self._p_cam_init có bằng None hay không
        self._process_and_publish(p_cam)"""

cb_new = """    def _on_hand_state(self, msg: HandState):
        \"\"\"Xử lý HandState cho cả 2 mode để luôn cập nhật quỹ đạo thực tế (UI)\"\"\"
        if not msg.is_tracked:
            return
            
        p_cam = np.array([msg.x, msg.y, msg.z])
        self._last_p_cam = p_cam
        self._calib_buffer.append(p_cam)
        
        # Lọc quỹ đạo thực tế
        p_cam_filtered = self._apply_filter(p_cam, self._actual_filter)
        if p_cam_filtered is None:
            return
            
        # Luôn publish quỹ đạo thực tế đã lọc để UI vẽ (Actual)
        filtered_pt = PointStamped()
        filtered_pt.header.frame_id = 'camera_frame'
        filtered_pt.header.stamp = self.get_clock().now().to_msg()
        filtered_pt.point.x = float(p_cam_filtered[0])
        filtered_pt.point.y = float(p_cam_filtered[1])
        filtered_pt.point.z = float(p_cam_filtered[2])
        self._filtered_hand_pub.publish(filtered_pt)
        
        # Nếu đang ở ground_truth, dùng quỹ đạo này điều khiển robot
        if self._mode == 'ground_truth':
            self._transform_and_publish_target(p_cam_filtered)

    def _on_prediction(self, msg: HandPrediction):
        \"\"\"Xử lý HandPrediction khi mode = prediction\"\"\"
        if self._mode != 'prediction':
            return

        # Lấy tọa độ theo prediction_step
        if hasattr(msg, 'pred_x') and len(msg.pred_x) > 0:
            step = min(self._pred_step, len(msg.pred_x) - 1)
            p_cam = np.array([msg.pred_x[step], msg.pred_y[step], msg.pred_z[step]])
        else:
            p_cam = np.array([msg.x, msg.y, msg.z])
            
        # Lọc quỹ đạo dự đoán bằng state riêng
        p_cam_filtered = self._apply_filter(p_cam, self._pred_filter)
        if p_cam_filtered is None:
            return
            
        self._transform_and_publish_target(p_cam_filtered)"""

content = content.replace(cb_old, cb_new)

with open('src/coord_transform/coord_transform/transform_node.py', 'w') as f:
    f.write(content)

