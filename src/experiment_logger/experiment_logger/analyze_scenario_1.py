#!/usr/bin/env python3
"""
analyze_scenario_1.py
Phân tích Kịch bản 1: Độ trễ và Độ ổn định (Latency & Stability)

Đọc file CSV và vẽ đồ thị so sánh Vị trí (Position) và Vận tốc (Velocity)
của Tay người (Hand Base) và Robot End-Effector (Robot EE) theo thời gian.
Giúp trực quan hóa độ trễ pha (phase delay) giữa Baseline 1 và Baseline 2/3.
"""

import os
import sys
import csv
import argparse
import numpy as np
import matplotlib.pyplot as plt

def load_csv_data(csv_path):
    print(f"Reading {csv_path}...")
    data = {'t': [], 'hx': [], 'rx': [], 'hv': [], 'rv': []}
    
    with open(csv_path, 'r') as f:
        lines = f.readlines()
        
    clean_lines = [l for l in lines if not l.strip().startswith('=')]
    reader = csv.DictReader(clean_lines)
    
    for row in reader:
        try:
            if not row['ros_timestamp_ns'] or not row['hand_base_x'] or not row['robot_ee_x']:
                continue
                
            t_sec = float(row['ros_timestamp_ns']) / 1e9
            data['t'].append(t_sec)
            data['hx'].append(float(row['hand_base_x']))
            data['rx'].append(float(row['robot_ee_x']))
            data['hv'].append(float(row['hand_vel_x']))
            data['rv'].append(float(row['ee_vel_x']))
        except (ValueError, KeyError):
            continue
            
    for k in data:
        data[k] = np.array(data[k])
    
    if len(data['t']) > 0:
        data['t'] = data['t'] - data['t'][0]  # Normalize time to start at 0
        
    return data

def moving_average(signal, window_size):
    if window_size < 2: return signal
    return np.convolve(signal, np.ones(window_size)/window_size, mode='same')

def analyze_and_plot(csv_file):
    data = load_csv_data(csv_file)
    if len(data['t']) == 0:
        print("Lỗi: Không tìm thấy dữ liệu trong file CSV.")
        return

    # Lọc mượt (smooth) vận tốc để dễ nhìn
    window = 10
    hv_smooth = moving_average(data['hv'], window)
    rv_smooth = moving_average(data['rv'], window)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    mode_name = "Unknown Mode"
    if "ground_truth" in csv_file.lower() or "baseline1" in csv_file.lower():
        mode_name = "Baseline 1 (Ground Truth)"
    elif "predict" in csv_file.lower() or "baseline2" in csv_file.lower():
        mode_name = "Baseline 2 (Prediction Only)"
    elif "ergonomic" in csv_file.lower() or "baseline3" in csv_file.lower() or "proposed" in csv_file.lower():
        mode_name = "Baseline 3 (Proposed System)"

    fig.suptitle(f"Kịch Bản 1: Phân Tích Độ Trễ (Latency) - {mode_name}", fontsize=16)

    # 1. Đồ thị Vị trí (Position)
    ax1.plot(data['t'], data['hx'], label='Hand Base X', color='blue', linewidth=2)
    ax1.plot(data['t'], data['rx'], label='Robot EE X', color='red', linestyle='--', linewidth=2)
    ax1.set_ylabel('Vị trí X (m)')
    ax1.set_title('So sánh Vị trí (Hand vs Robot)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. Đồ thị Vận tốc (Velocity)
    ax2.plot(data['t'], hv_smooth, label='Hand Velocity X (Smoothed)', color='blue', alpha=0.7)
    ax2.plot(data['t'], rv_smooth, label='Robot Velocity X (Smoothed)', color='red', alpha=0.7)
    ax2.set_xlabel('Thời gian (s)')
    ax2.set_ylabel('Vận tốc (m/s)')
    ax2.set_title('So sánh Vận tốc để đo Pha trễ (Phase Delay)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Phân tích Kịch bản 1: Độ trễ")
    parser.add_argument("csv_file", help="Đường dẫn tới file CSV")
    args = parser.parse_args()
    
    if os.path.exists(args.csv_file):
        analyze_and_plot(args.csv_file)
    else:
        print(f"Không tìm thấy file: {args.csv_file}")
