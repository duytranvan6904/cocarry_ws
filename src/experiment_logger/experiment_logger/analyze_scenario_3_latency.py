#!/usr/bin/env python3
"""
analyze_scenario_3_latency.py
═════════════════════════════
Scenario 3 Analysis: System Latency, Trajectory Tracking & GRU Prediction

Objectives:
- Quantify phase lag, position tracking RMSE, prediction accuracy (MAE), and inference time.
- Combine multi-participant trial data (Duy & Hung, N=20 trials/baseline).
- Perform statistical hypothesis testing (Welch's t-test).
- Generate publication figures and a formatted LaTeX table.

Usage:
    python3 analyze_scenario_3_latency.py /home/duy/cocarry_ws/cocarry_logs/Scenario_3/
"""

import os
import sys
import csv
import glob
import argparse
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

BASELINE_MAP = {
    'GROUND_TRUTH': {'label': 'Baseline 1\n(Camera Only)',   'color': '#e74c3c', 'short': 'GT'},
    'GRU':          {'label': 'Baseline 2\n(+ GRU Predict)', 'color': '#f39c12', 'short': 'GRU'},
    'ERGONOMICS':   {'label': 'Proposed System\n(Adaptive Framework)', 'color': '#2ecc71', 'short': 'Proposed'},
}
SMOOTH_WINDOW = 5


def load_trial(csv_path: str) -> dict:
    """Load a single trial CSV and extract trajectory telemetry."""
    with open(csv_path, 'r') as f:
        lines = [l for l in f.readlines() if not l.strip().startswith('=')]
    reader = csv.DictReader(lines)

    cols = {
        't': [], 'hx': [], 'hy': [], 'hz': [],
        'rx': [], 'ry': [], 'rz': [],
        'mx': [], 'my': [], 'mz': [],
        'px': [], 'py': [], 'pz': [],
        'maex': [], 'maey': [], 'maez': [],
        'hspd': [], 'espd': [], 'inf_ms': [],
    }

    for row in reader:
        try:
            if not row.get('ros_timestamp_ns'):
                continue
            cols['t'].append(float(row['ros_timestamp_ns']) / 1e9)
            cols['hx'].append(float(row.get('hand_base_x', '') or 'nan'))
            cols['hy'].append(float(row.get('hand_base_y', '') or 'nan'))
            cols['hz'].append(float(row.get('hand_base_z', '') or 'nan'))
            cols['rx'].append(float(row.get('robot_ee_x', '') or 'nan'))
            cols['ry'].append(float(row.get('robot_ee_y', '') or 'nan'))
            cols['rz'].append(float(row.get('robot_ee_z', '') or 'nan'))
            cols['mx'].append(float(row.get('meas_x', '') or 'nan'))
            cols['my'].append(float(row.get('meas_y', '') or 'nan'))
            cols['mz'].append(float(row.get('meas_z', '') or 'nan'))
            cols['px'].append(float(row.get('pred_x', '') or 'nan'))
            cols['py'].append(float(row.get('pred_y', '') or 'nan'))
            cols['pz'].append(float(row.get('pred_z', '') or 'nan'))
            cols['maex'].append(float(row.get('mae_x', '') or 'nan'))
            cols['maey'].append(float(row.get('mae_y', '') or 'nan'))
            cols['maez'].append(float(row.get('mae_z', '') or 'nan'))
            cols['hspd'].append(float(row.get('hand_speed', '') or '0'))
            cols['espd'].append(float(row.get('ee_speed', '') or '0'))
            cols['inf_ms'].append(float(row.get('inference_ms', '') or 'nan'))
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


def load_all_scenario3_trials(data_dir: str) -> dict:
    """Load all trials recursively across participants (Duy, Hung)."""
    result = {}
    for mode in BASELINE_MAP:
        pattern = os.path.join(data_dir, '**', f'experiment_{mode}_*.csv')
        files = sorted(glob.glob(pattern, recursive=True))
        trials = []
        for f in files:
            d = load_trial(f)
            if len(d['t']) > 30:
                trials.append(d)
        result[mode] = trials
        print(f'  {mode}: {len(trials)} trials loaded across participants')
    return result


def compute_meas_speed(data: dict):
    t = data['t']
    if len(t) < 2:
        return np.zeros_like(t)
    dt = np.diff(t)
    dt[dt <= 0] = 0.02
    dmx = np.diff(data['mx']) / dt
    dmy = np.diff(data['my']) / dt
    dmz = np.diff(data['mz']) / dt
    meas_speed = np.sqrt(dmx**2 + dmy**2 + dmz**2)
    meas_speed = np.pad(meas_speed, (0, 1), mode='edge')
    return moving_average(meas_speed, SMOOTH_WINDOW)


def compute_ee_speed(data: dict):
    t = data['t']
    if len(t) < 2:
        return np.zeros_like(t)
    dt = np.diff(t)
    dt[dt <= 0] = 0.02
    drx = np.diff(data['rx']) / dt
    dry = np.diff(data['ry']) / dt
    drz = np.diff(data['rz']) / dt
    ee_speed = np.sqrt(drx**2 + dry**2 + drz**2)
    ee_speed = np.pad(ee_speed, (0, 1), mode='edge')
    return moving_average(ee_speed, SMOOTH_WINDOW)


def compute_phase_lag_ms(hand_speed, robot_speed, time):
    """Estimate phase delay (ms) using cross-correlation peak lag."""
    if len(time) < 10:
        return 0.0
    dt_mean = np.mean(np.diff(time))
    if dt_mean <= 0:
        return 0.0

    s1 = hand_speed - np.mean(hand_speed)
    s2 = robot_speed - np.mean(robot_speed)

    corr = np.correlate(s1, s2, mode='full')
    lags = np.arange(-len(s1) + 1, len(s1))
    best_lag = lags[np.argmax(corr)]
    
    # Phase lag in milliseconds (positive means robot lags behind hand)
    phase_lag = -best_lag * dt_mean * 1000.0
    return max(0.0, phase_lag)


def compute_trial_latency_metrics(data: dict) -> dict:
    """Extract latency and tracking accuracy metrics for 1 trial relative to raw camera meas."""
    meas_speed = compute_meas_speed(data)
    ee_speed = compute_ee_speed(data)

    # Position RMSE (mm) between raw camera hand meas and robot EE
    pos_err_x = data['mx'] - data['rx']
    pos_err_y = data['my'] - data['ry']
    pos_err_z = data['mz'] - data['rz']
    pos_dist = np.sqrt(pos_err_x**2 + pos_err_y**2 + pos_err_z**2)
    pos_rmse_mm = np.sqrt(np.nanmean(pos_dist**2)) * 1000.0

    # Tracking Speed Error (m/s) against raw camera hand speed
    speed_err = np.nanmean(np.abs(meas_speed - ee_speed))

    # Phase Lag (ms) against raw camera hand speed
    phase_lag_ms = compute_phase_lag_ms(meas_speed, ee_speed, data['t'])

    # Prediction MAE 3D (mm)
    mae_x = np.nanmean(data['maex'])
    mae_y = np.nanmean(data['maey'])
    mae_z = np.nanmean(data['maez'])
    pred_mae_3d_mm = np.sqrt(mae_x**2 + mae_y**2 + mae_z**2) * 1000.0 if not np.isnan(mae_x) else np.nan

    # Inference Time (ms)
    inf_ms = np.nanmean(data['inf_ms']) if not np.isnan(np.nanmean(data['inf_ms'])) else np.nan

    # Completion Time (s)
    duration = data['t'][-1] if len(data['t']) > 0 else 0.0

    return {
        'phase_lag_ms': phase_lag_ms,
        'pos_rmse_mm': pos_rmse_mm,
        'speed_err': speed_err,
        'pred_mae_3d_mm': pred_mae_3d_mm,
        'inf_ms': inf_ms,
        'duration': duration,
        '_pos_dist_mm': pos_dist * 1000.0,
        '_meas_speed': meas_speed,
        '_ee_speed': ee_speed,
    }


def find_representative(trials, key='pos_rmse_mm'):
    """Select the trial whose metric is closest to the median performance."""
    metrics = [compute_trial_latency_metrics(t)[key] for t in trials]
    med_val = np.median(metrics)
    closest_idx = int(np.argmin(np.abs(np.array(metrics) - med_val)))
    return trials[closest_idx], closest_idx


def p_stars(p):
    if np.isnan(p):
        return ''
    if p < 0.001:
        return '***'
    elif p < 0.01:
        return '**'
    elif p < 0.05:
        return '*'
    else:
        return 'n.s.'


def format_p_val(p):
    if np.isnan(p):
        return 'N/A'
    if p < 0.001:
        return 'p < 0.001'
    return f'p = {p:.3f}'


# ══════════════════════════════════════════════════════════════════════
# FIGURE GENERATION
# ══════════════════════════════════════════════════════════════════════

def fig1_position_overlay(all_data: dict, save_dir: str):
    """Figure 1: Height tracking overlay comparison (Hand Target Z vs Robot EE Z)."""
    fig, axes = plt.subplots(3, 1, figsize=(11, 8.5), sharex=False)
    fig.suptitle('Scenario 3: Height Trajectory Tracking (Hand Meas Z vs Robot EE Z)\n(representative trial ≈ median performance)', fontsize=13, fontweight='bold', y=0.99)

    for idx, mode in enumerate(BASELINE_MAP):
        ax = axes[idx]
        cfg = BASELINE_MAP[mode]
        trial, ridx = find_representative(all_data[mode], 'pos_rmse_mm')

        ax.plot(trial['t'], trial['mz'], '--', color='#2980b9', linewidth=1.8, label='Hand Target Z (meas)', alpha=0.85)
        ax.plot(trial['t'], trial['rz'], '-', color=cfg['color'], linewidth=2.2, label='Robot EE Z')

        ax.set_ylabel('Height Z (m)', fontsize=11)
        ax.set_title(f"{cfg['label'].replace(chr(10), ' ')}", fontsize=11, fontweight='bold', color=cfg['color'], loc='left')
        ax.annotate(f'trial #{ridx+1} (median)', (0.99, 0.04),
                    xycoords='axes fraction', ha='right', fontsize=8, color='gray', style='italic')
        ax.legend(loc='upper right', fontsize=9, framealpha=0.9)
        ax.grid(True, alpha=0.3)
        ax.set_xlim([0, trial['t'][-1]])

    axes[-1].set_xlabel('Time (s)', fontsize=11)
    plt.tight_layout()
    path = os.path.join(save_dir, 'fig1_position_overlay.png')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    print(f'  Saved: {path}')
    plt.close()


def select_matched_trials(all_data):
    """Select the same matched-duration trials as RULA time-series for consistency (~8.6s)."""
    return {
        'GROUND_TRUTH': (all_data['GROUND_TRUTH'][1], 1),
        'GRU':          (all_data['GRU'][11], 11),
        'ERGONOMICS':   (all_data['ERGONOMICS'][16], 16)
    }


def fig2_velocity_lag(all_data: dict, save_dir: str):
    """Figure 2: Velocity profiles demonstrating phase delay relative to raw camera meas (using matched trials)."""
    fig, axes = plt.subplots(3, 1, figsize=(11, 8.5), sharex=False)

    selected = select_matched_trials(all_data)

    for idx, mode in enumerate(BASELINE_MAP):
        ax = axes[idx]
        cfg = BASELINE_MAP[mode]
        trial, ridx = selected[mode]
        metrics = compute_trial_latency_metrics(trial)

        ax.plot(trial['t'], metrics['_meas_speed'], '--', color='#7f8c8d', linewidth=1.5, label='Raw Hand Speed (meas)', alpha=0.75)
        ax.plot(trial['t'], metrics['_ee_speed'], '-', color=cfg['color'], linewidth=2.0, label='Robot Speed')

        lag = metrics['phase_lag_ms']
        ax.annotate(f'Phase Lag: {lag:.1f} ms', (0.05, 0.82), xycoords='axes fraction',
                    fontsize=9.5, fontweight='bold', color=cfg['color'],
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=cfg['color'], alpha=0.8))

        ax.set_ylabel('Speed (m/s)', fontsize=11)
        ax.set_title(f"{cfg['label'].replace(chr(10), ' ')}", fontsize=11, fontweight='bold', color=cfg['color'], loc='left')
        ax.legend(loc='upper right', fontsize=9, framealpha=0.9)
        ax.grid(True, alpha=0.3)
        ax.set_xlim([0, 8.5])

    axes[-1].set_xlabel('Time (s)', fontsize=11)
    plt.tight_layout()
    path = os.path.join(save_dir, 'fig2_velocity_lag.png')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    print(f'  Saved: {path}')
    plt.close()


def fig3_prediction_accuracy(all_data: dict, save_dir: str):
    """Figure 3: GRU Prediction vs Camera Measurement (Measured vs Predicted X)."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7.5), sharex=True)

    for idx, (mode, ax) in enumerate([('GRU', ax1), ('ERGONOMICS', ax2)]):
        cfg = BASELINE_MAP[mode]
        trial, ridx = find_representative(all_data[mode], 'pred_mae_3d_mm')

        valid_mask = ~np.isnan(trial['px'])
        t_v = trial['t'][valid_mask]
        mx_v = trial['mx'][valid_mask]
        px_v = trial['px'][valid_mask]
        mae_v = trial['maex'][valid_mask]

        ax.plot(t_v, mx_v, '-', color='#2980b9', linewidth=2.0, label='Measured Hand Pos (Camera GT)')
        ax.plot(t_v, px_v, '--', color=cfg['color'], linewidth=2.0, label='GRU Predicted Pos')
        ax.fill_between(t_v, px_v - mae_v, px_v + mae_v, color=cfg['color'], alpha=0.2, label='Prediction Error Band (±MAE)')

        mean_mae = np.nanmean(mae_v) * 1000.0
        ax.annotate(f'Mean MAE_x: {mean_mae:.1f} mm', (0.03, 0.85), xycoords='axes fraction',
                    fontsize=9.5, fontweight='bold', color=cfg['color'],
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=cfg['color'], alpha=0.8))

        ax.set_ylabel('Position X (m)', fontsize=11)
        ax.set_title(f"{cfg['label'].replace(chr(10), ' ')}", fontsize=11, fontweight='bold', color=cfg['color'], loc='left')
        ax.legend(loc='lower right', fontsize=9, framealpha=0.9)
        ax.grid(True, alpha=0.3)

    ax2.set_xlabel('Time (s)', fontsize=11)
    plt.tight_layout()
    path = os.path.join(save_dir, 'fig3_prediction_accuracy.png')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    print(f'  Saved: {path}')
    plt.close()


def fig4_latency_boxplots(metrics_by_mode: dict, save_dir: str):
    """Figure 4: Statistical Boxplots across combined trials (N=20/baseline)."""
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 5.0))

    metric_keys = [
        ('phase_lag_ms', 'Phase Lag (ms)', 'Lower is better'),
        ('speed_err',    'Speed Mismatch (m/s)', 'Lower is smoother'),
        ('duration',     'Task Duration (s)', 'Execution time'),
    ]

    modes = list(BASELINE_MAP.keys())

    for ax_idx, (key, ylabel, note) in enumerate(metric_keys):
        ax = axes[ax_idx]
        box_data = []
        for mode in modes:
            vals = [m[key] for m in metrics_by_mode[mode] if not np.isnan(m[key])]
            if key == 'phase_lag_ms' and mode == 'GROUND_TRUTH':
                vals = [v for v in vals if v < 3000]
            elif key == 'duration' and mode == 'GRU':
                vals = [v for v in vals if v < 11.0]
            box_data.append(vals)

        labels = [BASELINE_MAP[m]['short'] for m in modes]
        colors = [BASELINE_MAP[m]['color'] for m in modes]

        bp = ax.boxplot(box_data, labels=labels, patch_artist=True, widths=0.45,
                        medianprops=dict(color='black', linewidth=2.0))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.72)

        # Scatter points
        for i, (vals, color) in enumerate(zip(box_data, colors)):
            x = np.random.default_rng(42).normal(i + 1, 0.04, size=len(vals))
            ax.scatter(x, vals, color=color, edgecolors='black', s=32, zorder=5, alpha=0.85)

        # Welch's t-test Prop vs GT & Prop vs GRU
        _, p_gt  = stats.ttest_ind(box_data[2], box_data[0], equal_var=False)
        _, p_gru = stats.ttest_ind(box_data[2], box_data[1], equal_var=False)

        ymax = max([max(v) for v in box_data if len(v) > 0])
        h_step = max(0.1, ymax * 0.09)

        # GT vs Proposed
        ax.plot([1, 3], [ymax + h_step, ymax + h_step], color='#333333', lw=1.1)
        ax.text(2, ymax + h_step * 1.15, f"{p_stars(p_gt)} ({format_p_val(p_gt)})",
                ha='center', va='bottom', fontsize=8.5, fontweight='bold')

        # GRU vs Proposed
        ax.plot([2, 3], [ymax + h_step * 2.3, ymax + h_step * 2.3], color='#555555', lw=1.0, ls='--')
        ax.text(2.5, ymax + h_step * 2.45, f"{p_stars(p_gru)} ({format_p_val(p_gru)})",
                ha='center', va='bottom', fontsize=8, color='#555555')

        ax.set_ylabel(ylabel, fontsize=10)
        ax.set_title(note, fontsize=9, fontstyle='italic', color='#555555')
        ax.grid(True, axis='y', alpha=0.3)
        ax.set_ylim(bottom=0, top=ymax + h_step * 3.6)

    plt.tight_layout()
    path = os.path.join(save_dir, 'fig4_latency_boxplots.png')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    print(f'  Saved: {path}')
    plt.close()


def print_and_export_latex(metrics_by_mode: dict, save_dir: str):
    """Print statistical summary and export LaTeX table (with outlier filtering applied)."""
    metric_keys = [
        ('phase_lag_ms',   'Phase Lag (ms)'),
        ('pos_rmse_mm',    'Position RMSE (mm)'),
        ('speed_err',      'Speed Mismatch (m/s)'),
        ('duration',       'Task Completion Duration (s)'),
        ('pred_mae_3d_mm', '3D Prediction MAE (mm)'),
        ('inf_ms',         'Model Inference Latency (ms)'),
    ]

    filtered_vals = {}
    stats_summary = {}
    for key, name in metric_keys:
        filtered_vals[key] = {}
        stats_summary[key] = {}
        for mode in BASELINE_MAP:
            vals = [m[key] for m in metrics_by_mode[mode] if not np.isnan(m[key])]
            if key == 'phase_lag_ms' and mode == 'GROUND_TRUTH':
                vals = [v for v in vals if v < 3000]
            elif key == 'duration' and mode == 'GRU':
                vals = [v for v in vals if v < 11.0]
            filtered_vals[key][mode] = vals
            stats_summary[key][mode] = (np.mean(vals), np.std(vals)) if len(vals) > 0 else (np.nan, np.nan)

    print('\n' + '=' * 85)
    print(f'SCENARIO 3 LATENCY STATISTICAL SUMMARY (Filtered Outliers)')
    print('=' * 85)
    print(f'{"Metric":<28} {"GT (μ±σ)":<18} {"GRU (μ±σ)":<18} {"Proposed (μ±σ)":<18} {"p-val (vs GT)":<12}')
    print('-' * 85)

    for key, name in metric_keys:
        gt_m, gt_s = stats_summary[key]['GROUND_TRUTH']
        gru_m, gru_s = stats_summary[key]['GRU']
        pr_m, pr_s = stats_summary[key]['ERGONOMICS']

        pr_vals = filtered_vals[key]['ERGONOMICS']
        gt_vals = filtered_vals[key]['GROUND_TRUTH']

        p_val = stats.ttest_ind(pr_vals, gt_vals, equal_var=False).pvalue if len(pr_vals) > 0 and len(gt_vals) > 0 else np.nan

        p_str = format_p_val(p_val)
        gt_str = f'{gt_m:>6.2f} ± {gt_s:<6.2f}' if not np.isnan(gt_m) else 'N/A'
        gru_str = f'{gru_m:>6.2f} ± {gru_s:<6.2f}' if not np.isnan(gru_m) else 'N/A'
        pr_str = f'{pr_m:>6.2f} ± {pr_s:<6.2f}' if not np.isnan(pr_m) else 'N/A'

        print(f'{name:<28} {gt_str:<18} {gru_str:<18} {pr_str:<18} {p_str:<12}')
    print('=' * 85)

    # Export LaTeX table
    latex_code = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{Quantitative Latency and Tracking Performance in Scenario 3}",
        r"\label{tab:scenario3_latency}",
        r"\begin{tabular}{lcccc}",
        r"\toprule",
        r"\textbf{Metric} & \textbf{Baseline 1 (GT)} & \textbf{Baseline 2 (GRU)} & \textbf{Proposed System} & \textbf{$p$-value} \\",
        r"\midrule",
    ]

    for key, name in metric_keys:
        gt_m, gt_s = stats_summary[key]['GROUND_TRUTH']
        gru_m, gru_s = stats_summary[key]['GRU']
        pr_m, pr_s = stats_summary[key]['ERGONOMICS']

        pr_vals = filtered_vals[key]['ERGONOMICS']
        gt_vals = filtered_vals[key]['GROUND_TRUTH']
        p_val = stats.ttest_ind(pr_vals, gt_vals, equal_var=False).pvalue if len(pr_vals) > 0 and len(gt_vals) > 0 else np.nan

        stars = p_stars(p_val) if not np.isnan(p_val) else ''
        p_tex = f"$< 0.001^{{{stars}}}$" if p_val < 0.001 else (f"${p_val:.3f}^{{{stars}}}$" if not np.isnan(p_val) else "N/A")

        gt_tex = f"${gt_m:.2f} \\pm {gt_s:.2f}$" if not np.isnan(gt_m) else "N/A"
        gru_tex = f"${gru_m:.2f} \\pm {gru_s:.2f}$" if not np.isnan(gru_m) else "N/A"
        pr_tex = f"$\\mathbf{{{pr_m:.2f} \\pm {pr_s:.2f}}}$" if not np.isnan(pr_m) else "N/A"

        latex_code.append(
            f"{name} & {gt_tex} & {gru_tex} & {pr_tex} & {p_tex} \\\\"
        )

    latex_code.extend([
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}"
    ])

    latex_file = os.path.join(save_dir, 'scenario3_latency_table.tex')
    with open(latex_file, 'w') as f:
        f.write('\n'.join(latex_code))
    print(f'  LaTeX Table exported to: {latex_file}')


def main():
    parser = argparse.ArgumentParser(description='Scenario 3 Latency & Prediction Analysis')
    parser.add_argument('data_dir', help='Path to Scenario_3 log directory')
    parser.add_argument('--save-dir', default=None, help='Output directory for figures and LaTeX table')
    args = parser.parse_args()

    save_dir = args.save_dir or args.data_dir
    os.makedirs(save_dir, exist_ok=True)

    print(f'Loading Scenario 3 trials from: {args.data_dir}')
    all_data = load_all_scenario3_trials(args.data_dir)

    metrics_by_mode = {}
    for mode in BASELINE_MAP:
        if len(all_data[mode]) == 0:
            print(f'ERROR: No trials found for {mode}!')
            return
        metrics_by_mode[mode] = [compute_trial_latency_metrics(t) for t in all_data[mode]]

    print('\nGenerating publication figures...')
    fig2_velocity_lag(all_data, save_dir)
    fig4_latency_boxplots(metrics_by_mode, save_dir)
    print_and_export_latex(metrics_by_mode, save_dir)

    print('\n✓ Scenario 3 Latency & Prediction Analysis Completed Successfully!')


if __name__ == '__main__':
    main()
