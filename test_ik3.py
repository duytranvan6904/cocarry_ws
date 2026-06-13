import sys
import numpy as np
from src.hc10dtp_bringup.scripts.local_ik_solver import LocalIKSolver

solver = LocalIKSolver()
seed = [1.570787, 0.124237, -1.022417, 0.000011, -0.397854, 0.000011]
pos, quat = solver.fk_pose(seed)
print(f"FK pos: {pos}")
print(f"FK quat (x,y,z,w): {quat}")
