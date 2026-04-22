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
from std_msgs.msg import String
from std_srvs.srv import SetBool, Trigger

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
        if not self._is_drawing_ui:
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
        for lbl in [self._lbl_model, self._lbl_inf, self._lbl_fps, self._lbl_buf]:
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
        ctrl = QtWidgets.QHBoxLayout()

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
        ctrl.addWidget(model_grp)

        ctrl.addStretch()

        # Predictor toggle
        self.btn_pred = QtWidgets.QPushButton('▶ Start Prediction')
        self.btn_pred.setFixedWidth(160)
        self.btn_pred.setCheckable(True)
        self.btn_pred.setStyleSheet(self._btn_style('#1a6b2e', '#2ba347'))
        self.btn_pred.clicked.connect(self._toggle_prediction)
        ctrl.addWidget(self.btn_pred)

        # Calibrate Button
        self.btn_calib = QtWidgets.QPushButton('⌖ Calib & Save')
        self.btn_calib.setFixedWidth(140)
        self.btn_calib.setStyleSheet(self._btn_style('#2980b9', '#3498db'))
        self.btn_calib.clicked.connect(self._do_calibrate)
        ctrl.addWidget(self.btn_calib)

        # Draw control toggle
        self.btn_draw = QtWidgets.QPushButton('🖍 Start Draw')
        self.btn_draw.setFixedWidth(130)
        self.btn_draw.setCheckable(True)
        self.btn_draw.setStyleSheet(self._btn_style('#8e44ad', '#9b59b6'))
        self.btn_draw.clicked.connect(self._toggle_draw)
        ctrl.addWidget(self.btn_draw)

        # Draw clear
        self.btn_clear = QtWidgets.QPushButton('🔄 Reset Draw')
        self.btn_clear.setFixedWidth(130)
        self.btn_clear.setStyleSheet(self._btn_style('#f39c12', '#f1c40f'))
        self.btn_clear.clicked.connect(self._do_clear_draw)
        ctrl.addWidget(self.btn_clear)

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

    def _toggle_prediction(self, checked):
        self.node.call_predictor_toggle(checked)
        self.node.call_logger_toggle(checked)
        self.btn_pred.setText('⏸ Stop Prediction' if checked else '▶ Start Prediction')

    def _do_calibrate(self):
        self.node.call_calibrate()

    def _toggle_draw(self, checked):
        self.node._is_drawing_ui = checked
        self.btn_draw.setText('⏹ Stop Draw' if checked else '🖍 Start Draw')

    def _do_clear_draw(self):
        self.node.call_clear_draw()

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
