#!/usr/bin/env python3
"""
adaptive_shared_control.py
──────────────────────────
ICTA Adaptive Shared Control Framework — Modules A–F.

Implements the full pipeline:
  A. Prediction Reliability  (EMA-smoothed exponential confidence)
  B. Arm Comfort Score        (Mahalanobis distance from optimal RULA poses)
  C. Adaptive Weight Generator (Product-of-experts with Lyapunov convergence)
  D. Trajectory Smoother      (Weighted blend + EMA + velocity clamp)
  F. LQR Velocity Controller  (Joint-space optimal control via DARE)

Pure numpy — no ROS dependency. Testable standalone.

References:
  [3] Brown, R.G., "Smoothing, Forecasting and Prediction," 1963.
  [5] De Maesschalck et al., "The Mahalanobis distance," 2000.
  [6] McAtamney & Corlett, "RULA," Applied Ergonomics, 1993.
  [7] Hinton, "Training Products of Experts," Neural Computation, 2002.
  [8] Khalil, "Nonlinear Systems," 3rd ed., 2002.
  [13] Anderson & Moore, "Optimal Control: LQ Methods," 1990.
"""

import numpy as np
from typing import Optional, Tuple, Dict

# ═══════════════════════════════════════════════════════════════════════
# Module A — Prediction Reliability Score  (Eq. A1–A2)
# ═══════════════════════════════════════════════════════════════════════

class PredictionReliability:
    """
    EMA-smoothed exponential confidence score.

    s_r(t) = exp(-λ · ε̄(t))
    where ε̄(t) = α_ε · ε̄(t-1) + (1 - α_ε) · ε(t)

    Parameters
    ----------
    alpha_eps : float
        EMA smoothing factor for prediction error (default: 0.85).
    lam : float
        Sensitivity parameter in m⁻¹ (default: 7.0, s_r=0.5 at ε̄=0.10m).
    """

    def __init__(self, alpha_eps: float = 0.85, lam: float = 7.0):
        self.alpha_eps = alpha_eps
        self.lam = lam
        self.eps_bar = 0.0  # smoothed error state

    def update(self, p_predicted: np.ndarray, p_actual: np.ndarray) -> float:
        """
        Compute reliability score from prediction vs actual position.

        Parameters
        ----------
        p_predicted : (3,) predicted wrist position in robot base frame
        p_actual    : (3,) actual wrist position in robot base frame

        Returns
        -------
        s_r : float in (0, 1]
        """
        eps = float(np.linalg.norm(p_predicted - p_actual))
        self.eps_bar = self.alpha_eps * self.eps_bar + (1.0 - self.alpha_eps) * eps
        s_r = float(np.exp(-self.lam * self.eps_bar))
        return s_r

    def reset(self):
        self.eps_bar = 0.0


# ═══════════════════════════════════════════════════════════════════════
# Module B — Arm Comfort Score  (Eq. B3–B8)
# ═══════════════════════════════════════════════════════════════════════

def generate_default_theta_opt() -> np.ndarray:
    """
    Generate default optimal pose dataset from RULA score-1 ranges.

    Based on McAtamney & Corlett (1993) RULA worksheet:
      - Upper arm sagittal (α_s): score 1 when 0–20° → optimal ~10°
      - Upper arm coronal (α_c): no abduction penalty when |α_c| < 10° → optimal ~0°
      - Lower arm flexion (β_s): score 1 when 60–100° → optimal ~80°
      - Lower arm deviation (β_t): no penalty when |β_t| < 10° → optimal ~0°
      - Wrist bend (γ_s): score 1 when 0–15° → optimal ~5°

    Returns
    -------
    theta_opt : (M, 5) array of optimal arm configurations in degrees
    """
    rng = np.random.RandomState(42)  # reproducible
    M = 50  # 50 samples from optimal RULA ranges
    theta_opt = np.zeros((M, 5))
    # α_s: uniform in [5, 20] (score 1 range)
    theta_opt[:, 0] = rng.uniform(5.0, 20.0, M)
    # α_c: uniform in [-8, 8] (no abduction penalty)
    theta_opt[:, 1] = rng.uniform(-8.0, 8.0, M)
    # β_s: uniform in [60, 100] (score 1 range)
    theta_opt[:, 2] = rng.uniform(60.0, 100.0, M)
    # β_t: uniform in [-8, 8] (no deviation penalty)
    theta_opt[:, 3] = rng.uniform(-8.0, 8.0, M)
    # γ_s: uniform in [0, 15] (score 1 range)
    theta_opt[:, 4] = rng.uniform(0.0, 15.0, M)
    return theta_opt


class ArmComfortScore:
    """
    Mahalanobis distance-based comfort score.

    s_e(t) = exp(-κ · d(t))
    where d(t) = √[(Θ_arm - μ_opt)ᵀ Σ_reg⁻¹ (Θ_arm - μ_opt)]

    Parameters
    ----------
    theta_opt : (M, 5) array or None
        Optimal pose dataset. If None, uses default RULA-based dataset.
    kappa : float
        Sensitivity (default: 0.33, s_e=0.5 at d≈2.1).
    delta : float
        Covariance regularization in deg² (default: 1.0).
    """

    def __init__(self, theta_opt: Optional[np.ndarray] = None,
                 kappa: float = 0.33, delta: float = 1.0):
        self.kappa = kappa

        if theta_opt is None:
            theta_opt = generate_default_theta_opt()

        # Offline: compute statistics (Eq. B3–B6)
        self.mu_opt = np.mean(theta_opt, axis=0)           # (5,)
        sigma_opt = np.cov(theta_opt, rowvar=False)         # (5, 5)
        sigma_reg = sigma_opt + delta * np.eye(5)           # (5, 5)
        self.sigma_reg_inv = np.linalg.inv(sigma_reg)       # (5, 5)

    def update(self, theta_arm: np.ndarray) -> float:
        """
        Compute comfort score from current arm angles.

        Parameters
        ----------
        theta_arm : (5,) array [α_s, α_c, β_s, β_t, γ_s] in degrees

        Returns
        -------
        s_e : float in (0, 1]
        """
        diff = theta_arm - self.mu_opt                      # (5,)
        d = float(np.sqrt(diff @ self.sigma_reg_inv @ diff))
        s_e = float(np.exp(-self.kappa * d))
        return s_e


# ═══════════════════════════════════════════════════════════════════════
# Module C — Adaptive Weight Generator  (Eq. C2–C7)
# ═══════════════════════════════════════════════════════════════════════

class AdaptiveWeightGenerator:
    """
    Product-of-experts fusion with Lyapunov-stable convergence.

    w*(t) = s_r^p · s_e^q
    ẇ = -η(w - w*)  →  discrete: w += clip(δ·(w* - w), ±Δw_max)

    Parameters
    ----------
    p, q : float
        Importance exponents (default: p=1.0, q=0.6).
    delta_w : float
        Adaptation step size = η/f_c (default: 0.10).
    dw_max : float
        Rate limit per tick (default: 0.05).
    sr_crit : float
        Safety threshold (default: 0.15).
    hysteresis : float
        Hysteresis band for safety mode (default: 0.10).
    """

    def __init__(self, p: float = 1.0, q: float = 0.6,
                 delta_w: float = 0.10, dw_max: float = 0.05,
                 sr_crit: float = 0.15, hysteresis: float = 0.10):
        self.p = p
        self.q = q
        self.delta_w = delta_w
        self.dw_max = dw_max
        self.sr_crit = sr_crit
        self.hysteresis = hysteresis

        self.w = 0.5           # initial weight
        self.safety_mode = False

    def update(self, s_r: float, s_e: float) -> float:
        """
        Compute adaptive weight from reliability and comfort scores.

        Returns
        -------
        w : float in [0, 1]
        """
        # Target weight (Eq. C2)
        w_star = (s_r ** self.p) * (s_e ** self.q)

        # Safety override with hysteresis (Eq. C7)
        if s_r < self.sr_crit:
            self.safety_mode = True
        elif s_r > self.sr_crit + self.hysteresis:
            self.safety_mode = False

        if self.safety_mode:
            w_star = 0.0

        # Rate-limited convergence (Eq. C4–C6)
        dw = self.delta_w * (w_star - self.w)
        dw = np.clip(dw, -self.dw_max, self.dw_max)
        self.w = float(np.clip(self.w + dw, 0.0, 1.0))
        return self.w

    def reset(self, w0: float = 0.5):
        self.w = w0
        self.safety_mode = False


# ═══════════════════════════════════════════════════════════════════════
# Module D — Trajectory Smoother  (Eq. D1–D4)
# ═══════════════════════════════════════════════════════════════════════

class AdaptiveTrajectorySmoother:
    """
    Weighted blend + EMA smoothing + velocity clamp.

    p_raw = w·p_pre + (1-w)·p_fb
    p_smooth = (1-α_s)·p_smooth_prev + α_s·p_raw
    velocity clamp: ||v|| ≤ v_max

    Parameters
    ----------
    alpha_s : float
        EMA step size (default: 0.5, matches SMOOTH_ALPHA).
    v_max : float
        Max Cartesian velocity in m/s (default: 0.15, ISO/TS 15066).
    """

    def __init__(self, alpha_s: float = 0.5, v_max: float = 0.15):
        self.alpha_s = alpha_s
        self.v_max = v_max
        self.p_smooth: Optional[np.ndarray] = None

    def update(self, p_pre: np.ndarray, p_fb: np.ndarray,
               w: float, dt: float) -> np.ndarray:
        """
        Compute smoothed Cartesian command.

        Parameters
        ----------
        p_pre : (3,) predicted position
        p_fb  : (3,) robot feedback position
        w     : blending weight [0, 1]
        dt    : timestep in seconds

        Returns
        -------
        p_smooth : (3,) smoothed command position
        """
        # Weighted blend (Eq. D1)
        p_raw = w * p_pre + (1.0 - w) * p_fb

        # EMA smoothing (Eq. D2)
        if self.p_smooth is None:
            self.p_smooth = p_raw.copy()
        else:
            self.p_smooth = (1.0 - self.alpha_s) * self.p_smooth + self.alpha_s * p_raw

        # Velocity clamp (Eq. D3–D4)
        if dt > 1e-6 and self.p_smooth is not None:
            max_step = self.v_max * dt
            step = self.p_smooth - p_fb
            step_norm = float(np.linalg.norm(step))
            if step_norm > max_step:
                self.p_smooth = p_fb + step * (max_step / step_norm)

        return self.p_smooth.copy()

    def reset(self, p0: Optional[np.ndarray] = None):
        self.p_smooth = p0.copy() if p0 is not None else None


# ═══════════════════════════════════════════════════════════════════════
# Module F — LQR Velocity Controller  (Eq. F4–F16)
# ═══════════════════════════════════════════════════════════════════════

class LQRVelocityController:
    """
    Joint-space LQR controller using DARE-solved gains.

    State: x_i = [q_i - q_ref_i, q̇_i]ᵀ
    Control: u_i = q̈_i  (optimal acceleration)
    Output: (q_cmd, q̇_cmd) for MotoROS2

    Parameters
    ----------
    dt : float
        Control period in seconds (default: 1/15).
    q1 : float
        Position tracking weight (default: 50.0).
    q2 : float
        Velocity damping weight (default: 1.0).
    rho : float
        Acceleration penalty (default: 10.0).
    qdot_max : list of 6 floats
        Per-joint max velocity in rad/s.
    q_soft_min, q_soft_max : list of 6 floats
        Soft joint limits in radians.
    """

    def __init__(self, dt: float = 1.0 / 15.0,
                 q1: float = 50.0, q2: float = 1.0, rho: float = 10.0,
                 qdot_max: Optional[list] = None,
                 q_soft_min: Optional[list] = None,
                 q_soft_max: Optional[list] = None):
        self.dt = dt
        self.n_joints = 6

        # Default per-joint velocity limits
        if qdot_max is None:
            qdot_max = [0.20, 0.20, 0.20, 0.08, 0.08, 0.08]
        self.qdot_max = np.array(qdot_max)

        # Default soft joint limits
        if q_soft_min is None:
            q_soft_min = [0.00, -0.80, -2.00, -2.50, -2.09, -2.50]
        if q_soft_max is None:
            q_soft_max = [3.14,  1.20,  1.05,  2.50,  0.52,  2.50]
        self.q_soft_min = np.array(q_soft_min)
        self.q_soft_max = np.array(q_soft_max)

        # Discrete state-space (Eq. F4)
        A_d = np.array([[1.0, dt],
                        [0.0, 1.0]])
        B_d = np.array([[dt**2 / 2.0],
                        [dt]])

        Q = np.diag([q1, q2])
        R = np.array([[rho]])

        # Solve DARE (Eq. F8)
        self.K = self._solve_dare_gain(A_d, B_d, Q, R)
        self.K_p = float(self.K[0, 0])
        self.K_d = float(self.K[0, 1])

    def _solve_dare_gain(self, A, B, Q, R) -> np.ndarray:
        """Solve DARE and compute optimal gain K = (R + BᵀPB)⁻¹ BᵀPA."""
        try:
            from scipy.linalg import solve_discrete_are
            P = solve_discrete_are(A, B, Q, R)
            K = np.linalg.inv(R + B.T @ P @ B) @ (B.T @ P @ A)
            return K
        except ImportError:
            # Fallback: manually iterate Riccati (for systems without scipy)
            P = Q.copy()
            for _ in range(200):
                K = np.linalg.inv(R + B.T @ P @ B) @ (B.T @ P @ A)
                P_new = Q + A.T @ P @ A - A.T @ P @ B @ K
                if np.max(np.abs(P_new - P)) < 1e-12:
                    break
                P = P_new
            K = np.linalg.inv(R + B.T @ P @ B) @ (B.T @ P @ A)
            return K

    def update(self, q_ref: np.ndarray, q_fb: np.ndarray,
               qdot_fb: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute LQR-optimal (q_cmd, q̇_cmd) for each joint.

        Parameters
        ----------
        q_ref   : (6,) joint position reference from IK
        q_fb    : (6,) joint position feedback from /joint_states
        qdot_fb : (6,) joint velocity feedback from /joint_states

        Returns
        -------
        q_cmd    : (6,) commanded positions
        qdot_cmd : (6,) commanded velocities
        """
        q_cmd = np.zeros(self.n_joints)
        qdot_cmd = np.zeros(self.n_joints)

        for i in range(self.n_joints):
            # Position and velocity errors (Eq. F10–F11)
            e_pos = q_ref[i] - q_fb[i]
            e_vel = 0.0 - qdot_fb[i]   # target velocity = 0 (hold)

            # Optimal acceleration (Eq. F12)
            u = self.K_p * e_pos + self.K_d * e_vel

            # Integrate to velocity and position (Eq. F13–F14)
            qdot_cmd[i] = qdot_fb[i] + u * self.dt
            q_cmd[i] = q_fb[i] + qdot_cmd[i] * self.dt

            # Safety clamp (Eq. F15–F16)
            qdot_cmd[i] = np.clip(qdot_cmd[i], -self.qdot_max[i], self.qdot_max[i])
            q_cmd[i] = np.clip(q_cmd[i], self.q_soft_min[i], self.q_soft_max[i])

        return q_cmd, qdot_cmd


# ═══════════════════════════════════════════════════════════════════════
# Orchestrator — AdaptiveSharedControl
# ═══════════════════════════════════════════════════════════════════════

class AdaptiveSharedControl:
    """
    Orchestrates Modules A + B + C + D + F in correct order.

    Usage:
        asc = AdaptiveSharedControl()
        result = asc.update(p_predicted, p_hand, p_fb, theta_arm,
                            q_ref, q_fb, qdot_fb, dt)
    """

    def __init__(self, theta_opt: Optional[np.ndarray] = None,
                 control_hz: float = 15.0, **kwargs):
        dt = 1.0 / control_hz

        self.mod_a = PredictionReliability(
            alpha_eps=kwargs.get('alpha_eps', 0.85),
            lam=kwargs.get('lam', 7.0),
        )
        self.mod_b = ArmComfortScore(
            theta_opt=theta_opt,
            kappa=kwargs.get('kappa', 0.33),
        )
        self.mod_c = AdaptiveWeightGenerator(
            p=kwargs.get('p', 1.0),
            q=kwargs.get('q', 0.6),
            delta_w=kwargs.get('delta_w', 0.10),
            dw_max=kwargs.get('dw_max', 0.05),
        )
        self.mod_d = AdaptiveTrajectorySmoother(
            alpha_s=kwargs.get('alpha_s', 0.5),
            v_max=kwargs.get('v_max', 0.15),
        )
        self.mod_f = LQRVelocityController(
            dt=dt,
            q1=kwargs.get('q1', 50.0),
            q2=kwargs.get('q2', 1.0),
            rho=kwargs.get('rho', 10.0),
        )

    def update_cartesian(self, p_predicted: np.ndarray, p_hand: np.ndarray,
                         p_fb: np.ndarray, theta_arm: np.ndarray, dt: float) -> Dict:
        """
        Runs Modules A → B → C → D.
        (Call this before IK).
        """
        s_r = self.mod_a.update(p_predicted, p_hand)
        s_e = self.mod_b.update(theta_arm)
        w = self.mod_c.update(s_r, s_e)
        p_smooth = self.mod_d.update(p_predicted, p_fb, w, dt)
        return {
            'p_smooth': p_smooth,
            'w': w,
            's_r': s_r,
            's_e': s_e,
        }

    def update_joint(self, q_ref: np.ndarray, q_fb: np.ndarray, qdot_fb: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Runs Module F (LQR).
        (Call this after IK).
        """
        return self.mod_f.update(q_ref, q_fb, qdot_fb)

    def reset(self, p0: Optional[np.ndarray] = None):
        self.mod_a.reset()
        self.mod_c.reset()
        self.mod_d.reset(p0)


# ═══════════════════════════════════════════════════════════════════════
# Standalone Self-Test
# ═══════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("=" * 60)
    print("ICTA Adaptive Shared Control — Self Test")
    print("=" * 60)

    # --- Module A ---
    mod_a = PredictionReliability()
    s_r = mod_a.update(np.array([0.5, 0.3, 0.4]), np.array([0.5, 0.3, 0.4]))
    assert 0.99 < s_r <= 1.0, f"A: perfect prediction should give s_r≈1, got {s_r}"
    s_r = mod_a.update(np.array([1.0, 0.3, 0.4]), np.array([0.5, 0.3, 0.4]))
    assert 0.0 < s_r < 1.0, f"A: error should reduce s_r, got {s_r}"
    print(f"  Module A OK: s_r={s_r:.4f} after 0.5m error")

    # --- Module B ---
    mod_b = ArmComfortScore()
    # Optimal pose (near center of RULA score-1 ranges)
    s_e_good = mod_b.update(np.array([12.0, 0.0, 80.0, 0.0, 7.0]))
    s_e_bad = mod_b.update(np.array([120.0, 30.0, 30.0, 25.0, 40.0]))
    assert s_e_good > s_e_bad, f"B: good pose ({s_e_good:.3f}) should beat bad ({s_e_bad:.3f})"
    print(f"  Module B OK: s_e(good)={s_e_good:.4f}, s_e(bad)={s_e_bad:.4f}")

    # --- Module C ---
    mod_c = AdaptiveWeightGenerator()
    w = mod_c.update(0.9, 0.8)
    assert 0.0 <= w <= 1.0, f"C: w out of range: {w}"
    # Safety mode
    for _ in range(20):
        w = mod_c.update(0.05, 0.9)
    assert w < 0.1, f"C: safety mode should drive w→0, got {w}"
    print(f"  Module C OK: w={w:.4f} in safety mode")

    # --- Module D ---
    mod_d = AdaptiveTrajectorySmoother()
    p_fb = np.array([0.5, 0.3, 0.4])
    p_pre = np.array([0.6, 0.3, 0.4])
    p_s = mod_d.update(p_pre, p_fb, w=0.8, dt=1.0/15.0)
    assert p_s.shape == (3,), f"D: wrong shape {p_s.shape}"
    print(f"  Module D OK: p_smooth={p_s.round(4)}")

    # --- Module F ---
    mod_f = LQRVelocityController()
    print(f"  Module F: LQR gains K_p={mod_f.K_p:.4f}, K_d={mod_f.K_d:.4f}")
    q_ref = np.array([1.57, 0.07, -1.05, -0.03, -0.52, 0.0])
    q_fb = np.array([1.56, 0.07, -1.05, -0.03, -0.52, 0.0])
    qdot_fb = np.zeros(6)
    q_cmd, qdot_cmd = mod_f.update(q_ref, q_fb, qdot_fb)
    assert q_cmd.shape == (6,), f"F: wrong shape {q_cmd.shape}"
    print(f"  Module F OK: q_cmd[0]={q_cmd[0]:.4f}, qdot_cmd[0]={qdot_cmd[0]:.4f}")

    # --- Full pipeline ---
    asc = AdaptiveSharedControl()
    res_cart = asc.update_cartesian(
        p_predicted=np.array([0.55, 0.30, 0.40]),
        p_hand=np.array([0.50, 0.30, 0.40]),
        p_fb=np.array([0.50, 0.30, 0.40]),
        theta_arm=np.array([15.0, 2.0, 80.0, 1.0, 5.0]),
        dt=1.0/15.0,
    )
    
    q_cmd, qdot_cmd = asc.update_joint(q_ref=q_ref, q_fb=q_fb, qdot_fb=qdot_fb)
    
    print(f"\n  Full pipeline: w={res_cart['w']:.4f}, s_r={res_cart['s_r']:.4f}, s_e={res_cart['s_e']:.4f}")
    print(f"  p_smooth={res_cart['p_smooth'].round(4)}")
    print(f"  q_cmd={q_cmd.round(4)}")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60)
