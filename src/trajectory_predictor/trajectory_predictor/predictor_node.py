#!/usr/bin/env python3
"""
Predictor Node — ROS 2 node quản lý inference worker subprocess.

- Subscribe /hand_position (HandState) — tọa độ thô từ bridge.
- Duy trì sliding window 20 frames.
- Spawn inference_worker.py trong venv Python qua stdin/stdout JSON.
- Publish kết quả lên /ml/predicted_position (HandPrediction).
- Service /predictor/set_model để đổi model, /predictor/toggle để bật/tắt.
"""

import json
import os
import subprocess
import sys
import threading
import time
from collections import deque

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import SetBool

from human_hand_msgs.msg import HandState, HandPrediction, SystemStatus


class PredictorNode(Node):
    """ROS 2 Predictor Node với inference subprocess."""

    def __init__(self):
        super().__init__('trajectory_predictor')

        # ── Parameters ──────────────────────────────────────────────────────
        self.declare_parameter('model_dir', '')
        self.declare_parameter('default_model', 'gru')
        self.declare_parameter('scaler_x_file', 'scaler_x.pkl')
        self.declare_parameter('scaler_y_file', 'scaler_y.pkl')
        self.declare_parameter('window_size', 20)
        self.declare_parameter('num_features', 3)
        self.declare_parameter('auto_start', False)
        self.declare_parameter('clear_on_tracking_lost', 1.0)
        self.declare_parameter('model_files.rnn', 'rnn_velocity_3_layers.h5')
        self.declare_parameter('model_files.gru', 'gru_velocity_3_layers.h5')
        self.declare_parameter('model_files.lstm', 'lstm_velocity_3_layers.h5')
        # Path tới Python venv (nếu có), nếu không dùng sys.executable
        self.declare_parameter('venv_python', '')

        # ── Output filter parameters ─────────────────────────────────────────
        # Proximity clamp: max deviation from last measured position (m)
        self.declare_parameter('filter.max_deviation', 0.15)
        # Rate limiter: max change per frame (m). At ~30Hz, 0.07m ≈ 2.1 m/s
        self.declare_parameter('filter.max_rate', 0.07)
        # EMA smoothing factor (0 = no smoothing, 1 = raw prediction)
        self.declare_parameter('filter.ema_alpha', 0.4)
        # Enable/disable output filter
        self.declare_parameter('filter.enabled', True)

        self.model_dir = self.get_parameter('model_dir').value
        self.default_model = self.get_parameter('default_model').value
        self.scaler_x_file = self.get_parameter('scaler_x_file').value
        self.scaler_y_file = self.get_parameter('scaler_y_file').value
        self.window_size = self.get_parameter('window_size').value
        self.num_features = self.get_parameter('num_features').value
        self.auto_start = self.get_parameter('auto_start').value
        self.clear_timeout = self.get_parameter('clear_on_tracking_lost').value
        venv_python = self.get_parameter('venv_python').value
        self.python_exe = venv_python if venv_python else sys.executable

        # Filter config
        self._filter_max_dev = self.get_parameter('filter.max_deviation').value
        self._filter_max_rate = self.get_parameter('filter.max_rate').value
        self._filter_ema_alpha = self.get_parameter('filter.ema_alpha').value
        self._filter_enabled = self.get_parameter('filter.enabled').value

        self.model_files = {
            'rnn': self.get_parameter('model_files.rnn').value,
            'gru': self.get_parameter('model_files.gru').value,
            'lstm': self.get_parameter('model_files.lstm').value,
        }

        # ── State ────────────────────────────────────────────────────────────
        self._buffer: deque = deque(maxlen=self.window_size)
        self._last_data_time = 0.0
        self._predicting = self.auto_start
        self._current_model = self.default_model
        self._worker_ready = False
        self._worker_proc: subprocess.Popen | None = None
        self._worker_lock = threading.Lock()
        self._pending_model_switch: str | None = None

        # ── Output filter state ──────────────────────────────────────────────
        self._last_meas = [0.0, 0.0, 0.0]      # last measured position
        self._last_filtered = None              # last filtered prediction [x,y,z]
        self._filter_reject_count = 0

        # ── Publishers ───────────────────────────────────────────────────────
        self.pred_pub = self.create_publisher(
            HandPrediction, '/ml/predicted_position', 10)
        self.status_pub = self.create_publisher(
            SystemStatus, '/ml/predictor_status', 10)

        # ── Subscribers ──────────────────────────────────────────────────────
        self.create_subscription(HandState, '/hand_position', self._on_hand, 10)
        # Nếu bridge publish tọa độ thô (trước khi predict), cũng lắng nghe
        self.create_subscription(
            HandPrediction, '/predicted_position', self._on_bridge_data, 10)

        # Model switch command từ UI hay bridge
        self.create_subscription(String, '/predictor/model_cmd', self._on_model_cmd, 5)

        # ── Services ─────────────────────────────────────────────────────────
        self.create_service(SetBool, '/predictor/toggle', self._srv_toggle)
        self.create_service(SetBool, '/predictor/set_model_srv', self._srv_toggle)

        # ── Timers ───────────────────────────────────────────────────────────
        self.create_timer(1.0, self._publish_status)
        self.create_timer(self.clear_timeout, self._check_stale)

        # ── Launch inference worker ──────────────────────────────────────────
        self._launch_worker()

        self.get_logger().info(
            f'[Predictor] Started | model={self._current_model} | '
            f'window={self.window_size} | auto_start={self.auto_start}'
        )

    # ── Worker lifecycle ─────────────────────────────────────────────────────

    def _get_worker_script(self) -> str:
        """Tìm đường dẫn tới inference_worker.py."""
        # Thử cùng thư mục với file này
        here = os.path.dirname(os.path.abspath(__file__))
        candidate = os.path.join(here, 'inference_worker.py')
        if os.path.exists(candidate):
            return candidate
        # Thử share/ install
        share_candidate = os.path.join(
            os.path.expanduser('~'), 'hrc_ws', 'install',
            'trajectory_predictor', 'lib', 'trajectory_predictor',
            'inference_worker.py'
        )
        if os.path.exists(share_candidate):
            return share_candidate
        raise FileNotFoundError('inference_worker.py not found')

    def _launch_worker(self):
        """Spawn inference_worker.py subprocess."""
        if not self.model_dir:
            self.get_logger().warn('[Predictor] model_dir empty — worker not launched')
            return

        script = self._get_worker_script()
        config = {
            'model_dir': self.model_dir,
            'model_files': self.model_files,
            'scaler_x_file': self.scaler_x_file,
            'scaler_y_file': self.scaler_y_file,
            'default_model': self.default_model,
            'num_features': self.num_features,
            'window_size': self.window_size,
        }

        env = os.environ.copy()
        env['TF_CPP_MIN_LOG_LEVEL'] = '3'
        env['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

        try:
            proc = subprocess.Popen(
                [self.python_exe, script],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                env=env,
            )
            # Gửi config ban đầu
            proc.stdin.write(json.dumps(config) + '\n')
            proc.stdin.flush()

            with self._worker_lock:
                self._worker_proc = proc

            # Thread đọc stdout từ worker
            t = threading.Thread(target=self._reader_loop, daemon=True)
            t.start()

            # Thread đọc stderr
            t2 = threading.Thread(target=self._stderr_loop, daemon=True)
            t2.start()

            self.get_logger().info(f'[Predictor] Worker launched (pid={proc.pid})')
        except Exception as e:
            self.get_logger().error(f'[Predictor] Failed to launch worker: {e}')

    def _reader_loop(self):
        """Đọc JSON response từ worker stdout trong background thread."""
        proc = self._worker_proc
        if not proc:
            return
        for line in proc.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                resp = json.loads(line)
            except json.JSONDecodeError:
                continue

            rtype = resp.get('type', '')
            if rtype == 'ready':
                self._worker_ready = resp.get('success', False)
                model = resp.get('model_name', self._current_model)
                if self._worker_ready:
                    self.get_logger().info(
                        f'[Predictor] Worker READY | model={model}')
                    self._current_model = model
                else:
                    self.get_logger().error(
                        f'[Predictor] Worker NOT READY: {resp.get("message")}')

            elif rtype == 'model_loaded':
                ok = resp.get('success', False)
                model = resp.get('model_name', '')
                if ok:
                    self._current_model = model
                    self.get_logger().info(f'[Predictor] Model switched to {model}')
                else:
                    self.get_logger().warn(
                        f'[Predictor] Model switch failed: {resp.get("message")}')

            elif rtype == 'predict':
                pred = resp.get('prediction')
                if pred and len(pred) == 3:
                    self._publish_prediction(pred, resp.get('inference_ms', 0.0))

            elif rtype == 'info':
                self.get_logger().info(f'[Worker] {resp.get("message", "")}')

    def _stderr_loop(self):
        proc = self._worker_proc
        if not proc:
            return
        for line in proc.stderr:
            line = line.strip()
            if line:
                self.get_logger().warn(f'[Worker STDERR] {line}')

    def _send_to_worker(self, cmd: dict):
        with self._worker_lock:
            proc = self._worker_proc
        if proc and proc.poll() is None and self._worker_ready:
            try:
                proc.stdin.write(json.dumps(cmd) + '\n')
                proc.stdin.flush()
            except BrokenPipeError:
                self.get_logger().error('[Predictor] Worker pipe broken')

    # ── ROS Callbacks ────────────────────────────────────────────────────────

    def _on_hand(self, msg: HandState):
        """Nhận tọa độ từ /hand_position (HandState)."""
        if not msg.is_tracked:
            return
        self._last_meas = [msg.x, msg.y, msg.z]
        self._ingest_point(msg.x, msg.y, msg.z)

    def _on_bridge_data(self, msg: HandPrediction):
        """
        Nhận từ /predicted_position (output của bridge_node).
        Bridge node publish raw XYZ ở đây (trong pipeline mới, bridge
        publish HandPrediction với inference_time_ms=0 để forward tọa độ gốc).
        """
        # Chỉ dùng nếu /hand_position không hoạt động
        # (bridge gửi raw coords qua HandPrediction với model_name='raw')
        if msg.model_name == 'raw' or msg.model_name == '':
            self._ingest_point(msg.x, msg.y, msg.z)

    def _ingest_point(self, x: float, y: float, z: float):
        self._last_data_time = time.time()
        self._buffer.append([x, y, z])

        if not self._predicting or not self._worker_ready:
            return

        if len(self._buffer) < self.window_size:
            # Zero-pad ở đầu
            pad_count = self.window_size - len(self._buffer)
            padded = [[0.0, 0.0, 0.0]] * pad_count + list(self._buffer)
        else:
            padded = list(self._buffer)

        self._send_to_worker({'cmd': 'predict', 'data': padded})

    def _on_model_cmd(self, msg: String):
        """Nhận lệnh đổi model từ /predictor/model_cmd."""
        model_name = msg.data.strip().lower()
        if model_name not in self.model_files:
            self.get_logger().warn(
                f'[Predictor] Unknown model: {model_name}')
            return
        self.get_logger().info(f'[Predictor] Switching model → {model_name}')
        self._send_to_worker({'cmd': 'load_model', 'model_name': model_name})

    def _srv_toggle(self, request, response):
        self._predicting = request.data
        response.success = True
        response.message = 'Predicting STARTED' if self._predicting else 'Predicting STOPPED'
        if not self._predicting:
            self._buffer.clear()
            self._last_filtered = None
            self._filter_reject_count = 0
        self.get_logger().info(f'[Predictor] {response.message}')
        return response

    # ── Output Filter ────────────────────────────────────────────────────────

    def _filter_prediction(self, raw_pred: list) -> list:
        """3-layer output filter: proximity clamp → rate limiter → EMA.

        Layer 1 — Proximity Clamp:
            Giới hạn khoảng cách tối đa giữa dự đoán và vị trí thực tế.
            Nếu sai lệch trên bất kỳ trục nào vượt quá max_deviation,
            clamp giá trị đó lại gần vị trí đo được.

        Layer 2 — Rate Limiter:
            Giới hạn tốc độ thay đổi tối đa giữa 2 frame dự đoán liên tiếp.
            Ngăn hiện tượng nhảy đột ngột (jerk) khi model bị spike.

        Layer 3 — EMA Smoothing:
            Exponential Moving Average để làm mượt tín hiệu đầu ra.
            alpha nhỏ → mượt hơn nhưng trễ hơn.
        """
        filtered = [0.0, 0.0, 0.0]
        meas = self._last_meas
        max_dev = self._filter_max_dev
        max_rate = self._filter_max_rate
        alpha = self._filter_ema_alpha

        # ── Layer 1: Proximity clamp ─────────────────────────────────────
        for i in range(3):
            deviation = raw_pred[i] - meas[i]
            if abs(deviation) > max_dev:
                # Clamp: giữ hướng nhưng giới hạn biên độ
                clamped = meas[i] + max_dev * (1.0 if deviation > 0 else -1.0)
                filtered[i] = clamped
            else:
                filtered[i] = raw_pred[i]

        # ── Layer 2: Rate limiter ────────────────────────────────────────
        if self._last_filtered is not None:
            for i in range(3):
                delta = filtered[i] - self._last_filtered[i]
                if abs(delta) > max_rate:
                    filtered[i] = self._last_filtered[i] + max_rate * (1.0 if delta > 0 else -1.0)

        # ── Layer 3: EMA smoothing ───────────────────────────────────────
        if self._last_filtered is not None:
            for i in range(3):
                filtered[i] = alpha * filtered[i] + (1.0 - alpha) * self._last_filtered[i]

        self._last_filtered = filtered[:]
        return filtered

    # ── Publishing ───────────────────────────────────────────────────────────

    def _publish_prediction(self, pred: list, inf_ms: float):
        # Apply output filter if enabled
        if self._filter_enabled:
            filtered = self._filter_prediction(pred)
        else:
            filtered = pred

        msg = HandPrediction()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'world'
        msg.x = float(filtered[0])
        msg.y = float(filtered[1])
        msg.z = float(filtered[2])
        msg.inference_time_ms = float(inf_ms)
        msg.model_name = self._current_model
        msg.prediction_confidence = 1.0
        msg.buffer_size = len(self._buffer)
        self.pred_pub.publish(msg)

    def _publish_status(self):
        status = SystemStatus()
        status.header.stamp = self.get_clock().now().to_msg()
        status.node_name = 'trajectory_predictor'
        status.fps = 0.0
        if self._worker_ready and self._predicting:
            status.status = 'ok'
            status.message = f'Predicting | model={self._current_model} | buf={len(self._buffer)}'
        elif self._worker_ready:
            status.status = 'idle'
            status.message = f'Ready | model={self._current_model} | NOT predicting'
        else:
            status.status = 'warning'
            status.message = 'Worker not ready'
        self.status_pub.publish(status)

    def _check_stale(self):
        """Xóa buffer nếu không nhận dữ liệu trong thời gian dài."""
        if self._last_data_time > 0:
            dt = time.time() - self._last_data_time
            if dt > self.clear_timeout and self._buffer:
                self._buffer.clear()
                self.get_logger().info(
                    f'[Predictor] Buffer cleared (no data for {dt:.1f}s)')

    # ── Cleanup ──────────────────────────────────────────────────────────────

    def destroy_node(self):
        with self._worker_lock:
            proc = self._worker_proc
        if proc and proc.poll() is None:
            try:
                proc.stdin.write(json.dumps({'cmd': 'shutdown'}) + '\n')
                proc.stdin.flush()
                proc.wait(timeout=3.0)
            except Exception:
                proc.kill()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = PredictorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
