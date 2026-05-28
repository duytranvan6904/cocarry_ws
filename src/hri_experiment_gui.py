"""
Human-Robot Interaction Co-Manipulation Experiment GUI
A 2D top-down interface for HRI experiments with randomization support
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional
import json
from datetime import datetime
import threading
import socket


# ============================================================================
# CONFIGURATION AND DATA STRUCTURES
# ============================================================================

class ExperimentState(Enum):
    """State machine for experiment flow"""
    IDLE = "idle"
    READY = "ready"
    RUNNING = "running"
    WAITING_NEXT = "waiting_next"
    FINISHED = "finished"


class Mode(Enum):
    """Experiment modes"""
    FREE = "Free"
    OBSTACLE = "Obstacle"
    CHANGE = "Change"
    CHANGE_OBSTACLE = "Change + Obstacle"


@dataclass
class Scenario:
    """Represents a single experimental scenario"""
    scenario_id: int
    modus: Mode
    initial_target: int
    final_target: int
    
    def is_change_scenario(self) -> bool:
        """Check if this is a change scenario"""
        return self.initial_target != self.final_target
    
    def has_obstacle(self) -> bool:
        """Check if this scenario includes an obstacle"""
        return self.modus in [Mode.OBSTACLE, Mode.CHANGE_OBSTACLE]


# Workspace dimensions (in meters)
WORKSPACE_WIDTH = 0.8
WORKSPACE_HEIGHT = 1.5

# Target positions (x, y, z) in meters
TARGET_POSITIONS = {
    1: (0.3, 1.0, 0.0),
    2: (0.0, 1.4, 0.0),
    3: (-0.3, 1.2, 0.0)
}

# Obstacle properties
OBSTACLE_SIZE = (0.16, 0.10, 0.23)  # width, height, depth
OBSTACLE_CENTER = (0.0, 0.5, 0.0)

# Start position
START_POSITION = (0.0, 0.0, 0.0)

# All 18 scenarios per pair (fixed mapping)
SCENARIOS = [
    # Free mode (scenarios 1-3)
    Scenario(1, Mode.FREE, 1, 1),
    Scenario(2, Mode.FREE, 2, 2),
    Scenario(3, Mode.FREE, 3, 3),
    
    # Obstacle mode (scenarios 4-6)
    Scenario(4, Mode.OBSTACLE, 1, 1),
    Scenario(5, Mode.OBSTACLE, 2, 2),
    Scenario(6, Mode.OBSTACLE, 3, 3),
    
    # Change mode (scenarios 7-12)
    Scenario(7, Mode.CHANGE, 1, 2),
    Scenario(8, Mode.CHANGE, 1, 3),
    Scenario(9, Mode.CHANGE, 2, 1),
    Scenario(10, Mode.CHANGE, 2, 3),
    Scenario(11, Mode.CHANGE, 3, 1),
    Scenario(12, Mode.CHANGE, 3, 2),

    # Change + Obstacle mode (scenarios 13-18)
    Scenario(13, Mode.CHANGE_OBSTACLE, 1, 2),
    Scenario(14, Mode.CHANGE_OBSTACLE, 1, 3),
    Scenario(15, Mode.CHANGE_OBSTACLE, 2, 1),
    Scenario(16, Mode.CHANGE_OBSTACLE, 2, 3),
    Scenario(17, Mode.CHANGE_OBSTACLE, 3, 1),
    Scenario(18, Mode.CHANGE_OBSTACLE, 3, 2),
]


# ============================================================================
# EXPERIMENT MANAGER
# ============================================================================

class ExperimentManager:
    """Manages experiment logic, state, and scenario sequencing"""
    
    def __init__(self):
        self.current_pair_id = 1
        self.random_mode_enabled = True  # Random mode toggle
        self.random_scenario_enabled = True  # Random scenario within mode
        self.state = ExperimentState.IDLE
        self.y_threshold = 0.5  # Default Y-threshold in meters
        
        self.scenario_queue: List[Scenario] = []
        self.current_scenario: Optional[Scenario] = None
        self.current_scenario_index = 0
        self.completed_scenarios = 0
        self.current_mode: Optional[Mode] = None
        self.completed_modes: List[Mode] = []  # Track completed modes
        
        self.trial_start_time: Optional[float] = None
        self.change_triggered = False
        
    def initialize_mode(self):
        """Initialize and randomize mode selection"""
        if self.random_mode_enabled:
            # Get modes that haven't been completed yet
            available_modes = [m for m in Mode if m not in self.completed_modes]
            if available_modes:
                self.current_mode = random.choice(available_modes)
            else:
                # All modes completed
                self.current_mode = None
        # In manual mode, current_mode is set by user selection
        
    def initialize_scenarios(self):
        """Initialize scenario queue based on current mode and random settings"""
        if not self.current_mode:
            return
            
        # Get all scenarios for the current mode
        mode_scenarios = [s for s in SCENARIOS if s.modus == self.current_mode]
        
        if self.random_scenario_enabled:
            # Randomize scenarios within the mode
            self.scenario_queue = mode_scenarios.copy()
            random.shuffle(self.scenario_queue)
        else:
            # Manual scenario selection: queue contains all scenarios in order
            self.scenario_queue = mode_scenarios.copy()
        
        self.current_scenario_index = 0
        
    def randomize_mode(self):
        """Randomize and select a new mode from remaining modes"""
        if self.random_mode_enabled:
            # Get modes that haven't been completed yet
            available_modes = [m for m in Mode if m not in self.completed_modes]
            if available_modes:
                self.current_mode = random.choice(available_modes)
                return True
            else:
                # All modes completed
                self.current_mode = None
                return False
        return False
        
    def start_experiment(self):
        """Initialize experiment (only called once at beginning)"""
        # Ensure mode is selected
        if not self.current_mode:
            if self.random_mode_enabled:
                self.initialize_mode()
            else:
                return False  # Manual mode requires mode selection
        
        # Initialize scenarios if not already done
        if not self.scenario_queue:
            self.initialize_scenarios()
        
        # Only set current_scenario if we don't have one yet
        if self.scenario_queue and not self.current_scenario:
            self.current_scenario = self.scenario_queue[self.current_scenario_index]
        
        if self.current_scenario:
            self.state = ExperimentState.READY
            return True
        else:
            return False
    
    def begin_trial(self):
        """Begin the current trial. If no mode is selected, select one automatically."""
        if self.state in [ExperimentState.IDLE, ExperimentState.READY]:
            # Ensure we have a mode and scenario
            if not self.current_mode:
                self.initialize_mode()
                print(f"[ExperimentManager] Auto-selected mode: {self.current_mode}")
            
            if not self.scenario_queue:
                self.initialize_scenarios()
                print(f"[ExperimentManager] Initialized scenario queue (size: {len(self.scenario_queue)})")

            if not self.current_scenario and self.scenario_queue:
                self.current_scenario = self.scenario_queue[0]
                self.current_scenario_index = 0

            if not self.current_scenario:
                print("[ExperimentManager] ERROR: Failed to select scenario")
                return False
            
            self.state = ExperimentState.RUNNING
            self.trial_start_time = datetime.now().timestamp()
            self.change_triggered = False
            print(f"[ExperimentManager] Trial STARTED: Scenario {self.current_scenario.scenario_id}")
            return True
        return False
    
    def update_trial(self, current_y: float = None, force_trigger: bool = False) -> bool:
        """Update trial state, returns True if change should trigger.
        
        Args:
            current_y: Current Y coordinate (experiment Y = forward). 
                       If provided, checks against y_threshold.
            force_trigger: If True, forces the change trigger regardless of Y.
        """
        if self.state != ExperimentState.RUNNING:
            return False
        
        if self.current_scenario and self.current_scenario.is_change_scenario():
            if not self.change_triggered:
                should_trigger = force_trigger
                if current_y is not None and current_y > self.y_threshold:
                    should_trigger = True
                if should_trigger:
                    self.change_triggered = True
                    return True
        return False
    
    def next_scenario(self):
        """Move to next scenario"""
        self.current_scenario_index += 1
        self.completed_scenarios += 1
        
        if self.current_scenario_index < len(self.scenario_queue):
            self.current_scenario = self.scenario_queue[self.current_scenario_index]
            self.state = ExperimentState.READY
        else:
            # Finished all scenarios in current mode
            # Mark current mode as completed
            if self.current_mode and self.current_mode not in self.completed_modes:
                self.completed_modes.append(self.current_mode)
            
            if self.random_mode_enabled:
                # In random mode, select new mode from remaining modes
                if self.randomize_mode():
                    self.initialize_scenarios()
                    if self.scenario_queue:
                        self.current_scenario = self.scenario_queue[0]
                        self.current_scenario_index = 0
                        self.state = ExperimentState.READY
                    else:
                        self.state = ExperimentState.FINISHED
                else:
                    # No more modes available - all completed
                    self.state = ExperimentState.FINISHED
            else:
                # In manual mode, stay in waiting state
                self.state = ExperimentState.WAITING_NEXT
        
        self.trial_start_time = None
        self.change_triggered = False
    
    def set_manual_mode(self, mode: Mode):
        """Set mode manually (only in manual mode)"""
        if not self.random_mode_enabled:
            self.current_mode = mode
            self.initialize_scenarios()
    
    def set_manual_scenario(self, scenario: Scenario):
        """Set scenario manually (only in manual mode)"""
        if not self.random_mode_enabled:
            self.current_scenario = scenario
            self.current_mode = scenario.modus
            self.state = ExperimentState.IDLE
    
    def reset(self):
        """Reset experiment"""
        self.state = ExperimentState.IDLE
        self.scenario_queue = []
        self.current_scenario = None
        self.current_mode = None
        self.current_scenario_index = 0
        self.completed_scenarios = 0
        self.completed_modes = []  # Reset completed modes
        self.trial_start_time = None
        self.change_triggered = False


# ============================================================================
# GUI VISUALIZATION
# ============================================================================

class WorkspaceCanvas(tk.Canvas):
    """2D top-down visualization of the experimental workspace"""
    
    def __init__(self, parent, experiment_manager: ExperimentManager, **kwargs):
        super().__init__(parent, **kwargs)
        self.experiment_manager = experiment_manager
        
        # Default Canvas dimensions (will be updated by resize event)
        self.canvas_width = 1000 
        self.canvas_height = 600
        self.margin_left = 80
        self.margin_right = 20
        self.margin_top = 20
        self.margin_bottom = 20
        
        # Set initial background
        self.config(bg="#1a1a1a")
        
        # Effective drawing area and scaling (initial calculation)
        self.recalculate_scaling()
        
        # Visual elements
        self.start_zone_id = None
        self.target_ids = {1: None, 2: None, 3: None}
        self.obstacle_id = None
        
        # Bind resize event
        self.bind("<Configure>", self.on_resize)
        
        self.draw_workspace()

    def recalculate_scaling(self):
        """Recalculate content dimensions and scaling factors"""
        self.draw_width = self.canvas_width - self.margin_left - self.margin_right
        self.draw_height = self.canvas_height - self.margin_top - self.margin_bottom
        
        # Prevent division by zero if window is very small
        if self.draw_width <= 0: self.draw_width = 1
        if self.draw_height <= 0: self.draw_height = 1

        # Scaling factors (pixels per meter)
        # ROTATED: x-axis is now the long axis (1.5m), y-axis is short (0.8m)
        self.scale_x = self.draw_width / WORKSPACE_HEIGHT   # 1.5m mapped to width
        self.scale_y = self.draw_height / WORKSPACE_WIDTH   # 0.8m mapped to height

    def on_resize(self, event):
        """Handle canvas resize event"""
        self.canvas_width = event.width
        self.canvas_height = event.height
        self.recalculate_scaling()
        self.draw_workspace()
        
    def world_to_canvas(self, x: float, y: float) -> Tuple[int, int]:
        """Convert world coordinates (meters) to canvas coordinates (pixels)
        ROTATED LAYOUT:
        - World Y (0 to 1.5m) maps to Canvas X (left to right)
        - World X (-0.4 to 0.4m) maps to Canvas Y (top to bottom, centered)
        """
        # Y-axis (forward) becomes horizontal (left to right)
        canvas_x = self.margin_left + y * self.scale_x
        
        # X-axis (left-right) becomes vertical (centered, inverted)
        canvas_y = self.canvas_height / 2 - x * self.scale_y
        
        return int(canvas_x), int(canvas_y)
    
    def draw_workspace(self):
        """Draw the complete workspace"""
        self.delete("all")
        
        # Draw workspace boundary
        self.create_rectangle(
            2, 2, self.canvas_width - 2, self.canvas_height - 2,
            outline="#444444", width=2
        )
        
        # Draw coordinate axes (subtle) - horizontal centerline
        center_y = self.canvas_height / 2
        self.create_line(0, center_y, self.canvas_width, center_y, 
                        fill="#333333", dash=(2, 4))
        
        # Draw start zone
        self.draw_start_zone()
        
        # Draw targets
        self.draw_targets()
        
        # Draw obstacle (if applicable)
        self.draw_obstacle()
    
    def draw_start_zone(self):
        """Draw the start position zone"""
        cx, cy = self.world_to_canvas(START_POSITION[0], START_POSITION[1])
        size = 90
        
        # Determine color based on state
        if self.experiment_manager.state == ExperimentState.RUNNING:
            color = "#4CAF50"  # Green
            glow = "#6BB6FF"
        else:
            color = "#FF69B4"  # Pink
            glow = "#FFB6D9"
        
        # Glow effect
        self.create_rectangle(
            cx - size - 4, cy - size - 4,
            cx + size + 4, cy + size + 4,
            fill=glow, outline="", tags="start"
        )
        
        # Main rectangle
        self.start_zone_id = self.create_rectangle(
            cx - size, cy - size,
            cx + size, cy + size,
            fill=color, outline="#FFFFFF", width=2, tags="start"
        )
        
        # Label
        self.create_text(cx, cy, text="START", fill="white", 
                        font=("Arial", 25, "bold"), tags="start")
    
    def draw_targets(self):
        """Draw all target zones"""
        for target_id, position in TARGET_POSITIONS.items():
            self.draw_target(target_id, position)
    
    def draw_target(self, target_id: int, position: Tuple[float, float, float]):
        """Draw a single target zone"""
        cx, cy = self.world_to_canvas(position[0], position[1])
        size = 90
        
        # Determine if this target is active
        is_active = self.is_target_active(target_id)
        
        if is_active:
            # Active target: bright yellow with glow
            color = "#FFD700"
            glow_color = "#FFED4E"
            outline_color = "#FFA500"
            
            # Animated glow effect
            for i in range(3):
                self.create_rectangle(
                    cx - size - (i * 4), cy - size - (i * 4),
                    cx + size + (i * 4), cy + size + (i * 4),
                    fill="", outline=glow_color, width=2,
                    tags=f"target_{target_id}"
                )
        else:
            # Inactive target: dim yellow
            color = "#665500"
            outline_color = "#888800"
        
        # Main target rectangle
        self.target_ids[target_id] = self.create_rectangle(
            cx - size, cy - size,
            cx + size, cy + size,
            fill=color, outline=outline_color, width=2,
            tags=f"target_{target_id}"
        )
        
        # Label
        text_color = "white" if is_active else "#999999"
        self.create_text(cx, cy, text=f"T{target_id}", 
                        fill=text_color, font=("Arial", 80, "bold"),
                        tags=f"target_{target_id}")
    
    def draw_obstacle(self):
        """Draw the obstacle if applicable"""
        scenario = self.experiment_manager.current_scenario
        
        # Only draw if scenario has obstacle
        if scenario and scenario.has_obstacle():
            cx, cy = self.world_to_canvas(OBSTACLE_CENTER[0], OBSTACLE_CENTER[1])
            
            # Convert obstacle size to pixels
            width = OBSTACLE_SIZE[0] * self.scale_x
            height = OBSTACLE_SIZE[1] * self.scale_y
            
            # Draw obstacle
            self.obstacle_id = self.create_rectangle(
                cx - width / 2, cy - height / 2,
                cx + width / 2, cy + height / 2,
                fill="#8B0000", outline="#FF4444", width=2,
                tags="obstacle"
            )
            
            # Diagonal stripes for visibility
            self.create_line(
                cx - width / 2, cy - height / 2,
                cx + width / 2, cy + height / 2,
                fill="#FF6666", width=2, tags="obstacle"
            )
            self.create_line(
                cx - width / 2, cy + height / 2,
                cx + width / 2, cy - height / 2,
                fill="#FF6666", width=2, tags="obstacle"
            )
    
    def is_target_active(self, target_id: int) -> bool:
        """Determine if a target should be highlighted as active"""
        scenario = self.experiment_manager.current_scenario
        if not scenario:
            return False
        
        state = self.experiment_manager.state
        
        # Show target in READY and RUNNING states
        if state in [ExperimentState.IDLE, ExperimentState.WAITING_NEXT, ExperimentState.FINISHED]:
            return False
        
        # For change scenarios
        if scenario.is_change_scenario():
            # Only show final target if we're RUNNING and change has been triggered
            if state == ExperimentState.RUNNING and self.experiment_manager.change_triggered:
                return target_id == scenario.final_target
            else:
                # Show initial target in READY state or before change
                return target_id == scenario.initial_target
        else:
            # Non-change scenarios: always show the target
            return target_id == scenario.initial_target
    
    def update_display(self):
        """Refresh the entire display"""
        self.draw_workspace()


# ============================================================================
# CONTROL PANEL
# ============================================================================

class ControlPanel(ttk.Frame):
    """Experimenter control interface"""
    
    def __init__(self, parent, experiment_manager: ExperimentManager, 
                 canvas: WorkspaceCanvas):
        super().__init__(parent, padding=10)
        self.experiment_manager = experiment_manager
        self.canvas = canvas
        
        self.setup_ui()
        self.update_ui_state()
    
    def setup_ui(self):
        """Create all control panel widgets"""
        # Title
        title = ttk.Label(self, text="Experiment Control Panel", 
                         font=("Arial", 14, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Pair ID
        ttk.Label(self, text="Pair ID:").grid(row=1, column=0, sticky="w", pady=5)
        self.pair_spinbox = ttk.Spinbox(self, from_=1, to=100, width=10)
        self.pair_spinbox.set(1)
        self.pair_spinbox.grid(row=1, column=1, sticky="ew", pady=5)
        
        # Random mode toggle
        ttk.Label(self, text="Random Mode:").grid(row=2, column=0, sticky="w", pady=5)
        self.random_mode_var = tk.BooleanVar(value=True)
        self.random_mode_check = ttk.Checkbutton(
            self, variable=self.random_mode_var, 
            command=self.on_random_mode_toggle
        )
        self.random_mode_check.grid(row=2, column=1, sticky="w", pady=5)
        
        # Random scenario toggle (only for random mode)
        ttk.Label(self, text="Random Scenarios:").grid(row=3, column=0, sticky="w", pady=5)
        self.random_scenario_var = tk.BooleanVar(value=True)
        self.random_scenario_check = ttk.Checkbutton(
            self, variable=self.random_scenario_var,
            command=self.on_random_scenario_toggle
        )
        self.random_scenario_check.grid(row=3, column=1, sticky="w", pady=5)
        
        # Separator
        ttk.Separator(self, orient="horizontal").grid(
            row=4, column=0, columnspan=2, sticky="ew", pady=10
        )
        
        # Current scenario info
        ttk.Label(self, text="Current Mode:").grid(row=5, column=0, sticky="w", pady=5)
        self.mode_label = ttk.Label(self, text="—", font=("Arial", 10, "bold"))
        self.mode_label.grid(row=5, column=1, sticky="w", pady=5)
        
        ttk.Label(self, text="Scenario ID:").grid(row=6, column=0, sticky="w", pady=5)
        self.scenario_label = ttk.Label(self, text="—", font=("Arial", 10, "bold"))
        self.scenario_label.grid(row=6, column=1, sticky="w", pady=5)
        
        ttk.Label(self, text="Progress (in mode):").grid(row=7, column=0, sticky="w", pady=5)
        self.progress_label = ttk.Label(self, text="0 / 0")
        self.progress_label.grid(row=7, column=1, sticky="w", pady=5)
        
        ttk.Label(self, text="Completed Modes:").grid(row=8, column=0, sticky="nw", pady=5)
        self.completed_modes_label = ttk.Label(self, text="None", font=("Arial", 9), justify="left")
        self.completed_modes_label.grid(row=8, column=1, sticky="nw", pady=5)
        
        # Separator
        ttk.Separator(self, orient="horizontal").grid(
            row=9, column=0, columnspan=2, sticky="ew", pady=10
        )
        
        # Manual selection (disabled when random)
        ttk.Label(self, text="Manual Mode Selection:").grid(
            row=10, column=0, sticky="w", pady=5
        )
        self.mode_combo = ttk.Combobox(
            self, values=[m.value for m in Mode], state="disabled", width=18
        )
        self.mode_combo.grid(row=11, column=0, columnspan=2, sticky="ew", pady=5)
        self.mode_combo.bind("<<ComboboxSelected>>", self.on_mode_selected)
        
        ttk.Label(self, text="Manual Scenario Selection:").grid(
            row=12, column=0, sticky="w", pady=5
        )
        self.scenario_combo = ttk.Combobox(self, state="disabled", width=18)
        self.scenario_combo.grid(row=13, column=0, columnspan=2, sticky="ew", pady=5)
        self.scenario_combo.bind("<<ComboboxSelected>>", self.on_scenario_selected)
        
        # Separator
        ttk.Separator(self, orient="horizontal").grid(
            row=14, column=0, columnspan=2, sticky="ew", pady=10
        )
        
        # Y-threshold parameter (replaces old t_change)
        ttk.Label(self, text="Y-Threshold (meters):").grid(
            row=15, column=0, sticky="w", pady=5
        )
        self.y_threshold_spinbox = ttk.Spinbox(
            self, from_=0.1, to=2.0, increment=0.1, width=10
        )
        self.y_threshold_spinbox.set(0.5)
        self.y_threshold_spinbox.grid(row=15, column=1, sticky="ew", pady=5)
        
        # Separator
        ttk.Separator(self, orient="horizontal").grid(
            row=16, column=0, columnspan=2, sticky="ew", pady=10
        )
        
        # Control buttons
        self.randomize_button = ttk.Button(
            self, text="Randomize Mode", command=self.on_randomize_mode
        )
        self.randomize_button.grid(row=17, column=0, columnspan=2, sticky="ew", pady=5)
        
        self.start_button = ttk.Button(
            self, text="Start", command=self.on_start
        )
        self.start_button.grid(row=18, column=0, columnspan=2, sticky="ew", pady=5)
        
        self.next_button = ttk.Button(
            self, text="Next Scenario", command=self.on_next, state="disabled"
        )
        self.next_button.grid(row=19, column=0, columnspan=2, sticky="ew", pady=5)
        
        self.reset_button = ttk.Button(
            self, text="Reset Experiment", command=self.on_reset
        )
        self.reset_button.grid(row=20, column=0, columnspan=2, sticky="ew", pady=5)
        
        # State indicator
        self.state_label = ttk.Label(
            self, text="State: IDLE", 
            font=("Arial", 10, "italic"),
            foreground="blue"
        )
        self.state_label.grid(row=21, column=0, columnspan=2, pady=(10, 0))
    
    def on_random_mode_toggle(self):
        """Handle random mode toggle"""
        is_random = self.random_mode_var.get()
        self.experiment_manager.random_mode_enabled = is_random
        
        # Enable/disable manual controls and randomize button
        if is_random:
            self.mode_combo.config(state="disabled")
            self.scenario_combo.config(state="disabled")
            self.randomize_button.config(state="normal")
            self.random_scenario_check.config(state="normal")
        else:
            self.mode_combo.config(state="readonly")
            self.scenario_combo.config(state="readonly")
            self.randomize_button.config(state="disabled")
            self.random_scenario_check.config(state="disabled")
        
        # Reset experiment
        self.experiment_manager.reset()
        self.update_ui_state()
    
    def on_random_scenario_toggle(self):
        """Handle random scenario toggle"""
        is_random = self.random_scenario_var.get()
        self.experiment_manager.random_scenario_enabled = is_random
    
    def on_randomize_mode(self):
        """Handle randomize mode button"""
        if self.experiment_manager.randomize_mode():
            self.experiment_manager.initialize_scenarios()
            if self.experiment_manager.scenario_queue:
                self.experiment_manager.current_scenario = self.experiment_manager.scenario_queue[0]
                self.experiment_manager.current_scenario_index = 0
                self.experiment_manager.state = ExperimentState.READY
            self.update_ui_state()
            self.canvas.update_display()
    
    def on_mode_selected(self, event):
        """Handle manual mode selection"""
        if self.experiment_manager.random_mode_enabled:
            return
        
        mode_str = self.mode_combo.get()
        mode = Mode(mode_str)
        
        # Set mode and initialize scenarios
        self.experiment_manager.set_manual_mode(mode)
        
        # Update scenario dropdown
        scenario_ids = [str(s.scenario_id) for s in self.experiment_manager.scenario_queue]
        self.scenario_combo.config(values=scenario_ids)
        if scenario_ids:
            self.scenario_combo.current(0)
            # Set first scenario and go to READY state
            self.experiment_manager.current_scenario = self.experiment_manager.scenario_queue[0]
            self.experiment_manager.current_scenario_index = 0
            self.experiment_manager.state = ExperimentState.READY
        
        self.update_ui_state()
        self.canvas.update_display()
    
    def on_scenario_selected(self, event):
        """Handle manual scenario selection"""
        if self.experiment_manager.random_mode_enabled:
            return
        
        scenario_id_str = self.scenario_combo.get()
        if scenario_id_str:
            scenario_id = int(scenario_id_str)
            scenario = next(s for s in SCENARIOS if s.scenario_id == scenario_id)
            self.experiment_manager.current_scenario = scenario
            self.experiment_manager.current_mode = scenario.modus
            # Find index in queue
            for i, s in enumerate(self.experiment_manager.scenario_queue):
                if s.scenario_id == scenario_id:
                    self.experiment_manager.current_scenario_index = i
                    break
            self.experiment_manager.state = ExperimentState.READY
            self.update_ui_state()
            self.canvas.update_display()
    
    def on_start(self):
        """Handle start button"""
        # Update pair ID
        self.experiment_manager.current_pair_id = int(self.pair_spinbox.get())
        
        # Update y_threshold
        self.experiment_manager.y_threshold = float(self.y_threshold_spinbox.get())
        
        # Begin trial (not start_experiment, which would reset scenario)
        if self.experiment_manager.begin_trial():
            self.update_ui_state()
            self.canvas.update_display()
        else:
            messagebox.showerror("Error", "Please select a mode/scenario first")
    
    def on_next(self):
        """Handle next scenario button"""
        self.experiment_manager.next_scenario()
        self.update_ui_state()
        self.canvas.update_display()
        
        if self.experiment_manager.state == ExperimentState.FINISHED:
            messagebox.showinfo("Experiment Complete", 
                              f"All 18 scenarios completed for Pair {self.experiment_manager.current_pair_id}!")
    
    def on_reset(self):
        """Handle reset button"""
        self.experiment_manager.reset()
        self.update_ui_state()
        self.canvas.update_display()
    
    def update_ui_state(self):
        """Update UI elements based on current state"""
        state = self.experiment_manager.state
        scenario = self.experiment_manager.current_scenario
        
        # Update state label
        self.state_label.config(text=f"State: {state.value.upper()}")
        
        # Update scenario info
        if scenario:
            self.mode_label.config(text=scenario.modus.value)
            self.scenario_label.config(text=str(scenario.scenario_id))
        elif self.experiment_manager.current_mode:
            self.mode_label.config(text=self.experiment_manager.current_mode.value)
            self.scenario_label.config(text="—")
        else:
            self.mode_label.config(text="—")
            self.scenario_label.config(text="—")
        
        # Update progress (within current mode)
        total_in_mode = len(self.experiment_manager.scenario_queue)
        current_in_mode = self.experiment_manager.current_scenario_index
        self.progress_label.config(
            text=f"{current_in_mode} / {total_in_mode}"
        )
        
        # Update completed modes (display vertically)
        if self.experiment_manager.completed_modes:
            completed_str = "\n".join([f"✓ {m.value}" for m in self.experiment_manager.completed_modes])
            self.completed_modes_label.config(text=completed_str)
        else:
            self.completed_modes_label.config(text="None")
        
        # Update button states
        if state == ExperimentState.IDLE:
            self.start_button.config(state="normal" if self.experiment_manager.current_mode else "disabled")
            self.next_button.config(state="disabled")
        elif state == ExperimentState.READY:
            self.start_button.config(state="normal")
            self.next_button.config(state="disabled")
        elif state == ExperimentState.RUNNING:
            self.start_button.config(state="disabled")
            self.next_button.config(state="normal")
        elif state == ExperimentState.WAITING_NEXT:
            self.start_button.config(state="disabled")
            self.next_button.config(state="normal")
        elif state == ExperimentState.FINISHED:
            self.start_button.config(state="disabled")
            self.next_button.config(state="disabled")
        
        # Update y_threshold availability
        if scenario and scenario.is_change_scenario():
            self.y_threshold_spinbox.config(state="normal")
        else:
            self.y_threshold_spinbox.config(state="disabled")


# ============================================================================
# MAIN APPLICATION
# ============================================================================

class HRIExperimentGUI(tk.Tk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Configure Main Window (Control Panel)
        self.title("HRI Experiment - Control Panel")
        self.geometry("450x750")  # Size for control panel
        self.configure(bg="#f0f0f0")
        
        # Initialize experiment manager
        self.experiment_manager = ExperimentManager()
        
        # Create the separate display window first (so canvas exists)
        self.create_display_window()
        
        # Create control panel in the main window
        self.create_control_panel()
        
        # Start update loop
        self.update_experiment()
        
        # Bind close event to ensure everything closes
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def create_display_window(self):
        """Create the secondary window for the participant display"""
        self.display_window = tk.Toplevel(self)
        self.display_window.title("HRI Experiment - Participant Display")
        self.display_window.geometry("1000x800")
        self.display_window.configure(bg="#000000")
        
        # Create canvas frame to help with layout/padding if needed
        # But putting it directly in window is fine for maximizing space
        self.canvas = WorkspaceCanvas(self.display_window, self.experiment_manager)
        self.canvas.pack(fill="both", expand=True)

        # Optional: Bind key to toggle fullscreen on display window
        self.display_window.bind("<F11>", self.toggle_fullscreen)
        self.display_window.bind("<Escape>", self.exit_fullscreen)
        
    def create_control_panel(self):
        """Create the control panel interface in the main window"""
        # Main container with padding
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        # Container for the control panel class
        # We can put it in a LabelFrame or just directly
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding=10)
        control_frame.pack(fill="both", expand=True)
        
        self.control_panel = ControlPanel(control_frame, self.experiment_manager, 
                                         self.canvas)
        self.control_panel.pack(fill="both", expand=True)
    
    def update_experiment(self):
        """Update loop for experiment state"""
        # Handle external start signal from C# WPF
        if hasattr(self, '_start_trigger') and self._start_trigger:
            print("[HRI GUI] Received START_TRIAL trigger, attempting to begin trial...")
            self._start_trigger = False
            if self.experiment_manager.begin_trial():
                print(f"[HRI GUI] Trial started: Scenario {self.experiment_manager.current_scenario}")
                # Update the control panel UI (not just internal state)
                if hasattr(self, 'control_panel'):
                    self.control_panel.update_ui_state()
                self.canvas.update_display()
            else:
                print(f"[HRI GUI] FAILED to start trial - state={self.experiment_manager.state}")

        if self.experiment_manager.state == ExperimentState.RUNNING:
            # Check for externally-triggered change (via TCP from C# app)
            if hasattr(self, '_external_trigger') and self._external_trigger:
                print("[HRI GUI] Received Y_CROSSED trigger, forcing target change...")
                self._external_trigger = False
                
                # Force target change logic
                if self.experiment_manager.current_scenario and self.experiment_manager.current_scenario.is_change_scenario():
                    self.experiment_manager.update_trial(force_trigger=True)
                    print(f"[HRI GUI] Target state ADVANCED.")
                    
                    # ALWAYS refresh UI after a trigger
                    if hasattr(self, 'control_panel'):
                        self.control_panel.update_ui_state()
                    self.canvas.update_display()
                else:
                    print("[HRI GUI] Y_CROSSED ignored: Scenario is NOT a change scenario.")
        
        # Schedule next update
        self.after(100, self.update_experiment)

    def on_close(self):
        """Handle application closure"""
        self.destroy() # This will close the main window and the Toplevel child

    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode for display window"""
        state = self.display_window.attributes("-fullscreen")
        self.display_window.attributes("-fullscreen", not state)

    def exit_fullscreen(self, event=None):
        """Exit fullscreen mode"""
        self.display_window.attributes("-fullscreen", False)


# ============================================================================
# ENTRY POINT
# ============================================================================

def main():
    """Application entry point"""
    app = HRIExperimentGUI()
    
    # Start TCP listener thread for receiving Y_CROSSED signal from C# app
    def tcp_listener():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind(('127.0.0.1', 9091))
            server.listen(1)
            server.settimeout(1.0)
            print("[TCP Listener] Listening on 127.0.0.1:9091 for Y_CROSSED signals...")
            while True:
                try:
                    conn, addr = server.accept()
                    print(f"[TCP Listener] Connection from {addr}")
                    data = conn.recv(1024).decode('utf-8').strip()
                    print(f"[TCP Listener] Received data: '{data}'")
                    if data == 'Y_CROSSED':
                        app._external_trigger = True
                        print("[TCP Listener] COMPLETED: External trigger set to True")
                    elif data == 'START_TRIAL':
                        app._start_trigger = True
                        print("[TCP Listener] COMPLETED: Start trigger set to True")
                    else:
                        print(f"[TCP Listener] UNKNOWN command: {data}")
                    conn.close()
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"[TCP Listener] Error: {e}")
                    break
        except Exception as e:
            print(f"[TCP Listener] Failed to start: {e}")
        finally:
            server.close()
    
    listener_thread = threading.Thread(target=tcp_listener, daemon=True)
    listener_thread.start()
    
    app.mainloop()


if __name__ == "__main__":
    main()
