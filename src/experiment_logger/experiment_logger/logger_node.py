#!/usr/bin/env python3
"""
Experiment Logger Node — subscribes to /hand_position and
/predicted_position, logs synchronized data to CSV for offline analysis.

Output CSV columns:
  ros_timestamp_ns, wall_time, trajectory_mode,
  meas_x, meas_y, meas_z, is_tracked,
  pred_x, pred_y, pred_z,
  mae_x, mae_y, mae_z,
  inference_ms, buffer_size,
  robot_ee_x, robot_ee_y, robot_ee_z

Author: Duy (auto-generated — extend as needed)
"""

import csv
import math
import os
import time
from datetime import datetime

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
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

        # Trajectory mode tracking
        self._trajectory_mode = 'ground_truth'  # default

        # Robot EE pose tracking (for jerk calculation)
        self._last_robot_ee = None  # (x, y, z)

        # Task timing
        self._start_wall_time = 0.0
        self._stop_wall_time = 0.0

        if self.is_logging:
            self._start_logging()

        # Latest data (quick-and-dirty sync: log on each prediction)
        self.last_meas = None

        # Subscribers
        self.create_subscription(HandState, '/hand_position', self._on_hand, 10)
        self.create_subscription(HandPrediction, '/ml/predicted_position', self._on_prediction, 10)
        # Stop command from bridge (scenario_id string from Windows)
        self.create_subscription(String, '/bridge/stop_command', self._on_stop_command, 5)
        # Trajectory mode from UI
        self.create_subscription(String, '/trajectory_mode', self._on_trajectory_mode, 10)
        # Robot EE pose from cartesian_streamer (for jerk calculation)
        self.create_subscription(
            PoseStamped, '/cartesian_streamer/current_pose',
            self._on_robot_ee_pose, 10)

        # Service to toggle recording
        self.toggle_srv = self.create_service(SetBool, '/logger/toggle', self._srv_toggle)

        # Flush timer
        self.create_timer(5.0, self._flush)

        self.get_logger().info('Logger ready.')

    def _start_logging(self):
        try:
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            # Dùng model name hoặc GROUND_TRUTH tùy mode
            if self._trajectory_mode == 'ground_truth':
                model_tag = 'GROUND_TRUTH'
            else:
                model_tag = str(self.current_model).upper() if self.current_model else "UNKNOWN"
            self.csv_path = os.path.join(self.log_dir, f'experiment_{model_tag}_{ts}.csv')
            
            self.get_logger().info(f'Attempting to open CSV file: {self.csv_path}')
            
            # Ensure directory exists once more
            os.makedirs(self.log_dir, exist_ok=True)
            
            self.csv_file = open(self.csv_path, 'w', newline='')
            self.csv_writer = csv.writer(self.csv_file)
            self.csv_writer.writerow([
                'ros_timestamp_ns', 'wall_time', 'trajectory_mode',
                'meas_x', 'meas_y', 'meas_z', 'is_tracked',
                'pred_x', 'pred_y', 'pred_z',
                'mae_x', 'mae_y', 'mae_z',
                'inference_ms', 'buffer_size',
                'robot_ee_x', 'robot_ee_y', 'robot_ee_z'
            ])
            self.csv_file.flush()
            self.row_count = 0
            self._start_wall_time = time.time()
            self.get_logger().info(f'✓ SUCCESSFULLY started logging to {self.csv_path}')
        except Exception as e:
            self.get_logger().error(f'✗ FAILED to start logging: {e}')
            self.is_logging = False
            self.csv_file = None
            self.csv_writer = None

    def _stop_logging_and_calc_metrics(self):
        self._stop_wall_time = time.time()
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
        self._stop_wall_time = time.time()
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

    def _on_trajectory_mode(self, msg: String):
        """Nhận chế độ trajectory từ UI."""
        self._trajectory_mode = msg.data
        self.get_logger().info(f'Trajectory mode: {self._trajectory_mode}')

    def _on_robot_ee_pose(self, msg: PoseStamped):
        """Lưu vị trí EE hiện tại của robot (dùng cho jerk calculation)."""
        self._last_robot_ee = (
            msg.pose.position.x,
            msg.pose.position.y,
            msg.pose.position.z,
        )

    def _on_hand(self, msg: HandState):
        self.last_meas = msg
        # Ở ground_truth mode: ghi row ngay từ hand data (không cần chờ prediction)
        if (self._trajectory_mode == 'ground_truth'
                and self.is_logging
                and self.csv_writer is not None):
            self._write_row(msg, None)

    def _on_prediction(self, msg: HandPrediction):
        new_model = msg.model_name
        
        # If we were logging with "UNKNOWN" and now know the model, rename the file
        if self.is_logging and self.csv_file and self.current_model.lower() == 'unknown':
            if new_model.lower() != 'unknown':
                self._rename_current_log(new_model)

        self.current_model = new_model
        # Ở prediction mode: ghi row khi nhận prediction
        if (self._trajectory_mode == 'prediction'
                and self.is_logging
                and self.csv_writer is not None):
            self._write_row(self.last_meas, msg)

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

        # Robot EE pose
        rex = rey = rez = ''
        if self._last_robot_ee is not None:
            rex = f'{self._last_robot_ee[0]:.6f}'
            rey = f'{self._last_robot_ee[1]:.6f}'
            rez = f'{self._last_robot_ee[2]:.6f}'

        self.csv_writer.writerow([
            now_ns, wall, self._trajectory_mode,
            mx, my, mz, tracked,
            px, py, pz, mae_x, mae_y, mae_z,
            inf_ms, buf,
            rex, rey, rez
        ])
        self.row_count += 1

    def _calculate_metrics(self, csv_file_path):
        try:
            with open(csv_file_path, 'r') as f:
                reader = csv.DictReader(f)
                total_inference = 0.0
                total_mse = 0.0
                total_error = 0.0
                total_error_x = 0.0
                total_error_y = 0.0
                total_error_z = 0.0
                pred_count = 0

                # Robot EE trajectory for jerk calculation
                ee_positions = []  # list of (wall_time_str, x, y, z)

                for row in reader:
                    # Collect robot EE positions for jerk
                    try:
                        rex = float(row['robot_ee_x'])
                        rey = float(row['robot_ee_y'])
                        rez = float(row['robot_ee_z'])
                        wt = row['wall_time']
                        ee_positions.append((wt, rex, rey, rez))
                    except (ValueError, KeyError):
                        pass

                    # Prediction metrics (only for prediction mode rows)
                    try:
                        inf_ms = float(row['inference_ms'])
                        mx = float(row['meas_x'])
                        my = float(row['meas_y'])
                        mz = float(row['meas_z'])
                        px_val = float(row['pred_x'])
                        py_val = float(row['pred_y'])
                        pz_val = float(row['pred_z'])
                        total_inference += inf_ms
                        ex = px_val - mx
                        ey = py_val - my
                        ez = pz_val - mz
                        
                        # Mean Squared Error (MSE)
                        dist_sq = ex*ex + ey*ey + ez*ez
                        total_mse += dist_sq
                        
                        # Mean Absolute Error (MAE)
                        dist = math.sqrt(dist_sq)
                        total_error += dist
                        total_error_x += abs(ex)
                        total_error_y += abs(ey)
                        total_error_z += abs(ez)
                        pred_count += 1
                    except (ValueError, KeyError):
                        pass

                # ── Task completion time ──
                task_time = self._stop_wall_time - self._start_wall_time

                # ── Jerk from robot EE trajectory ──
                jerk_result = self._compute_jerk(ee_positions)

                # ── Build summary ──
                summary_lines = [
                    f"\n{'='*60}",
                    f"EXPERIMENT METRICS",
                    f"  File: {os.path.basename(csv_file_path)}",
                    f"  Total samples: {len(ee_positions)}",
                    f"  Task completion time: {task_time:.2f} s",
                ]

                if pred_count > 0:
                    avg_inf = total_inference / pred_count
                    avg_mse = total_mse / pred_count
                    avg_mae = total_error / pred_count
                    avg_x = total_error_x / pred_count
                    avg_y = total_error_y / pred_count
                    avg_z = total_error_z / pred_count

                    summary_lines += [
                        f"  --- Prediction Accuracy (over {pred_count} samples) ---",
                        f"  Avg Inference Time: {avg_inf:.2f} ms",
                        f"  Mean Squared Error (MSE): {avg_mse:.6f} m²",
                        f"  Mean Absolute Error (MAE - 3D): {avg_mae:.4f} m",
                        f"      MAE X: {avg_x:.4f} m",
                        f"      MAE Y: {avg_y:.4f} m",
                        f"      MAE Z: {avg_z:.4f} m",
                    ]
                else:
                    summary_lines.append(
                        "  Mode: GROUND TRUTH (no prediction metrics)")

                if jerk_result:
                    summary_lines += [
                        f"  --- Trajectory Smoothness (Robot EE) ---",
                        f"  Mean Jerk (3D): {jerk_result['mean_jerk_3d']:.4f} m/s³",
                        f"      Jerk X: {jerk_result['mean_jerk_x']:.4f} m/s³",
                        f"      Jerk Y: {jerk_result['mean_jerk_y']:.4f} m/s³",
                        f"      Jerk Z: {jerk_result['mean_jerk_z']:.4f} m/s³",
                        f"  Max Jerk (3D): {jerk_result['max_jerk_3d']:.4f} m/s³",
                        f"  RMS Jerk (3D): {jerk_result['rms_jerk_3d']:.4f} m/s³",
                    ]
                else:
                    summary_lines.append(
                        "  Jerk: insufficient EE data for calculation")

                summary_lines.append(f"{'='*60}")
                summary = '\n'.join(summary_lines)
                self.get_logger().info(summary)
                
                # Also append to the CSV file
                with open(csv_file_path, 'a') as f:
                    f.write("\n" + summary + "\n")

        except Exception as e:
            self.get_logger().error(f"Failed to calculate metrics: {e}")

    def _compute_jerk(self, ee_positions):
        """
        Compute jerk from robot EE trajectory.
        
        Jerk = d³position/dt³ (m/s³)
        Uses finite differences: jerk = Δacceleration / Δt

        Args:
            ee_positions: list of (wall_time_iso_str, x, y, z)

        Returns:
            dict with mean/max/rms jerk values, or None if insufficient data
        """
        if len(ee_positions) < 4:
            return None

        # Parse timestamps
        timestamps = []
        positions = []  # list of (x, y, z)
        for wt_str, x, y, z in ee_positions:
            try:
                dt_obj = datetime.fromisoformat(wt_str)
                timestamps.append(dt_obj.timestamp())
                positions.append((x, y, z))
            except (ValueError, TypeError):
                continue

        if len(timestamps) < 4:
            return None

        # Compute velocity: v[i] = (pos[i+1] - pos[i]) / (t[i+1] - t[i])
        velocities = []
        vel_times = []
        for i in range(len(positions) - 1):
            dt = timestamps[i + 1] - timestamps[i]
            if dt <= 0:
                continue
            vx = (positions[i + 1][0] - positions[i][0]) / dt
            vy = (positions[i + 1][1] - positions[i][1]) / dt
            vz = (positions[i + 1][2] - positions[i][2]) / dt
            velocities.append((vx, vy, vz))
            vel_times.append((timestamps[i] + timestamps[i + 1]) / 2.0)

        if len(velocities) < 3:
            return None

        # Compute acceleration: a[i] = (v[i+1] - v[i]) / (t[i+1] - t[i])
        accelerations = []
        acc_times = []
        for i in range(len(velocities) - 1):
            dt = vel_times[i + 1] - vel_times[i]
            if dt <= 0:
                continue
            ax = (velocities[i + 1][0] - velocities[i][0]) / dt
            ay = (velocities[i + 1][1] - velocities[i][1]) / dt
            az = (velocities[i + 1][2] - velocities[i][2]) / dt
            accelerations.append((ax, ay, az))
            acc_times.append((vel_times[i] + vel_times[i + 1]) / 2.0)

        if len(accelerations) < 2:
            return None

        # Compute jerk: j[i] = (a[i+1] - a[i]) / (t[i+1] - t[i])
        jerks_x = []
        jerks_y = []
        jerks_z = []
        jerks_3d = []
        for i in range(len(accelerations) - 1):
            dt = acc_times[i + 1] - acc_times[i]
            if dt <= 0:
                continue
            jx = (accelerations[i + 1][0] - accelerations[i][0]) / dt
            jy = (accelerations[i + 1][1] - accelerations[i][1]) / dt
            jz = (accelerations[i + 1][2] - accelerations[i][2]) / dt
            j3d = math.sqrt(jx * jx + jy * jy + jz * jz)
            jerks_x.append(abs(jx))
            jerks_y.append(abs(jy))
            jerks_z.append(abs(jz))
            jerks_3d.append(j3d)

        if len(jerks_3d) == 0:
            return None

        n = len(jerks_3d)
        return {
            'mean_jerk_x': sum(jerks_x) / n,
            'mean_jerk_y': sum(jerks_y) / n,
            'mean_jerk_z': sum(jerks_z) / n,
            'mean_jerk_3d': sum(jerks_3d) / n,
            'max_jerk_3d': max(jerks_3d),
            'rms_jerk_3d': math.sqrt(sum(j * j for j in jerks_3d) / n),
        }

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
