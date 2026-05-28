#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import random
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional
import json
import os
import time
from datetime import datetime
import threading
import csv

# ROS 2 imports
import rclpy
from rclpy.node import Node as RosNode
from rclpy.executors import MultiThreadedExecutor
from geometry_msgs.msg import PointStamped, PoseStamped

# ============================================================================
# CONFIGURATION AND DATA STRUCTURES
# ============================================================================

class ExperimentState(Enum):
    IDLE = "idle"
    READY = "ready"
    RUNNING = "running"
    FINISHED = "finished"

class Mode(Enum):
    FREE = "Free"
    CHANGE = "Change"

@dataclass
class Scenario:
    scenario_id: str
    modus: Mode
    initial_target: int
    final_target: int
    
    def is_change_scenario(self) -> bool:
        return self.initial_target != self.final_target

# Workspace bounds (meters)
WORKSPACE_WIDTH = 1.0  # X: -0.5 to 0.5
WORKSPACE_HEIGHT = 1.2 # Y: 0 to 1.2

# 3 New Targets Layout
TARGET_POSITIONS = {
    1: (0.30, 0.80, 0.30),   # Right
    2: (-0.30, 0.80, 0.30),  # Left
    3: (0.00, 1.00, 0.45)    # Center, Far, High
}

START_POSITION = (0.0, 0.40, 0.25)

# Total 9 Scenarios
SCENARIOS = [
    # Free mode
    Scenario("SCF1", Mode.FREE, 1, 1),
    Scenario("SCF2", Mode.FREE, 2, 2),
    Scenario("SCF3", Mode.FREE, 3, 3),
    
    # Change mode
    Scenario("SCC1", Mode.CHANGE, 1, 2),
    Scenario("SCC2", Mode.CHANGE, 2, 1),
    Scenario("SCC3", Mode.CHANGE, 1, 3),
    Scenario("SCC4", Mode.CHANGE, 2, 3),
    Scenario("SCC5", Mode.CHANGE, 3, 1),
    Scenario("SCC6", Mode.CHANGE, 3, 2),
]

OUTPUT_DIR = os.path.expanduser("~/cocarry_ws/cocarry_logs/data_collection")

# ============================================================================
# ROS 2 DATA COLLECTOR
# ============================================================================

class HandPoseSubscriber(RosNode):
    """ROS 2 Node that subscribes to wrist position and logs it via an internal timer."""
    def __init__(self, sample_rate: float):
        super().__init__('data_collection_gui_node')
        
        self.latest_pose = None
        self.is_recording = False
        self.trial_data = []
        
        self.sub_pose = self.create_subscription(
            PoseStamped,
            '/transformed_hand_pose',
            self.pose_callback,
            10
        )
        
        self.sample_period = 1.0 / sample_rate
        self.timer = self.create_timer(self.sample_period, self.timer_callback)
        self.start_time = 0.0

    def pose_callback(self, msg):
        self.latest_pose = (msg.pose.position.x, msg.pose.position.y, msg.pose.position.z)
        
    def timer_callback(self):
        if not self.is_recording:
            return
            
        current_time = time.time()
        elapsed_s = current_time - self.start_time
        
        if self.latest_pose:
            x, y, z = self.latest_pose
            self.trial_data.append((elapsed_s, x, y, z))
        else:
            self.trial_data.append((elapsed_s, 0.0, 0.0, 0.0))

    def start_recording(self):
        self.trial_data = []
        self.is_recording = True
        self.start_time = time.time()

    def stop_recording(self) -> list:
        self.is_recording = False
        return self.trial_data

# ============================================================================
# EXPERIMENT LOGIC MANAGER
# ============================================================================

class ScenarioManager:
    def __init__(self):
        self.participant_id = "p01"
        self.trial_duration = 8.0
        self.sample_rate = 16.0
        self.y_threshold = 0.60
        
        self.random_scenario_enabled = True
        
        self.state = ExperimentState.IDLE
        self.scenario_queue: List[Scenario] = []
        self.current_scenario_idx = 0
        self.current_scenario: Optional[Scenario] = None
        
        self.recording_start_time = 0.0
        self.change_triggered = False
        self.repeats_per_scenario = 4
        self.current_repeat = 1
        
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        self.initialize_scenarios()

    def initialize_scenarios(self):
        if self.random_scenario_enabled:
            self.scenario_queue = SCENARIOS.copy()
            random.shuffle(self.scenario_queue)
        else:
            # When manual, we just queue the current scenario selected
            pass
            
        self.current_scenario_idx = 0
        if self.scenario_queue:
            self.current_scenario = self.scenario_queue[0]
        self.current_repeat = 1
        self.state = ExperimentState.READY
        self.change_triggered = False

    def next_scenario(self):
        self.current_repeat += 1
        if self.current_repeat > self.repeats_per_scenario:
            self.current_repeat = 1
            self.current_scenario_idx += 1
            
        if self.current_scenario_idx < len(self.scenario_queue):
            self.current_scenario = self.scenario_queue[self.current_scenario_idx]
            self.state = ExperimentState.READY
        else:
            self.state = ExperimentState.FINISHED
            
        self.change_triggered = False

    def reset(self):
        self.initialize_scenarios()

    def save_to_csv(self, data: list):
        if not self.current_scenario:
            return None
            
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.participant_id}_{self.current_scenario.scenario_id}_r{self.current_repeat:02d}_{timestamp_str}.csv"
        
        participant_dir = os.path.join(OUTPUT_DIR, self.participant_id)
        os.makedirs(participant_dir, exist_ok=True)
        filepath = os.path.join(participant_dir, filename)
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([f"# participant_id: {self.participant_id}"])
            writer.writerow([f"# scenario_id: {self.current_scenario.scenario_id}"])
            writer.writerow([f"# mode: {self.current_scenario.modus.value}"])
            writer.writerow([f"# initial_target: {self.current_scenario.initial_target}"])
            writer.writerow([f"# final_target: {self.current_scenario.final_target}"])
            writer.writerow([f"# sample_rate_hz: {self.sample_rate}"])
            writer.writerow([f"# trial_duration_s: {self.trial_duration}"])
            writer.writerow([f"# y_threshold_trigger: {self.y_threshold}"])
            writer.writerow([f"# recorded_at: {datetime.now().isoformat()}"])
            
            writer.writerow(['timestamp_s', 'x', 'y', 'z'])
            for row in data:
                writer.writerow([f"{row[0]:.4f}", f"{row[1]:.4f}", f"{row[2]:.4f}", f"{row[3]:.4f}"])
                
        return filepath

# ============================================================================
# GUI VISUALIZATION
# ============================================================================

class WorkspaceCanvas(tk.Canvas):
    """2D top-down visualization of the experimental workspace"""
    def __init__(self, parent, manager: ScenarioManager, **kwargs):
        super().__init__(parent, **kwargs)
        self.manager = manager
        
        self.canvas_width = 1000 
        self.canvas_height = 800
        self.margin_x = 100
        self.margin_y = 100
        
        self.config(bg="#1a1a1a")
        self.recalculate_scaling()
        
        self.bind("<Configure>", self.on_resize)
        self.draw_workspace()

    def recalculate_scaling(self):
        self.draw_width = self.canvas_width - 2 * self.margin_x
        self.draw_height = self.canvas_height - 2 * self.margin_y
        
        if self.draw_width <= 0: self.draw_width = 1
        if self.draw_height <= 0: self.draw_height = 1

        self.scale_x = self.draw_width / WORKSPACE_WIDTH
        self.scale_y = self.draw_height / WORKSPACE_HEIGHT

    def on_resize(self, event):
        self.canvas_width = event.width
        self.canvas_height = event.height
        self.recalculate_scaling()
        self.draw_workspace()
        
    def world_to_canvas(self, x: float, y: float) -> Tuple[int, int]:
        canvas_x = self.canvas_width / 2 + x * self.scale_x
        canvas_y = self.canvas_height - self.margin_y - y * self.scale_y
        return int(canvas_x), int(canvas_y)
    
    def draw_workspace(self):
        self.delete("all")
        
        self.create_rectangle(2, 2, self.canvas_width - 2, self.canvas_height - 2, outline="#444444", width=2)
        
        center_x = self.canvas_width / 2
        base_y = self.canvas_height - self.margin_y
        self.create_line(center_x, base_y, center_x, self.margin_y, fill="#333333", dash=(2, 4))
        
        # Draw threshold line if change scenario
        if self.manager.current_scenario and self.manager.current_scenario.is_change_scenario():
            _, thresh_y = self.world_to_canvas(0, self.manager.y_threshold)
            self.create_line(self.margin_x, thresh_y, self.canvas_width - self.margin_x, thresh_y, fill="#555500", dash=(4, 4), width=2)
            self.create_text(self.margin_x + 30, thresh_y - 10, text=f"Trigger Y = {self.manager.y_threshold}m", fill="#888800")
            
        self.draw_start_zone()
        self.draw_targets()
        self.draw_hud()
    
    def draw_start_zone(self):
        cx, cy = self.world_to_canvas(START_POSITION[0], START_POSITION[1])
        size = 60
        
        color = "#4CAF50" if self.manager.state == ExperimentState.RUNNING else "#FF69B4"
        glow = "#6BB6FF" if self.manager.state == ExperimentState.RUNNING else "#FFB6D9"
        
        self.create_rectangle(cx - size - 4, cy - size - 4, cx + size + 4, cy + size + 4, fill=glow, outline="")
        self.create_rectangle(cx - size, cy - size, cx + size, cy + size, fill=color, outline="#FFFFFF", width=2)
        self.create_text(cx, cy, text="START", fill="white", font=("Arial", 16, "bold"))
    
    def draw_targets(self):
        for target_id, position in TARGET_POSITIONS.items():
            self.draw_target(target_id, position)
            
    def draw_target(self, target_id: int, position: Tuple[float, float, float]):
        cx, cy = self.world_to_canvas(position[0], position[1])
        size = 60
        
        is_active = self.is_target_active(target_id)
        
        if is_active:
            color = "#FFD700"
            outline_color = "#FFA500"
            for i in range(2):
                self.create_rectangle(cx - size - (i*4), cy - size - (i*4), cx + size + (i*4), cy + size + (i*4), outline="#FFED4E", width=2)
        else:
            color = "#665500"
            outline_color = "#888800"
        
        self.create_rectangle(cx - size, cy - size, cx + size, cy + size, fill=color, outline=outline_color, width=2)
        text_color = "white" if is_active else "#999999"
        self.create_text(cx, cy, text=f"T{target_id}", fill=text_color, font=("Arial", 40, "bold"))
    
    def is_target_active(self, target_id: int) -> bool:
        scenario = self.manager.current_scenario
        if not scenario or self.manager.state == ExperimentState.IDLE:
            return False
            
        if scenario.is_change_scenario():
            if self.manager.state == ExperimentState.RUNNING and self.manager.change_triggered:
                return target_id == scenario.final_target
            return target_id == scenario.initial_target
        else:
            return target_id == scenario.initial_target

    def draw_hud(self):
        if self.manager.state == ExperimentState.RUNNING:
            if int(time.time() * 2) % 2 == 0:
                self.create_text(self.canvas_width/2, 40, text="🔴 RECORDING", fill="red", font=("Arial", 24, "bold"))
            
            elapsed = time.time() - self.manager.recording_start_time
            remaining = max(0, self.manager.trial_duration - elapsed)
            progress = min(1.0, elapsed / self.manager.trial_duration)
            
            bar_width = 400
            bar_x = self.canvas_width/2 - bar_width/2
            bar_y = 80
            
            self.create_rectangle(bar_x, bar_y, bar_x + bar_width, bar_y + 20, fill="#333333", outline="white")
            self.create_rectangle(bar_x, bar_y, bar_x + (bar_width * progress), bar_y + 20, fill="#4CAF50", outline="")
            self.create_text(self.canvas_width/2, bar_y + 40, text=f"{remaining:.1f}s", fill="white", font=("Arial", 16))
            
            if self.manager.current_scenario.is_change_scenario() and self.manager.change_triggered:
                self.create_text(self.canvas_width/2, self.canvas_height - 40, text="CHANGE TARGET NOW!", fill="yellow", font=("Arial", 30, "bold"))

    def update_display(self):
        self.draw_workspace()

# ============================================================================
# CONTROL PANEL
# ============================================================================

class ControlPanel(ttk.Frame):
    def __init__(self, parent, manager: ScenarioManager, canvas: WorkspaceCanvas, ros_node: HandPoseSubscriber):
        super().__init__(parent, padding=10)
        self.manager = manager
        self.canvas = canvas
        self.ros_node = ros_node
        self.setup_ui()
        self.update_ui_state()
        
    def setup_ui(self):
        title = ttk.Label(self, text="Data Collection Control Panel", font=("Arial", 14, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # Participant ID
        ttk.Label(self, text="Participant ID:").grid(row=1, column=0, sticky="w", pady=5)
        self.part_entry = ttk.Entry(self, width=15)
        self.part_entry.insert(0, "p01")
        self.part_entry.grid(row=1, column=1, sticky="w", pady=5)
        
        # Duration & Threshold
        ttk.Label(self, text="Duration (s):").grid(row=2, column=0, sticky="w", pady=5)
        self.duration_spinbox = ttk.Spinbox(self, from_=2.0, to=20.0, increment=1.0, width=13)
        self.duration_spinbox.set(8.0)
        self.duration_spinbox.grid(row=2, column=1, sticky="w", pady=5)
        
        ttk.Label(self, text="Y-Threshold (m):").grid(row=3, column=0, sticky="w", pady=5)
        self.threshold_spinbox = ttk.Spinbox(self, from_=0.1, to=1.2, increment=0.05, width=13)
        self.threshold_spinbox.set(0.60)
        self.threshold_spinbox.grid(row=3, column=1, sticky="w", pady=5)

        ttk.Separator(self, orient="horizontal").grid(row=4, column=0, columnspan=2, sticky="ew", pady=10)

        # Mode Selection (Random / Manual)
        ttk.Label(self, text="Random Mode:").grid(row=5, column=0, sticky="w", pady=5)
        self.random_var = tk.BooleanVar(value=True)
        self.random_check = ttk.Checkbutton(self, variable=self.random_var, command=self.on_random_toggle)
        self.random_check.grid(row=5, column=1, sticky="w", pady=5)

        ttk.Label(self, text="Manual Scenario:").grid(row=6, column=0, sticky="w", pady=5)
        self.scenario_combo = ttk.Combobox(self, values=[s.scenario_id for s in SCENARIOS], state="disabled", width=13)
        self.scenario_combo.grid(row=6, column=1, sticky="w", pady=5)
        self.scenario_combo.bind("<<ComboboxSelected>>", self.on_manual_select)

        ttk.Separator(self, orient="horizontal").grid(row=7, column=0, columnspan=2, sticky="ew", pady=10)
        
        # Status
        ttk.Label(self, text="Current Scenario:").grid(row=8, column=0, sticky="w", pady=5)
        self.scenario_label = ttk.Label(self, text="—", font=("Arial", 12, "bold"))
        self.scenario_label.grid(row=8, column=1, sticky="w", pady=5)
        
        ttk.Label(self, text="Repeat:").grid(row=9, column=0, sticky="w", pady=5)
        self.repeat_label = ttk.Label(self, text="1 / 4")
        self.repeat_label.grid(row=9, column=1, sticky="w", pady=5)
        
        ttk.Label(self, text="Progress:").grid(row=10, column=0, sticky="w", pady=5)
        self.progress_label = ttk.Label(self, text="0 / 9")
        self.progress_label.grid(row=10, column=1, sticky="w", pady=5)
        
        # Buttons
        self.start_btn = ttk.Button(self, text="START TRIAL", command=self.on_start)
        self.start_btn.grid(row=11, column=0, columnspan=2, sticky="ew", pady=10, ipady=10)
        
        self.next_btn = ttk.Button(self, text="Next Scenario", command=self.on_next, state="disabled")
        self.next_btn.grid(row=12, column=0, columnspan=2, sticky="ew", pady=5)
        
        self.reset_btn = ttk.Button(self, text="Reset Queue", command=self.on_reset)
        self.reset_btn.grid(row=13, column=0, columnspan=2, sticky="ew", pady=20)
        
        # Console output
        self.console = tk.Text(self, height=8, width=35, bg="black", fg="lime", font=("Courier", 9))
        self.console.grid(row=14, column=0, columnspan=2, sticky="ew")
        self.log("System initialized.")
        
    def log(self, message: str):
        self.console.insert(tk.END, f"{message}\n")
        self.console.see(tk.END)

    def on_random_toggle(self):
        is_random = self.random_var.get()
        self.manager.random_scenario_enabled = is_random
        if is_random:
            self.scenario_combo.config(state="disabled")
            self.manager.initialize_scenarios()
        else:
            self.scenario_combo.config(state="readonly")
            if self.scenario_combo.get() == "":
                self.scenario_combo.current(0)
            self.on_manual_select(None)
        self.update_ui_state()
        self.canvas.update_display()

    def on_manual_select(self, event):
        scenario_id = self.scenario_combo.get()
        if scenario_id:
            scenario = next(s for s in SCENARIOS if s.scenario_id == scenario_id)
            self.manager.scenario_queue = [scenario]
            self.manager.current_scenario_idx = 0
            self.manager.current_scenario = scenario
            self.manager.current_repeat = 1
            self.manager.state = ExperimentState.READY
            self.update_ui_state()
            self.canvas.update_display()
        
    def on_start(self):
        # Update config
        self.manager.participant_id = self.part_entry.get().strip()
        self.manager.trial_duration = float(self.duration_spinbox.get())
        self.manager.y_threshold = float(self.threshold_spinbox.get())
        
        # Update state
        self.manager.state = ExperimentState.RUNNING
        self.manager.recording_start_time = time.time()
        self.manager.change_triggered = False
        
        # Start ROS collector
        self.ros_node.start_recording()
        
        self.log(f"Started {self.manager.current_scenario.scenario_id} rep {self.manager.current_repeat}")
        self.update_ui_state()
        self.canvas.update_display()
        
    def on_next(self):
        self.manager.next_scenario()
        self.update_ui_state()
        self.canvas.update_display()
        
    def on_reset(self):
        self.manager.reset()
        self.update_ui_state()
        self.canvas.update_display()
        self.log("Reset scenario queue.")

    def update_ui_state(self):
        state = self.manager.state
        scen = self.manager.current_scenario
        
        if scen:
            self.scenario_label.config(text=scen.scenario_id)
            self.repeat_label.config(text=f"{self.manager.current_repeat} / {self.manager.repeats_per_scenario}")
            if self.manager.random_scenario_enabled:
                self.progress_label.config(text=f"{self.manager.current_scenario_idx + 1} / {len(self.manager.scenario_queue)}")
            else:
                self.progress_label.config(text="Manual Mode")
        else:
            self.scenario_label.config(text="DONE")
        
        if state in [ExperimentState.IDLE, ExperimentState.READY]:
            self.start_btn.config(state="normal")
            self.next_btn.config(state="disabled")
            self.part_entry.config(state="normal")
            self.duration_spinbox.config(state="normal")
            self.threshold_spinbox.config(state="normal")
            self.random_check.config(state="normal")
            if not self.manager.random_scenario_enabled:
                self.scenario_combo.config(state="readonly")
        elif state == ExperimentState.RUNNING:
            self.start_btn.config(state="disabled")
            self.next_btn.config(state="disabled")
            self.part_entry.config(state="disabled")
            self.duration_spinbox.config(state="disabled")
            self.threshold_spinbox.config(state="disabled")
            self.random_check.config(state="disabled")
            self.scenario_combo.config(state="disabled")
        elif state == ExperimentState.FINISHED:
            self.start_btn.config(state="disabled")
            self.next_btn.config(state="disabled")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

class App(tk.Tk):
    def __init__(self, ros_node):
        super().__init__()
        self.title("Data Collection - Control Panel")
        self.geometry("400x700")
        self.configure(bg="#f0f0f0")
        
        self.ros_node = ros_node
        self.manager = ScenarioManager()
        
        # Create separate Display Window
        self.display_window = tk.Toplevel(self)
        self.display_window.title("Participant Display")
        self.display_window.geometry("1000x800")
        self.display_window.configure(bg="#000000")
        
        self.canvas = WorkspaceCanvas(self.display_window, self.manager)
        self.canvas.pack(fill="both", expand=True)
        
        # Optional: bind F11 for fullscreen
        self.display_window.bind("<F11>", lambda e: self.display_window.attributes("-fullscreen", not self.display_window.attributes("-fullscreen")))
        self.display_window.bind("<Escape>", lambda e: self.display_window.attributes("-fullscreen", False))

        # Setup Control Panel in main window
        self.control_panel = ControlPanel(self, self.manager, self.canvas, self.ros_node)
        self.control_panel.pack(fill="both", expand=True)
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.update_loop()
        
    def update_loop(self):
        if self.manager.state == ExperimentState.RUNNING:
            elapsed = time.time() - self.manager.recording_start_time
            
            # Distance-based trigger logic
            if self.manager.current_scenario.is_change_scenario() and not self.manager.change_triggered:
                if self.ros_node.latest_pose is not None:
                    _, current_y, _ = self.ros_node.latest_pose
                    if current_y >= self.manager.y_threshold:
                        self.manager.change_triggered = True
                        self.bell()  # Play system bell
                        print(f"BEEP! Y crossed threshold: {current_y:.3f} >= {self.manager.y_threshold}")
            
            # Check for end of trial
            if elapsed >= self.manager.trial_duration:
                # STOP RECORDING
                data = self.ros_node.stop_recording()
                saved_path = self.manager.save_to_csv(data)
                
                self.manager.state = ExperimentState.IDLE
                self.control_panel.log(f"Saved: {os.path.basename(saved_path) if saved_path else 'Error'}")
                self.bell() # Double beep
                self.after(200, self.bell)
                
                # Auto-advance
                self.after(1000, self.auto_advance)
                
            self.canvas.update_display()
            
        self.after(50, self.update_loop)
        
    def auto_advance(self):
        self.manager.next_scenario()
        self.control_panel.update_ui_state()
        self.canvas.update_display()
        if self.manager.state == ExperimentState.READY:
            self.control_panel.log("Ready for next trial.")
        
    def on_close(self):
        self.destroy()

# ============================================================================
# ENTRY
# ============================================================================

def main():
    rclpy.init()
    
    # 16 Hz sampling rate
    data_collector_node = HandPoseSubscriber(sample_rate=16.0)
    
    executor = MultiThreadedExecutor()
    executor.add_node(data_collector_node)
    
    ros_thread = threading.Thread(target=executor.spin, daemon=True)
    ros_thread.start()
    
    try:
        app = App(data_collector_node)
        app.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        executor.shutdown()
        data_collector_node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
