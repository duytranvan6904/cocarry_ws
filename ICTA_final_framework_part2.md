# ICTA — Final Framework (Part 2: Modules E–F, Stability, Summary)

> Continuation from Part 1 (Modules A–D).

---

## Module E — Inverse Kinematics (DLS + Quaternion)

### E.1 Purpose

Convert the smoothed Cartesian command p_smooth(t) ∈ ℝ³ into joint-space reference q_ref(t) ∈ ℝ⁶ for the 6-DOF HC10DTP. Orientation is maintained via unit quaternion representation to avoid gimbal lock [10].

### E.2 Forward Kinematics

Kinematic chain from URDF (6 revolute joints):

```
T(q) = T₁(q₁) · T₂(q₂) · T₃(q₃) · T₄(q₄) · T₅(q₅) · T₆(q₆) · T_tool0  ∈ SE(3)   (E1)
```

- **T(q) ∈ ℝ^{4×4}**: homogeneous transformation matrix (base_link → tool0)
- **q = [q₁, ..., q₆]ᵀ ∈ ℝ⁶**: joint angles (radians)
- Joint axes: J1(Z), J2(Y), J3(−Y), J4(Z), J5(−Y), J6(Z)

Position: **p(q) = T(q)[1:3, 4] ∈ ℝ³**

Orientation: **R(q) = T(q)[1:3, 1:3] ∈ SO(3)** → converted to quaternion Q = [x, y, z, w] via Shepperd's algorithm [11].

### E.3 Pose Error

**Position error**:

```
e_pos(t) = p_target(t) − p_current(t)  ∈ ℝ³                                 (E2)
```

**Orientation error** via SO(3) logarithmic map [10]:

```
e_ori(t) = log_SO3(R_target · R_currentᵀ)  ∈ ℝ³                             (E3)
```

where log_SO3 extracts the rotation vector (axis × angle) from the relative rotation matrix. This avoids singularities inherent in Euler angle representations.

**Combined 6D error** (position prioritized):

```
e(t) = [e_pos(t); 0.5 · e_ori(t)]  ∈ ℝ⁶                                    (E4)
```

The 0.5 scaling on orientation reduces its influence relative to position tracking — appropriate for co-carrying where end-effector position is critical.

### E.4 Numerical Jacobian

```
J ∈ ℝ^{6×6}                                                                  (E5)
```

Computed by forward finite differences with step ε_J = 10⁻⁷:

```
J[1:3, i] = (p(q + ε_J·eᵢ) − p(q)) / ε_J            (position rows)       (E6)
J[4:6, i] = log_SO3(R(q + ε_J·eᵢ) · R(q)ᵀ) / ε_J    (orientation rows)    (E7)
```

where eᵢ ∈ ℝ⁶ is the i-th unit vector.

### E.5 Damped Least Squares (DLS) Update [12]

```
Δq = Jᵀ(JJᵀ + λ_DLS² · I₆)⁻¹ · e  ∈ ℝ⁶                                   (E8)
```

- **J ∈ ℝ^{6×6}**: Jacobian at current q
- **JJᵀ ∈ ℝ^{6×6}**: manipulability matrix
- **λ_DLS² · I₆ ∈ ℝ^{6×6}**: damping regularization (prevents singularity)
- **λ_DLS = 0.01**: damping factor

DLS is equivalent to Tikhonov regularization and ensures well-conditioned inversion even near kinematic singularities [12].

**Update with joint clamping**:

```
q ← clip(q + α_IK · Δq, q_min, q_max)                                      (E9)
```

- **α_IK = 1.0**: step size (full Newton step)
- **q_min, q_max ∈ ℝ⁶**: soft joint limits (tighter than URDF, specific to co-carrying)

Iterate E5–E9 until ‖e_pos‖ < 0.5 mm and ‖e_ori‖ < 0.01 rad, or max 50 iterations.

### E.6 Per-Axis Delta Clamping (Safety)

After IK convergence, limit the step from the previous command:

```
Δq_i = clip(q_ref_i − q_prev_i, −Δq_max_i, +Δq_max_i),   i = 1,...,6       (E10)
q_ref_i = q_prev_i + Δq_i
```

| Joint | Δq_max (rad/tick) | Equivalent max velocity |
|-------|-------------------|------------------------|
| J1–J3 | 0.07 | 0.07 × 15 = 1.05 rad/s |
| J4–J6 | 0.09 | 0.09 × 15 = 1.35 rad/s |

### E.7 Performance

| Metric | Value | Source |
|--------|-------|--------|
| FK time | ~0.02 ms | local_ik_solver benchmark |
| IK time (near seed) | 0.3–1.0 ms | local_ik_solver benchmark |
| Position accuracy | < 0.5 mm | Convergence tolerance |

### E.8 References

- [10] Siciliano, B., et al., "Robotics: Modelling, Planning and Control," *Springer*, 2009, Ch. 3. — Quaternion representation and SO(3) logarithmic map.
- [11] Shepperd, S.W., "Quaternion from Rotation Matrix," *Journal of Guidance and Control*, 1(3), 223–224, 1978.
- [12] Wampler, C.W., "Manipulator Inverse Kinematic Solutions Based on Vector Formulations and Damped Least-Squares Methods," *IEEE Trans. Systems, Man, and Cybernetics*, 16(1), 93–101, 1986.

---

## Module F — LQR Velocity Controller

### F.1 Purpose

Replace the current heuristic velocity computation (finite-difference Δq/Δt with clamp) with an **optimal controller** that generates both position and velocity commands (q_cmd, q̇_cmd) for MotoROS2 Point Queue Mode. The LQR formulation explicitly minimizes a cost function that penalizes acceleration, thereby **reducing trajectory jerk** [13].

### F.2 State-Space Model

Each joint i ∈ {1, ..., 6} is modeled as a **double integrator** (kinematic model — dynamics handled internally by YRC1000):

```
State vector:    xᵢ(t) = [qᵢ(t) − q_ref_i(t)]  ∈ ℝ²                       (F1)
                          [    q̇ᵢ(t)           ]

Control input:   uᵢ(t) = q̈ᵢ(t)  ∈ ℝ                                       (F2)
```

**Continuous-time dynamics**:

```
ẋᵢ = A · xᵢ + B · uᵢ                                                       (F3)

A = [0  1]  ∈ ℝ^{2×2}      B = [0]  ∈ ℝ^{2×1}
    [0  0]                      [1]
```

- **A**: state transition (position integrates velocity)
- **B**: input matrix (acceleration drives velocity)
- **xᵢ[1]**: position error (joint i vs. reference)
- **xᵢ[2]**: joint velocity

**Discrete-time** (Zero-Order Hold, Δt = 1/f_c) [14]:

```
A_d = [1   Δt ]  ∈ ℝ^{2×2}      B_d = [Δt²/2]  ∈ ℝ^{2×1}                  (F4)
      [0    1 ]                        [  Δt  ]
```

At f_c = 15 Hz: Δt = 0.0667 s, so:

```
A_d = [1.0000   0.0667]      B_d = [0.002222]
      [0.0000   1.0000]            [0.066667]
```

### F.3 LQR Cost Function [13]

For each joint i, minimize the infinite-horizon cost:

```
Jᵢ = Σ_{k=0}^{∞} [xᵢ(k)ᵀ · Q · xᵢ(k) + uᵢ(k)ᵀ · R · uᵢ(k)]             (F5)
```

**State weight matrix**:

```
Q = [q₁   0 ]  ∈ ℝ^{2×2}     (symmetric positive semi-definite)             (F6)
    [ 0   q₂]
```

- **q₁** (position weight): penalizes deviation from q_ref → **tracking accuracy**
- **q₂** (velocity weight): penalizes residual velocity → **damping**

**Control weight**:

```
R = [ρ]  ∈ ℝ^{1×1}     (positive definite, scalar)                          (F7)
```

- **ρ** (acceleration penalty): penalizes q̈ → **smoothness / less jerk**

**Key ratio q₁/ρ**: determines the trade-off between fast tracking and smooth motion.

| q₁/ρ | Behavior |
|------|----------|
| Large (>10) | Aggressive tracking, higher jerk |
| ~5 | Balanced |
| Small (<1) | Very smooth but slow tracking |

### F.4 Solving the DARE [14]

The Discrete Algebraic Riccati Equation:

```
P = Q + A_dᵀ · P · A_d − A_dᵀ · P · B_d · (R + B_dᵀ · P · B_d)⁻¹ · B_dᵀ · P · A_d   (F8)
```

- **P ∈ ℝ^{2×2}**: solution matrix (symmetric positive definite)
- Solved **once offline** since A_d, B_d, Q, R are constant
- Standard solver: `scipy.linalg.solve_discrete_are(A_d, B_d, Q, R)`

**Optimal gain**:

```
K = (R + B_dᵀ · P · B_d)⁻¹ · B_dᵀ · P · A_d  ∈ ℝ^{1×2} = [K_p, K_d]      (F9)
```

- **K_p**: proportional (position) gain
- **K_d**: derivative (velocity) gain
- K is computed **once offline** and stored

### F.5 Online Control Law

Every tick, for each joint i:

```
eᵢ(t) = q_ref_i(t) − q_fb_i(t)                    (position error)         (F10)
ėᵢ(t) = 0 − q̇_fb_i(t)                              (velocity error)        (F11)
```

Optimal acceleration:

```
uᵢ(t) = K_p · eᵢ(t) + K_d · ėᵢ(t)                                         (F12)
```

Integrate to get commanded velocity and position:

```
q̇_cmd_i(t) = q̇_fb_i(t) + uᵢ(t) · Δt                                      (F13)
q_cmd_i(t) = q_fb_i(t) + q̇_cmd_i(t) · Δt                                   (F14)
```

**Safety clamp**:

```
q̇_cmd_i(t) = clip(q̇_cmd_i(t), −q̇_max_i, +q̇_max_i)                       (F15)
q_cmd_i(t) = clip(q_cmd_i(t), q_soft_min_i, q_soft_max_i)                   (F16)
```

**Output to MotoROS2**:

```python
point.positions  = [q_cmd_1, ..., q_cmd_6]
point.velocities = [q̇_cmd_1, ..., q̇_cmd_6]
```

### F.6 Joint Velocity Feedback

MotoROS2 publishes joint velocities **directly** in the `/joint_states` topic (message type `sensor_msgs/JointState`):

```python
# From /joint_states (MotoROS2 driver on YRC1000):
q_fb(t)  = msg.position    # [q₁, ..., q₆] ∈ ℝ⁶   (rad)
q̇_fb(t) = msg.velocity    # [q̇₁, ..., q̇₆] ∈ ℝ⁶   (rad/s)              (F17)
τ_fb(t)  = msg.effort      # [τ₁, ..., τ₆] ∈ ℝ⁶   (N·m)                (F18)
```

- **Source**: confirmed from `logger_node.py` (dòng 308–309) where `j1_vel...j6_vel` and `j1_eff...j6_eff` are logged directly from `msg.velocity` and `msg.effort`
- **No estimation needed**: q̇_fb is read directly from the robot encoder feedback — no finite-difference or EMA required
- **τ_fb** (joint effort/torque) is also available and can be used for post-hoc analysis (e.g., joint torque gradient as a smoothness metric)

### F.7 Parameter Table

| Symbol | Value | Unit | Meaning |
|--------|-------|------|---------|
| q₁ | 50.0 | — | Position tracking weight |
| q₂ | 1.0 | — | Velocity damping weight |
| ρ | 10.0 | — | Acceleration penalty (smoothness) |

| q̇_max (J1–J3) | 0.20 | rad/s | Max joint velocity (base joints) |
| q̇_max (J4–J6) | 0.08 | rad/s | Max joint velocity (wrist joints) |

### F.8 Computational Complexity

K computed offline (once). Online: 6 joints × (2 multiplies + 2 adds + 2 clips) = **O(n) = O(6)** — negligible.

### F.9 References

- [13] Anderson, B.D.O. & Moore, J.B., "Optimal Control: Linear Quadratic Methods," *Prentice Hall*, 1990. — LQR theory and DARE.
- [14] Franklin, G.F., Powell, J.D., & Emami-Naeini, A., "Feedback Control of Dynamic Systems," 8th ed., *Pearson*, 2019, Ch. 7–8. — Discrete-time LQR, state-space discretization.

---

## 7. Stability Analysis

### 7.1 Lipschitz Continuity of p_smooth

p_smooth is output of EMA filter (D2) with velocity clamp (D4):

```
‖p_smooth(t) − p_smooth(t−1)‖ ≤ v_max / f_c = 0.15/15 = 0.01 m/tick       (S1)
```

### 7.2 Smoothness of w(t)

Rate limit |Δw| ≤ 0.05 per tick (C5). Plus the Lyapunov law (C3) is itself a first-order low-pass with τ = 1/η = 0.67 s. Combined: ‖dw/dt‖ ≤ Δw_max · f_c = 0.75 s⁻¹.

### 7.3 LQR Closed-Loop Stability

The LQR gain K is designed so that all eigenvalues of (A_d − B_d · K) lie strictly inside the unit circle [13]. This is guaranteed by the DARE solution when (A_d, B_d) is controllable and (A_d, Q^{1/2}) is observable — both trivially satisfied for the double integrator.

### 7.4 Anti-Oscillation Summary

| Mechanism | Equation | Effect |
|-----------|----------|--------|
| EMA on ε | (A1) | Filters s_r noise |
| w rate limit | (C5) | Prevents authority chattering |
| Safety hysteresis | (C7) | Debounces mode switching |
| EMA smoother | (D2) | Filters p_smooth jumps |
| Velocity clamp | (D4) | Bounds Cartesian speed |
| LQR damping (q₂) | (F6) | Reduces joint velocity oscillation |
| Joint delta clamp | (E10) | Bounds per-tick joint change |

---

## 8. Complete Equation Summary

```
── Module A: Prediction Reliability ──
(A1)  ε̄(t) = 0.85·ε̄(t−1) + 0.15·ε(t)
(A2)  s_r(t) = exp(−7.0·ε̄(t))

── Module B: Arm Comfort ──
(B7)  d(t) = √[(Θ_arm − μ_opt)ᵀ · Σ_reg⁻¹ · (Θ_arm − μ_opt)]
(B8)  s_e(t) = exp(−0.33·d(t))

── Module C: Adaptive Weight ──
(C2)  w*(t) = s_r(t) · s_e(t)^0.6
(C7)  Safety: if s_r < 0.15 → w* = 0 (hysteresis Δ_h = 0.10)
(C4)  Δw = clip(0.10·(w* − w), −0.05, +0.05)
(C6)  w(t+1) = clip(w + Δw, 0, 1)

── Module D: Trajectory Smoother ──
(D1)  p_raw = w·p̂_pre(t+k) + (1−w)·p_fb
(D2)  p_smooth = 0.5·p_smooth_prev + 0.5·p_raw
(D4)  Velocity clamp: ‖v‖ ≤ 0.15 m/s

── Module E: IK (DLS) ──
(E4)  e = [p_target − p_current; 0.5·log_SO3(R_target·R_currentᵀ)]
(E8)  Δq = Jᵀ(JJᵀ + 0.0001·I₆)⁻¹ · e
(E9)  q_ref = clip(q + Δq, q_min, q_max)

── Module F: LQR Controller ──
(F9)  K = [K_p, K_d] from DARE(A_d, B_d, Q, R)  — offline
(F12) u_i = K_p·(q_ref_i − q_fb_i) + K_d·(0 − q̇_fb_i)
(F13) q̇_cmd_i = q̇_fb_i + u_i·Δt
(F14) q_cmd_i = q_fb_i + q̇_cmd_i·Δt
```

---

## 9. Pseudocode

```
OFFLINE:
    μ_opt, Σ_reg⁻¹ ← compute_from(Θ_opt)
    K = [K_p, K_d] ← solve_DARE(A_d, B_d, Q=[50,1], R=[10])

INITIALIZE:
    ε̄ ← 0,  w ← 0.5,  safety_mode ← false
    p_smooth ← p_fb(0),  q̇_fb ← zeros(6)

LOOP at f_c = 15 Hz:
    // Sensors
    p_wr, Θ_arm ← camera.get_pose()
    p̂_pre ← GRU.predict(history)
    q_fb ← robot.joint_states.positions
    p_fb ← FK(q_fb)
    q̇_fb ← EMA_filter(finite_diff(q_fb))

    // Module A
    ε ← ‖p̂_pre_current − p_wr‖
    ε̄ ← 0.85·ε̄ + 0.15·ε
    s_r ← exp(−7.0·ε̄)

    // Module B
    d ← mahalanobis(Θ_arm, μ_opt, Σ_reg⁻¹)
    s_e ← exp(−0.33·d)

    // Module C
    w* ← s_r · s_e^0.6
    update safety_mode with hysteresis(s_r, 0.15, 0.25)
    if safety_mode: w* ← 0
    w ← w + clip(0.10·(w* − w), −0.05, +0.05)
    w ← clip(w, 0, 1)

    // Module D
    p_raw ← w·p̂_pre + (1−w)·p_fb
    p_smooth ← 0.5·p_smooth + 0.5·p_raw
    enforce ‖v‖ ≤ 0.15 m/s

    // Module E
    q_ref ← DLS_IK(p_smooth, orientation, q_seed)
    q_ref ← enforce_delta_limits(q_ref, q_prev)

    // Module F
    for i in 1..6:
        u_i ← K_p·(q_ref_i − q_fb_i) + K_d·(−q̇_fb_i)
        q̇_cmd_i ← clip(q̇_fb_i + u_i·Δt, ±q̇_max_i)
        q_cmd_i ← clip(q_fb_i + q̇_cmd_i·Δt, q_min_i, q_max_i)

    // Send to robot
    MotoROS2.queue_point(q_cmd, q̇_cmd, time_from_start)
```

---

## 10. Hyperparameter Table (Complete)

| # | Module | Symbol | Value | Unit | Source/Derivation |
|---|--------|--------|-------|------|-------------------|
| 1 | A | α_ε | 0.85 | — | EMA window ≈ 7 samples |
| 2 | A | λ | 7.0 | m⁻¹ | s_r=0.5 at ε̄=0.10m |
| 3 | B | δ | 1.0 | deg² | Covariance regularization |
| 4 | B | κ | 0.33 | — | s_e=0.5 at d=2.1 |
| 5 | C | p | 1.0 | — | Linear reliability |
| 6 | C | q | 0.6 | — | Sub-linear comfort |
| 7 | C | δ_w | 0.10 | — | η/f_c = 1.5/15 |
| 8 | C | Δw_max | 0.05 | — | Max 0.75/s |
| 9 | C | s_r_crit | 0.15 | — | Safety threshold |
| 10 | C | Δ_h | 0.10 | — | Hysteresis band |
| 11 | D | α_s | 0.5 | — | SMOOTH_ALPHA |
| 12 | D | v_max | 0.15 | m/s | ISO/TS 15066 |
| 13 | E | λ_DLS | 0.01 | — | DLS damping |
| 14 | F | q₁ | 50.0 | — | Position tracking |
| 15 | F | q₂ | 1.0 | — | Velocity damping |
| 16 | F | ρ | 10.0 | — | Acceleration penalty |


---

## 11. Ablation Study

| ID | Config | Tests |
|----|--------|-------|
| A1 | w = 0.5 (fixed) | Baseline: no adaptation |
| A2 | w = s_r (no ergonomics) | Remove comfort contribution |
| A3 | w = αs_r + βs_e (linear) | Current draft formulation |
| A4 | w = s_r^p · s_e^q (proposed) | Product-form fusion |
| A5 | A4 without EMA on ε | Effect of error smoothing |
| A6 | A4 without LQR (direct q_ref) | Effect of optimal velocity |
| A7 | A4 + LQR (full proposed) | Complete system |

---

## 12. Evaluation Metrics

| Category | Metric | Description |
|----------|--------|-------------|
| Tracking | RMSE | √(mean ‖p_smooth − p_wr‖²) |
| Smoothness | Mean jerk | (1/T)Σ‖d³p/dt³‖ |
| Smoothness | Joint torque gradient | RMS of dτ/dt |
| Ergonomics | Mean RULA | Average over task |
| Ergonomics | % time RULA > 5 | High-risk exposure |
| Safety | Max EE velocity | max ‖ṗ_EE‖ |
| Task | Completion time | Total co-carry duration |
| Subjective | NASA-TLX | Workload questionnaire |

---

## 13. References (Complete)

| # | Citation |
|---|----------|
| [1] | Lugaresi, C., et al., "MediaPipe: A Framework for Building Perception Pipelines," *arXiv:1906.08172*, 2019. |
| [2] | Cho, K., et al., "Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation," *EMNLP*, 2014. |
| [3] | Brown, R.G., "Smoothing, Forecasting and Prediction of Discrete Time Series," *Prentice-Hall*, 1963. |
| [4] | Bishop, C.M., "Pattern Recognition and Machine Learning," *Springer*, 2006. |
| [5] | De Maesschalck, R., et al., "The Mahalanobis distance," *Chemometrics and Intelligent Lab. Systems*, 50(1), 1–18, 2000. |
| [6] | McAtamney, L. & Corlett, E.N., "RULA: A survey method for work-related upper limb disorders," *Applied Ergonomics*, 24(2), 91–99, 1993. |
| [7] | Hinton, G.E., "Training Products of Experts by Minimizing Contrastive Divergence," *Neural Computation*, 14(8), 2002. |
| [8] | Khalil, H.K., "Nonlinear Systems," 3rd ed., *Prentice Hall*, 2002. |
| [9] | ISO/TS 15066:2016, "Robots and robotic devices — Collaborative robots," *ISO*, 2016. |
| [10] | Siciliano, B., et al., "Robotics: Modelling, Planning and Control," *Springer*, 2009. |
| [11] | Shepperd, S.W., "Quaternion from Rotation Matrix," *J. Guidance and Control*, 1(3), 1978. |
| [12] | Wampler, C.W., "Manipulator Inverse Kinematic Solutions Based on Damped Least-Squares Methods," *IEEE Trans. SMC*, 16(1), 1986. |
| [13] | Anderson, B.D.O. & Moore, J.B., "Optimal Control: Linear Quadratic Methods," *Prentice Hall*, 1990. |
| [14] | Franklin, G.F., et al., "Feedback Control of Dynamic Systems," 8th ed., *Pearson*, 2019. |
