#!/usr/bin/env python3
"""
UI Node — PyQtGraph live dashboard so sánh tọa độ thực tế vs dự đoán.

- Subscribe /hand_position        → tọa độ thực tế (HandState)
- Subscribe /ml/predicted_position → tọa độ dự đoán (HandPrediction)
- 3 đồ thị cuộn real-time: X, Y, Z
- Hiển thị: inference time, FPS, model name, buffer size
- Nút Start/Stop logging (gọi service /logger/toggle)
- Nút đổi model (publish tới /predictor/model_cmd)
"""

import sys
import time
import threading
from collections import deque

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from std_msgs.msg import String
from std_srvs.srv import SetBool, Trigger
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from builtin_interfaces.msg import Duration

from human_hand_msgs.msg import HandState, HandPrediction

try:
    import pyqtgraph as pg
    from pyqtgraph.Qt import QtWidgets, QtCore
    HAS_PYQTGRAPH = True
except ImportError:
    HAS_PYQTGRAPH = False


MAX_POINTS = 300   # Số điểm hiển thị trên mỗi trục
UPDATE_HZ = 20     # FPS cập nhật plot


class PredictorUiNode(Node):
    """ROS 2 node + PyQtGraph dashboard."""

    def __init__(self):
        super().__init__('predictor_ui')

        self.declare_parameter('max_points', MAX_POINTS)
        self.declare_parameter('update_hz', float(UPDATE_HZ))
        n_pts = self.get_parameter('max_points').value
        upd_hz = self.get_parameter('update_hz').value

        # ── Data buffers ────────────────────────────────────────────────────
        self._meas = {'x': deque(maxlen=n_pts),
                      'y': deque(maxlen=n_pts),
                      'z': deque(maxlen=n_pts)}
        self._pred = {'x': deque(maxlen=n_pts),
                      'y': deque(maxlen=n_pts),
                      'z': deque(maxlen=n_pts)}
        self._t_meas: deque = deque(maxlen=n_pts)
        self._t_pred: deque = deque(maxlen=n_pts)

        # ── Stats display ────────────────────────────────────────────────────
        self._inf_ms = 0.0
        self._model_name = 'N/A'
        self._buf_size = 0
        self._fps_meas = 0.0
        self._fps_pred = 0.0
        self._fps_counter_m = 0
        self._fps_counter_p = 0
        self._fps_t = time.time()
        self._fps_t = time.time()
        self._logging = False
        self._is_drawing_ui = False
        self._is_predicting = False
        self._is_calibrated = False
        self._is_init_pose_captured = False
        self._backend_mode = 'UNKNOWN'
        self._trajectory_mode = 'ground_truth'  # 'ground_truth' or 'prediction'
        self._lock = threading.Lock()

        # ── Subscribers ──────────────────────────────────────────────────────
        self.create_subscription(HandState, '/hand_position', self._cb_meas, 10)
        self.create_subscription(
            HandPrediction, '/ml/predicted_position', self._cb_pred, 10)

        # ── Publishers ───────────────────────────────────────────────────────
        self._model_pub = self.create_publisher(String, '/predictor/model_cmd', 5)

        # ── Service clients ──────────────────────────────────────────────────
        self._logger_cli = self.create_client(SetBool, '/logger/toggle')
        self._predictor_cli = self.create_client(SetBool, '/predictor/toggle')
        self._calib_cli = self.create_client(Trigger, '/realsense/calibrate_origin')
        self._capture_init_cli = self.create_client(Trigger, '/coord_transform/capture_init_pose')
        self._stop_traj_cli = self.create_client(Trigger, '/yaskawa/stop_traj_mode')
        self._servo_on_cli = self.create_client(Trigger, '/yaskawa/servo_on')
        self._reset_error_cli = self.create_client(Trigger, '/yaskawa/reset_error')

        # ── Action clients ───────────────────────────────────────────────────
        self._go_home_sim_action = ActionClient(
            self,
            FollowJointTrajectory,
            '/hc10dtp_arm_controller/follow_joint_trajectory',
        )
        self._go_home_real_action = ActionClient(
            self,
            FollowJointTrajectory,
            '/yaskawa/follow_joint_trajectory',
        )

        # ── FPS timer ───────────────────────────────────────────────────────
        self.create_timer(1.0, self._update_fps)

        # ── Spin in background thread ────────────────────────────────────────
        self._spin_thread = threading.Thread(
            target=rclpy.spin, args=(self,), daemon=True)
        self._spin_thread.start()

        self.get_logger().info('[UI] Node started')

    # ── ROS Callbacks ────────────────────────────────────────────────────────

    def _cb_meas(self, msg: HandState):
        if not msg.is_tracked or not self._is_drawing_ui:
            return
        t = time.time()
        with self._lock:
            self._t_meas.append(t)
            self._meas['x'].append(msg.x)
            self._meas['y'].append(msg.y)
            self._meas['z'].append(msg.z)
            self._fps_counter_m += 1

    def _cb_pred(self, msg: HandPrediction):
        if not self._is_drawing_ui or not self._is_predicting:
            return
        t = time.time()
        with self._lock:
            self._t_pred.append(t)
            self._pred['x'].append(msg.x)
            self._pred['y'].append(msg.y)
            self._pred['z'].append(msg.z)
            self._inf_ms = msg.inference_time_ms
            self._model_name = msg.model_name or 'N/A'
            self._buf_size = msg.buffer_size
            self._fps_counter_p += 1

    def _update_fps(self):
        now = time.time()
        dt = now - self._fps_t
        if dt > 0:
            with self._lock:
                self._fps_meas = self._fps_counter_m / dt
                self._fps_pred = self._fps_counter_p / dt
                self._fps_counter_m = 0
                self._fps_counter_p = 0
        self._fps_t = now

    def get_buffers(self):
        with self._lock:
            return (
                list(self._meas['x']), list(self._meas['y']), list(self._meas['z']),
                list(self._pred['x']), list(self._pred['y']), list(self._pred['z']),
                self._inf_ms, self._model_name, self._buf_size,
                self._fps_meas, self._fps_pred,
            )

    # ── Service calls ────────────────────────────────────────────────────────

    def call_logger_toggle(self, enable: bool):
        if not self._logger_cli.service_is_ready():
            self.get_logger().warn('[UI] /logger/toggle not ready')
            return
        req = SetBool.Request()
        req.data = enable
        self._logger_cli.call_async(req)
        self._logging = enable

    def call_predictor_toggle(self, enable: bool):
        if not self._predictor_cli.service_is_ready():
            self.get_logger().warn('[UI] /predictor/toggle not ready')
            return
        req = SetBool.Request()
        req.data = enable
        self._predictor_cli.call_async(req)
        self._is_predicting = enable

    def set_trajectory_mode(self, mode: str):
        """Set trajectory mode: 'ground_truth' or 'prediction'"""
        if mode not in ['ground_truth', 'prediction']:
            self.get_logger().warn(f'[UI] Invalid trajectory mode: {mode}')
            return
        self._trajectory_mode = mode
        self.get_logger().info(f'[UI] Trajectory mode set to: {mode}')

    def send_model_cmd(self, model_name: str):
        msg = String()
        msg.data = model_name
        self._model_pub.publish(msg)
        self.get_logger().info(f'[UI] Model cmd → {model_name}')

    def call_calibrate(self):
        if not self._calib_cli.service_is_ready():
            self.get_logger().warn('[UI] /realsense/calibrate_origin not ready')
            return
        req = Trigger.Request()
        self._calib_cli.call_async(req)
        self._is_calibrated = True

    def call_capture_init_pose(self):
        if not self._capture_init_cli.service_is_ready():
            self.get_logger().warn('[UI] /coord_transform/capture_init_pose not ready')
            return False
        req = Trigger.Request()
        self._capture_init_cli.call_async(req)
        self._is_init_pose_captured = True
        return True

    def call_trigger_service(self, client, name: str):
        if not client.service_is_ready():
            self.get_logger().warn(f'[UI] {name} not ready')
            return False
        req = Trigger.Request()
        client.call_async(req)
        return True

    def detect_backend_mode(self) -> str:
        sim_ready = self._go_home_sim_action.wait_for_server(timeout_sec=0.05)
        real_ready = self._go_home_real_action.wait_for_server(timeout_sec=0.05)
        if real_ready:
            self._backend_mode = 'REAL'
        elif sim_ready:
            self._backend_mode = 'SIM'
        elif self._stop_traj_cli.wait_for_service(timeout_sec=0.01):
            # Có yaskawa service nhưng chưa có action ready => backend trung gian.
            self._backend_mode = 'HYBRID'
        else:
            self._backend_mode = 'UNKNOWN'
        return self._backend_mode

    def go_home(self):
        action_client = None
        if self._go_home_real_action.wait_for_server(timeout_sec=0.1):
            action_client = self._go_home_real_action
        elif self._go_home_sim_action.wait_for_server(timeout_sec=0.1):
            action_client = self._go_home_sim_action
        else:
            self.get_logger().warn('[UI] No follow_joint_trajectory action server available')
            return False

        goal_msg = FollowJointTrajectory.Goal()
        goal_msg.trajectory.joint_names = [
            'joint_1_s', 'joint_2_l', 'joint_3_u',
            'joint_4_r', 'joint_5_b', 'joint_6_t'
        ]
        point = JointTrajectoryPoint()
        point.positions = [0.0] * 6
        point.time_from_start = Duration(sec=3, nanosec=0)
        goal_msg.trajectory.points = [point]
        action_client.send_goal_async(goal_msg)
        return True

    def call_clear_draw(self):
        with self._lock:
            for k in ['x', 'y', 'z']:
                self._meas[k].clear()
                self._pred[k].clear()
            self._t_meas.clear()
            self._t_pred.clear()


# ── PyQtGraph Window ─────────────────────────────────────────────────────────

class DashboardWindow:
    """PyQtGraph dashboard window."""

    COLOR_MEAS = (100, 200, 255)   # blue — thực tế
    COLOR_PRED = (255, 150, 50)    # orange — dự đoán

    def __init__(self, node: PredictorUiNode):
        self.node = node
        pg.setConfigOption('antialias', True)
        pg.setConfigOption('background', '#1a1a2e')
        pg.setConfigOption('foreground', '#e0e0e0')

        self.app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

        self.win = QtWidgets.QWidget()
        self.win.setWindowTitle('HRC Trajectory Dashboard — Ubuntu')
        self.win.resize(1200, 750)
        self.win.setStyleSheet('background: #1a1a2e; color: #e0e0e0;')

        main_layout = QtWidgets.QVBoxLayout(self.win)

        # ── Top bar: stats ────────────────────────────────────────────────
        top = QtWidgets.QHBoxLayout()
        self._lbl_model = QtWidgets.QLabel('Model: N/A')
        self._lbl_inf = QtWidgets.QLabel('Inf: 0.0 ms')
        self._lbl_fps = QtWidgets.QLabel('FPS: 0 | 0')
        self._lbl_buf = QtWidgets.QLabel('Buf: 0')
        self._lbl_backend = QtWidgets.QLabel('Backend: UNKNOWN')
        for lbl in [self._lbl_model, self._lbl_inf, self._lbl_fps, self._lbl_buf, self._lbl_backend]:
            lbl.setStyleSheet('color: #a0f0a0; font-size: 13px; font-weight: bold;')
            top.addWidget(lbl)
        top.addStretch()
        main_layout.addLayout(top)

        # ── Plots ─────────────────────────────────────────────────────────
        self.gw = pg.GraphicsLayoutWidget()
        self.gw.setFixedHeight(520)
        plots_data = [('X axis (m)', 'meas_x', 'pred_x'),
                      ('Y axis (m)', 'meas_y', 'pred_y'),
                      ('Z axis (m)', 'meas_z', 'pred_z')]

        self.plots = {}
        self.curves_m = {}
        self.curves_p = {}

        for i, (title, mk, pk) in enumerate(plots_data):
            p = self.gw.addPlot(row=0, col=i, title=title)
            p.setLabel('left', title)
            p.setLabel('bottom', 'Frames')
            p.addLegend(offset=(5, 5))
            p.showGrid(x=True, y=True, alpha=0.3)
            
            p.getAxis('left').enableAutoSIPrefix(False)
            p.getAxis('bottom').enableAutoSIPrefix(False)
            
            # Cố định scale theo yêu cầu
            p.setXRange(0, 300, padding=0)
            p.enableAutoRange(axis='y', enable=False)
            
            if i == 0:
                p.setYRange(-1.0, 1.0, padding=0)  # X axis
            elif i == 1:
                p.setYRange(0.0, 2.0, padding=0)   # Y axis
            elif i == 2:
                p.setYRange(-0.1, 0.8, padding=0)   # Z axis

            self.curves_m[i] = p.plot(pen=pg.mkPen(self.COLOR_MEAS, width=2),
                                      name='Actual')
            self.curves_p[i] = p.plot(pen=pg.mkPen(self.COLOR_PRED, width=2),
                                      name='Predicted')
            self.plots[i] = p

        main_layout.addWidget(self.gw)

        # ── Bottom bar: controls ──────────────────────────────────────────
        ctrl = QtWidgets.QVBoxLayout()

        # Model buttons
        model_grp = QtWidgets.QGroupBox('Model')
        model_grp.setStyleSheet(
            'QGroupBox { color: #e0e0e0; border: 1px solid #555; border-radius: 4px; margin-top: 6px; }'
            'QGroupBox::title { subcontrol-origin: margin; left: 8px; }'
        )
        mg_l = QtWidgets.QHBoxLayout(model_grp)
        for m in ['RNN', 'GRU', 'LSTM']:
            btn = QtWidgets.QPushButton(m)
            btn.setFixedWidth(70)
            btn.setStyleSheet(
                'QPushButton { background: #16213e; color: #e0e0e0; border: 1px solid #0f3460; '
                'border-radius: 4px; padding: 4px; } '
                'QPushButton:hover { background: #0f3460; }'
            )
            btn.clicked.connect(lambda checked, n=m.lower(): node.send_model_cmd(n))
            mg_l.addWidget(btn)
        row_1 = QtWidgets.QHBoxLayout()
        row_1.addWidget(model_grp)
        row_1.addStretch()

        # Trajectory mode selector
        traj_grp = QtWidgets.QGroupBox('Trajectory Mode')
        traj_grp.setStyleSheet(
            'QGroupBox { color: #e0e0e0; border: 1px solid #555; border-radius: 4px; margin-top: 6px; }'
            'QGroupBox::title { subcontrol-origin: margin; left: 8px; }'
        )
        traj_l = QtWidgets.QHBoxLayout(traj_grp)
        self.btn_traj_gt = QtWidgets.QPushButton('📍 Ground Truth')
        self.btn_traj_gt.setFixedWidth(120)
        self.btn_traj_gt.setCheckable(True)
        self.btn_traj_gt.setChecked(True)
        self.btn_traj_gt.setStyleSheet(self._btn_style('#1a6b2e', '#2ba347'))
        self.btn_traj_gt.clicked.connect(lambda: self._set_trajectory_mode('ground_truth'))
        traj_l.addWidget(self.btn_traj_gt)
        
        self.btn_traj_pred = QtWidgets.QPushButton('🧠 Prediction')
        self.btn_traj_pred.setFixedWidth(120)
        self.btn_traj_pred.setCheckable(True)
        self.btn_traj_pred.setStyleSheet(self._btn_style('#6c3483', '#8e44ad'))
        self.btn_traj_pred.clicked.connect(lambda: self._set_trajectory_mode('prediction'))
        traj_l.addWidget(self.btn_traj_pred)
        row_1.addWidget(traj_grp)
        row_1.addStretch()

        # Run toggle
        self.btn_pred = QtWidgets.QPushButton('▶ Start Run')
        self.btn_pred.setFixedWidth(160)
        self.btn_pred.setCheckable(True)
        self.btn_pred.setStyleSheet(self._btn_style('#1a6b2e', '#2ba347'))
        self.btn_pred.clicked.connect(self._toggle_run)
        row_1.addWidget(self.btn_pred)

        # Calibrate Button
        self.btn_calib = QtWidgets.QPushButton('⌖ Calibrate Camera')
        self.btn_calib.setFixedWidth(150)
        self.btn_calib.setStyleSheet(self._btn_style('#2980b9', '#3498db'))
        self.btn_calib.clicked.connect(self._do_calibrate)
        row_1.addWidget(self.btn_calib)

        self.btn_capture = QtWidgets.QPushButton('📌 Capture Init Pose')
        self.btn_capture.setFixedWidth(165)
        self.btn_capture.setStyleSheet(self._btn_style('#145a86', '#1f78b4'))
        self.btn_capture.clicked.connect(self._do_capture_init_pose)
        row_1.addWidget(self.btn_capture)

        ctrl.addLayout(row_1)

        row_2 = QtWidgets.QHBoxLayout()

        self.btn_enable_robot = QtWidgets.QPushButton('⚡ Enable Robot')
        self.btn_enable_robot.setFixedWidth(145)
        self.btn_enable_robot.setStyleSheet(self._btn_style('#125c2b', '#1f8a3a'))
        self.btn_enable_robot.clicked.connect(self._enable_robot)
        row_2.addWidget(self.btn_enable_robot)

        self.btn_disable_robot = QtWidgets.QPushButton('⛔ Disable Robot')
        self.btn_disable_robot.setFixedWidth(145)
        self.btn_disable_robot.setStyleSheet(self._btn_style('#7b241c', '#922b21'))
        self.btn_disable_robot.clicked.connect(self._disable_robot)
        row_2.addWidget(self.btn_disable_robot)

        self.btn_soft_stop = QtWidgets.QPushButton('🛑 Soft Stop')
        self.btn_soft_stop.setFixedWidth(120)
        self.btn_soft_stop.setStyleSheet(self._btn_style('#8e0000', '#c0392b'))
        self.btn_soft_stop.clicked.connect(self._soft_stop)
        row_2.addWidget(self.btn_soft_stop)

        self.btn_go_home = QtWidgets.QPushButton('🏠 Go Home')
        self.btn_go_home.setFixedWidth(120)
        self.btn_go_home.setStyleSheet(self._btn_style('#6c3483', '#8e44ad'))
        self.btn_go_home.clicked.connect(self._go_home)
        row_2.addWidget(self.btn_go_home)

        # Draw control toggle
        self.btn_draw = QtWidgets.QPushButton('🖍 Start Draw')
        self.btn_draw.setFixedWidth(130)
        self.btn_draw.setCheckable(True)
        self.btn_draw.setStyleSheet(self._btn_style('#8e44ad', '#9b59b6'))
        self.btn_draw.clicked.connect(self._toggle_draw)
        row_2.addWidget(self.btn_draw)

        # Draw clear
        self.btn_clear = QtWidgets.QPushButton('🔄 Reset Draw')
        self.btn_clear.setFixedWidth(130)
        self.btn_clear.setStyleSheet(self._btn_style('#f39c12', '#f1c40f'))
        self.btn_clear.clicked.connect(self._do_clear_draw)
        row_2.addWidget(self.btn_clear)

        row_2.addStretch()
        ctrl.addLayout(row_2)

        self._lbl_status = QtWidgets.QLabel('State: PREPARE | Ready checks pending')
        self._lbl_status.setStyleSheet('color: #ffd479; font-size: 12px; font-weight: bold;')
        ctrl.addWidget(self._lbl_status)

        main_layout.addLayout(ctrl)

        # ── Timer ─────────────────────────────────────────────────────────
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._refresh)
        self.timer.start(int(1000 / UPDATE_HZ))

        self.win.show()

    @staticmethod
    def _btn_style(bg_off, bg_on):
        return (
            f'QPushButton {{ background: {bg_off}; color: #e0e0e0; border: none; '
            f'border-radius: 4px; padding: 6px 10px; font-weight: bold; }}'
            f'QPushButton:checked {{ background: {bg_on}; }}'
            f'QPushButton:hover {{ opacity: 0.85; }}'
        )

    def _toggle_run(self, checked):
        if checked:
            if not self.node._is_calibrated:
                self._set_status('State: ALIGN | Calibrate camera first')
                self.btn_pred.setChecked(False)
                return
            if not self.node._is_init_pose_captured:
                self._set_status('State: ALIGN | Capture init pose first')
                self.btn_pred.setChecked(False)
                return
        
        # Only enable prediction if in prediction mode
        if checked and self.node._trajectory_mode == 'prediction':
            self.node.call_predictor_toggle(True)
        elif not checked:
            self.node.call_predictor_toggle(False)
        
        self.node.call_logger_toggle(checked)
        self.btn_pred.setText('⏸ Stop Run' if checked else '▶ Start Run')
        
        mode_str = f'({self.node._trajectory_mode.replace("_", " ").upper()})'
        self._set_status('State: RUN | Streaming enabled ' + mode_str if checked else 'State: PREPARE | Run stopped')

    def _do_calibrate(self):
        self.node.call_calibrate()
        self._set_status('State: ALIGN | Camera origin calibrated')

    def _do_capture_init_pose(self):
        # Ensure prediction is NOT enabled during capture
        self.node.call_predictor_toggle(False)
        ok = self.node.call_capture_init_pose()
        if ok:
            self._set_status('State: ALIGN | Init pose captured (robot paused, safe)')
        else:
            self._set_status('State: ALIGN | Capture init pose failed')

    def _enable_robot(self):
        ok_reset = self.node.call_trigger_service(self.node._reset_error_cli, '/yaskawa/reset_error')
        ok_servo = self.node.call_trigger_service(self.node._servo_on_cli, '/yaskawa/servo_on')
        if ok_reset and ok_servo:
            self._set_status('State: PREPARE | Robot enabled (reset + servo_on)')
        else:
            self._set_status('State: PREPARE | Robot enable failed')

    def _disable_robot(self):
        ok = self.node.call_trigger_service(self.node._stop_traj_cli, '/yaskawa/stop_traj_mode')
        self.node.call_predictor_toggle(False)
        self.node.call_logger_toggle(False)
        self.btn_pred.setChecked(False)
        self.btn_pred.setText('▶ Start Run')
        if ok:
            mode_str = self.node._trajectory_mode.replace('_', ' ').upper()
            self._set_status(f'State: RECOVER | Robot disabled ({mode_str} mode remains selected)')
        else:
            self._set_status('State: RECOVER | Disable request failed')

    def _soft_stop(self):
        ok = self.node.call_trigger_service(self.node._stop_traj_cli, '/yaskawa/stop_traj_mode')
        if ok:
            self._set_status('State: RECOVER | Soft stop sent')
        else:
            self._set_status('State: RECOVER | Soft stop unavailable')

    def _go_home(self):
        ok = self.node.go_home()
        if ok:
            self._set_status('State: RECOVER | Go-home command sent')
        else:
            self._set_status('State: RECOVER | Go-home action server unavailable')

    def _set_trajectory_mode(self, mode: str):
        self.node.set_trajectory_mode(mode)
        # Update button states
        if mode == 'ground_truth':
            self.btn_traj_gt.setChecked(True)
            self.btn_traj_pred.setChecked(False)
            self._set_status('State: PREPARE | Trajectory mode: GROUND TRUTH (default)')
        else:
            self.btn_traj_gt.setChecked(False)
            self.btn_traj_pred.setChecked(True)
            self._set_status('State: PREPARE | Trajectory mode: PREDICTION (requires model)')

    def _toggle_draw(self, checked):
        self.node._is_drawing_ui = checked
        self.btn_draw.setText('⏹ Stop Draw' if checked else '🖍 Start Draw')

    def _do_clear_draw(self):
        self.node.call_clear_draw()

    def _set_status(self, text: str):
        self._lbl_status.setText(text)

    def _refresh(self):
        (mx, my, mz, px, py, pz,
         inf_ms, model, buf, fps_m, fps_p) = self.node.get_buffers()

        axes_m = [mx, my, mz]
        axes_p = [px, py, pz]

        for i in range(3):
            ym = axes_m[i]
            yp = axes_p[i]
            
            xm = list(range(len(ym)))
            
            offset = len(ym) - len(yp)
            if offset < 0:
                offset = 0
            xp = [x + offset for x in range(len(yp))]
            
            self.curves_m[i].setData(xm, ym)
            self.curves_p[i].setData(xp, yp)

        self._lbl_model.setText(f'Model: {model}')
        self._lbl_inf.setText(f'Inf: {inf_ms:.1f} ms')
        self._lbl_fps.setText(f'Actual: {fps_m:.1f} Hz | Pred: {fps_p:.1f} Hz')
        self._lbl_buf.setText(f'Buf: {buf}')
        mode = self.node.detect_backend_mode()
        self._lbl_backend.setText(f'Backend: {mode}')

    def exec(self):
        return self.app.exec()


# ── main ─────────────────────────────────────────────────────────────────────

def main(args=None):
    if not HAS_PYQTGRAPH:
        print('[ui_node] ERROR: pyqtgraph not installed. Run: pip install pyqtgraph PyQt5')
        sys.exit(1)

    rclpy.init(args=args)
    node = PredictorUiNode()

    try:
        dashboard = DashboardWindow(node)
        sys.exit(dashboard.exec())
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
