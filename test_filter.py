import numpy as np

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

class MockNode:
    def __init__(self):
        self._filter_outlier_threshold = 0.15
        self._filter_median_size_y = 3
        self._filter_stationary_threshold = 5
        self._noise_tolerance = 0.02
        self._moving_deadzone_tol = 0.015
        self._filter_ema_x_hold = 0.08
        self._filter_ema_y_hold = 0.02
        self._filter_ema_z_hold = 0.05
        self._filter_ema_x_moving = 0.30
        self._filter_ema_y_moving = 0.18
        self._filter_ema_z_moving = 0.30
        
        self._p_cam_init = None

    def get_logger(self):
        class Logger:
            def info(self, msg, **kwargs): pass
            def warn(self, msg, **kwargs): pass
            def debug(self, msg, **kwargs): pass
        return Logger()

    def _apply_filter(self, p_cam: np.ndarray, state: CameraFilterState):
        if not np.all(np.isfinite(p_cam)):
            return None

        # ─── Outlier Rejection (Loại bỏ đỉnh nhọn) ─────────
        if state.last_raw_p_cam is not None:
            deviation_from_last = np.linalg.norm(p_cam - state.last_raw_p_cam)
            if deviation_from_last > self._filter_outlier_threshold:
                state.outlier_count += 1
                if state.outlier_count < 5:
                    return None
                else:
                    state.outlier_count = 0
            else:
                state.outlier_count = 0
        
        state.last_raw_p_cam = p_cam.copy()

        # ─── Median Pre-filter cho trục Y (depth, nhiễu nhất) ────
        state.median_buffer_y.append(p_cam[1])
        min_median = max(3, self._filter_median_size_y // 2 + 1)
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

            if self._p_cam_init is not None:
                deviation_from_init = np.linalg.norm(mean_pos - self._p_cam_init)
                if deviation_from_init < self._noise_tolerance:
                    should_hold = True
                    hold_position = self._p_cam_init.copy()
            
            if not should_hold:
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
            if hold_position is not None:
                state.hold_p_cam = hold_position
        else:
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

node = MockNode()
state = CameraFilterState(3)

print("Simulating pre-run (calibration)...")
for i in range(10):
    p = np.array([0.1, 0.2, 0.3])
    out = node._apply_filter(p, state)
    print("Out:", out)

node._p_cam_init = np.array([0.1, 0.2, 0.3])
print("\nSimulating Start Run (_p_cam_init updated)...")

for i in range(5):
    p = np.array([0.101, 0.201, 0.301]) # small movement
    out = node._apply_filter(p, state)
    print("Out:", out)

print("\nSimulating hand movement away...")
for i in range(5):
    p = np.array([0.5, 0.6, 0.7]) # large movement
    out = node._apply_filter(p, state)
    print("Out:", out)

