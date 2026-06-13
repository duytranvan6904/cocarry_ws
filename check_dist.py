import sys, rclpy, math, numpy as np
from geometry_msgs.msg import PoseStamped

# Tọa độ T2 từ file yaml
t2 = np.array([0.047798, 1.120817, 0.477037])

def callback(msg):
    pos = [msg.pose.position.x, msg.pose.position.y, msg.pose.position.z]
    dist = np.linalg.norm(np.array(pos) - t2)
    print(f"Current Target Base: {pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f}")
    print(f"T2 Target Base     : {t2[0]:.3f}, {t2[1]:.3f}, {t2[2]:.3f}")
    print(f"Distance to T2     : {dist*100:.2f} cm")
    print(f"Bán kính snap_radius hiện tại: 8.0 cm")
    
    if dist <= 0.08:
        print("=> Nằm TRONG vùng snap!")
    else:
        print("=> Nằm NGOÀI vùng snap!")
    sys.exit(0)

rclpy.init()
node = rclpy.create_node('check_dist_node')
sub = node.create_subscription(PoseStamped, '/cartesian_streamer/target_pose', callback, 10)
# Thêm timer timeout 3s
node.create_timer(3.0, lambda: sys.exit("No data received on /cartesian_streamer/target_pose"))
rclpy.spin(node)
