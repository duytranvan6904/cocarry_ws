#!/usr/bin/env python3
"""
analyze_latency.py — Onset Detection method
────────────────────────────────────────────
Measures system latency by detecting individual movement bursts in the
hand-tracking signal and finding the corresponding onset in the robot
(and predictor) signals.

Method:
  1. Resample all signals to uniform 100 Hz grid.
  2. Compute velocity magnitude for hand, predictor, and robot.
  3. Smooth velocities with a moving-average window to suppress noise.
  4. Detect "movement bursts" in the hand signal (velocity > threshold).
  5. For each burst, find the onset time in the robot/predictor signal
     within a search window after the hand onset.
  6. Compute delay = t_robot_onset - t_hand_onset for each burst.
  7. Report statistics (mean, median, std, min, max, percentiles).

This is much more reliable than cross-correlation because:
  - Each burst gives an independent delay sample.
  - Stationary periods are ignored entirely.
  - Outlier bursts (no response) are flagged and excluded.
"""
import os
import sys
import csv
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
        except (ValueError, KeyError):
            continue

    # Convert lists to numpy arrays
    for key in data:
        data[key] = np.array(data[key])

    return data


def moving_average(signal, window_size):
    """Smooth a signal with a moving average filter."""
    if window_size < 2:
        return signal
    kernel = np.ones(window_size) / window_size
    # Use 'same' mode and handle edges
    smoothed = np.convolve(signal, kernel, mode='same')
    return smoothed


def compute_velocity_magnitude(x, y, z, dt):
    """Compute 3D velocity magnitude from position arrays."""
    vx = np.diff(x) / dt
    vy = np.diff(y) / dt
    vz = np.diff(z) / dt
    return np.sqrt(vx**2 + vy**2 + vz**2)


def find_movement_bursts(velocity, dt, threshold, min_duration_s=0.15,
                         min_gap_s=0.3):
    """
    Detect movement bursts in a velocity signal.

    Returns a list of (start_idx, end_idx) tuples for each burst.

    Parameters:
        velocity:       velocity magnitude array
        dt:             sampling period (seconds)
        threshold:      velocity threshold to consider "moving" (m/s)
        min_duration_s: minimum burst duration to keep (seconds)
        min_gap_s:      minimum gap between bursts; closer bursts are merged
    """
    above = velocity > threshold
    min_dur = int(min_duration_s / dt)
    min_gap = int(min_gap_s / dt)

    # Find contiguous regions above threshold
    bursts = []
    in_burst = False
    start = 0
    for i in range(len(above)):
        if above[i] and not in_burst:
            start = i
            in_burst = True
        elif not above[i] and in_burst:
            bursts.append((start, i - 1))
            in_burst = False
    if in_burst:
        bursts.append((start, len(above) - 1))

    if not bursts:
        return []

    # Merge bursts that are too close together
    merged = [bursts[0]]
    for s, e in bursts[1:]:
        prev_s, prev_e = merged[-1]
        if s - prev_e < min_gap:
            merged[-1] = (prev_s, e)
        else:
            merged.append((s, e))

    # Filter out bursts that are too short
    filtered = [(s, e) for s, e in merged if (e - s) >= min_dur]

    return filtered


def find_onset_time(velocity, start_search_idx, end_search_idx, threshold):
    """
    Find the first index where velocity crosses above threshold
    within the search range [start_search_idx, end_search_idx].

    Returns the index, or None if not found.
    """
    for i in range(max(0, start_search_idx), min(len(velocity), end_search_idx)):
        if velocity[i] > threshold:
            return i
    return None


def analyze_latency(data, plot_path=None, is_ground_truth=False):
    t = data['t']
    if len(t) < 10:
        print("Error: Too few samples in CSV file.")
        return

    # Subtract start time to start at 0
    t = t - t[0]

    # ── 1. Resample to uniform 100 Hz grid ──
    dt = 0.01  # 10 ms
    t_uniform = np.arange(t[0], t[-1], dt)
    N = len(t_uniform)

    hx_uni = np.interp(t_uniform, t, data['hx'])
    hy_uni = np.interp(t_uniform, t, data['hy'])
    hz_uni = np.interp(t_uniform, t, data['hz'])

    px_uni = np.interp(t_uniform, t, data['px'])
    py_uni = np.interp(t_uniform, t, data['py'])
    pz_uni = np.interp(t_uniform, t, data['pz'])

    rx_uni = np.interp(t_uniform, t, data['rx'])
    ry_uni = np.interp(t_uniform, t, data['ry'])
    rz_uni = np.interp(t_uniform, t, data['rz'])

    # ── 2. Compute velocity magnitudes ──
    v_hand = compute_velocity_magnitude(hx_uni, hy_uni, hz_uni, dt)
    v_pred = compute_velocity_magnitude(px_uni, py_uni, pz_uni, dt)
    v_robot = compute_velocity_magnitude(rx_uni, ry_uni, rz_uni, dt)

    # ── 3. Smooth velocities to suppress noise ──
    smooth_window = 7  # 70ms moving average
    v_hand_smooth = moving_average(v_hand, smooth_window)
    v_pred_smooth = moving_average(v_pred, smooth_window)
    v_robot_smooth = moving_average(v_robot, smooth_window)

    # ── 4. Determine adaptive threshold ──
    # Use a percentile-based threshold: movement = top portion of velocity
    hand_baseline = np.percentile(v_hand_smooth, 60)
    hand_peak = np.percentile(v_hand_smooth, 95)
    # Threshold is between baseline and peak
    hand_threshold = hand_baseline + 0.3 * (hand_peak - hand_baseline)
    hand_threshold = max(hand_threshold, 0.015)  # absolute minimum 15 mm/s

    # Robot threshold: lower because robot moves slower/smoother
    robot_baseline = np.percentile(v_robot_smooth, 60)
    robot_peak = np.percentile(v_robot_smooth, 95)
    robot_threshold = robot_baseline + 0.25 * (robot_peak - robot_baseline)
    robot_threshold = max(robot_threshold, 0.005)  # absolute minimum 5 mm/s

    # Predictor threshold: similar to hand
    pred_baseline = np.percentile(v_pred_smooth, 60)
    pred_peak = np.percentile(v_pred_smooth, 95)
    pred_threshold = pred_baseline + 0.3 * (pred_peak - pred_baseline)
    pred_threshold = max(pred_threshold, 0.010)

    # ── 5. Detect movement bursts in hand signal ──
    bursts = find_movement_bursts(v_hand_smooth, dt, hand_threshold,
                                  min_duration_s=0.15, min_gap_s=0.3)

    # ── 6. For each burst, measure onset delays ──
    max_search_s = 2.0  # search up to 2s after hand onset
    max_search_samples = int(max_search_s / dt)

    delays_hand_robot = []
    delays_hand_pred = []
    delays_pred_robot = []
    burst_details = []  # for plotting/debugging

    time_axis = t_uniform[:-1]  # velocity arrays are 1 shorter than position

    for burst_idx, (burst_start, burst_end) in enumerate(bursts):
        # Hand onset: first crossing of threshold in this burst
        hand_onset = burst_start

        # Search for robot onset after hand onset
        search_end = min(burst_start + max_search_samples, len(v_robot_smooth))
        robot_onset = find_onset_time(v_robot_smooth, burst_start,
                                      search_end, robot_threshold)

        # Search for predictor onset
        pred_onset = find_onset_time(v_pred_smooth, max(0, burst_start - 50),
                                     search_end, pred_threshold)

        # Compute delays
        delay_hr = None
        delay_hp = None
        delay_pr = None

        if robot_onset is not None:
            delay_hr = (robot_onset - hand_onset) * dt
            delays_hand_robot.append(delay_hr)

        if pred_onset is not None:
            delay_hp = (pred_onset - hand_onset) * dt
            delays_hand_pred.append(delay_hp)

        if robot_onset is not None and pred_onset is not None:
            delay_pr = (robot_onset - pred_onset) * dt
            delays_pred_robot.append(delay_pr)

        burst_details.append({
            'burst_idx': burst_idx + 1,
            'hand_onset_t': time_axis[hand_onset],
            'robot_onset_t': time_axis[robot_onset] if robot_onset else None,
            'pred_onset_t': time_axis[pred_onset] if pred_onset else None,
            'delay_hr': delay_hr,
            'delay_hp': delay_hp,
            'delay_pr': delay_pr,
            'burst_start': burst_start,
            'burst_end': burst_end,
        })

    # ── 7. Report Results ──
    delays_hand_robot = np.array(delays_hand_robot)
    delays_hand_pred = np.array(delays_hand_pred)
    delays_pred_robot = np.array(delays_pred_robot)

    print("\n" + "=" * 60)
    print("     LATENCY MEASUREMENT — Onset Detection Method")
    print("=" * 60)
    print(f"Total samples: {N} | Duration: {t_uniform[-1]:.1f}s | "
          f"Rate: {1/dt:.0f} Hz")
    print(f"Movement bursts detected: {len(bursts)}")
    if is_ground_truth:
        print(f"Thresholds — Hand: {hand_threshold*1000:.1f} mm/s | "
              f"Robot: {robot_threshold*1000:.1f} mm/s")
    else:
        print(f"Thresholds — Hand: {hand_threshold*1000:.1f} mm/s | "
              f"Robot: {robot_threshold*1000:.1f} mm/s | "
              f"Pred: {pred_threshold*1000:.1f} mm/s")

    # Per-burst detail table
    print("-" * 60)
    if is_ground_truth:
        print(f"{'Burst':>5} | {'Hand onset':>10} | {'Robot onset':>11} | "
              f"{'H→R Delay':>9}")
    else:
        print(f"{'Burst':>5} | {'Hand onset':>10} | {'Robot onset':>11} | "
              f"{'H→R Delay':>9} | {'H→P Delay':>9} | {'P→R Delay':>9}")
    print("-" * 60)
    for d in burst_details:
        h_t = f"{d['hand_onset_t']:.2f}s"
        r_t = f"{d['robot_onset_t']:.2f}s" if d['robot_onset_t'] is not None else "  N/A"
        d_hr = f"{d['delay_hr']*1000:.0f} ms" if d['delay_hr'] is not None else "  N/A"
        d_hp = f"{d['delay_hp']*1000:.0f} ms" if d['delay_hp'] is not None else "  N/A"
        d_pr = f"{d['delay_pr']*1000:.0f} ms" if d['delay_pr'] is not None else "  N/A"
        
        if is_ground_truth:
            print(f"  #{d['burst_idx']:>3} | {h_t:>10} | {r_t:>11} | {d_hr:>9}")
        else:
            print(f"  #{d['burst_idx']:>3} | {h_t:>10} | {r_t:>11} | "
                  f"{d_hr:>9} | {d_hp:>9} | {d_pr:>9}")

    # Summary statistics
    print("=" * 60)

    def print_stats(name, delays_arr):
        if len(delays_arr) == 0:
            print(f"\n  {name}:")
            print(f"    No valid measurements.")
            return
        ms = delays_arr * 1000  # convert to ms
        print(f"\n  {name} ({len(ms)} samples):")
        print(f"    Mean:   {np.mean(ms):>8.0f} ms")
        print(f"    Median: {np.median(ms):>8.0f} ms")
        print(f"    Std:    {np.std(ms):>8.0f} ms")
        print(f"    Min:    {np.min(ms):>8.0f} ms")
        print(f"    Max:    {np.max(ms):>8.0f} ms")
        if len(ms) >= 4:
            print(f"    P25:    {np.percentile(ms, 25):>8.0f} ms")
            print(f"    P75:    {np.percentile(ms, 75):>8.0f} ms")

    print("\n── SUMMARY STATISTICS ──")
    if is_ground_truth:
        print("  (Note: Predictor metrics are hidden in Ground Truth mode)")
    print_stats("1. Hand → Robot (Total End-to-End Delay)", delays_hand_robot)
    
    if not is_ground_truth:
        print_stats("2. Hand → Predictor (Model Phase Shift)", delays_hand_pred)
        print_stats("3. Predictor → Robot (Tracking Delay)", delays_pred_robot)
    print("=" * 60)

    # ── 8. Visual Plotting ──
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches

        fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=False)

        # --- Plot 1: Velocity profiles with burst regions highlighted ---
        ax1 = axes[0]
        ax1.plot(time_axis, v_hand_smooth, label='Hand velocity (smoothed)',
                 color='#1f77b4', alpha=0.9, linewidth=1.2)
        if not is_ground_truth:
            ax1.plot(time_axis, v_pred_smooth, label='Predictor velocity (smoothed)',
                     color='#2ca02c', alpha=0.7, linewidth=1.0)
        ax1.plot(time_axis, v_robot_smooth, label='Robot velocity (smoothed)',
                 color='#d62728', alpha=0.7, linewidth=1.0)

        # Mark burst regions
        for d in burst_details:
            s, e = d['burst_start'], d['burst_end']
            ax1.axvspan(time_axis[s], time_axis[min(e, len(time_axis)-1)],
                        alpha=0.12, color='#1f77b4')

        # Mark onset points
        for d in burst_details:
            ax1.axvline(x=d['hand_onset_t'], color='#1f77b4',
                        linestyle=':', alpha=0.5, linewidth=0.8)
            if d['robot_onset_t'] is not None:
                ax1.axvline(x=d['robot_onset_t'], color='#d62728',
                            linestyle=':', alpha=0.5, linewidth=0.8)

        ax1.axhline(y=hand_threshold, color='#1f77b4', linestyle='--',
                     alpha=0.4, label=f'Hand threshold ({hand_threshold*1000:.1f} mm/s)')
        ax1.axhline(y=robot_threshold, color='#d62728', linestyle='--',
                     alpha=0.4, label=f'Robot threshold ({robot_threshold*1000:.1f} mm/s)')

        ax1.set_title("Velocity Profiles & Movement Burst Detection")
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("Speed (m/s)")
        ax1.legend(loc='upper right', fontsize=8)
        ax1.grid(True, alpha=0.3)

        # --- Plot 2: Per-burst delay bar chart ---
        ax2 = axes[1]
        if burst_details:
            burst_nums = [d['burst_idx'] for d in burst_details]
            hr_delays = [d['delay_hr'] * 1000 if d['delay_hr'] is not None
                         else 0 for d in burst_details]
            pr_delays = [d['delay_pr'] * 1000 if d['delay_pr'] is not None
                         else 0 for d in burst_details]

            x_pos = np.arange(len(burst_nums))
            bar_w = 0.35
            
            if is_ground_truth:
                bars1 = ax2.bar(x_pos, hr_delays, bar_w,
                                label='Hand → Robot', color='#1f77b4', alpha=0.8)
            else:
                bars1 = ax2.bar(x_pos - bar_w/2, hr_delays, bar_w,
                                label='Hand → Robot', color='#1f77b4', alpha=0.8)
                bars2 = ax2.bar(x_pos + bar_w/2, pr_delays, bar_w,
                                label='Pred → Robot', color='#2ca02c', alpha=0.8)

            # Add value labels on bars
            for bar in bars1:
                h = bar.get_height()
                if h > 0:
                    ax2.text(bar.get_x() + bar.get_width()/2, h + 10,
                             f'{h:.0f}', ha='center', va='bottom', fontsize=7)
            
            if not is_ground_truth:
                for bar in bars2:
                    h = bar.get_height()
                    if h > 0:
                        ax2.text(bar.get_x() + bar.get_width()/2, h + 10,
                                 f'{h:.0f}', ha='center', va='bottom', fontsize=7)

            # Draw mean lines
            if len(delays_hand_robot) > 0:
                ax2.axhline(y=np.mean(delays_hand_robot)*1000, color='#1f77b4',
                            linestyle='--', alpha=0.6,
                            label=f'Mean H→R: {np.mean(delays_hand_robot)*1000:.0f} ms')
            
            if not is_ground_truth and len(delays_pred_robot) > 0:
                ax2.axhline(y=np.mean(delays_pred_robot)*1000, color='#2ca02c',
                            linestyle='--', alpha=0.6,
                            label=f'Mean P→R: {np.mean(delays_pred_robot)*1000:.0f} ms')

            ax2.set_xticks(x_pos)
            ax2.set_xticklabels([f'#{n}' for n in burst_nums])
            ax2.set_xlabel("Movement Burst")
            ax2.set_ylabel("Delay (ms)")
            ax2.set_title("Per-Burst Onset Delays")
            ax2.legend(fontsize=8)
            ax2.grid(True, axis='y', alpha=0.3)

        # --- Plot 3: Zoomed view of a representative burst ---
        ax3 = axes[2]
        # Pick the burst with the median delay for representative view
        if len(delays_hand_robot) > 0:
            valid_bursts = [d for d in burst_details if d['delay_hr'] is not None]
            if valid_bursts:
                # Sort by delay and pick the middle one
                sorted_bursts = sorted(valid_bursts, key=lambda x: x['delay_hr'])
                rep = sorted_bursts[len(sorted_bursts) // 2]

                # Show ±0.5s around the burst
                margin = int(0.5 / dt)
                zoom_s = max(0, rep['burst_start'] - margin)
                zoom_e = min(len(time_axis) - 1, rep['burst_end'] + margin)

                ax3.plot(time_axis[zoom_s:zoom_e],
                         v_hand_smooth[zoom_s:zoom_e],
                         label='Hand', color='#1f77b4', linewidth=1.5)
                ax3.plot(time_axis[zoom_s:zoom_e],
                         v_pred_smooth[zoom_s:zoom_e],
                         label='Predictor', color='#2ca02c', linewidth=1.5)
                ax3.plot(time_axis[zoom_s:zoom_e],
                         v_robot_smooth[zoom_s:zoom_e],
                         label='Robot', color='#d62728', linewidth=1.5)

                # Mark onsets with vertical lines and annotations
                ax3.axvline(x=rep['hand_onset_t'], color='#1f77b4',
                            linestyle='-', linewidth=2, alpha=0.8,
                            label=f'Hand onset: {rep["hand_onset_t"]:.2f}s')
                if rep['robot_onset_t'] is not None:
                    ax3.axvline(x=rep['robot_onset_t'], color='#d62728',
                                linestyle='-', linewidth=2, alpha=0.8,
                                label=f'Robot onset: {rep["robot_onset_t"]:.2f}s')

                    # Draw delay arrow
                    y_arrow = max(v_hand_smooth[zoom_s:zoom_e]) * 0.85
                    ax3.annotate('', xy=(rep['robot_onset_t'], y_arrow),
                                 xytext=(rep['hand_onset_t'], y_arrow),
                                 arrowprops=dict(arrowstyle='<->',
                                                 color='black', lw=1.5))
                    mid_t = (rep['hand_onset_t'] + rep['robot_onset_t']) / 2
                    ax3.text(mid_t, y_arrow * 1.05,
                             f"Delay: {rep['delay_hr']*1000:.0f} ms",
                             ha='center', fontsize=9, fontweight='bold')

                ax3.set_title(f"Zoom: Burst #{rep['burst_idx']} "
                              f"(Median delay)")
                ax3.set_xlabel("Time (s)")
                ax3.set_ylabel("Speed (m/s)")
                ax3.legend(fontsize=8)
                ax3.grid(True, alpha=0.3)

        plt.tight_layout()
        if plot_path:
            plt.savefig(plot_path, dpi=150)
            print(f"\nSaved plot to: {plot_path}")
        else:
            plt.show()

    except ImportError:
        print("\nNote: matplotlib not installed. Skipping plot.")


def get_latest_csv(log_dir):
    if not os.path.exists(log_dir):
        return None
    files = [os.path.join(log_dir, f) for f in os.listdir(log_dir)
             if f.endswith('.csv')]
    if not files:
        return None
    # Sort by modification time
    return max(files, key=os.path.getmtime)


def main():
    parser = argparse.ArgumentParser(
        description="Measure hand-to-robot latency using Onset Detection.")
    parser.add_argument("--csv",
                        help="Path to specific CSV file. "
                             "If omitted, uses latest file in log directory.")
    parser.add_argument("--dir",
                        default=os.path.expanduser(
                            "~/cocarry_ws/cocarry_logs"),
                        help="Logs directory to search in.")
    parser.add_argument("--plot",
                        help="Save plot to file (e.g. latency.png) "
                             "instead of displaying interactively.")

    args = parser.parse_args()

    csv_file = args.csv
    if not csv_file:
        # Try workspace logs, fallback to home directories
        csv_file = get_latest_csv(args.dir)
        if not csv_file:
            csv_file = get_latest_csv(os.path.expanduser("~/cocarry_logs"))
        if not csv_file:
            csv_file = get_latest_csv(os.path.expanduser("~/hrc_logs"))

    if not csv_file or not os.path.exists(csv_file):
        print("Error: No CSV log files found. Please specify path with --csv.")
        sys.exit(1)

    data = load_csv(csv_file)
    
    is_ground_truth = "ground_truth" in os.path.basename(csv_file).lower()
    analyze_latency(data, args.plot, is_ground_truth)


if __name__ == "__main__":
    main()
