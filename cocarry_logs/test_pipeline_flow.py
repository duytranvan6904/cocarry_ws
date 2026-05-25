import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from human_hand_msgs.msg import HandState, HandPrediction
from geometry_msgs.msg import PoseStamped, PointStamped
from std_msgs.msg import String, Bool
from std_srvs.srv import SetBool, Trigger
import time
import math
import sys
import threading

class PipelineTester(Node):
    def __init__(self):
        super().__init__('pipeline_tester')
        
        # Publishers
        self.hand_pub = self.create_publisher(HandState, '/hand_position', 10)
        self.pose_pub = self.create_publisher(PoseStamped, '/cartesian_streamer/current_pose', 10)
        self.mode_pub = self.create_publisher(String, '/trajectory_mode', 10)
        self.run_pub = self.create_publisher(Bool, '/run_status', 10)
        
        # Subscribers
        self.pred_sub = self.create_subscription(HandPrediction, '/ml/predicted_position', self.cb_pred, 10)
        self.filtered_sub = self.create_subscription(PointStamped, '/coord_transform/filtered_hand_position', self.cb_filtered, 10)
        self.target_sub = self.create_subscription(PoseStamped, '/cartesian_streamer/target_pose', self.cb_target, 10)
        
        # Counters
        self.cnt_pred = 0
        self.cnt_filtered = 0
        self.cnt_target = 0
        
        self.start_time = time.time()
        self.timer_pose = self.create_timer(0.1, self.publish_pose)
        self.timer_hand = self.create_timer(0.05, self.publish_hand)
        
        # Clients
        self.cli_capture = self.create_client(Trigger, '/coord_transform/capture_init_pose')
        self.cli_toggle = self.create_client(SetBool, '/predictor/toggle')
        
    def publish_pose(self):
        msg = PoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        msg.pose.position.x = 0.5
        msg.pose.position.y = 0.0
        msg.pose.position.z = 0.4
        msg.pose.orientation.x = 0.0
        msg.pose.orientation.y = 1.0
        msg.pose.orientation.z = 0.0
        msg.pose.orientation.w = 0.0
        self.pose_pub.publish(msg)
        
    def publish_hand(self):
        t = time.time() - self.start_time
        msg = HandState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'camera_frame'
        # Add smooth movement
        msg.x = 0.05 * math.sin(2 * math.pi * 0.2 * t)
        msg.y = 0.45 + 0.03 * math.cos(2 * math.pi * 0.1 * t)
        msg.z = 0.35
        msg.is_tracked = True
        msg.confidence = 0.95
        msg.source = 'test'
        self.hand_pub.publish(msg)
        
    def cb_pred(self, msg):
        self.cnt_pred += 1
        print(f"[TESTER] Received Prediction #{self.cnt_pred}: x={msg.x:.4f}, y={msg.y:.4f}, z={msg.z:.4f}, inf={msg.inference_time_ms:.1f}ms")
        
    def cb_filtered(self, msg):
        self.cnt_filtered += 1
        print(f"[TESTER] Received Filtered Hand Pos #{self.cnt_filtered}: x={msg.point.x:.4f}, y={msg.point.y:.4f}, z={msg.point.z:.4f}")
        
    def cb_target(self, msg):
        self.cnt_target += 1
        print(f"[TESTER] Received Robot Target #{self.cnt_target}: x={msg.pose.position.x:.4f}, y={msg.pose.position.y:.4f}, z={msg.pose.position.z:.4f}")

def run_tester():
    rclpy.init()
    tester = PipelineTester()
    
    # Run spin with MultiThreadedExecutor
    executor = MultiThreadedExecutor()
    executor.add_node(tester)
    thread = threading.Thread(target=executor.spin, daemon=True)
    thread.start()
    
    print("[TESTER] Waiting for capture_init_pose service...")
    if not tester.cli_capture.wait_for_service(timeout_sec=10.0):
        print("[TESTER] ERROR: capture_init_pose service not available!")
        rclpy.shutdown()
        return

    print("[TESTER] Waiting for predictor/toggle service...")
    if not tester.cli_toggle.wait_for_service(timeout_sec=10.0):
        print("[TESTER] ERROR: predictor/toggle service not available!")
        rclpy.shutdown()
        return

    print("[TESTER] Waiting 5 seconds to ensure current pose is received by transform_node...")
    time.sleep(5.0)

    # 1. Call Capture Initial Pose
    print("[TESTER] Calling capture_init_pose...")
    req = Trigger.Request()
    future = tester.cli_capture.call_async(req)
    while not future.done():
        time.sleep(0.1)
    res = future.result()
    if res:
        print(f"[TESTER] Capture result: success={res.success}, message='{res.message}'")
    else:
        print("[TESTER] Capture service call failed")
        
    # 2. Start running in Ground Truth Mode
    print("\n=== STARTING GROUND TRUTH MODE ===")
    run_msg = Bool()
    run_msg.data = True
    tester.run_pub.publish(run_msg)
    
    mode_msg = String()
    mode_msg.data = 'ground_truth'
    tester.mode_pub.publish(mode_msg)
    
    time.sleep(4.0)
    
    # 3. Switch to Prediction Mode
    print("\n=== SWITCHING TO PREDICTION MODE ===")
    
    # Enable predictor service
    print("[TESTER] Toggling predictor node ON...")
    req_toggle = SetBool.Request()
    req_toggle.data = True
    future_toggle = tester.cli_toggle.call_async(req_toggle)
    while not future_toggle.done():
        time.sleep(0.1)
    res_toggle = future_toggle.result()
    if res_toggle:
         print(f"[TESTER] Toggle result: success={res_toggle.success}, message='{res_toggle.message}'")
    else:
         print("[TESTER] Toggle service call failed")
         
    mode_msg.data = 'prediction'
    tester.mode_pub.publish(mode_msg)
    
    time.sleep(6.0)
    
    # Finish and print counts
    print("\n=== TEST CONCLUDED ===")
    print(f"Total Predictions received: {tester.cnt_pred}")
    print(f"Total Filtered positions received: {tester.cnt_filtered}")
    print(f"Total Robot Targets received: {tester.cnt_target}")
    
    rclpy.shutdown()

if __name__ == '__main__':
    run_tester()
