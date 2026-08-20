#!/usr/bin/env python3
"""
analyze_scenario_2.py
═════════════════════
Kịch bản 2: Phân tích an toàn khi giật tay đột ngột (Sudden Jerk Safety)

Mục tiêu: Chứng minh Proposed System (Ergonomics) giữ robot mượt mà
trong khi Ground Truth và GRU cho robot vọt theo nguy hiểm.

Đầu vào: Thư mục chứa các file CSV thu được từ 3 baseline x N trials.
Đầu ra:  4 figure phân tích + bảng thống kê tóm tắt.

Usage:
    python3 analyze_scenario_2.py /path/to/Scenario_2/
"""

import os
import sys
import csv
import glob
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# ── Cấu hình ────────────────────────────────────────────────────────
BASELINE_MAP = {
    'GROUND_TRUTH': {'label': 'Baseline 1\n(Camera Only)',   'color': '#e74c3c', 'short': 'GT'},
    'GRU':          {'label': 'Baseline 2\n(+ GRU Predict)', 'color': '#f39c12', 'short': 'GRU'},
    'ERGONOMICS':   {'label': 'Proposed System\n(Full Framework)', 'color': '#2ecc71', 'short': 'Proposed'},
}
SMOOTH_WINDOW = 3  # moving average window cho velocity/jerk


# ══════════════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════════════

def load_trial(csv_path: str) -> dict:
    """Load 1 file CSV trial, trả về dict các numpy arrays."""
    with open(csv_path, 'r') as f:
        lines = [l for l in f.readlines() if not l.strip().startswith('=')]
    reader = csv.DictReader(lines)

    cols = {
        't': [], 'hz': [], 'rz': [],
        'hspd': [], 'espd': [],
        'w': [], 'sr': [], 'se': [],
    }

    for row in reader:
        try:
            if not row.get('ros_timestamp_ns'):
                continue
            cols['t'].append(float(row['ros_timestamp_ns']) / 1e9)
            cols['hz'].append(float(row.get('hand_base_z', '') or 'nan'))
            cols['rz'].append(float(row.get('robot_ee_z', '') or 'nan'))
            cols['hspd'].append(float(row.get('hand_speed', '') or '0'))
            cols['espd'].append(float(row.get('ee_speed', '') or '0'))
            try:
                cols['w'].append(float(row.get('adapt_w', '') or '1'))
                cols['sr'].append(float(row.get('adapt_sr', '') or '1'))
                cols['se'].append(float(row.get('adapt_se', '') or '1'))
            except ValueError:
                cols['w'].append(1.0)
                cols['sr'].append(1.0)
                cols['se'].append(1.0)
        except (ValueError, KeyError):
            continue

    data = {k: np.array(v) for k, v in cols.items()}
    if len(data['t']) > 1:
        data['t'] -= data['t'][0]
    return data


def moving_average(signal, window):
    if window < 2 or len(signal) < window:
        return signal
    return np.convolve(signal, np.ones(window) / window, mode='same')


def compute_jerk_from_speed(speed, time):
    """Jerk = d(acceleration)/dt = d²(speed)/dt²"""
    dt = np.diff(time)
    dt[dt == 0] = np.mean(dt[dt > 0]) if np.any(dt > 0) else 0.001

    accel = np.diff(speed) / dt
    accel = np.insert(accel, 0, accel[0])

    dt2 = np.diff(time)
    dt2[dt2 == 0] = np.mean(dt2[dt2 > 0]) if np.any(dt2 > 0) else 0.001
    jerk = np.diff(accel) / dt2
    jerk = np.insert(jerk, 0, jerk[0])

    return moving_average(np.abs(jerk), SMOOTH_WINDOW)


def compute_velocity_z(pos_z, time):
    """Velocity trên trục Z (trục giật tay)."""
    dt = np.diff(time)
    dt[dt == 0] = np.mean(dt[dt > 0]) if np.any(dt > 0) else 0.001
    vz = np.diff(pos_z) / dt
    vz = np.insert(vz, 0, vz[0])
    return vz


def load_all_trials(data_dir: str) -> dict:
    """Load tất cả trials theo baseline."""
    result = {}
    for mode in BASELINE_MAP:
        pattern = os.path.join(data_dir, f'experiment_{mode}_*.csv')
        files = sorted(glob.glob(pattern))
        trials = []
        for f in files:
            d = load_trial(f)
            if len(d['t']) > 20:
                trials.append(d)
        result[mode] = trials
        print(f'  {mode}: {len(trials)} trials loaded')
    return result


# ══════════════════════════════════════════════════════════════════════
# METRICS
# ══════════════════════════════════════════════════════════════════════

def compute_trial_metrics(data: dict) -> dict:
    """Tính các chỉ số an toàn cho 1 trial."""
    hand_jerk = compute_jerk_from_speed(data['hspd'], data['t'])
    robot_jerk = compute_jerk_from_speed(data['espd'], data['t'])

    robot_vz = compute_velocity_z(data['rz'], data['t'])

    mean_h_jerk = np.nanmean(hand_jerk)
    mean_r_jerk = np.nanmean(robot_jerk)
    jerk_ratio = mean_r_jerk / mean_h_jerk if mean_h_jerk > 1e-6 else 0.0

    return {
        'peak_robot_vel_z': np.nanmax(np.abs(robot_vz)),
        'peak_robot_jerk': np.nanmax(robot_jerk),
        'mean_robot_jerk': mean_r_jerk,
        'mean_hand_jerk': mean_h_jerk,
        'jerk_ratio': jerk_ratio,
        'peak_robot_speed': np.nanmax(data['espd']),
        # Time-series cho đồ thị
        '_hand_jerk': hand_jerk,
        '_robot_jerk': robot_jerk,
        '_robot_vz': robot_vz,
    }


# ══════════════════════════════════════════════════════════════════════
# FIGURES
# ══════════════════════════════════════════════════════════════════════

def fig1_representative_position(all_data: dict, save_dir: str):
    """
    Figure 1: Overlay Position Z — 1 trial đại diện mỗi baseline.
    Hand Z (dashed) vs Robot Z (solid) để thấy GT/GRU bám sát, Ergo bị hãm.
    """
    fig, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=False)
    fig.suptitle('Scenario 2: Position Response during Sudden Jerk', fontsize=16, fontweight='bold')

    for idx, mode in enumerate(BASELINE_MAP):
        ax = axes[idx]
        cfg = BASELINE_MAP[mode]
        trial = all_data[mode][0]  # trial đầu tiên

        ax.plot(trial['t'], trial['hz'], '--', color='#3498db', linewidth=1.5, label='Hand Z', alpha=0.8)
        ax.plot(trial['t'], trial['rz'], '-', color=cfg['color'], linewidth=2, label='Robot EE Z')
        ax.set_ylabel('Position Z (m)', fontsize=11)
        ax.set_title(cfg['label'].replace('\n', ' — '), fontsize=12, fontweight='bold', color=cfg['color'])
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_xlim([0, trial['t'][-1]])

    axes[-1].set_xlabel('Time (s)', fontsize=12)
    plt.tight_layout()
    path = os.path.join(save_dir, 'fig1_position_response.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    print(f'  Saved: {path}')
    plt.close()


def fig2_representative_velocity(all_data: dict, save_dir: str):
    """
    Figure 2: Overlay Velocity Z — Robot velocity trên trục giật.
    Thể hiện GT/GRU có peak rất cao, Ergonomics bị dập.
    """
    fig, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=False)
    fig.suptitle('Scenario 2: Robot Velocity Response on Z-axis', fontsize=16, fontweight='bold')

    for idx, mode in enumerate(BASELINE_MAP):
        ax = axes[idx]
        cfg = BASELINE_MAP[mode]
        trial = all_data[mode][0]

        hand_vz = moving_average(compute_velocity_z(trial['hz'], trial['t']), SMOOTH_WINDOW)
        robot_vz = moving_average(compute_velocity_z(trial['rz'], trial['t']), SMOOTH_WINDOW)

        ax.plot(trial['t'], hand_vz, '--', color='#3498db', linewidth=1.2, label='Hand Vel Z', alpha=0.7)
        ax.plot(trial['t'], robot_vz, '-', color=cfg['color'], linewidth=2, label='Robot Vel Z')
        ax.axhline(y=0, color='gray', linewidth=0.5, linestyle='-')
        ax.set_ylabel('Velocity Z (m/s)', fontsize=11)
        ax.set_title(cfg['label'].replace('\n', ' — '), fontsize=12, fontweight='bold', color=cfg['color'])
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_xlim([0, trial['t'][-1]])

    axes[-1].set_xlabel('Time (s)', fontsize=12)
    plt.tight_layout()
    path = os.path.join(save_dir, 'fig2_velocity_response.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    print(f'  Saved: {path}')
    plt.close()


def fig3_boxplot_comparison(all_data: dict, save_dir: str):
    """
    Figure 3: Box-plot thống kê trên N trials.
    3 subplot: Peak Robot Velocity Z | Mean Robot Jerk | Jerk Attenuation Ratio
    """
    # Tính metrics cho tất cả trials
    metrics_by_mode = {}
    for mode in BASELINE_MAP:
        metrics_list = [compute_trial_metrics(t) for t in all_data[mode]]
        metrics_by_mode[mode] = metrics_list

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    fig.suptitle('Scenario 2: Statistical Comparison (N=5 trials per baseline)',
                 fontsize=14, fontweight='bold')

    metric_keys = [
        ('peak_robot_vel_z', 'Peak Robot |Velocity Z|\n(m/s)', 'Lower is safer'),
        ('mean_robot_jerk',  'Mean Robot Jerk\n(m/s³)', 'Lower is smoother'),
        ('jerk_ratio',       'Jerk Transfer Ratio\n(Robot/Hand)', 'Lower is better'),
    ]

    for ax_idx, (key, ylabel, note) in enumerate(metric_keys):
        ax = axes[ax_idx]
        box_data = []
        labels = []
        colors = []

        for mode in BASELINE_MAP:
            cfg = BASELINE_MAP[mode]
            values = [m[key] for m in metrics_by_mode[mode]]
            box_data.append(values)
            labels.append(cfg['short'])
            colors.append(cfg['color'])

        bp = ax.boxplot(box_data, labels=labels, patch_artist=True, widths=0.5,
                        medianprops=dict(color='black', linewidth=2))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        # Thêm scatter points
        for i, (vals, color) in enumerate(zip(box_data, colors)):
            x = np.random.normal(i + 1, 0.04, size=len(vals))
            ax.scatter(x, vals, color=color, edgecolors='black', s=40, zorder=5, alpha=0.8)

        ax.set_ylabel(ylabel, fontsize=10)
        ax.set_title(note, fontsize=9, fontstyle='italic', color='gray')
        ax.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
    path = os.path.join(save_dir, 'fig3_boxplot_comparison.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    print(f'  Saved: {path}')
    plt.close()

    # In bảng thống kê text
    print('\n' + '=' * 75)
    print(f'{"Metric":<28} {"GT (μ±σ)":<20} {"GRU (μ±σ)":<20} {"Proposed (μ±σ)"}')
    print('=' * 75)
    for key, ylabel, _ in metric_keys:
        vals = {}
        for mode in BASELINE_MAP:
            v = [m[key] for m in metrics_by_mode[mode]]
            vals[mode] = (np.mean(v), np.std(v))
        short_label = ylabel.split('\n')[0]
        print(f'{short_label:<28} '
              f'{vals["GROUND_TRUTH"][0]:>7.3f}±{vals["GROUND_TRUTH"][1]:.3f}   '
              f'{vals["GRU"][0]:>7.3f}±{vals["GRU"][1]:.3f}   '
              f'{vals["ERGONOMICS"][0]:>7.3f}±{vals["ERGONOMICS"][1]:.3f}')
    print('=' * 75)


def fig4_adaptive_weights(all_data: dict, save_dir: str):
    """
    Figure 4: Diễn biến Adaptive Weights (w, sr, se) theo thời gian.
    Chỉ vẽ cho Ergonomics mode, overlay lên velocity Z.
    """
    trial = all_data['ERGONOMICS'][0]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True)
    fig.suptitle('Scenario 2: Adaptive Control Response (Proposed System)',
                 fontsize=14, fontweight='bold')

    # Top: Position Z
    robot_vz = moving_average(compute_velocity_z(trial['rz'], trial['t']), SMOOTH_WINDOW)
    hand_vz = moving_average(compute_velocity_z(trial['hz'], trial['t']), SMOOTH_WINDOW)
    ax1.plot(trial['t'], hand_vz, '--', color='#3498db', linewidth=1.2, label='Hand Vel Z', alpha=0.7)
    ax1.plot(trial['t'], robot_vz, '-', color='#2ecc71', linewidth=2, label='Robot Vel Z')
    ax1.axhline(y=0, color='gray', linewidth=0.5)
    ax1.set_ylabel('Velocity Z (m/s)', fontsize=11)
    ax1.set_title('Robot velocity bị kìm hãm khi tay giật', fontsize=11)
    ax1.legend(loc='upper right', fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Bottom: Adaptive weights
    ax2.plot(trial['t'], trial['w'], '-', color='#9b59b6', linewidth=2, label='w (Adaptive Weight)')
    ax2.plot(trial['t'], trial['sr'], '--', color='#e67e22', linewidth=1.5, label='$s_r$ (Prediction Reliability)')
    ax2.plot(trial['t'], trial['se'], ':', color='#1abc9c', linewidth=1.5, label='$s_e$ (Ergonomic Comfort)')
    ax2.set_xlabel('Time (s)', fontsize=12)
    ax2.set_ylabel('Weight Value', fontsize=11)
    ax2.set_ylim([-0.05, 1.15])
    ax2.set_title('Adaptive weights giảm khi phát hiện chuyển động giật cục', fontsize=11)
    ax2.legend(loc='lower right', fontsize=9)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    path = os.path.join(save_dir, 'fig4_adaptive_weights.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    print(f'  Saved: {path}')
    plt.close()


# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='Phân tích Kịch bản 2: Sudden Jerk Safety')
    parser.add_argument('data_dir',
                        help='Thư mục chứa các file CSV Scenario 2')
    parser.add_argument('--save-dir', default=None,
                        help='Thư mục lưu ảnh (mặc định: cùng data_dir)')
    args = parser.parse_args()

    save_dir = args.save_dir or args.data_dir
    os.makedirs(save_dir, exist_ok=True)

    print('Loading data...')
    all_data = load_all_trials(args.data_dir)

    # Kiểm tra đủ data
    for mode in BASELINE_MAP:
        if len(all_data[mode]) == 0:
            print(f'ERROR: Không tìm thấy trial nào cho {mode}!')
            return

    print('\nGenerating figures...')
    fig1_representative_position(all_data, save_dir)
    fig2_representative_velocity(all_data, save_dir)
    fig3_boxplot_comparison(all_data, save_dir)
    fig4_adaptive_weights(all_data, save_dir)

    print('\n✓ Hoàn tất phân tích Kịch bản 2!')


if __name__ == '__main__':
    main()
