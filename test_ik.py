import sys
import numpy as np
from src.hc10dtp_bringup.scripts.local_ik_solver import LocalIKSolver

solver = LocalIKSolver()
pos = [-0.16, 0.331, 0.449]
quat = [0.0, 1.0, 0.0, 0.0]
seed = [1.570787, 0.124237, -1.022417, 0.000011, -0.397854, 0.000011]
res = solver.solve_ik(pos, quat, seed)
print(f"IK result: {res}")
