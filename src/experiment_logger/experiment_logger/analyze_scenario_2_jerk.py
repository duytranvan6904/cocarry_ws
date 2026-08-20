#!/usr/bin/env python3
"""
analyze_scenario_2_jerk.py  —  Scenario 2: Sudden Jerk Safety Analysis
=======================================================================
Usage:
    python3 analyze_scenario_2_jerk.py /path/to/cocarry_logs/Scenario_2/
"""

import os, csv, glob, argparse
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

BASELINE_MAP = {
    'GROUND_TRUTH': {'label': 'Baseline 1 (Camera Only)',          'color': '#e74c3c', 'short': 'GT'},
    'GRU':          {'label': 'Baseline 2 (+ GRU Predict)',        'color': '#f39c12', 'short': 'GRU'},
    'ERGONOMICS':   {'label': 'Proposed System (Adaptive)',        'color': '#2ecc71', 'short': 'Proposed'},
}

SMOOTH_WIN   = 5    # wider smooth to reduce noise in jerk
SKIP_START_S = 3.0  # skip first 3 s (robot startup transient)
SKIP_END_S   = 1.5  # skip last 1.5 s


# ── helpers ─────────────────────────────────────────────────────────────────

def load_trial(path):
    with open(path) as f:
        lines = [l for l in f if not l.strip().startswith('=')]
    rows = list(csv.DictReader(lines))
    cols = {k: [] for k in ('t','mz','hz','rz','hspd','espd','hvel_z','evel_z','w','sr','se')}
    for r in rows:
        try:
            if not r.get('ros_timestamp_ns'): continue
            cols['t'].append(float(r['ros_timestamp_ns'])/1e9)
            cols['mz'].append(float(r.get('meas_z','')    or 'nan'))  # raw camera
            cols['hz'].append(float(r.get('hand_base_z','') or 'nan'))  # transformed target
            cols['rz'].append(float(r.get('robot_ee_z','')  or 'nan'))  # robot actual
            cols['hspd'].append(float(r.get('hand_speed','')  or '0'))
            cols['espd'].append(float(r.get('ee_speed','')    or '0'))
            cols['hvel_z'].append(float(r.get('hand_vel_z','') or '0'))
            cols['evel_z'].append(float(r.get('ee_vel_z','')  or '0'))
            cols['w'].append(float(r.get('adapt_w','')  or '1'))
            cols['sr'].append(float(r.get('adapt_sr','') or '1'))
            cols['se'].append(float(r.get('adapt_se','') or '1'))
        except (ValueError, KeyError):
            continue
    d = {k: np.array(v) for k, v in cols.items()}
    if len(d['t']) > 1:
        d['t'] -= d['t'][0]
    return d


def smooth(sig, w=SMOOTH_WIN):
    if w < 2 or len(sig) < w: return sig
    return np.convolve(sig, np.ones(w)/w, mode='same')


def jerk_from_speed(spd, t):
    dt = np.diff(t); dt[dt == 0] = 0.04
    a  = np.diff(spd)/dt;   a  = np.insert(a,  0, a[0])
    j  = np.diff(a)/dt;     j  = np.insert(j,  0, j[0])
    return smooth(np.abs(j), SMOOTH_WIN)


def vel_z(pos_z, t):
    dt = np.diff(t); dt[dt == 0] = 0.04
    v  = np.diff(pos_z)/dt
    return np.insert(v, 0, v[0])


def detect_motion_window(d, skip_s=SKIP_START_S, end_skip_s=SKIP_END_S):
    """
    Detect sudden hand-raise and lower event window based on hand vertical velocity:
      - Event start: hand_vel_z > 0.15 m/s (sudden upward motion)
      - Event end: after downward motion occurs (hand_vel_z < -0.10 m/s),
                   when velocity settles back to |hand_vel_z| < 0.10 m/s.
    Returns (t_onset, t_peak, t_end) or (None, None, None).
    """
    t  = d['t']
    hz = d['hz']
    # Use hand_vel_z if available, else numerical derivative of target hand z
    hvz = d.get('hvel_z', np.array([]))
    if len(hvz) == 0 or np.all(hvz == 0):
        dt = np.diff(t); dt[dt == 0] = 0.04
        hvz = np.diff(hz) / dt
        hvz = np.insert(hvz, 0, hvz[0])
    hvz = smooth(hvz, 3)

    valid = (t >= skip_s) & (t <= (t[-1] - end_skip_s))
    start_candidates = np.where(valid & (hvz > 0.15))[0]
    if len(start_candidates) == 0:
        return None, None, None

    start_idx = start_candidates[0]

    up_window = np.where((t >= t[start_idx]) & (t <= t[start_idx] + 3.0))[0]
    pk_idx = up_window[np.argmax(hvz[up_window])] if len(up_window) > 0 else start_idx

    lower_candidates = np.where((t > t[start_idx]) & (hvz < -0.06))[0]
    if len(lower_candidates) > 0:
        first_lower = lower_candidates[0]
        settle_candidates = np.where((t > t[first_lower]) & (np.abs(hvz) < 0.06))[0]
        end_idx = settle_candidates[0] if len(settle_candidates) > 0 else len(t) - 1
    else:
        end_candidates = np.where((t > t[start_idx]) & (np.abs(hvz) < 0.06))[0]
        end_idx = end_candidates[0] if len(end_candidates) > 0 else len(t) - 1

    dt_mean = float(np.mean(np.diff(t))) if len(t) > 1 else 0.04
    margin = max(1, int(0.2 / dt_mean))
    on = max(0, start_idx - margin)
    en = min(len(t) - 1, end_idx + margin)

    return t[on], t[pk_idx], t[en]


def detect_jerk_event(hspd, t, skip_s=SKIP_START_S, end_skip_s=SKIP_END_S):
    """Fallback / legacy interface wrapping motion window detection."""
    # This wrapper maintains backwards compatibility if called with (hspd, t)
    hj = jerk_from_speed(hspd, t)
    valid = (t >= skip_s) & (t <= (t[-1] - end_skip_s))
    masked = np.where(valid, hj, 0.0)
    if masked.max() < 2.0:
        return None, None, None
    pk = int(np.argmax(masked))
    dt_mean = float(np.mean(np.diff(t))) if len(t) > 1 else 0.04
    margin = max(1, int(1.5 / dt_mean))
    return t[max(0, pk - margin)], t[pk], t[min(len(t)-1, pk + margin)]


def get_trial_event(d):
    """Retrieve event window using detect_motion_window."""
    to, tp, te = detect_motion_window(d)
    if to is not None:
        return to, tp, te
    return detect_jerk_event(d['hspd'], d['t'])


def load_all(data_dir):
    result = {}
    for mode in BASELINE_MAP:
        files = sorted(glob.glob(os.path.join(data_dir, f'experiment_{mode}_*.csv')))
        trials = [load_trial(f) for f in files if len(load_trial(f)['t']) > 20]
        result[mode] = trials
        print(f'  {mode}: {len(trials)} trials')
    return result


def trial_peak_robot_jerk_in_event(d):
    """Peak robot jerk restricted to the intentional jerk event window."""
    t_on, t_pk, t_en = get_trial_event(d)
    rj = jerk_from_speed(d['espd'], d['t'])
    if t_on is None:
        return float(np.nanmax(rj))
    mask = (d['t'] >= t_on) & (d['t'] <= t_en)
    return float(np.nanmax(rj[mask])) if mask.any() else float(np.nanmax(rj))


def find_representative(trials):
    """Return the trial whose peak robot jerk in event is closest to the median."""
    peaks = [trial_peak_robot_jerk_in_event(d) for d in trials]
    med   = np.median(peaks)
    best  = int(np.argmin(np.abs(np.array(peaks) - med)))
    return trials[best], best


def compute_metrics(d):
    """Metrics restricted to the intentional jerk event window."""
    hj = jerk_from_speed(d['hspd'], d['t'])
    rj = jerk_from_speed(d['espd'], d['t'])
    rvz= vel_z(d['rz'], d['t'])

    t_on, t_pk, t_en = get_trial_event(d)
    if t_on is not None:
        ev = (d['t'] >= t_on) & (d['t'] <= t_en)
    else:
        ev = np.ones(len(d['t']), bool)

    mhj = float(np.nanmean(hj[ev])) if ev.any() else float(np.nanmean(hj))
    mrj = float(np.nanmean(rj[ev])) if ev.any() else float(np.nanmean(rj))
    prj = float(np.nanmax(rj[ev]))  if ev.any() else float(np.nanmax(rj))
    prv = float(np.nanmax(np.abs(rvz[ev]))) if ev.any() else float(np.nanmax(np.abs(rvz)))
    ratio = mrj / mhj if mhj > 1e-6 else 0.0

    return dict(
        peak_robot_jerk=prj, mean_robot_jerk=mrj,
        mean_hand_jerk=mhj,  jerk_ratio=ratio,
        peak_robot_vel_z=prv,
        _hj=hj, _rj=rj, _rvz=rvz, _hvz=vel_z(d['hz'], d['t']),
        _event=(t_on, t_pk, t_en),
    )


def p_stars(p):
    return '***' if p < 0.001 else ('**' if p < 0.01 else ('*' if p < 0.05 else 'n.s.'))


def format_p_val(p):
    if p < 0.001:
        return 'p < 0.001'
    return f'p = {p:.3f}'


# ── figures ──────────────────────────────────────────────────────────────────

def fig1_delta_z(all_data, save_dir):
    """
    Figure 1: Delta-Z position (change from rest) for hand and robot.
    Using delta_z removes the constant hand-EE offset so we can clearly see
    whether the robot follows the jerk (GT/GRU) or is damped (Proposed).
    One representative trial per baseline (median-selected), labelled clearly.
    """
    fig, axes = plt.subplots(3, 1, figsize=(11, 8.5), sharex=False)
    fig.suptitle(
        'Scenario 2: Position Displacement $\\Delta z(t)=z(t)-z_{rest}$\n'
        'during Sudden Hand-Raise & Lower Event  (representative trial ≈ median)',
        fontsize=13, fontweight='bold', y=0.99)

    for idx, mode in enumerate(BASELINE_MAP):
        ax   = axes[idx]
        cfg  = BASELINE_MAP[mode]
        trials = all_data[mode]
        rep, ridx = find_representative(trials)

        # ── rest baseline (first SKIP_START_S seconds) ────────────────
        skip_idx = np.searchsorted(rep['t'], SKIP_START_S)

        if mode == 'GROUND_TRUTH':
            # For Baseline 1 (Camera Only), use meas_z raw camera position as target directly
            mz = rep['mz']
            m_rest = float(np.nanmean(mz[:skip_idx])) if skip_idx > 0 else float(mz[0])
            dh = mz - m_rest
        else:
            h_rest = float(np.nanmean(rep['hz'][:skip_idx])) if skip_idx > 0 else float(rep['hz'][0])
            dh = rep['hz'] - h_rest

        r_rest = float(np.nanmean(rep['rz'][:skip_idx])) if skip_idx > 0 else float(rep['rz'][0])
        dr = rep['rz'] - r_rest

        # ── Hand and Robot EE delta_z ──────────────────────────────────
        ax.plot(rep['t'], dh, '--', color='#2980b9', lw=1.8, label='Hand $\\Delta z$ (target)', alpha=0.9)
        ax.plot(rep['t'], dr, '-',  color=cfg['color'], lw=2.2, label='Robot EE $\\Delta z$ (actual)')

        # ── Motion window shading (velocity-based: raise -> lower) ────
        t_s, t_p, t_e = get_trial_event(rep)
        if t_s is not None:
            ax.axvspan(t_s, t_e, color='#f39c12', alpha=0.12, label='Sudden Motion Event')

        ax.set_ylabel('$\\Delta z$ (m)', fontsize=11)
        ax.set_title(cfg['label'], fontsize=11, fontweight='bold', color=cfg['color'], loc='left')
        ax.legend(loc='upper left', fontsize=8.5, framealpha=0.9, ncol=2)
        ax.grid(True, alpha=0.3)
        ax.set_xlim([0, 14.0])

    axes[-1].set_xlabel('Time (s)', fontsize=11)
    plt.tight_layout()
    path = os.path.join(save_dir, 'fig1_delta_z_response.png')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    print(f'  Saved: {path}')
    plt.close()


def fig2_jerk_event_zoom(all_data, save_dir):
    """
    Figure 2: Jerk profiles across full trial (0 to 14 s).
    Startup transient excluded; peak jerk annotated inside event.
    """
    fig, axes = plt.subplots(3, 1, figsize=(11, 8.5), sharex=False)

    for idx, mode in enumerate(BASELINE_MAP):
        ax  = axes[idx]
        cfg = BASELINE_MAP[mode]
        rep, ridx = find_representative(all_data[mode])
        m   = compute_metrics(rep)
        t_on, t_pk, t_en = m['_event']

        ax.plot(rep['t'], m['_hj'], '--', color='#7f8c8d', lw=1.5, label='Hand Jerk',  alpha=0.7)
        ax.plot(rep['t'], m['_rj'], '-',  color=cfg['color'], lw=2.0, label='Robot Jerk')

        if t_on is not None:
            ax.axvspan(t_on, t_en, color='#e74c3c', alpha=0.12, label='Sudden Motion Event')
            # annotate actual peak inside event
            ev_mask = (rep['t'] >= t_on) & (rep['t'] <= t_en)
            rj_ev   = np.where(ev_mask, m['_rj'], 0.0)
            pk_idx  = int(np.argmax(rj_ev))
            pk_val  = m['_rj'][pk_idx]
            ax.plot(rep['t'][pk_idx], pk_val, 'o', color=cfg['color'], ms=8, zorder=5)
            ax.annotate(f'Peak: {pk_val:.1f} m/s³',
                        (rep['t'][pk_idx], pk_val),
                        xytext=(15, 8), textcoords='offset points',
                        fontsize=9.5, fontweight='bold', color=cfg['color'],
                        arrowprops=dict(arrowstyle='->', color=cfg['color'], lw=1.2))

        ax.set_xlim([5.0, 11.0])
        ax.set_ylim([0, 400])
        ax.set_ylabel('Jerk (m/s³)', fontsize=11)
        ax.set_title(cfg['label'], fontsize=11, fontweight='bold', color=cfg['color'], loc='left')
        ax.legend(loc='upper right', fontsize=9, framealpha=0.9)
        ax.grid(True, alpha=0.3)

    axes[-1].set_xlabel('Time (s)', fontsize=11)
    plt.tight_layout()
    path = os.path.join(save_dir, 'fig2_jerk_event_zoom.png')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    print(f'  Saved: {path}')
    plt.close()


def fig3_adaptive_weights(all_data, save_dir):
    """Figure 3: w / s_r / s_e dynamics for Proposed System during sudden motion event."""
    rep, ridx = find_representative(all_data['ERGONOMICS'])
    m = compute_metrics(rep)
    t_on, t_pk, t_en = m['_event']

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), sharex=True)

    # Top: Velocity Z (shows robot braking)
    hvz_s = smooth(m['_hvz'], 5)
    rvz_s = smooth(m['_rvz'], 5)
    ax1.plot(rep['t'], hvz_s, '--', color='#2980b9', lw=1.5, label='Hand Vel Z', alpha=0.8)
    ax1.plot(rep['t'], rvz_s, '-',  color='#2ecc71', lw=2.2, label='Robot Vel Z')
    ax1.axhline(0, color='gray', lw=0.8, ls=':')

    # Bottom: weights
    ax2.plot(rep['t'], rep['w'],  '-',  color='#9b59b6', lw=2.2, label='Blend weight $w$')
    ax2.plot(rep['t'], rep['sr'], '--', color='#e67e22', lw=1.8,
             label='Prediction reliability $s_r$')
    ax2.plot(rep['t'], rep['se'], ':',  color='#1abc9c', lw=1.8,
             label='Ergonomic comfort $s_e$')

    if t_on is not None:
        for ax in (ax1, ax2):
            ax.axvspan(t_on, t_en, color='#e74c3c', alpha=0.10, label='Sudden Motion Event')

    ax1.set_ylabel('Velocity Z (m/s)', fontsize=11)
    ax1.set_xlim([0, 14.0])
    ax1.legend(fontsize=9, framealpha=0.9)
    ax1.grid(True, alpha=0.3)

    ax2.set_xlabel('Time (s)', fontsize=11)
    ax2.set_ylabel('Parameter value', fontsize=11)
    ax2.set_ylim([-0.05, 1.15])
    ax2.set_xlim([0, 14.0])
    ax2.legend(loc='lower right', fontsize=9, framealpha=0.9)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    path = os.path.join(save_dir, 'fig3_adaptive_weights.png')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    print(f'  Saved: {path}')
    plt.close()


def fig4_boxplot(metrics_by_mode, save_dir):
    """Figure 4: Statistical boxplots with p-values (all N=10 trials/baseline)."""
    fig, axes = plt.subplots(1, 3, figsize=(14, 5.0))

    keys = [
        ('peak_robot_jerk', 'Peak Robot Jerk\n(m/s³)',   'Lower = safer'),
        ('mean_robot_jerk', 'Mean Robot Jerk\n(m/s³)',   'Lower = smoother'),
        ('jerk_ratio',      'Jerk Transfer Ratio\n($J_{robot}/J_{hand}$)', 'Lower = better attenuation'),
    ]
    modes = list(BASELINE_MAP.keys())

    for ai, (key, ylabel, note) in enumerate(keys):
        ax  = axes[ai]
        bdata  = [[m[key] for m in metrics_by_mode[md]] for md in modes]
        labels = [BASELINE_MAP[m]['short'] for m in modes]
        colors = [BASELINE_MAP[m]['color'] for m in modes]

        bp = ax.boxplot(bdata, labels=labels, patch_artist=True, widths=0.45,
                        medianprops=dict(color='black', linewidth=2.2))
        for patch, c in zip(bp['boxes'], colors):
            patch.set_facecolor(c); patch.set_alpha(0.72)

        for i, (vals, c) in enumerate(zip(bdata, colors)):
            jx = np.random.default_rng(42).normal(i+1, 0.04, len(vals))
            ax.scatter(jx, vals, color=c, edgecolors='black', s=38, zorder=5, alpha=0.9)

        # p-values: Proposed vs GT, Proposed vs GRU
        _, p_gt  = stats.ttest_ind(bdata[2], bdata[0], equal_var=False)
        _, p_gru = stats.ttest_ind(bdata[2], bdata[1], equal_var=False)
        ymax = max(max(v) for v in bdata)
        hs   = ymax * 0.09

        # GT vs Proposed
        ax.plot([1, 3], [ymax+hs,   ymax+hs],   color='#333', lw=1.1)
        ax.text(2, ymax+hs*1.15, f'{p_stars(p_gt)} ({format_p_val(p_gt)})',
                ha='center', va='bottom', fontsize=8.5, fontweight='bold')
        # GRU vs Proposed
        ax.plot([2, 3], [ymax+hs*2.1, ymax+hs*2.1], color='#555', lw=1.0, ls='--')
        ax.text(2.5, ymax+hs*2.25, f'{p_stars(p_gru)} ({format_p_val(p_gru)})',
                ha='center', va='bottom', fontsize=8, color='#555')

        ax.set_ylabel(ylabel, fontsize=10)
        ax.set_title(note, fontsize=9, fontstyle='italic', color='#555555')
        ax.grid(True, axis='y', alpha=0.3)
        ax.set_ylim(bottom=0, top=ymax + hs*3.2)

    plt.tight_layout()
    path = os.path.join(save_dir, 'fig4_boxplot_comparison.png')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    print(f'  Saved: {path}')
    plt.close()


def export_latex(metrics_by_mode, save_dir):
    keys = [
        ('peak_robot_jerk', 'Peak Robot Jerk (m/s$^3$)'),
        ('mean_robot_jerk', 'Mean Robot Jerk (m/s$^3$)'),
        ('jerk_ratio',      'Jerk Transfer Ratio'),
        ('peak_robot_vel_z','Peak Robot $|v_z|$ (m/s)'),
    ]
    rows = []
    print('\n' + '='*85)
    print('SCENARIO 2  —  Metrics within intentional jerk event  (N=10 trials/baseline)')
    print('='*85)
    print(f'{"Metric":<30} {"GT (μ±σ)":<20} {"GRU (μ±σ)":<20} {"Proposed (μ±σ)":<20} p(vs GT)')
    print('-'*85)
    for key, name in keys:
        g = [m[key] for m in metrics_by_mode['GROUND_TRUTH']]
        u = [m[key] for m in metrics_by_mode['GRU']]
        p = [m[key] for m in metrics_by_mode['ERGONOMICS']]
        pv = stats.ttest_ind(p, g, equal_var=False).pvalue
        print(f'{name:<30} {np.mean(g):>6.3f}±{np.std(g):<6.3f}  '
              f'{np.mean(u):>6.3f}±{np.std(u):<6.3f}  '
              f'{np.mean(p):>6.3f}±{np.std(p):<6.3f}  p={pv:.4f}')
        rows.append((name, g, u, p, pv))
    print('='*85)

    ltx = [r'\begin{table}[htbp]', r'\centering',
           r'\caption{Jerk Safety Metrics within Intentional Jerk Event (Scenario~2)}',
           r'\label{tab:s2_jerk}',
           r'\begin{tabular}{lcccc}', r'\toprule',
           r'\textbf{Metric} & \textbf{Baseline~1} & \textbf{Baseline~2} '
           r'& \textbf{Proposed} & \textbf{$p$-value} \\', r'\midrule']
    for name, g, u, p, pv in rows:
        s = p_stars(pv)
        ps = f'$<0.001^{{{s}}}$' if pv < 0.001 else f'${pv:.3f}^{{{s}}}$'
        ltx.append(f'{name} & ${np.mean(g):.3f}\\pm{np.std(g):.3f}$ '
                   f'& ${np.mean(u):.3f}\\pm{np.std(u):.3f}$ '
                   f'& $\\mathbf{{{np.mean(p):.3f}\\pm{np.std(p):.3f}}}$ & {ps} \\\\')
    ltx += [r'\bottomrule', r'\end{tabular}', r'\end{table}']

    out = os.path.join(save_dir, 'scenario2_table.tex')
    with open(out, 'w') as f:
        f.write('\n'.join(ltx))
    print(f'  LaTeX → {out}')


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('data_dir')
    ap.add_argument('--save-dir', default=None)
    args = ap.parse_args()
    save_dir = args.save_dir or args.data_dir
    os.makedirs(save_dir, exist_ok=True)

    print(f'Loading trials from {args.data_dir}')
    all_data = load_all(args.data_dir)
    for mode in BASELINE_MAP:
        if not all_data[mode]:
            print(f'ERROR: no trials for {mode}'); return

    print('\nComputing metrics (event-restricted)...')
    mbm = {md: [compute_metrics(d) for d in all_data[md]] for md in BASELINE_MAP}

    print('\nGenerating figures...')
    fig1_delta_z(all_data, save_dir)
    fig2_jerk_event_zoom(all_data, save_dir)
    fig3_adaptive_weights(all_data, save_dir)
    fig4_boxplot(mbm, save_dir)
    export_latex(mbm, save_dir)

    print('\n✓ Done!')

if __name__ == '__main__':
    main()
