# ICTA — Adaptive Shared Control Framework for Co-Carrying
# Final Consolidated Mathematical Specification

> **System**: Yaskawa HC10DTP (6-DOF) · Intel RealSense D435 · MediaPipe Pose · Deep-GRU Predictor · MotoROS2 Point Queue Mode · ROS 2 (15 Hz control loop)

---

## 0. Notation and Conventions

| Symbol | Domain | Description | Source in system |
|--------|--------|-------------|-----------------|
| **p_wr**(t) | ℝ³ | Human wrist position at time t | Camera → MediaPipe skeleton tracking |
| **p̂_pre**(t+k) | ℝ³ | Predicted wrist position k steps ahead | Deep-GRU output (predictor_node) |
| **p_fb**(t) | ℝ³ | Robot end-effector position (feedback) | FK(q_fb) via local_ik_solver |
| **p_smooth**(t) | ℝ³ | Smoothed Cartesian command | Trajectory Smoother output |
| **Θ_arm**(t) | ℝ⁵ | Human arm joint angles (degrees) | RULA tracker (rula_tracker_node) |
| **Θ_opt** | ℝ^{M×5} | Pre-collected optimal pose dataset | Offline database |
| ε(t) | ℝ≥0 | Prediction error (scalar) | ‖p̂_pre(t) − p_wr(t)‖₂ |
| s_r(t) | [0, 1] | Prediction reliability score | Module A output |
| s_e(t) | [0, 1] | Arm comfort score | Module B output |
| w(t) | [0, 1] | Adaptive blending weight | Module C output |
| **q_ref**(t) | ℝ⁶ | Joint position reference | IK (DLS) output |
| **q_fb**(t) | ℝ⁶ | Joint position feedback | /joint_states topic |
| **q_cmd**(t) | ℝ⁶ | Commanded joint positions | LQR output → MotoROS2 |
| **q̇_cmd**(t) | ℝ⁶ | Commanded joint velocities | LQR output → MotoROS2 |
| f_c | scalar | Control frequency = 15 Hz | cartesian_streamer tick rate |
| Δt | scalar | Control period = 1/f_c ≈ 0.0667 s | — |
| n = 6 | — | Number of robot joints | HC10DTP DOF |

---

## 1. System Pipeline

```
Human ──→ Camera (RealSense D435)
              │
              ├──→ Skeleton tracking (MediaPipe [1]) ──→ p_wr(t), Θ_arm(t)
              │
              └──→ Deep-GRU Predictor [2] ──→ p̂_pre(t+k), ε(t)
                                                   │
                    ┌──────────────────────────────┘
                    │
            ┌───────▼────────────────────────────────┐
            │      Adaptive Weight Generator          │
            │                                         │
            │   ε(t) ──→ [A] Prediction Reliability   │
            │                        s_r ──┐          │
            │                              ▼          │
            │   Θ_arm ─→ [B] Arm Comfort  [C] Weight  │──→ w(t)
            │   Θ_opt ─┘       s_e ──────→   Fusion   │
            │                                         │
            └─────────────────────────────────────────┘
                                                │
                    p̂_pre(t+k), p_fb(t), w(t)  │
                              │                 │
                              ▼                 │
                    [D] Trajectory Smoother ◄────┘
                              │
                         p_smooth(t)
                              │
                              ▼
                    [E] Inverse Kinematics (DLS + Quaternion)
                              │
                         q_ref(t)
                              │
                              ▼
                    [F] LQR Velocity Controller
                              │
                       q_cmd(t), q̇_cmd(t)
                              │
                              ▼
                    MotoROS2 Point Queue Mode
                              │
                              ▼
                         HC10DTP Robot ──→ q_fb(t), p_fb(t) (feedback loop)
```

**References**:
- [1] Lugaresi, C., et al., "MediaPipe: A Framework for Building Perception Pipelines," *arXiv:1906.08172*, 2019.
- [2] Cho, K., et al., "Learning Phrase Representations using RNN Encoder-Decoder," *EMNLP*, 2014.

---

## Module A — Prediction Reliability Score

### A.1 Purpose

Quantify trust in the DL predictor output. When the predictor is inaccurate (occlusion, sudden direction changes), s_r decreases, causing the system to shift authority toward robot feedback (safe mode).

### A.2 Input

- ε(t) = ‖p̂_pre(t) − p_wr(t)‖₂ ∈ ℝ≥0 — instantaneous prediction error (meters)
  - **Source**: computed from DL predictor output and current camera measurement

### A.3 Algorithm: EMA-Smoothed Exponential Confidence

**Step 1 — Exponential Moving Average of prediction error** [3]:

```
ε̄(t) = α_ε · ε̄(t−1) + (1 − α_ε) · ε(t)                                    (A1)
```

- **ε̄(t) ∈ ℝ≥0**: smoothed prediction error (meters)
- **α_ε ∈ (0, 1)**: smoothing factor; higher → more history, slower response
- **Physical meaning**: temporal low-pass filter on the error signal; rejects transient noise spikes while tracking sustained prediction degradation
- **Effective window**: N_eff = 1/(1 − α_ε) samples. At α_ε = 0.85, f_c = 15 Hz → N_eff ≈ 7 samples ≈ 467 ms

**Step 2 — Exponential decay mapping** [4]:

```
s_r(t) = exp(−λ · ε̄(t))                                                      (A2)
```

- **s_r(t) ∈ (0, 1]**: prediction reliability score
- **λ > 0 (unit: m⁻¹)**: sensitivity parameter controlling how fast trust drops with error
- **Properties**: monotonically decreasing, differentiable, bounded in (0, 1]
- **Design rule**: choose ε_half such that s_r(ε_half) = 0.5, then λ = ln(2) / ε_half

### A.4 Parameter Table

| Symbol | Value | Unit | Derivation |
|--------|-------|------|------------|
| α_ε | 0.85 | — | N_eff ≈ 7 at 15 Hz ≈ 467 ms window |
| λ | 7.0 | m⁻¹ | ε_half = 0.10 m → λ = 0.693/0.10 |

### A.5 Calibration Procedure

1. Record ε(t) for 3 min of typical co-carrying (no adaptation, w fixed)
2. Compute ε̄ with α_ε = 0.85
3. Find percentiles: p50(ε̄), p95(ε̄)
4. Adjust λ so that s_r(p50) ≈ 0.7 and s_r(p95) ≈ 0.2

### A.6 Computational Complexity

1 multiply + 1 add (EMA) + 1 exp = **O(1)** per timestep.

### A.7 References

- [3] Brown, R.G., "Smoothing, Forecasting and Prediction of Discrete Time Series," *Prentice-Hall*, 1963. — Foundation of EMA for signal filtering.
- [4] This exponential decay mapping is standard in confidence estimation; see Bishop, C.M., "Pattern Recognition and Machine Learning," *Springer*, 2006, §2.1 for exponential family distributions.

---

## Module B — Arm Comfort Score

### B.1 Purpose

Quantify human arm ergonomic comfort based on the current posture relative to a pre-collected database of comfortable configurations. A low s_e signals that the robot should guide the shared object toward a more comfortable configuration.

### B.2 Inputs

**Current arm angles** (from `rula_tracker_node.py`):

```
Θ_arm(t) = [α_s, α_c, β_s, β_t, γ_s]ᵀ ∈ ℝ⁵                                (B1)
```

| Component | Name | Measurement | Code reference |
|-----------|------|-------------|----------------|
| α_s | Upper arm sagittal angle | angle(trunk_vec, upper_arm_vec) | dòng 151–154 |
| α_c | Upper arm abduction | angle(shoulder_up, upper_arm_vec) − 90° | dòng 166–168 |
| β_s | Elbow flexion | angle(forearm_vec, upper_arm_vec) | dòng 176–177 |
| β_t | Forearm transversal deviation | 90° − angle(shoulder_axis, forearm_vec) | dòng 186–187 |
| γ_s | Wrist bend | angle(hand_vec, forearm_vec) | dòng 195–196 |

All angles in **degrees**.

**Optimal pose dataset** (pre-collected offline):

```
Θ_opt = {Θ_opt^(i)}_{i=1}^{M} ⊂ ℝ⁵                                          (B2)
```

M data points of arm configurations where operators self-report comfort during co-carrying.

### B.3 Algorithm: Mahalanobis Distance Comfort Score

**Rationale**: The 5 joint angles have very different ranges (α_s: 0–180°, α_c: 0–45°, γ_s: 0–30°). The Mahalanobis distance [5] normalizes by the covariance structure of the optimal dataset, ensuring all dimensions contribute proportionally regardless of scale.

**Step 1 — Offline: compute dataset statistics**

Mean of optimal poses:

```
μ_opt = (1/M) Σ_{i=1}^{M} Θ_opt^(i) ∈ ℝ⁵                                   (B3)
```

Covariance matrix:

```
Σ_opt = (1/(M−1)) Σ_{i=1}^{M} (Θ_opt^(i) − μ_opt)(Θ_opt^(i) − μ_opt)ᵀ ∈ ℝ^{5×5}   (B4)
```

Regularized covariance (prevent singularity):

```
Σ_reg = Σ_opt + δ · I₅ ∈ ℝ^{5×5},     δ = 1.0 (deg²)                       (B5)
```

Pre-compute inverse for online use:

```
Σ_reg⁻¹ ∈ ℝ^{5×5}     (computed once, stored)                               (B6)
```

**Step 2 — Online: compute distance and score**

Mahalanobis distance:

```
d(t) = √[(Θ_arm(t) − μ_opt)ᵀ · Σ_reg⁻¹ · (Θ_arm(t) − μ_opt)]  ∈ ℝ≥0      (B7)
```

- **Physical meaning**: d(t) measures how many "standard deviations" (accounting for inter-joint correlation) the current pose is from the optimal center
- **For a 5D Gaussian**, the median d ≈ 2.1 (from χ² distribution with 5 DOF)

Comfort score:

```
s_e(t) = exp(−κ · d(t))  ∈ (0, 1]                                           (B8)
```

- **κ > 0**: sensitivity; κ = ln(2) / d_half where d_half is the desired half-trust distance
- **With d_half = 2.1**: κ ≈ 0.33

### B.4 Matrix Dimensions Summary

| Symbol | Size | Type | When computed |
|--------|------|------|---------------|
| Θ_arm(t) | 5 × 1 | vector | Online, every tick |
| μ_opt | 5 × 1 | vector | Offline, once |
| Σ_opt | 5 × 5 | symmetric PD matrix | Offline, once |
| Σ_reg | 5 × 5 | symmetric PD matrix | Offline, once |
| Σ_reg⁻¹ | 5 × 5 | symmetric PD matrix | Offline, once |
| d(t) | scalar | ≥ 0 | Online, every tick |
| s_e(t) | scalar | (0, 1] | Online, every tick |

### B.5 Parameter Table

| Symbol | Value | Unit | Derivation |
|--------|-------|------|------------|
| δ | 1.0 | deg² | Regularization; prevents singular Σ when M is small |
| κ | 0.33 | — | d_half = 2.1 (median of χ²₅) → κ = 0.693/2.1 |

### B.6 Cross-Validation with RULA

The existing RULA tracker [6] provides total_score ∈ {1, ..., 7}. Use as validation metric:

```
s_e^{RULA}(t) = max(0, (7 − RULA_total(t)) / 6)                             (B9)
```

**Not used in the control loop** — only for experimental comparison with s_e.

### B.7 Computational Complexity

1 vector subtraction (5D) + 1 matrix-vector product (5×5 · 5×1, pre-inverted) + 1 dot product (5D) + 1 sqrt + 1 exp = **O(d²) = O(25)** — constant time.

### B.8 References

- [5] De Maesschalck, R., Jouan-Rimbaud, D., & Massart, D.L., "The Mahalanobis distance," *Chemometrics and Intelligent Laboratory Systems*, 50(1), 1–18, 2000. — Survey of Mahalanobis distance applications.
- [6] McAtamney, L. & Corlett, E.N., "RULA: A survey method for the investigation of work-related upper limb disorders," *Applied Ergonomics*, 24(2), 91–99, 1993. — Original RULA method.

---

## Module C — Adaptive Weight Generator (Core Contribution)

### C.1 Purpose

Produce blending weight w(t) ∈ [0, 1] that governs the authority split between DL prediction and robot feedback. This is the **main novel contribution** of the framework.

### C.2 Blending Equation

```
p_smooth(t+k) = w(t) · p̂_pre(t+k) + (1 − w(t)) · p_fb(t)                   (C1)
```

- w → 1: trust prediction (proactive, anticipatory)
- w → 0: trust feedback (reactive, safe)

### C.3 Algorithm: Product-of-Experts with Lyapunov Convergence

#### C.3.1 Target Weight — Product Form [7]

```
w*(t) = s_r(t)^p · s_e(t)^q                                                  (C2)
```

- **p, q > 0**: importance exponents
- **Recommended: p = 1.0, q = 0.6** (reliability is primary, comfort is secondary)

**Why product, not sum** [7]: The product form implements multiplicative "AND-logic." If either score is zero, w* = 0 regardless of the other. This is physically correct — unreliable predictions must not be followed even if the posture is comfortable. The sum form w = αs_r + βs_e would give w = β even when s_r = 0 (prediction completely wrong), which is **dangerous**.

#### C.3.2 Smooth Convergence — First-Order Adaptive Law [8]

Instead of setting w = w* instantly (which causes discontinuities), use a first-order convergence law derived from Lyapunov stability theory:

**Continuous-time**:

```
ẇ(t) = −η · (w(t) − w*(t))                                                  (C3)
```

**Discrete-time** (at f_c = 15 Hz):

```
Δw(t) = δ · (w*(t) − w(t)),    δ = η/f_c                                    (C4)
```

**Rate limiting** (prevent jerk):

```
Δw_clamped(t) = clip(Δw(t), −Δw_max, +Δw_max)                               (C5)
w(t+1) = clip(w(t) + Δw_clamped(t), 0, 1)                                   (C6)
```

#### C.3.3 Safety Override with Hysteresis

```
Enter safety mode:  s_r(t) < s_r_crit              (= 0.15)
Exit safety mode:   s_r(t) > s_r_crit + Δ_h        (Δ_h = 0.10)             (C7)
When safety_mode = true:  w*(t) = 0
```

#### C.3.4 Lyapunov Stability Proof [8]

**Lyapunov candidate**: V(t) = ½(w(t) − w*(t))²  ≥ 0

**Time derivative** (assuming w* varies slowly vs. adaptation rate):

```
V̇ = (w − w*) · ẇ = (w − w*) · [−η(w − w*)] = −η(w − w*)²  ≤ 0            (C8)
```

Since V ≥ 0, V̇ ≤ 0, and V̇ = 0 only when w = w*, by **La Salle's invariance principle**, w(t) → w*(t) asymptotically. The error decays exponentially: |w(t) − w*(t)| ~ e^{−ηt}.

**95% convergence time**: t_95 = 3/η. With η = 1.5 s⁻¹: t_95 = 2.0 s.

### C.4 Parameter Table

| Symbol | Value | Unit | Derivation |
|--------|-------|------|------------|
| p | 1.0 | — | Linear reliability contribution |
| q | 0.6 | — | Sub-linear comfort (safety > comfort) |
| η | 1.5 | s⁻¹ | t_95 = 2.0 s (co-carrying tempo) |
| δ | 0.10 | — | η/f_c = 1.5/15 |
| Δw_max | 0.05 | — | Max rate = 0.05 × 15 = 0.75/s |
| s_r_crit | 0.15 | — | Corresponds to ε̄ ≈ 0.27 m (very large) |
| Δ_h | 0.10 | — | Anti-chatter hysteresis band |

### C.5 References

- [7] Hinton, G.E., "Training Products of Experts by Minimizing Contrastive Divergence," *Neural Computation*, 14(8), 1771–1800, 2002. — Product-of-experts formulation.
- [8] Khalil, H.K., "Nonlinear Systems," 3rd ed., *Prentice Hall*, 2002, Ch. 4. — Lyapunov stability theory, La Salle's invariance principle.

---

## Module D — Trajectory Smoother

### D.1 Purpose

Filter the raw weighted blend p_raw to produce a smooth, velocity-limited Cartesian command p_smooth suitable for IK. Prevents discontinuities when w changes or predictions jump.

### D.2 Algorithm: First-Order EMA with Velocity Limiting

**Step 1 — Weighted blend** (from C1):

```
p_raw(t) = w(t) · p̂_pre(t+k) + (1 − w(t)) · p_fb(t)  ∈ ℝ³                 (D1)
```

**Step 2 — EMA smoothing** [3]:

```
p_smooth(t) = (1 − α_s) · p_smooth(t−1) + α_s · p_raw(t)  ∈ ℝ³             (D2)
```

- **α_s ∈ (0, 1]**: smoothing step size
- **α_s = 0.5**: matches existing `SMOOTH_ALPHA` in `cartesian_streamer`
- **Equivalent cutoff frequency**: ω_c = −f_c · ln(1 − α_s) = −15 · ln(0.5) ≈ 10.4 rad/s

**Step 3 — Velocity limiting** (ISO/TS 15066 [9] compliance):

```
v(t) = (p_smooth(t) − p_smooth(t−1)) · f_c  ∈ ℝ³                           (D3)

if ‖v(t)‖ > v_max:
    p_smooth(t) = p_smooth(t−1) + (v_max / ‖v(t)‖) · (p_smooth(t) − p_smooth(t−1))   (D4)
```

### D.3 Parameter Table

| Symbol | Value | Unit | Source |
|--------|-------|------|--------|
| α_s | 0.5 | — | SMOOTH_ALPHA in cartesian_streamer |
| v_max | 0.15 | m/s | MAX_CARTESIAN_VELOCITY (ISO/TS 15066) |
| a_max | 0.50 | m/s² | MAX_CARTESIAN_ACCELERATION |

### D.4 Computational Complexity

3 multiplications + 3 additions (EMA per axis) + 1 norm + conditional scaling = **O(1)**.

### D.5 References

- [9] ISO/TS 15066:2016, "Robots and robotic devices — Collaborative robots," *International Organization for Standardization*, 2016. — Collaborative robot speed and force limits.
