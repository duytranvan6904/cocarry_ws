#!/usr/bin/env python3
"""
calibrate_camera_to_robot.py
──────────────────────────────
Tính ma trận transform từ camera frame (RealSense) → robot base frame.

QUY TRÌNH:
  1. Đặt 6-8 marker tại vị trí cố định trong workspace
  2. Dùng teach pendant đọc tọa độ XYZ (robot base frame)
  3. Đọc tọa độ XYZ từ RealSense (camera frame)
  4. Điền vào POINTS_CAM và POINTS_ROBOT
  5. Chạy script

CHẠY:
  python3 calibrate_camera_to_robot.py
  python3 calibrate_camera_to_robot.py --output ../config/transform_params.yaml

YÊU CẦU:
  pip install numpy scipy pyyaml
"""

import numpy as np
from scipy.spatial.transform import Rotation
import yaml
import argparse
import sys


# ══════════════════════════════════════════════════════════════════════════════
# NHẬP DỮ LIỆU ĐO ĐẠC (điền vào sau khi đo thực tế)
# ══════════════════════════════════════════════════════════════════════════════

# Tọa độ các điểm marker đo từ camera RealSense (camera frame, meters)
POINTS_CAM = np.array([
    # [x_cam,  y_cam,  z_cam ]
    [ 0.10,   0.05,   0.82  ],
    [ 0.30,   0.08,   0.91  ],
    [-0.12,  -0.03,   0.85  ],
    [ 0.05,   0.18,   0.76  ],
    [ 0.22,  -0.10,   0.88  ],
    [-0.05,   0.12,   0.79  ],
])

# Tọa độ các điểm marker đọc từ robot teach pendant (robot base frame, meters)
POINTS_ROBOT = np.array([
    # [x_base, y_base, z_base]
    [ 0.50,   0.12,   0.38  ],
    [ 0.62,  -0.08,   0.35  ],
    [ 0.42,   0.15,   0.40  ],
    [ 0.52,  -0.04,   0.48  ],
    [ 0.58,   0.20,   0.36  ],
    [ 0.44,   0.08,   0.45  ],
])

# ══════════════════════════════════════════════════════════════════════════════


def solve_rigid_transform(points_src: np.ndarray, points_dst: np.ndarray):
    """
    Tìm R, t sao cho: points_dst ≈ R @ points_src + t
    Sử dụng SVD (Kabsch algorithm).

    Returns:
        R: (3,3) rotation matrix
        t: (3,) translation vector
        quat: (4,) quaternion [x, y, z, w]
        rmse_mm: residual error in mm
    """
    assert points_src.shape == points_dst.shape
    assert points_src.shape[0] >= 3

    c_src = points_src.mean(axis=0)
    c_dst = points_dst.mean(axis=0)

    A = points_src - c_src
    B = points_dst - c_dst

    H = A.T @ B
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T

    if np.linalg.det(R) < 0:
        Vt[-1, :] *= -1
        R = Vt.T @ U.T

    t = c_dst - R @ c_src

    transformed = (R @ points_src.T).T + t
    residuals = np.linalg.norm(transformed - points_dst, axis=1)
    rmse_mm = residuals.mean() * 1000.0

    quat = Rotation.from_matrix(R).as_quat()
    return R, t, quat, rmse_mm


def print_results(R, t, quat, rmse_mm):
    print('\n' + '=' * 60)
    print('  KẾT QUẢ CALIBRATION')
    print('=' * 60)
    print(f'\nResidual RMSE: {rmse_mm:.2f} mm')
    if rmse_mm > 20:
        print('  ⚠  RMSE > 20mm — kiểm tra lại dữ liệu!')
    elif rmse_mm > 10:
        print('  ⚠  RMSE > 10mm — chấp nhận được nhưng nên đo thêm')
    else:
        print('  ✓  RMSE tốt (< 10mm)')

    print(f'\nRotation matrix R:')
    for row in R:
        print(f'  [{row[0]:+.6f}  {row[1]:+.6f}  {row[2]:+.6f}]')

    print(f'\nQuaternion (x, y, z, w):')
    print(f'  x = {quat[0]:+.8f}')
    print(f'  y = {quat[1]:+.8f}')
    print(f'  z = {quat[2]:+.8f}')
    print(f'  w = {quat[3]:+.8f}')

    print(f'\nTranslation (meters):')
    print(f'  tx = {t[0]:+.6f}')
    print(f'  ty = {t[1]:+.6f}')
    print(f'  tz = {t[2]:+.6f}')
    print()


def write_yaml(output_path: str, quat, t, current_yaml_path=None):
    """Ghi kết quả vào file YAML params."""
    if current_yaml_path:
        try:
            with open(current_yaml_path) as f:
                data = yaml.safe_load(f)
        except FileNotFoundError:
            data = {}
    else:
        data = {}

    if 'coord_transform' not in data:
        data['coord_transform'] = {}
    if 'ros__parameters' not in data['coord_transform']:
        data['coord_transform']['ros__parameters'] = {}

    params = data['coord_transform']['ros__parameters']
    params['cam_to_base_qx'] = float(quat[0])
    params['cam_to_base_qy'] = float(quat[1])
    params['cam_to_base_qz'] = float(quat[2])
    params['cam_to_base_qw'] = float(quat[3])
    params['cam_to_base_tx'] = float(t[0])
    params['cam_to_base_ty'] = float(t[1])
    params['cam_to_base_tz'] = float(t[2])

    with open(output_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    print(f'✓ Đã ghi kết quả vào: {output_path}')


def main():
    parser = argparse.ArgumentParser(
        description='Calibrate camera-to-robot base transform')
    parser.add_argument(
        '--output', type=str, default=None,
        help='Path to output YAML file')
    parser.add_argument(
        '--update', type=str, default=None,
        help='Path to existing YAML to update')
    args = parser.parse_args()

    if len(POINTS_CAM) < 4:
        print('LỖI: Cần ít nhất 4 cặp điểm.')
        sys.exit(1)

    print(f'Số cặp điểm: {len(POINTS_CAM)}')
    R, t, quat, rmse_mm = solve_rigid_transform(POINTS_CAM, POINTS_ROBOT)
    print_results(R, t, quat, rmse_mm)

    if args.output:
        write_yaml(args.output, quat, t, current_yaml_path=args.update)
    else:
        print('Dùng --output <file.yaml> để lưu kết quả.')


if __name__ == '__main__':
    main()
