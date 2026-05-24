#!/usr/bin/env python3
import os
import sys
import csv
import math
import argparse
import numpy as np

def load_csv(csv_path):
    print(f"Reading {csv_path}...")
    data = {
        't': [],
        'hx': [], 'hy': [], 'hz': [],
        'px': [], 'py': [], 'pz': [],
        'rx': [], 'ry': [], 'rz': [],
        'tracked': []
    }
    
    with open(csv_path, 'r') as f:
        # Check if file has summary at the end
        lines = f.readlines()
        
    clean_lines = []
    for line in lines:
        if line.strip().startswith('='):
            # Reached summary lines, stop reading
            break
        clean_lines.append(line)
        
    reader = csv.DictReader(clean_lines)
    for row in reader:
        try:
            # Skip rows without timestamps or coordinates
            if not row['ros_timestamp_ns'] or not row['meas_x'] or not row['robot_ee_x']:
                continue
                
            t_sec = float(row['ros_timestamp_ns']) / 1e9
            
            data['t'].append(t_sec)
            data['hx'].append(float(row['meas_x']))
            data['hy'].append(float(row['meas_y']))
            data['hz'].append(float(row['meas_z']))
            
            # Predict values might be empty in ground_truth mode
            if row.get('pred_x'):
                data['px'].append(float(row['pred_x']))
                data['py'].append(float(row['pred_y']))
                data['pz'].append(float(row['pred_z']))
            else:
                data['px'].append(float(row['meas_x']))
                data['py'].append(float(row['meas_y']))
                data['pz'].append(float(row['meas_z']))
                
            data['rx'].append(float(row['robot_ee_x']))
            data['ry'].append(float(row['robot_ee_y']))
            data['rz'].append(float(row['robot_ee_z']))
            data['tracked'].append(row.get('is_tracked', 'True') == 'True')
        except (ValueError, KeyError) as e:
            continue
            
    # Convert lists to numpy arrays
    for key in data:
        data[key] = np.array(data[key])
        
    return data

def analyze_latency(data, plot_path=None):
    t = data['t']
    if len(t) < 10:
        print("Error: Too few samples in CSV file.")
        return
        
    # Subtract start time to start at 0
    t = t - t[0]
    
    # 1. Resample to uniform grid (e.g. 100 Hz, dt = 0.01s)
    dt = 0.01
    t_uniform = np.arange(t[0], t[-1], dt)
    
    hx_uni = np.interp(t_uniform, t, data['hx'])
    hy_uni = np.interp(t_uniform, t, data['hy'])
    hz_uni = np.interp(t_uniform, t, data['hz'])
    
    px_uni = np.interp(t_uniform, t, data['px'])
    py_uni = np.interp(t_uniform, t, data['py'])
    pz_uni = np.interp(t_uniform, t, data['pz'])
    
    rx_uni = np.interp(t_uniform, t, data['rx'])
    ry_uni = np.interp(t_uniform, t, data['ry'])
    rz_uni = np.interp(t_uniform, t, data['rz'])
    
    # 2. Compute velocities (more robust than positions for correlation)
    v_hand_x = np.diff(hx_uni) / dt
    v_hand_y = np.diff(hy_uni) / dt
    v_hand_z = np.diff(hz_uni) / dt
    v_hand = np.sqrt(v_hand_x**2 + v_hand_y**2 + v_hand_z**2)
    
    v_pred_x = np.diff(px_uni) / dt
    v_pred_y = np.diff(py_uni) / dt
    v_pred_z = np.diff(pz_uni) / dt
    v_pred = np.sqrt(v_pred_x**2 + v_pred_y**2 + v_pred_z**2)
    
    v_robot_x = np.diff(rx_uni) / dt
    v_robot_y = np.diff(ry_uni) / dt
    v_robot_z = np.diff(rz_uni) / dt
    v_robot = np.sqrt(v_robot_x**2 + v_robot_y**2 + v_robot_z**2)
    
    # We will run cross correlation on the velocity magnitudes
    # Normalize by subtracting mean and dividing by std
    v_hand_norm = (v_hand - np.mean(v_hand)) / (np.std(v_hand) + 1e-6)
    v_pred_norm = (v_pred - np.mean(v_pred)) / (np.std(v_pred) + 1e-6)
    v_robot_norm = (v_robot - np.mean(v_robot)) / (np.std(v_robot) + 1e-6)
    
    # Set search range for lag (up to 1.5 seconds)
    max_lag_sec = 1.5
    max_lag_samples = int(max_lag_sec / dt)
    lags = np.arange(-max_lag_samples, max_lag_samples + 1)
    
    # Measure Latency: Hand vs Robot
    corr_hand_robot = []
    for lag in lags:
        if lag > 0:
            h = v_hand_norm[:-lag]
            r = v_robot_norm[lag:]
        elif lag < 0:
            h = v_hand_norm[-lag:]
            r = v_robot_norm[:lag]
        else:
            h = v_hand_norm
            r = v_robot_norm
        corr_hand_robot.append(np.mean(h * r))
        
    best_idx_hr = np.argmax(corr_hand_robot)
    latency_hr_sec = lags[best_idx_hr] * dt
    max_corr_hr = corr_hand_robot[best_idx_hr]
    
    # Measure Latency: Hand vs Predictor
    corr_hand_pred = []
    for lag in lags:
        if lag > 0:
            h = v_hand_norm[:-lag]
            p = v_pred_norm[lag:]
        elif lag < 0:
            h = v_hand_norm[-lag:]
            p = v_pred_norm[:lag]
        else:
            h = v_hand_norm
            p = v_pred_norm
        corr_hand_pred.append(np.mean(h * p))
        
    best_idx_hp = np.argmax(corr_hand_pred)
    latency_hp_sec = lags[best_idx_hp] * dt
    max_corr_hp = corr_hand_pred[best_idx_hp]
    
    # Measure Latency: Predictor vs Robot
    corr_pred_robot = []
    for lag in lags:
        if lag > 0:
            p = v_pred_norm[:-lag]
            r = v_robot_norm[lag:]
        elif lag < 0:
            p = v_pred_norm[-lag:]
            r = v_robot_norm[:lag]
        else:
            p = v_pred_norm
            r = v_robot_norm
        corr_pred_robot.append(np.mean(p * r))
        
    best_idx_pr = np.argmax(corr_pred_robot)
    latency_pr_sec = lags[best_idx_pr] * dt
    max_corr_pr = corr_pred_robot[best_idx_pr]
    
    # ── Report Results ──
    print("\n" + "="*50)
    print("           LATENCY MEASUREMENT RESULTS")
    print("="*50)
    print(f"Total rows analyzed: {len(t)}")
    print(f"Sampling period (resampled): dt = {dt*1000:.0f} ms ({1/dt:.0f} Hz)")
    print("-"*50)
    print("1. Hand tracking to Robot physical movement (Total delay):")
    print(f"   ► Delay: {latency_hr_sec * 1000:.1f} ms")
    print(f"   ► Correlation: {max_corr_hr:.3f} (Values > 0.6 show solid motion alignment)")
    print("-"*50)
    print("2. Hand tracking to ML predictor output (Predictor phase shift):")
    if latency_hp_sec < 0:
        print(f"   ► Lead (Anticipation): {abs(latency_hp_sec) * 1000:.1f} ms (Predictor is successfully anticipating future hand positions)")
    else:
        print(f"   ► Lag (Delay): {latency_hp_sec * 1000:.1f} ms (Predictor is lagging behind raw inputs)")
    print(f"   ► Correlation: {max_corr_hp:.3f}")
    print("-"*50)
    print("3. ML Predictor to Robot physical movement:")
    print(f"   ► Delay: {latency_pr_sec * 1000:.1f} ms")
    print(f"   ► Correlation: {max_corr_pr:.3f}")
    print("="*50)
    
    # ── Visual Plotting ──
    try:
        import matplotlib.pyplot as plt
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # Plot velocities to show alignment
        time_axis = t_uniform[:-1]
        ax1.plot(time_axis, v_hand, label='Hand Velocity (Raw Tracked)', color='#1f77b4', alpha=0.8)
        ax1.plot(time_axis, v_pred, label='Predictor Velocity (Filtered)', color='#2ca02c', alpha=0.8)
        # Shift robot velocity back by computed lag to show visual alignment
        ax1.plot(time_axis - latency_hr_sec, v_robot, label=f'Robot Velocity (Shifted by -{latency_hr_sec*1000:.0f}ms)', color='#d62728', linestyle='--')
        
        ax1.set_title("Velocity Profiles and Alignment")
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("Speed (m/s)")
        ax1.legend()
        ax1.grid(True)
        
        # Plot cross correlation curve
        ax2.plot(lags * dt * 1000, corr_hand_robot, label='Hand vs Robot Correlation', color='#d62728')
        ax2.axvline(x=latency_hr_sec * 1000, color='#d62728', linestyle=':', label=f'Peak = {latency_hr_sec*1000:.1f} ms')
        
        ax2.set_title("Cross-Correlation vs Time Lag")
        ax2.set_xlabel("Lag / Shift (ms)")
        ax2.set_ylabel("Correlation Coefficient")
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        if plot_path:
            plt.savefig(plot_path)
            print(f"Saved alignment plot to: {plot_path}")
        else:
            plt.show()
            
    except ImportError:
        print("Note: matplotlib not installed. Skipping graphical plot visualization.")

def get_latest_csv(log_dir):
    if not os.path.exists(log_dir):
        return None
    files = [os.path.join(log_dir, f) for f in os.listdir(log_dir) if f.endswith('.csv')]
    if not files:
        return None
    # Sort by modification time
    return max(files, key=os.path.getmtime)

def main():
    parser = argparse.ArgumentParser(description="Calculate hand-to-robot physical latency from experiment log CSV files.")
    parser.add_argument("--csv", help="Path to specific CSV file. If omitted, uses latest file in log directory.")
    parser.add_argument("--dir", default=os.path.expanduser("~/cocarry_logs"), help="Logs directory to search in.")
    parser.add_argument("--plot", help="Save the plot to a file path (e.g. latency.png) instead of displaying it.")
    
    args = parser.parse_args()
    
    csv_file = args.csv
    if not csv_file:
        # Try both cocarry_logs and hrc_logs
        csv_file = get_latest_csv(args.dir)
        if not csv_file:
            csv_file = get_latest_csv(os.path.expanduser("~/hrc_logs"))
            
    if not csv_file or not os.path.exists(csv_file):
        print(f"Error: No CSV log files found. Please specify path with --csv.")
        sys.exit(1)
        
    data = load_csv(csv_file)
    analyze_latency(data, args.plot)

if __name__ == "__main__":
    main()
