with open('src/coord_transform/coord_transform/transform_node.py', 'r') as f:
    content = f.read()

# Refactor _process_and_publish into _apply_filter and _transform_and_publish_target
old_func = """    def _process_and_publish(self, p_cam: np.ndarray):
        \"\"\"Hàm dùng chung để clamp và tính pose đích\"\"\"

        if not np.all(np.isfinite(p_cam)):
            self.get_logger().warn(
                f'Tọa độ không hợp lệ: {p_cam}',
                throttle_duration_sec=1.0,
            )
            return

        # ─── Outlier Rejection (Loại bỏ đỉnh nhọn) ─────────
        if self._last_raw_p_cam is not None:
            deviation_from_last = np.linalg.norm(p_cam - self._last_raw_p_cam)
            if deviation_from_last > self._filter_outlier_threshold:
                self._outlier_count += 1
                if self._outlier_count < 5:
                    self.get_logger().warn(f'Outlier rejected #{self._outlier_count} (jumped {deviation_from_last*1000:.1f}mm). Ignoring.')
                    return
                else:
                    self.get_logger().info(f'Too many outliers ({self._outlier_count}). Resetting filter to new position.')
                    self._outlier_count = 0
            else:
                self._outlier_count = 0
        
        self._last_raw_p_cam = p_cam.copy()

        # ─── Median Pre-filter cho trục Y (depth, nhiễu nhất) ────
        self._median_buffer_y.append(p_cam[1])
        min_median = max(3, self._filter_median_size_y // 2 + 1)  # ít nhất 3 mẫu
        if len(self._median_buffer_y) >= min_median:
            p_cam = p_cam.copy()
            p_cam[1] = float(np.median(self._median_buffer_y))

        # ─── Dynamic Deadband Logic ─────────────────────────
        # Kết hợp 2 cơ chế:
        #   (A) Initial deadband: giữ yên quanh vị trí calibrate ban đầu (chỉ khi đã calib)
        #   (B) Moving deadband: giữ yên khi tay dừng tại BẤT KỲ vị trí nào
        self._recent_buffer.append(p_cam)
        
        should_hold = False
        hold_position = None

        if len(self._recent_buffer) >= 5:
            recent_data = np.array(self._recent_buffer)
            mean_pos = np.mean(recent_data, axis=0)

            # (A) Initial deadband: tay ở gần vị trí calibrate
            if self._p_cam_init is not None:
                deviation_from_init = np.linalg.norm(mean_pos - self._p_cam_init)
                if deviation_from_init < self._noise_tolerance:
                    should_hold = True
                    hold_position = self._p_cam_init.copy()
            
            if not should_hold:
                # (B) Moving deadband: tay đã di chuyển nhưng đang đứng yên
                # Đo độ phân tán gần đây (std) — nếu std nhỏ = tay đứng yên
                recent_std = np.std(recent_data, axis=0)
                # Chỉ cần trục Y (depth) ổn định là đủ để hold
                depth_std = recent_std[1]
                depth_range = np.max(recent_data[:, 1]) - np.min(recent_data[:, 1])
                
                if depth_range < self._moving_deadzone_tol:
                    self._stationary_counter += 1
                else:
                    self._stationary_counter = 0
                    self._last_moving_p_cam = p_cam.copy()

                if self._stationary_counter >= self._filter_stationary_threshold:
                    should_hold = True
                    # Giữ tại mean gần đây (ổn định hơn raw)
                    hold_position = mean_pos.copy()

        if should_hold:
            if not self._is_holding_position:
                self._is_holding_position = True
                self._hold_p_cam = hold_position
                self.get_logger().info(
                    f'Deadband: HOLD at ({hold_position[0]:.3f}, {hold_position[1]:.3f}, {hold_position[2]:.3f})',
                    throttle_duration_sec=2.0)
            # Cập nhật hold position liên tục (mean gần đây) để tránh drift
            if hold_position is not None:
                self._hold_p_cam = hold_position
        else:
            if self._is_holding_position:
                self.get_logger().info(
                    f'Deadband: RELEASE — motion detected',
                    throttle_duration_sec=2.0)
            self._is_holding_position = False
            self._stationary_counter = 0

        if self._is_holding_position and self._hold_p_cam is not None:
            # Khi hold: lock CẢ 3 TRỤC để tránh lắc lư ngang và depth
            target_p_cam = self._hold_p_cam.copy()
        else:
            target_p_cam = p_cam

        if self._smoothed_p_cam is None:
            self._smoothed_p_cam = target_p_cam.copy()
        else:
            # Asymmetric EMA Filter: smooth transition
            # Mỗi trục có alpha riêng dựa trên đặc tính nhiễu:
            #   X (left-right): nhiễu thấp → phản ứng nhanh
            #   Y (depth):      nhiễu rất cao → lọc mạnh
            #   Z (height):     nhiễu trung bình
            if self._is_holding_position:
                alpha_x = self._filter_ema_x_hold
                alpha_y = self._filter_ema_y_hold
                alpha_z = self._filter_ema_z_hold
            else:
                alpha_x = self._filter_ema_x_moving
                alpha_y = self._filter_ema_y_moving
                alpha_z = self._filter_ema_z_moving

            self._smoothed_p_cam[0] = alpha_x * target_p_cam[0] + (1.0 - alpha_x) * self._smoothed_p_cam[0]
            self._smoothed_p_cam[1] = alpha_y * target_p_cam[1] + (1.0 - alpha_y) * self._smoothed_p_cam[1]
            self._smoothed_p_cam[2] = alpha_z * target_p_cam[2] + (1.0 - alpha_z) * self._smoothed_p_cam[2]

        p_cam_to_use = self._smoothed_p_cam

        # ─── Publish tọa độ ĐÃ LỌC ra topic cho UI vẽ ───────────────────
        filtered_pt = PointStamped()
        filtered_pt.header.frame_id = 'camera_frame'
        filtered_pt.header.stamp = self.get_clock().now().to_msg()
        filtered_pt.point.x = float(p_cam_to_use[0])
        filtered_pt.point.y = float(p_cam_to_use[1])
        filtered_pt.point.z = float(p_cam_to_use[2])
        self._filtered_hand_pub.publish(filtered_pt)

        # Nếu chưa calibrate hoặc chưa bắt đầu chạy robot, dừng ở đây (không gửi target cho robot)
        if self._p_cam_init is None or not self._running:
            self.get_logger().debug(
                f'Skip robot target: p_cam_init={self._p_cam_init is not None}, running={self._running}',
                throttle_duration_sec=2.0)
            return

        # Bước 2: Lấy độ dời tương đối từ camera, cộng thêm object offset"""

new_func = """    def _apply_filter(self, p_cam: np.ndarray, state: CameraFilterState):
        \"\"\"Hàm dùng chung để áp dụng các bộ lọc (outlier, median, deadband, EMA)\"\"\"
        if not np.all(np.isfinite(p_cam)):
            self.get_logger().warn(
                f'Tọa độ không hợp lệ: {p_cam}',
                throttle_duration_sec=1.0,
            )
            return None

        # ─── Outlier Rejection (Loại bỏ đỉnh nhọn) ─────────
        if state.last_raw_p_cam is not None:
            deviation_from_last = np.linalg.norm(p_cam - state.last_raw_p_cam)
            if deviation_from_last > self._filter_outlier_threshold:
                state.outlier_count += 1
                if state.outlier_count < 5:
                    self.get_logger().warn(f'Outlier rejected #{state.outlier_count} (jumped {deviation_from_last*1000:.1f}mm). Ignoring.')
                    return None
                else:
                    self.get_logger().info(f'Too many outliers ({state.outlier_count}). Resetting filter to new position.')
                    state.outlier_count = 0
            else:
                state.outlier_count = 0
        
        state.last_raw_p_cam = p_cam.copy()

        # ─── Median Pre-filter cho trục Y (depth, nhiễu nhất) ────
        state.median_buffer_y.append(p_cam[1])
        min_median = max(3, self._filter_median_size_y // 2 + 1)  # ít nhất 3 mẫu
        if len(state.median_buffer_y) >= min_median:
            p_cam = p_cam.copy()
            p_cam[1] = float(np.median(state.median_buffer_y))

        # ─── Dynamic Deadband Logic ─────────────────────────
        state.recent_buffer.append(p_cam)
        
        should_hold = False
        hold_position = None

        if len(state.recent_buffer) >= 5:
            recent_data = np.array(state.recent_buffer)
            mean_pos = np.mean(recent_data, axis=0)

            # (A) Initial deadband: tay ở gần vị trí calibrate
            if self._p_cam_init is not None:
                deviation_from_init = np.linalg.norm(mean_pos - self._p_cam_init)
                if deviation_from_init < self._noise_tolerance:
                    should_hold = True
                    hold_position = self._p_cam_init.copy()
            
            if not should_hold:
                # (B) Moving deadband: tay đã di chuyển nhưng đang đứng yên
                recent_std = np.std(recent_data, axis=0)
                depth_range = np.max(recent_data[:, 1]) - np.min(recent_data[:, 1])
                
                if depth_range < self._moving_deadzone_tol:
                    state.stationary_counter += 1
                else:
                    state.stationary_counter = 0
                    state.last_moving_p_cam = p_cam.copy()

                if state.stationary_counter >= self._filter_stationary_threshold:
                    should_hold = True
                    hold_position = mean_pos.copy()

        if should_hold:
            if not state.is_holding_position:
                state.is_holding_position = True
                state.hold_p_cam = hold_position
                self.get_logger().info(
                    f'Deadband: HOLD at ({hold_position[0]:.3f}, {hold_position[1]:.3f}, {hold_position[2]:.3f})',
                    throttle_duration_sec=2.0)
            if hold_position is not None:
                state.hold_p_cam = hold_position
        else:
            if state.is_holding_position:
                self.get_logger().info(
                    f'Deadband: RELEASE — motion detected',
                    throttle_duration_sec=2.0)
            state.is_holding_position = False
            state.stationary_counter = 0

        if state.is_holding_position and state.hold_p_cam is not None:
            target_p_cam = state.hold_p_cam.copy()
        else:
            target_p_cam = p_cam

        if state.smoothed_p_cam is None:
            state.smoothed_p_cam = target_p_cam.copy()
        else:
            if state.is_holding_position:
                alpha_x = self._filter_ema_x_hold
                alpha_y = self._filter_ema_y_hold
                alpha_z = self._filter_ema_z_hold
            else:
                alpha_x = self._filter_ema_x_moving
                alpha_y = self._filter_ema_y_moving
                alpha_z = self._filter_ema_z_moving

            state.smoothed_p_cam[0] = alpha_x * target_p_cam[0] + (1.0 - alpha_x) * state.smoothed_p_cam[0]
            state.smoothed_p_cam[1] = alpha_y * target_p_cam[1] + (1.0 - alpha_y) * state.smoothed_p_cam[1]
            state.smoothed_p_cam[2] = alpha_z * target_p_cam[2] + (1.0 - alpha_z) * state.smoothed_p_cam[2]

        return state.smoothed_p_cam

    def _transform_and_publish_target(self, p_cam_to_use: np.ndarray):
        \"\"\"Tính toán target pose từ p_cam đã lọc và gửi xuống robot\"\"\"
        if self._p_cam_init is None or not self._running:
            self.get_logger().debug(
                f'Skip robot target: p_cam_init={self._p_cam_init is not None}, running={self._running}',
                throttle_duration_sec=2.0)
            return

        # Bước 2: Lấy độ dời tương đối từ camera, cộng thêm object offset"""

content = content.replace(old_func, new_func)

with open('src/coord_transform/coord_transform/transform_node.py', 'w') as f:
    f.write(content)
