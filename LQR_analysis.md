# Phân Tích: Tích Hợp Bộ Điều Khiển LQR Vào Pipeline Co-Carrying

## 1. Hiện Trạng Hệ Thống

### 1.1 Cách gửi lệnh hiện tại

Trong `cartesian_streamer_hc10dtp.py`, mỗi tick (15 Hz) gửi một `JointTrajectoryPoint` gồm **2 trường**:

```python
# MOTION point (dòng 1177-1189):
point.positions = [float(j) for j in joints]       # q_ref từ IK
raw_velocities = [
    float((target - queued) / dt)                   # sai phân đơn giản
    for target, queued in zip(joints, self._last_queued_joints)
]
clamped_velocities = [
    max(-MAX_JOINT_VELOCITIES[i], min(MAX_JOINT_VELOCITIES[i], v))
    for i, v in enumerate(raw_velocities)
]
point.velocities = clamped_velocities
```

**Vấn đề**: Velocity hiện tại được tính bằng **sai phân bậc 1 đơn giản** `(q_new − q_old) / dt` rồi clamp. Đây là "tốc độ trung bình giữa 2 điểm", **không phải** vận tốc tối ưu — nó không xem xét:
- Trạng thái động học hiện tại (vận tốc đang có)
- Mục tiêu giảm thiểu jerk
- Sự cân bằng giữa tracking nhanh vs. mượt

### 1.2 MotoROS2 Point Queue Mode nhận gì?

MotoROS2 nhận `JointTrajectoryPoint` với:
- `positions`: vị trí joint đích → **BẮT BUỘC**
- `velocities`: vận tốc joint tại điểm đó → **TÙY CHỌN** nhưng được hỗ trợ
- `time_from_start`: thời điểm (tích lũy) → **BẮT BUỘC**

Khi cả `positions` và `velocities` đều được cung cấp, YRC1000 controller nội bộ sẽ **nội suy cubic** giữa các điểm kề nhau, sử dụng cả vị trí và vận tốc tại 2 đầu mút. Điều này tạo ra quỹ đạo mượt hơn nhiều so với chỉ gửi positions (nội suy tuyến tính).

> **Kết luận**: Hệ thống **đã hỗ trợ** velocity field. Việc thêm LQR để tính velocity tối ưu là **hoàn toàn khả thi** và không cần thay đổi giao tiếp với MotoROS2.

---

## 2. Vị Trí Của LQR Trong Pipeline

### 2.1 Pipeline hiện tại

```
p_smooth → IK (DLS) → q_ref → [sai phân Δq/Δt] → (q_ref, q̇_raw) → MotoROS2 → Robot
```

### 2.2 Pipeline đề xuất (thêm LQR)

```
p_smooth → IK (DLS) → q_ref → LQR Controller → (q_cmd, q̇_cmd) → MotoROS2 → Robot
                                    ↑
                              q_fb, q̇_fb (từ /joint_states)
```

LQR nằm **giữa IK output và MotoROS2 input**, thay thế bước sai phân đơn giản.

> [!IMPORTANT]
> LQR ở đây **KHÔNG** thay thế controller nội bộ của YRC1000. YRC1000 vẫn là tầng điều khiển thấp nhất. LQR đóng vai trò **tầng trung gian** — tạo ra cặp (q_cmd, q̇_cmd) tối ưu để YRC1000 nội suy tốt hơn.

---

## 3. Mô Hình Toán Học

### 3.1 Mô hình trạng thái (State-Space Model)

Mô hình hóa mỗi joint i ∈ {1, ..., 6} như hệ integrator kép (double integrator):

```
Trạng thái:   x_i = [q_i, q̇_i]ᵀ ∈ ℝ²
Đầu vào:      u_i = q̈_i ∈ ℝ           (gia tốc — biến điều khiển)
Tham chiếu:   r_i = q_ref_i ∈ ℝ        (từ IK)
```

Phương trình liên tục:

```
ẋ_i = A · x_i + B · u_i

A = [0  1]      B = [0]
    [0  0]          [1]
```

Đây là mô hình **rất chuẩn** trong điều khiển — không cần biết động lực học robot vì YRC1000 đã xử lý tầng torque.

### 3.2 Hàm chi phí LQR

Tối thiểu hóa:

```
J_i = Σ_{k=0}^{∞} [ (x_i(k) − r_i(k))ᵀ Q (x_i(k) − r_i(k)) + u_i(k)ᵀ R u_i(k) ]
```

Trong đó:

```
           [q₁  0 ]                    
Q = diag   [      ]      R = [ρ]      (scalar)
           [0   q₂]                    
```

- **q₁**: Trọng số tracking vị trí — muốn q_i → q_ref_i
- **q₂**: Trọng số tracking vận tốc — muốn q̇_i → 0 (damping)  
- **ρ (R)**: Trọng số phạt gia tốc — **ρ lớn → ít jerk**

### 3.3 Ý nghĩa vật lý của Q và R

| Tham số | Tăng | Giảm | Ý nghĩa |
|---------|------|------|---------|
| q₁ | Bám sát q_ref hơn, phản ứng nhanh | Cho phép sai lệch, mượt hơn | Tracking accuracy |
| q₂ | Giảm vận tốc nhanh (dừng nhanh) | Cho phép duy trì momentum | Velocity damping |
| ρ | Hạn chế gia tốc → ít jerk hơn | Cho phép gia tốc mạnh → nhanh | **Smoothness vs. Speed** |

**Tỉ lệ quan trọng nhất**: **q₁/ρ** — quyết định cân bằng giữa tracking nhanh và chuyển động mượt.

### 3.4 Giải LQR — Phương trình Riccati

#### Rời rạc hóa (ZOH, Δt = 1/f_c = 1/15 s)

```
A_d = [1   Δt]      B_d = [Δt²/2]
      [0    1]            [  Δt  ]
```

#### Phương trình Algebraic Riccati rời rạc (DARE)

```
P = Q + A_dᵀ P A_d − A_dᵀ P B_d (R + B_dᵀ P B_d)⁻¹ B_dᵀ P A_d
```

Giải offline (chỉ 1 lần vì A, B, Q, R không đổi) → ma trận P ∈ ℝ^{2×2}.

#### Gain matrix

```
K = (R + B_dᵀ P B_d)⁻¹ B_dᵀ P A_d ∈ ℝ^{1×2} = [K_p, K_d]
```

K_p: gain vị trí (proportional), K_d: gain vận tốc (derivative).

### 3.5 Luật điều khiển online

Mỗi tick, với mỗi joint i:

```
e_i(t) = q_ref_i(t) − q_fb_i(t)        (sai số vị trí)
ė_i(t) = 0 − q̇_fb_i(t)                 (sai số vận tốc, target vel = 0 cho hold)
         hoặc
ė_i(t) = q̇_ref_i(t) − q̇_fb_i(t)       (nếu có velocity reference)

u_i(t) = K_p · e_i(t) + K_d · ė_i(t)   (gia tốc tối ưu)
```

Sau đó tích phân để có velocity command:

```
q̇_cmd_i(t) = q̇_fb_i(t) + u_i(t) · Δt
q_cmd_i(t) = q_fb_i(t) + q̇_cmd_i(t) · Δt
```

Clamp safety:

```
q̇_cmd_i(t) = clip(q̇_cmd_i(t), −q̇_max_i, +q̇_max_i)
q_cmd_i(t) = clip(q_cmd_i(t), q_min_i, q_max_i)
```

Gửi xuống MotoROS2:

```python
point.positions = [q_cmd_1, ..., q_cmd_6]
point.velocities = [q̇_cmd_1, ..., q̇_cmd_6]
```

---

## 4. Thiết Kế Tham Số Cụ Thể Cho HC10DTP

### 4.1 Tham số đề xuất

Vì mục tiêu là **minimum jerk** cho co-carrying (chuyển động chậm, an toàn), đề xuất ρ lớn:

```
Q = diag([50.0, 1.0])     →  q₁ = 50.0, q₂ = 1.0
R = [10.0]                →  ρ = 10.0
```

Tỉ lệ q₁/ρ = 5.0 — ưu tiên tracking nhưng **phạt gia tốc đáng kể**.

### 4.2 Tính K cụ thể (Python)

```python
import numpy as np
from scipy.linalg import solve_discrete_are

dt = 1.0 / 15.0  # 15 Hz

A_d = np.array([[1, dt],
                [0, 1]])
B_d = np.array([[dt**2 / 2],
                [dt]])

Q = np.diag([50.0, 1.0])
R = np.array([[10.0]])

P = solve_discrete_are(A_d, B_d, Q, R)
K = np.linalg.inv(R + B_d.T @ P @ B_d) @ (B_d.T @ P @ A_d)

print(f"K = [{K[0,0]:.4f}, {K[0,1]:.4f}]")
print(f"  K_p = {K[0,0]:.4f} (position gain)")
print(f"  K_d = {K[0,1]:.4f} (velocity gain)")
```

K sẽ cho ra dạng [K_p, K_d] ≈ [~1.5–2.5, ~0.3–0.6] tùy theo Q, R — chỉ cần tính **một lần** offline.

### 4.3 Adaptive Q (Liên kết với w)

Đây là điểm **rất hay cho paper** — liên kết LQR gain với adaptive weight w:

```
q₁(t) = q₁_base · (0.5 + w(t))
```

- **w cao** (trust prediction) → q₁ lớn → tracking sát q_ref (proactive)
- **w thấp** (trust feedback) → q₁ nhỏ → phản ứng chậm, mượt (conservative)

Khi q₁ thay đổi, cần **re-solve DARE** — nhưng vì 2×2, chi phí rất nhỏ (~μs).

---

## 5. So Sánh: Có LQR vs. Không LQR

| Tiêu chí | Hiện tại (sai phân) | Với LQR |
|----------|---------------------|---------|
| Velocity command | Δq/Δt rồi clamp | Optimal từ cost function |
| Jerk | Không kiểm soát | Tối thiểu (phạt qua R) |
| Tracking | Trực tiếp (1 tick delay) | Optimal convergence rate |
| Stability | Heuristic clamp | Provable (Lyapunov) |
| Computational cost | O(1) | O(1) — K tính offline |
| Paper contribution | Không có | Optimal control formulation |
| MotoROS2 cubic interpolation | Velocity có thể không khớp | Velocity tối ưu → cubic mượt hơn |

---

## 6. Tích Hợp Vào Code

### 6.1 Thay đổi tối thiểu

Chỉ cần sửa trong `_send_joint_point()` phần MOTION point (dòng 1168-1191):

```python
# TRƯỚC (sai phân đơn giản):
raw_velocities = [(target - queued) / dt for target, queued in zip(joints, self._last_queued_joints)]

# SAU (LQR):
for i in range(6):
    e_pos = joints[i] - self._current_joints[i]          # q_ref - q_fb
    e_vel = 0.0 - self._current_joint_velocities[i]      # target vel = 0
    u = K_p * e_pos + K_d * e_vel                         # optimal accel
    q_dot_cmd = self._current_joint_velocities[i] + u * dt
    q_cmd = self._current_joints[i] + q_dot_cmd * dt
    lqr_positions[i] = q_cmd
    lqr_velocities[i] = q_dot_cmd

point.positions = lqr_positions   # thay vì joints trực tiếp
point.velocities = lqr_velocities # thay vì sai phân
```

### 6.2 Cần thêm: Ước lượng q̇_fb

Hiện tại `/joint_states` chỉ có `positions`. Cần ước lượng vận tốc:

```python
# Trong _on_joint_state callback:
self._current_joint_velocities[i] = (new_position - old_position) / dt_joint_states
```

Hoặc dùng EMA để lọc nhiễu.

---

## 7. Đánh Giá Cho Paper

### 7.1 Đóng góp thêm

Thêm LQR tạo ra **3 tầng adaptive**:

1. **Tầng 1**: Adaptive Weight Generator (w) — cân bằng prediction vs. feedback
2. **Tầng 2**: Trajectory Smoother — lọc quỹ đạo Cartesian
3. **Tầng 3 (MỚI)**: LQR Controller — tối ưu velocity ở không gian joint

Đặc biệt nếu kết hợp **Adaptive Q** (liên kết q₁ với w), toàn bộ hệ thống trở thành **end-to-end adaptive** — rất mạnh cho paper.

### 7.2 Equations cho paper

```
State:      x(t) = [q(t) − q_ref(t), q̇(t)]ᵀ ∈ ℝ^{12}  (6 joints × 2 states)
Control:    u(t) = [q̈₁, ..., q̈₆]ᵀ ∈ ℝ⁶
Cost:       J = Σ [xᵀ Q̃ x + uᵀ R̃ u]

Q̃ = diag(q₁I₆, q₂I₆) ∈ ℝ^{12×12}
R̃ = ρ · I₆ ∈ ℝ^{6×6}

Optimal gain: K* = (R̃ + B̃ᵀPB̃)⁻¹ B̃ᵀPÃ
Control law:  u*(t) = −K* · x(t)
```

Vì các joint **decoupled** trong mô hình integrator kép, K* thực chất là **6 bộ LQR 2×2 độc lập** — rất hiệu quả.

---

## 8. Kết Luận

> [!TIP]
> **Hoàn toàn nên thêm LQR.** Nó:
> - Thay thế sai phân heuristic bằng optimal control — **có cơ sở lý thuyết**
> - Tận dụng velocity field mà MotoROS2 đã hỗ trợ
> - Giảm jerk rõ rệt qua penalty ρ
> - Thêm contribution cho paper (optimal + adaptive)
> - Code thay đổi rất ít (~20 dòng trong `_send_joint_point`)
> - Computational cost: O(1) vì K tính offline

> [!WARNING]
> **Lưu ý**: Cần test kỹ trên robot thật vì:
> - q̇_fb ước lượng từ sai phân có thể nhiễu → cần EMA filter
> - K_p, K_d cần tune trên robot thật (bắt đầu conservative: q₁=20, ρ=20)
> - Adaptive Q (liên kết với w) cần test tính ổn định khi w thay đổi nhanh
