# ICTA Shared Control Framework

This repository contains the implementation of the **Integrated Collaborative Trajectory Adaptation (ICTA)** framework for human-robot co-carrying tasks using the Yaskawa HC10DTP cobot. 

The framework is designed to seamlessly blend predicted human trajectories with real-time feedback and ergonomics data (RULA) to ensure smooth, safe, and comfortable shared control.

## System Architecture

The ICTA framework is implemented as an add-on module to the existing `CartesianStreamer` node. It intercepts the stream of trajectories and processes them through 6 core modules before sending joint commands down to the hardware queue mode.

### Data Flow
1. **Camera/Hand Tracking**: 
   - Uses MediaPipe to track hand position.
   - `transform_node.py` transforms raw hand positions (`/coord_transform/filtered_hand_position`) into the robot's base frame (`/cartesian_streamer/hand_base_pose`).
   - Supports 3 modes: `prediction` (GRU model), `ground_truth` (raw camera), and `ergonomics` (ICTA adaptive blending).
2. **Trajectory Prediction**:
   - `predictor_node.py` uses a Deep-GRU model to forecast future hand positions.
   - Output published to `/cartesian_streamer/target_pose` as $p_{pre}$.
3. **Ergonomics Evaluation**:
   - External nodes calculate RULA scores and publish arm joint angles to `/rula_scores`.
4. **Streamer Core**:
   - `cartesian_streamer_hc10dtp.py` handles IK and queue communications.
   - When launched with `--adaptive`, it integrates the `AdaptiveSharedControl` module.

### Core Modules (`adaptive_shared_control.py`)
- **Module A (Prediction Reliability - $s_r$)**: Evaluates how closely the actual hand follows the predicted trajectory over a sliding window.
- **Module B (Arm Comfort Score - $s_e$)**: Uses Mahalanobis distance to evaluate real-time human arm angles against optimal RULA joint angles (based on paper 1805.06270v3).
- **Module C (Adaptive Weight Generator - $w$)**: A fuzzy-like blending mechanism that calculates a smooth weight parameter based on $s_r$ and $s_e$.
- **Module D (Trajectory Smoother)**: Blends the predicted trajectory ($p_{pre}$) with the robot's current position ($p_{fb}$) using the adaptive weight $w$ to produce a smooth, safe target $p_{smooth}$.
- **Module E (Kinematics Constraint Solver)**: Evaluates structural limits (currently handled by the Streamer's Local IK solver).
- **Module F (LQR Velocity Controller)**: Replaces finite-difference velocity calculations with an optimized Linear Quadratic Regulator (LQR) derived via DARE (Discrete Algebraic Riccati Equation), ensuring minimum-jerk velocity profiles.

## Usage

### 1. Standard Operation
To run the standard system (prediction or ground truth) without adaptive blending:
```bash
ros2 run hc10dtp_bringup cartesian_streamer
```

### 2. ICTA Adaptive Mode
To enable the full ICTA framework with LQR and Ergonomics blending:
```bash
ros2 run hc10dtp_bringup cartesian_streamer --adaptive
```

In the UI or control panel, set the transform node mode to `ergonomics`:
```bash
ros2 topic pub /coord_transform/mode std_msgs/String "data: 'ergonomics'" -1
```

### 3. Monitoring Adaptive Status
The adaptive parameters ($w$, $s_r$, $s_e$) are published in real-time for logging and monitoring:
```bash
ros2 topic echo /cartesian_streamer/adaptive_status
```
*(Array format: [weight, reliability, comfort])*

### 4. Running the Full Experimental System
To conduct a complete experiment with data logging and real-time visualization (e.g., using RViz simulation or the real robot):

1. **Start the Robot/Simulation & Camera Tracking:**
   Launch the robot bringup (or RViz) and the realsense tracking nodes according to your standard workspace setup.

2. **Start the RULA Tracker:**
   ```bash
   ros2 run rula_tracker rula_tracker_node --ros-args -p model_path:=/path/to/pose_landmarker.task
   ```

3. **Start the ICTA Adaptive Streamer:**
   ```bash
   ros2 run hc10dtp_bringup cartesian_streamer --adaptive
   ```

4. **Start the ML Predictor (if using prediction mode):**
   ```bash
   ros2 run ml_inference predictor_node
   ```

5. **Launch the Dashboard UI:**
   Displays 3D trajectory tracking and the real-time Ergonomics & Adaptive Control chart ($s_e$, $w$, RULA total).
   ```bash
   ros2 run predictor_ui predictor_ui
   ```

6. **Start the Experiment Logger:**
   Listens to `/joint_states`, `/rula_scores`, `/cartesian_streamer/adaptive_status`, and trajectory data. Records 43 columns of data to CSV for offline analysis.
   ```bash
   ros2 run experiment_logger logger
   ```

## Tuning Parameters
If the LQR or Blending is too aggressive or sluggish, you can tune the parameters directly in `adaptive_shared_control.py`:
- `window_size` (Module A): The number of samples for deviation tracking.
- `Q` and `R` matrices (Module F): Adjust the penalty for position error vs velocity jerk.

## Citation & References
- Optimal RULA posture values are derived from academic literature on ergonomic human-robot collaboration (e.g., 1805.06270v3).
- System kinematics solver integrated tightly with Yaskawa MotoROS2.
