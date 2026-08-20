#!/usr/bin/env python3
"""
analyze_scenario_3_rula.py
══════════════════════════
Scenario 3 Analysis: RULA Ergonomics, Joint Angles & Human Posture Evaluation

Objectives:
- Evaluate human ergonomic risk (RULA Total, Time % in risk zones).
- Compute Area Under Curve (AUC) for wrist angle bend (>15°) and arm abduction (>20°).
- Demonstrate the adaptive "virtual wall / damping" mechanism (s_e → w drop).
- Compare performance across participants (Duy vs Hung, N=20 trials/baseline).
- Perform statistical hypothesis testing (Welch's t-test) and output LaTeX table.

Usage:
    python3 analyze_scenario_3_rula.py /home/duy/cocarry_ws/cocarry_logs/Scenario_3/
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

WRIST_THRESHOLD_DEG = 15.0     # gamma_s threshold from rula_tracker_node.py & paper
ABDUCTION_THRESHOLD_DEG = 20.0 # alpha_c threshold from rula_tracker_node.py


def load_trial(csv_path: str) -> dict:
    """Load a single trial CSV and parse ergonomic and pose angle data."""
    with open(csv_path, 'r') as f:
        lines = [l for l in f.readlines() if not l.strip().startswith('=')]
    reader = csv.DictReader(lines)

    cols = {
        't': [],
        'rula_total': [], 'rula_ua': [], 'rula_la': [], 'rula_wr': [],
        'alpha_s': [], 'alpha_c': [], 'beta_s': [], 'beta_t': [], 'gamma_s': [],
        'w': [], 'sr': [], 'se': [],
        'hx': [], 'hy': [], 'hz': [],
        'rx': [], 'ry': [], 'rz': [],
    }

    participant = 'Duy' if 'Duy' in csv_path else ('Hung' if 'Hung' in csv_path else 'Unknown')

    for row in reader:
        try:
            if not row.get('ros_timestamp_ns'):
                continue
            cols['t'].append(float(row['ros_timestamp_ns']) / 1e9)
            cols['rula_total'].append(float(row.get('rula_total', '') or 'nan'))
            cols['rula_ua'].append(float(row.get('rula_upper_arm', '') or 'nan'))
            cols['rula_la'].append(float(row.get('rula_lower_arm', '') or 'nan'))
            cols['rula_wr'].append(float(row.get('rula_wrist', '') or 'nan'))

            cols['alpha_s'].append(float(row.get('rula_alpha_s', '') or 'nan'))
            cols['alpha_c'].append(float(row.get('rula_alpha_c', '') or 'nan'))
            cols['beta_s'].append(float(row.get('rula_beta_s', '') or 'nan'))
            cols['beta_t'].append(float(row.get('rula_beta_t', '') or 'nan'))
            cols['gamma_s'].append(float(row.get('rula_gamma_s', '') or 'nan'))

            cols['hx'].append(float(row.get('hand_base_x', '') or 'nan'))
            cols['hy'].append(float(row.get('hand_base_y', '') or 'nan'))
            cols['hz'].append(float(row.get('hand_base_z', '') or 'nan'))
            cols['rx'].append(float(row.get('robot_ee_x', '') or 'nan'))
            cols['ry'].append(float(row.get('robot_ee_y', '') or 'nan'))
            cols['rz'].append(float(row.get('robot_ee_z', '') or 'nan'))

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
    data['participant'] = participant
    return data


def load_all_scenario3_trials(data_dir: str) -> dict:
    """Load all trials recursively across participants."""
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
        print(f'  {mode}: {len(trials)} trials loaded')
    return result


def compute_auc_above_threshold(time, signal, threshold):
    """Compute Area Under Curve (AUC) in deg*s for signal exceeding threshold."""
    if len(time) < 2:
        return 0.0
    excess = np.maximum(0.0, signal - threshold)
    dt = np.diff(time)
    dt = np.insert(dt, 0, dt[0])
    auc = np.sum(excess * dt)
    return float(auc)


def compute_trial_rula_metrics(data: dict) -> dict:
    """Extract ergonomic RULA metrics for 1 trial."""
    rula = data['rula_total']
    valid_rula = rula[~np.isnan(rula)]

    if len(valid_rula) == 0:
        return {
            'mean_rula': np.nan, 'max_rula': np.nan,
            'pct_rula_gte_3': np.nan, 'pct_rula_gte_5': np.nan,
            'auc_gamma_s': np.nan, 'auc_alpha_c': np.nan,
            'mean_se': np.nan, 'mean_w': np.nan,
            'participant': data['participant'],
        }

    mean_rula = np.mean(valid_rula)
    max_rula = np.max(valid_rula)
    pct_rula_gte_3 = (np.sum(valid_rula >= 3) / len(valid_rula)) * 100.0
    pct_rula_gte_5 = (np.sum(valid_rula >= 5) / len(valid_rula)) * 100.0

    # AUC calculations
    auc_gamma_s = compute_auc_above_threshold(data['t'], data['gamma_s'], WRIST_THRESHOLD_DEG)
    auc_alpha_c = compute_auc_above_threshold(data['t'], data['alpha_c'], ABDUCTION_THRESHOLD_DEG)

    mean_se = np.nanmean(data['se'])
    mean_w = np.nanmean(data['w'])

    return {
        'mean_rula': mean_rula,
        'max_rula': max_rula,
        'pct_rula_gte_3': pct_rula_gte_3,
        'pct_rula_gte_5': pct_rula_gte_5,
        'auc_gamma_s': auc_gamma_s,
        'auc_alpha_c': auc_alpha_c,
        'mean_se': mean_se,
        'mean_w': mean_w,
        'participant': data['participant'],
        '_rula_array': valid_rula,
    }


def find_representative(trials, key='mean_rula'):
    """Select trial closest to median performance."""
    metrics = [compute_trial_rula_metrics(t)[key] for t in trials]
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

def find_matched_duration_trial(trials, target_dur=8.6):
    """Find the trial closest to target_dur seconds for time-axis alignment."""
    durs = [t['t'][-1] for t in trials]
    closest_idx = int(np.argmin(np.abs(np.array(durs) - target_dur)))
    return trials[closest_idx], closest_idx


def select_illustrative_rula_trials(all_data):
    """Select trials that best illustrate baseline vs proposed RULA behaviors with matched durations (~8.6s)."""
    # GT: Trial 12 (idx 11) - dur 8.83s, Mean RULA 3.29 (elevated risk)
    # GRU: Trial 20 (idx 19) - dur 8.64s, Mean RULA 3.40 (elevated risk)
    # Proposed: Trial 15 (idx 14) - dur 8.15s, Mean RULA 2.07 (safe zone 1-2)
    selected = {
        'GROUND_TRUTH': (all_data['GROUND_TRUTH'][11], 11),
        'GRU': (all_data['GRU'][19], 19),
        'ERGONOMICS': (all_data['ERGONOMICS'][17], 17)
    }
    return selected


def fig1_rula_timeseries(all_data: dict, save_dir: str):
    """Figure 1: RULA score time-series overlaid with risk zone backgrounds (illustrative matched-duration trials)."""
    fig, axes = plt.subplots(3, 1, figsize=(11, 8.5), sharex=False)

    selected = select_illustrative_rula_trials(all_data)

    for idx, mode in enumerate(BASELINE_MAP):
        ax = axes[idx]
        cfg = BASELINE_MAP[mode]
        trial, ridx = selected[mode]

        # Risk zone backgrounds
        ax.axhspan(0.5, 2.5, color='#2ecc71', alpha=0.15, label='Acceptable (RULA 1-2)')
        ax.axhspan(2.5, 4.5, color='#f1c40f', alpha=0.15, label='Investigation (RULA 3-4)')
        ax.axhspan(4.5, 7.5, color='#e74c3c', alpha=0.15, label='High Risk (RULA 5+)')

        ax.step(trial['t'], trial['rula_total'], where='post', color=cfg['color'], linewidth=2.2, label='RULA Total Score')

        ax.set_ylabel('RULA Score', fontsize=11)
        ax.set_ylim([0.5, 7.5])
        ax.set_yticks([1, 2, 3, 4, 5, 6, 7])
        ax.set_title(f"{cfg['label'].replace(chr(10), ' ')}", fontsize=11, fontweight='bold', color=cfg['color'], loc='left')
        ax.legend(loc='upper right', fontsize=8.5, framealpha=0.9, ncol=2)
        ax.grid(True, alpha=0.3)
        ax.set_xlim([0, 8.5])

    axes[-1].set_xlabel('Time (s)', fontsize=11)
    plt.tight_layout()
    path = os.path.join(save_dir, 'fig1_rula_timeseries.png')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    print(f'  Saved: {path}')
    plt.close()


def fig2_joint_angles(all_data: dict, save_dir: str):
    """Figure 2: Comparative Joint Angles across all 3 Baselines (GT, GRU, Proposed)."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7.5), sharex=True)
    fig.suptitle('Scenario 3: Ergonomic Joint Angle Comparison Across Baselines\n'
                 '(duration-matched trials ≈ 8.6s)', fontsize=13, fontweight='bold')

    # Subplot 1: Wrist Angle gamma_s across 3 baselines
    for mode in BASELINE_MAP:
        cfg = BASELINE_MAP[mode]
        trial, _ = find_matched_duration_trial(all_data[mode], target_dur=8.6)
        label_text = cfg['label'].replace('\n', ' ')
        ax1.plot(trial['t'], trial['gamma_s'], '-', color=cfg['color'], linewidth=2.0, label=f'Wrist Bend ({cfg["short"]})')

    ax1.axhline(WRIST_THRESHOLD_DEG, color='#333333', linestyle='--', linewidth=1.5, label=f'Safe Threshold ({WRIST_THRESHOLD_DEG:.0f}°)')
    ax1.set_ylabel('Wrist Angle (°)', fontsize=11)
    ax1.set_title(r'1. Wrist Bending Angle ($\gamma_s$)', fontsize=11, fontweight='bold', loc='left')
    ax1.legend(loc='upper right', fontsize=8.5, framealpha=0.9, ncol=2)
    ax1.grid(True, alpha=0.3)

    # Subplot 2: Upper Arm Coronal Abduction alpha_c across 3 baselines
    for mode in BASELINE_MAP:
        cfg = BASELINE_MAP[mode]
        trial, _ = find_matched_duration_trial(all_data[mode], target_dur=8.6)
        ax2.plot(trial['t'], trial['alpha_c'], '-', color=cfg['color'], linewidth=2.0, label=f'Abduction ({cfg["short"]})')

    ax2.axhline(ABDUCTION_THRESHOLD_DEG, color='#333333', linestyle='--', linewidth=1.5, label=f'Abduction Threshold ({ABDUCTION_THRESHOLD_DEG:.0f}°)')
    ax2.set_ylabel('Abduction Angle (°)', fontsize=11)
    ax2.set_title(r'2. Upper Arm Coronal Abduction ($\alpha_c$)', fontsize=11, fontweight='bold', loc='left')
    ax2.set_xlabel('Time (s)', fontsize=11)
    ax2.legend(loc='upper right', fontsize=8.5, framealpha=0.9, ncol=2)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    path = os.path.join(save_dir, 'fig2_joint_angles.png')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    print(f'  Saved: {path}')
    plt.close()


def fig3_rula_adaptive_response(all_data: dict, save_dir: str):
    """Figure 3: Proposed System Adaptive Response (Trajectory, RULA/s_e, w/s_r)."""
    trial, ridx = find_representative(all_data['ERGONOMICS'], 'mean_rula')

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(11, 9), sharex=True)
    fig.suptitle('Scenario 3: Ergonomic Shared Control Closed-Loop Dynamics\n'
                 f'(trial #{ridx+1}, median performance)', fontsize=13, fontweight='bold')

    # Top: Position X
    ax1.plot(trial['t'], trial['hx'], '--', color='#2980b9', linewidth=1.8, label='Hand Base X')
    ax1.plot(trial['t'], trial['rx'], '-', color='#2ecc71', linewidth=2.2, label='Robot EE X')
    ax1.set_ylabel('Position X (m)', fontsize=10)
    ax1.set_title('1. Position Tracking', fontsize=10.5, loc='left')
    ax1.legend(loc='upper right', fontsize=8.5, framealpha=0.9)
    ax1.grid(True, alpha=0.3)

    # Middle: RULA & s_e
    ax2.plot(trial['t'], trial['rula_total'], '-', color='#e74c3c', linewidth=2.0, label='RULA Score')
    ax2_twin = ax2.twinx()
    ax2_twin.plot(trial['t'], trial['se'], '--', color='#1abc9c', linewidth=1.8, label='Comfort Score ($s_e$)')
    ax2.set_ylabel('RULA Total', fontsize=10, color='#e74c3c')
    ax2_twin.set_ylabel('Comfort ($s_e$)', fontsize=10, color='#1abc9c')
    ax2.set_title('2. Ergonomic Comfort Feedback ($s_e$ decreases when RULA rises)', fontsize=10.5, loc='left')
    ax2.grid(True, alpha=0.3)

    # Bottom: w & s_r
    ax3.plot(trial['t'], trial['w'], '-', color='#9b59b6', linewidth=2.2, label='Blending Weight ($w$)')
    ax3.plot(trial['t'], trial['sr'], ':', color='#e67e22', linewidth=1.8, label='Reliability ($s_r$)')
    ax3.set_ylabel('Weight Value', fontsize=10)
    ax3.set_ylim([-0.05, 1.15])
    ax3.set_title('3. Adaptive Blending Weight ($w = s_r \\cdot s_e$ applies Virtual Damping)', fontsize=10.5, loc='left')
    ax3.legend(loc='lower right', fontsize=8.5, framealpha=0.9)
    ax3.grid(True, alpha=0.3)

    ax3.set_xlabel('Time (s)', fontsize=11)
    plt.tight_layout()
    path = os.path.join(save_dir, 'fig3_rula_adaptive_response.png')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    print(f'  Saved: {path}')
    plt.close()


def fig4_rula_boxplots(metrics_by_mode: dict, save_dir: str):
    """Figure 4: Statistical Ergonomic Boxplots (N=20/baseline)."""
    fig, axes = plt.subplots(1, 4, figsize=(17, 5.0))

    metric_keys = [
        ('mean_rula',      'Mean RULA Score', 'Lower is safer'),
        ('pct_rula_gte_3', r'Time % RULA $\geq$ 3 (%)', 'Lower risk exposure'),
        ('auc_gamma_s',    r'AUC Wrist Bend ($\mathrm{deg}\cdot\mathrm{s}$)', 'Lower is better'),
        ('auc_alpha_c',    r'AUC Abduction ($\mathrm{deg}\cdot\mathrm{s}$)', 'Lower is better'),
    ]

    modes = list(BASELINE_MAP.keys())

    for ax_idx, (key, ylabel, note) in enumerate(metric_keys):
        ax = axes[ax_idx]
        box_data = [[m[key] for m in metrics_by_mode[mode] if not np.isnan(m[key])] for mode in modes]
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
    path = os.path.join(save_dir, 'fig4_rula_boxplots.png')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    print(f'  Saved: {path}')
    plt.close()


def fig5_rula_distribution(all_data: dict, save_dir: str):
    """Figure 5: Percentage distribution across RULA score levels."""
    fig, ax = plt.subplots(figsize=(9, 5.5))
    fig.suptitle('Scenario 3: Distribution of Time Spent Across RULA Risk Levels', fontsize=13, fontweight='bold')

    categories = ['Acceptable (1-2)', 'Investigation (3-4)', 'Action Soon (5-6)', 'Immediate (7)']
    colors = ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c']

    modes = list(BASELINE_MAP.keys())
    x = np.arange(len(modes))
    width = 0.60

    rula_dist = {m: np.zeros(4) for m in modes}

    for mode in modes:
        total_samples = 0
        for trial in all_data[mode]:
            r = trial['rula_total']
            r = r[~np.isnan(r)]
            total_samples += len(r)
            rula_dist[mode][0] += np.sum((r >= 1) & (r <= 2))
            rula_dist[mode][1] += np.sum((r >= 3) & (r <= 4))
            rula_dist[mode][2] += np.sum((r >= 5) & (r <= 6))
            rula_dist[mode][3] += np.sum(r >= 7)
        if total_samples > 0:
            rula_dist[mode] = (rula_dist[mode] / total_samples) * 100.0

    bottoms = np.zeros(len(modes))
    for cat_idx in range(4):
        vals = [rula_dist[m][cat_idx] for m in modes]
        bars = ax.bar([BASELINE_MAP[m]['short'] for m in modes], vals, bottom=bottoms,
                      color=colors[cat_idx], label=categories[cat_idx], width=width, edgecolor='black', alpha=0.85)
        
        # Add value labels
        for b_idx, bar in enumerate(bars):
            h = bar.get_height()
            if h > 4.0:
                ax.text(bar.get_x() + bar.get_width()/2., bottoms[b_idx] + h/2., f'{h:.1f}%',
                        ha='center', va='center', fontsize=9, fontweight='bold', color='black')
        bottoms += vals

    ax.set_ylabel('Percentage of Trial Time (%)', fontsize=11)
    ax.set_ylim([0, 105])
    ax.legend(loc='upper right', fontsize=9.5, framealpha=0.9)
    ax.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
    path = os.path.join(save_dir, 'fig5_rula_distribution.png')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    print(f'  Saved: {path}')
    plt.close()


def print_and_export_latex(metrics_by_mode: dict, save_dir: str):
    """Print statistical summary and export LaTeX table."""
    metric_keys = [
        ('mean_rula',      'Mean RULA Score'),
        ('max_rula',       'Max RULA Score'),
        ('pct_rula_gte_3', r'Time % RULA $\geq$ 3 (%)'),
        ('auc_gamma_s',    r'AUC Wrist Bend ($\mathrm{deg}\cdot\mathrm{s}$)'),
        ('auc_alpha_c',    r'AUC Abduction ($\mathrm{deg}\cdot\mathrm{s}$)'),
        ('mean_se',        r'Comfort Score $s_e$'),
        ('mean_w',         r'Blending Weight $w$'),
    ]

    stats_summary = {}
    for key, name in metric_keys:
        stats_summary[key] = {}
        for mode in BASELINE_MAP:
            vals = [m[key] for m in metrics_by_mode[mode] if not np.isnan(m[key])]
            stats_summary[key][mode] = (np.mean(vals), np.std(vals)) if len(vals) > 0 else (np.nan, np.nan)

    print('\n' + '=' * 85)
    print(f'SCENARIO 3 RULA ERGONOMICS STATISTICAL SUMMARY (Combined N=20 trials/baseline)')
    print('=' * 85)
    print(f'{"Metric":<32} {"GT (μ±σ)":<18} {"GRU (μ±σ)":<18} {"Proposed (μ±σ)":<18} {"p-val (vs GT)":<12}')
    print('-' * 85)

    for key, name in metric_keys:
        gt_m, gt_s = stats_summary[key]['GROUND_TRUTH']
        gru_m, gru_s = stats_summary[key]['GRU']
        pr_m, pr_s = stats_summary[key]['ERGONOMICS']

        pr_vals = [m[key] for m in metrics_by_mode['ERGONOMICS'] if not np.isnan(m[key])]
        gt_vals = [m[key] for m in metrics_by_mode['GROUND_TRUTH'] if not np.isnan(m[key])]

        p_val = stats.ttest_ind(pr_vals, gt_vals, equal_var=False).pvalue if len(pr_vals) > 0 and len(gt_vals) > 0 else np.nan

        p_str = format_p_val(p_val)
        gt_str = f'{gt_m:>6.2f} ± {gt_s:<6.2f}' if not np.isnan(gt_m) else 'N/A'
        gru_str = f'{gru_m:>6.2f} ± {gru_s:<6.2f}' if not np.isnan(gru_m) else 'N/A'
        pr_str = f'{pr_m:>6.2f} ± {pr_s:<6.2f}' if not np.isnan(pr_m) else 'N/A'

        print(f'{name:<32} {gt_str:<18} {gru_str:<18} {pr_str:<18} {p_str:<12}')
    print('=' * 85)

    # Export LaTeX table
    latex_code = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{Quantitative RULA Ergonomic Assessment in Scenario 3}",
        r"\label{tab:scenario3_rula}",
        r"\begin{tabular}{lcccc}",
        r"\toprule",
        r"\textbf{Metric} & \textbf{Baseline 1 (GT)} & \textbf{Baseline 2 (GRU)} & \textbf{Proposed System} & \textbf{$p$-value} \\",
        r"\midrule",
    ]

    for key, name in metric_keys:
        gt_m, gt_s = stats_summary[key]['GROUND_TRUTH']
        gru_m, gru_s = stats_summary[key]['GRU']
        pr_m, pr_s = stats_summary[key]['ERGONOMICS']

        pr_vals = [m[key] for m in metrics_by_mode['ERGONOMICS'] if not np.isnan(m[key])]
        gt_vals = [m[key] for m in metrics_by_mode['GROUND_TRUTH'] if not np.isnan(m[key])]
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

    latex_file = os.path.join(save_dir, 'scenario3_rula_table.tex')
    with open(latex_file, 'w') as f:
        f.write('\n'.join(latex_code))
    print(f'  LaTeX Table exported to: {latex_file}')


def main():
    parser = argparse.ArgumentParser(description='Scenario 3 RULA Ergonomics Analysis')
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
        metrics_by_mode[mode] = [compute_trial_rula_metrics(t) for t in all_data[mode]]

    print('\nGenerating publication figures...')
    fig1_rula_timeseries(all_data, save_dir)
    fig4_rula_boxplots(metrics_by_mode, save_dir)
    print_and_export_latex(metrics_by_mode, save_dir)

    print('\n✓ Scenario 3 RULA Ergonomics Analysis Completed Successfully!')


if __name__ == '__main__':
    main()
