#!/usr/bin/env python3
"""
Experiment Logger Node — subscribes to /hand_position and
/predicted_position, logs synchronized data to CSV for offline analysis.

Output CSV columns:
  ros_timestamp, meas_x, meas_y, meas_z, pred_x, pred_y, pred_z,
  model_name, inference_ms, buffer_size

Author: Duy (auto-generated — extend as needed)
"""

import csv
import os
import time
from datetime import datetime

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import SetBool

from human_hand_msgs.msg import HandState, HandPrediction


class ExperimentLoggerNode(Node):
    """Logs measured + predicted positions to CSV and computes metrics."""

    def __init__(self):
        super().__init__('experiment_logger')

        self.declare_parameter('log_dir', os.path.expanduser('~/hrc_logs'))
        self.declare_parameter('auto_start', False)
        self.declare_parameter('default_model', 'unknown')

        self.log_dir = self.get_parameter('log_dir').value
        os.makedirs(self.log_dir, exist_ok=True)

        self.current_model = self.get_parameter('default_model').value
        self.is_logging = self.get_parameter('auto_start').value
        self.csv_file = None
        self.csv_writer = None
        self.csv_path = ''
        self.row_count = 0

        if self.is_logging:
            self._start_logging()

        # Latest data (quick-and-dirty sync: log on each prediction)
        self.last_meas = None

        # Subscribers
        self.create_subscription(HandState, '/hand_position', self._on_hand, 10)
        self.create_subscription(HandPrediction, '/ml/predicted_position', self._on_prediction, 10)
        # Stop command from bridge (scenario_id string from Windows)
        self.create_subscription(String, '/bridge/stop_command', self._on_stop_command, 5)

        # Service to toggle recording
        self.toggle_srv = self.create_service(SetBool, '/logger/toggle', self._srv_toggle)

        # Flush timer
        self.create_timer(5.0, self._flush)

        self.get_logger().info('Logger ready.')

    def _start_logging(self):
        try:
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            # Fallback for model name if it hasn't been received yet
            model_tag = str(self.current_model).upper() if self.current_model else "UNKNOWN"
            self.csv_path = os.path.join(self.log_dir, f'experiment_{model_tag}_{ts}.csv')
            
            self.get_logger().info(f'Attempting to open CSV file: {self.csv_path}')
            
            # Ensure directory exists once more
            os.makedirs(self.log_dir, exist_ok=True)
            
            self.csv_file = open(self.csv_path, 'w', newline='')
            self.csv_writer = csv.writer(self.csv_file)
            self.csv_writer.writerow([
                'ros_timestamp_ns', 'wall_time',
                'meas_x', 'meas_y', 'meas_z', 'is_tracked',
                'pred_x', 'pred_y', 'pred_z',
                'mae_x', 'mae_y', 'mae_z',
                'inference_ms', 'buffer_size'
            ])
            self.csv_file.flush()
            self.row_count = 0
            self.get_logger().info(f'✓ SUCCESSFULLY started logging to {self.csv_path}')
        except Exception as e:
            self.get_logger().error(f'✗ FAILED to start logging: {e}')
            self.is_logging = False
            self.csv_file = None
            self.csv_writer = None

    def _stop_logging_and_calc_metrics(self):
        if self.csv_file:
            try:
                self.csv_file.flush()
                self.csv_file.close()
                self.get_logger().info(f'Stopped logging. Saved {self.row_count} rows to {self.csv_path}')
                self._calculate_metrics(self.csv_path)
            except Exception as e:
                self.get_logger().error(f'Error during stop/metrics: {e}')
            finally:
                self.csv_file = None
                self.csv_writer = None

    def _on_stop_command(self, msg: String):
        """Nhận scenario_id từ bridge khi Windows bấm Stop."""
        scenario_id = msg.data.strip()
        self.get_logger().info(
            f'Stop command received from bridge | scenario_id={scenario_id!r}')

        if not self.is_logging:
            self.get_logger().info('Logger already stopped, ignoring stop command.')
            return

        # Dừng logging
        self.is_logging = False
        self._stop_logging_and_rename(scenario_id)

    def _stop_logging_and_rename(self, scenario_id: str):
        """Dừng ghi CSV và đổi tên file để thêm _ScenarioXXX."""
        if self.csv_file:
            try:
                self.csv_file.flush()
                self.csv_file.close()
                old_path = self.csv_path

                if scenario_id:
                    dir_name = os.path.dirname(old_path)
                    base = os.path.basename(old_path)
                    # Thêm _ScenarioID trước .csv
                    if base.endswith('.csv'):
                        new_name = base[:-4] + f'_Scenario{scenario_id}.csv'
                    else:
                        new_name = base + f'_Scenario{scenario_id}'
                    new_path = os.path.join(dir_name, new_name)
                    try:
                        os.rename(old_path, new_path)
                        self.csv_path = new_path
                        self.get_logger().info(
                            f'CSV renamed: {base} → {new_name}')
                    except Exception as e_rename:
                        self.get_logger().error(f'Rename failed: {e_rename}')

                self.get_logger().info(
                    f'Stopped logging. Saved {self.row_count} rows to {self.csv_path}')
                self._calculate_metrics(self.csv_path)
            except Exception as e:
                self.get_logger().error(f'Error during stop/rename: {e}')
            finally:
                self.csv_file = None
                self.csv_writer = None

    def _srv_toggle(self, request, response):
        self.get_logger().info(f'Service called: /logger/toggle with data={request.data}')
        
        if request.data == self.is_logging:
            response.success = True
            response.message = f'Already {"LOGGING" if self.is_logging else "STOPPED"}'
            return response

        self.is_logging = request.data
        if self.is_logging:
            self._start_logging()
            if self.csv_file:
                response.success = True
                response.message = 'Logger STARTED'
            else:
                response.success = False
                response.message = 'Logger FAILED TO START (check terminal)'
        else:
            self._stop_logging_and_calc_metrics()
            response.success = True
            response.message = 'Logger STOPPED & Metrics Computed'

        return response

    def _on_hand(self, msg: HandState):
        self.last_meas = msg
        # Optional: could log every hand state frame even if prediction is late?
        # For now, stay with prediction-synced logging as it defines the "experiment" row.

    def _on_prediction(self, msg: HandPrediction):
        new_model = msg.model_name
        
        # If we were logging with "UNKNOWN" and now know the model, rename the file
        if self.is_logging and self.csv_file and self.current_model.lower() == 'unknown':
            if new_model.lower() != 'unknown':
                self._rename_current_log(new_model)

        self.current_model = new_model
        if self.is_logging:
            if self.csv_writer is not None:
                self._write_row(self.last_meas, msg)
            else:
                pass

    def _rename_current_log(self, new_model_name):
        """Renames the currently open log file to include the correct model name."""
        try:
            old_path = self.csv_path
            if not os.path.exists(old_path):
                return

            # Keep the original timestamp but replace UNKNOWN with the new model
            dir_name = os.path.dirname(old_path)
            file_name = os.path.basename(old_path)
            new_file_name = file_name.replace('UNKNOWN', new_model_name.upper())
            new_path = os.path.join(dir_name, new_file_name)

            if old_path == new_path:
                return

            self.get_logger().info(f'Renaming log file: {file_name} -> {new_file_name}')
            
            # Flush and close temporarily to rename
            self.csv_file.flush()
            self.csv_file.close()
            
            os.rename(old_path, new_path)
            
            # Re-open in append mode
            self.csv_path = new_path
            self.csv_file = open(self.csv_path, 'a', newline='')
            self.csv_writer = csv.writer(self.csv_file)
        except Exception as e:
            self.get_logger().error(f'Failed to rename log file: {e}')

    def _write_row(self, meas, pred):
        now_ns = self.get_clock().now().nanoseconds
        wall = datetime.now().isoformat()

        mx = my = mz = ''
        tracked = ''
        if meas:
            mx, my, mz = f'{meas.x:.6f}', f'{meas.y:.6f}', f'{meas.z:.6f}'
            tracked = str(meas.is_tracked)

        px = py = pz = inf_ms = buf = ''
        mae_x = mae_y = mae_z = ''
        if pred:
            px, py, pz = f'{pred.x:.6f}', f'{pred.y:.6f}', f'{pred.z:.6f}'
            inf_ms = f'{pred.inference_time_ms:.2f}'
            buf = str(pred.buffer_size)
            if meas:
                mae_x = f'{abs(pred.x - meas.x):.6f}'
                mae_y = f'{abs(pred.y - meas.y):.6f}'
                mae_z = f'{abs(pred.z - meas.z):.6f}'

        self.csv_writer.writerow([
            now_ns, wall, mx, my, mz, tracked, px, py, pz, mae_x, mae_y, mae_z, inf_ms, buf
        ])
        self.row_count += 1

    def _calculate_metrics(self, csv_file_path):
        import math
        try:
            with open(csv_file_path, 'r') as f:
                reader = csv.DictReader(f)
                total_inference = 0.0
                total_mse = 0.0
                total_error = 0.0
                total_error_x = 0.0
                total_error_y = 0.0
                total_error_z = 0.0
                count = 0
                for row in reader:
                    try:
                        inf_ms = float(row['inference_ms'])
                        mx, my, mz = float(row['meas_x']), float(row['meas_y']), float(row['meas_z'])
                        px, py, pz = float(row['pred_x']), float(row['pred_y']), float(row['pred_z'])
                        total_inference += inf_ms
                        ex = px - mx
                        ey = py - my
                        ez = pz - mz
                        
                        # Mean Squared Error (MSE)
                        dist_sq = ex*ex + ey*ey + ez*ez
                        total_mse += dist_sq
                        
                        # Mean Absolute Error (MAE)
                        dist = math.sqrt(dist_sq)
                        total_error += dist
                        total_error_x += abs(ex)
                        total_error_y += abs(ey)
                        total_error_z += abs(ez)
                        count += 1
                    except (ValueError, KeyError):
                        pass

                if count > 0:
                    avg_inf = total_inference / count
                    avg_mse = total_mse / count
                    avg_mae = total_error / count
                    avg_x = total_error_x / count
                    avg_y = total_error_y / count
                    avg_z = total_error_z / count

                    summary = (
                        f"\n{'='*50}\n"
                        f"EXPERIMENT METRICS (Evaluated over {count} samples):\n"
                        f"  File: {os.path.basename(csv_file_path)}\n"
                        f"  Avg Inference Time: {avg_inf:.2f} ms\n"
                        f"  Mean Squared Error (MSE): {avg_mse:.6f} m²\n"
                        f"  Mean Absolute Error (MAE - 3D): {avg_mae:.4f} m\n"
                        f"      MAE X: {avg_x:.4f} m\n"
                        f"      MAE Y: {avg_y:.4f} m\n"
                        f"      MAE Z: {avg_z:.4f} m\n"
                        f"{'='*50}"
                    )
                    self.get_logger().info(summary)
                    
                    # Also append to the CSV file
                    with open(csv_file_path, 'a') as f:
                        f.write("\n" + summary + "\n")
                else:
                    self.get_logger().warn("No valid prediction/measurement pairs found in CSV.")
        except Exception as e:
            self.get_logger().error(f"Failed to calculate metrics: {e}")

    def _flush(self):
        try:
            if self.csv_file:
                self.csv_file.flush()
        except Exception:
            pass

    def destroy_node(self):
        self._stop_logging_and_calc_metrics()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = ExperimentLoggerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
