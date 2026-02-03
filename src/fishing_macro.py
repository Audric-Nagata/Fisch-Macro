import threading
import time
import sys
import random
from pynput import keyboard
from pynput.keyboard import Key, Listener
import pygetwindow as gw
import pyautogui
import mss
import cv2
import numpy as np
import json
import os
import win32api
import win32con
import tkinter as tk

class RobloxFishingMacro:
    def __init__(self):
        self.is_running = False
        self.area_toggle = False
        self.macro_thread = None
        self.listener = None
        
        # PD Controller parameters
        self.Kp = 0.01  # Proportional gain
        self.Kd = 0.005  # Derivative gain
        self.previous_error = 0
        self.last_time = time.time()
        self.mouse_held = False
        
        # Visual indicator windows
        self.arrow_window = None
        self.left_bar_window = None
        self.right_bar_window = None
        self.middle_bar_window = None
        
        # Recast timer
        self.last_arrow_found_time = time.time()
        self.recast_timeout = 2.5  # Seconds before recasting
        
        # Load saved area coordinates if available
        self.load_area_coordinates()
        
        # Initialize PyAutoGUI settings
        pyautogui.FAILSAFE = True  # Move mouse to top-left corner to abort
        pyautogui.PAUSE = 0.1  # Pause between actions

    def load_area_coordinates(self):
        """Load area coordinates from config file"""
        # Try multiple possible paths for the config file
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "config", "rod_location.json"),
            os.path.join(os.path.dirname(__file__), "rod_location.json"),
            os.path.join("config", "rod_location.json"),
            "rod_location.json"
        ]
        
        for config_path in possible_paths:
            try:
                if os.path.exists(config_path):
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                        self.area_coords = config.get('rod_location', None)
                        if self.area_coords:
                            print(f"✓ Loaded rod location from: {config_path}")
                            print(f"  Area: {self.area_coords}")
                            return
            except (FileNotFoundError, json.JSONDecodeError) as e:
                continue
        
        # If no config found
        self.area_coords = None
        print("⚠ No rod location config found. Please select an area using F2.")

    def start_listening(self):
        """Start the keyboard listener"""
        self.listener = Listener(on_press=self.on_key_press)
        self.listener.start()

    def on_key_press(self, key):
        try:
            if key.char == 'f1':
                self.toggle_macro()
            elif key.char == 'f2':
                self.toggle_area()
            elif key.char == 'f3':
                self.exit_app()
        except AttributeError:
            # Special keys (ctrl, alt, etc.) don't have char attribute
            if key == Key.f1:
                self.toggle_macro()
            elif key == Key.f2:
                self.toggle_area()
            elif key == Key.f3:
                self.exit_app()

    def toggle_macro(self):
        self.is_running = not self.is_running
        if self.is_running:
            print("=" * 50)
            print("🎣 Starting color detection macro...")
            print("=" * 50)
            # Start the macro in a separate thread
            self.macro_thread = threading.Thread(target=self.run_macro)
            self.macro_thread.daemon = True
            self.macro_thread.start()
        else:
            print("=" * 50)
            print("⏹ Stopping macro...")
            print("=" * 50)

    def toggle_area(self):
        self.area_toggle = not self.area_toggle
        area_name = "Alternative" if self.area_toggle else "Normal"
        print(f"🔄 Toggled to {area_name} area")

    def run_macro(self):
        """Main macro loop - this is where the color search happens"""
        if not self.area_coords:
            print("❌ ERROR: No area coordinates loaded!")
            print("   Please select an area using F2 before starting the macro.")
            self.is_running = False
            return
        
        # Click at specific position before initial cast
        print("=" * 50)
        print("🖱️  Initial Setup Click")
        print("=" * 50)
        
        # Get screen center for later
        screen_width, screen_height = pyautogui.size()
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        # Move to position first
        pyautogui.moveTo(2527, 55, duration=0.2)
        print("✓ Moved to (2527, 55)")
        
        # Super low delay before click
        time.sleep(0.05)
        
        # Click using win32api
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        print("✓ Clicked")
        
        # Move back to center
        pyautogui.moveTo(center_x, center_y, duration=0.3)
        print(f"✓ Moved back to center ({center_x}, {center_y})")
        
        time.sleep(0.5)
        print("-" * 50)
        
        # Perform initial recast when macro starts
        print("=" * 50)
        print("🎣 Initial Cast")
        print("=" * 50)
        self.recast()
        print("-" * 50)
        
        loop_count = 0
        
        while self.is_running:
            try:
                loop_count += 1
                
                # Capture the defined area for processing
                x1, y1, x2, y2 = self.area_coords
                
                # Calculate the region for mss
                monitor = {
                    "top": min(y1, y2),
                    "left": min(x1, x2),
                    "width": abs(x2 - x1),
                    "height": abs(y2 - y1)
                }

                # Capture the area using mss
                with mss.mss() as sct:
                    screenshot = sct.grab(monitor)
                    
                    # Convert the screenshot to a numpy array for OpenCV
                    img = np.array(screenshot)
                    
                    # Convert from BGRA (MSS format) to BGR (OpenCV format)
                    img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                    
                    # Define the color range (BGR format: Blue, Green, Red)
                    # RGB(232, 193, 209) → BGR(209, 193, 232)
                    tolerance = 5
                    lower_bound = np.array([209-tolerance, 193-tolerance, 232-tolerance])
                    upper_bound = np.array([209+tolerance, 193+tolerance, 232+tolerance])
                    
                    # Create a mask for pixels within the color range
                    mask = cv2.inRange(img_bgr, lower_bound, upper_bound)
                    
                    # Count the number of pixels that match the color criteria
                    matching_pixels = cv2.countNonZero(mask)
                    
                    # Find contours of the matching regions
                    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    
                    # Find the topmost contour (contour with the smallest y-coordinate)
                    found_match = False
                    topmost_y = float('inf')
                    topmost_x = 0
                    
                    for contour in contours:
                        # Get the bounding rectangle for each contour
                        x, y, w, h = cv2.boundingRect(contour)
                        
                        # Check if this is the topmost match (smallest y value)
                        if y < topmost_y:
                            topmost_y = y
                            topmost_x = x + w // 2  # Use center of the bounding box
                            found_match = True
                    
                    # Prepare result data and print single output per loop
                    if found_match:
                        # Convert local coordinates to screen coordinates
                        screen_x = monitor['left'] + topmost_x
                        screen_y = monitor['top'] + topmost_y
                        
                        # After finding arrow color, search for bar points
                        bar_result = self.search_bar_points(img_bgr, monitor)
                        
                        # Print single output per loop with topmost match and pixel count
                        if bar_result['found']:
                            left_pt = bar_result['left_point']
                            right_pt = bar_result['right_point']
                            mid_pt = bar_result['middle_point']
                            
                            # Update last found time
                            self.last_arrow_found_time = time.time()
                            
                            # Activate PD controller to control bar position
                            control_output = self.pd_controller(int(screen_x), mid_pt[0])
                            
                            # Update visual indicators
                            self.update_arrow_indicator(int(screen_x), int(screen_y))
                            self.update_bar_indicators(left_pt, mid_pt, right_pt)
                            
                            print(f"✓ [{loop_count:04d}] Arrow: ({int(screen_x):4d}, {int(screen_y):4d}) | Bar: L({left_pt[0]:4d}, {left_pt[1]:4d}) M({mid_pt[0]:4d}, {mid_pt[1]:4d}) R({right_pt[0]:4d}, {right_pt[1]:4d}) | Control: {control_output:+.3f} | Pixels: {matching_pixels:5d}")
                        else:
                            # Update last found time
                            self.last_arrow_found_time = time.time()
                            
                            # Release mouse if bar not found
                            self.release_left_click()
                            
                            # Still show arrow even if bar not found
                            self.update_arrow_indicator(int(screen_x), int(screen_y))
                            
                            print(f"✓ [{loop_count:04d}] Arrow: ({int(screen_x):4d}, {int(screen_y):4d}) | Bar: Not found | Pixels: {matching_pixels:5d}")
                        
                        result = {
                            'coordinates': [int(screen_x), int(screen_y)],
                            'found': True,
                            'pixel_count': matching_pixels,
                            'bar_left_point': bar_result['left_point'],
                            'bar_middle_point': bar_result['middle_point'],
                            'bar_right_point': bar_result['right_point'],
                            'bar_found': bar_result['found'],
                            'timestamp': time.time(),
                            'loop_count': loop_count
                        }
                    else:
                        # Release mouse if arrow not found
                        self.release_left_click()
                        
                        # Hide all indicators when arrow not found
                        self.hide_all_indicators()
                        
                        # Check if we need to recast (5 seconds without finding arrow)
                        time_since_last_found = time.time() - self.last_arrow_found_time
                        if time_since_last_found >= self.recast_timeout:
                            self.recast()
                        
                        # Only print "not found" occasionally to avoid spam
                        if loop_count % 10 == 0:
                            print(f"○ [{loop_count:04d}] No match | Pixels: {matching_pixels:5d} | Timeout: {time_since_last_found:.1f}s")
            except Exception as e:
                print(f"❌ Screenshot error: {e}")
                

    def hold_left_click(self):
        """Hold left mouse button using win32api (no delay)"""
        if not self.mouse_held:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            self.mouse_held = True

    def release_left_click(self):
        """Release left mouse button using win32api (no delay)"""
        if self.mouse_held:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            self.mouse_held = False

    def recast(self):
        """Recast the fishing rod: press 2, press 1, hold left click for 2 seconds"""
        print("🎣 RECASTING...")
        
        # Make sure mouse is released before recasting
        self.release_left_click()
        time.sleep(0.1)
        
        # Press 2 using win32api (Virtual key code for '2' is 0x32)
        win32api.keybd_event(0x32, 0, 0, 0)  # Key down
        win32api.keybd_event(0x32, 0, win32con.KEYEVENTF_KEYUP, 0)  # Key up
        time.sleep(0.15)
        
        # Press 1 using win32api (Virtual key code for '1' is 0x31)
        win32api.keybd_event(0x31, 0, 0, 0)  # Key down
        win32api.keybd_event(0x31, 0, win32con.KEYEVENTF_KEYUP, 0)  # Key up
        time.sleep(0.15)
        
        # Hold left click for 0.75 seconds
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.75)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        
        # Reset timer
        self.last_arrow_found_time = time.time()
        
        print("✓ Recast complete")

    def pd_controller(self, arrow_x, middle_x):
        """
        PD controller to control bar position
        
        Args:
            arrow_x: Target X position (arrow)
            middle_x: Current X position (middle point)
        
        Returns:
            control_output: Control signal
        """
        # Calculate error (positive = need to increase middle_x)
        error = arrow_x - middle_x
        
        # Calculate time delta
        current_time = time.time()
        dt = current_time - self.last_time
        
        # Avoid division by zero
        if dt == 0:
            dt = 0.001
        
        # Calculate derivative
        derivative = (error - self.previous_error) / dt
        
        # PD control output
        control_output = self.Kp * error + self.Kd * derivative
        
        # Update state
        self.previous_error = error
        self.last_time = current_time
        
        # Apply control
        if control_output > 0:
            # Need to increase middle_x -> hold left click
            self.hold_left_click()
        else:
            # Need to decrease middle_x -> release left click
            self.release_left_click()
        
        return control_output

    def update_arrow_indicator(self, x, y):
        """Show or update lime green arrow at bobber position"""
        try:
            arrow_height = 40
            arrow_width = 30
            window_x = x - arrow_width // 2
            window_y = y - arrow_height - 10
            
            if self.arrow_window is None:
                self.arrow_window = tk.Toplevel()
                self.arrow_window.attributes('-topmost', True)
                self.arrow_window.overrideredirect(True)
                self.arrow_window.attributes('-transparentcolor', 'white')
                self.arrow_window.configure(bg='white')
                
                canvas = tk.Canvas(self.arrow_window, width=arrow_width, height=arrow_height,
                                 bg='white', highlightthickness=0)
                canvas.pack()
                
                center_x = arrow_width // 2
                arrow_points = [
                    center_x, arrow_height,
                    center_x - 15, arrow_height - 20,
                    center_x + 15, arrow_height - 20
                ]
                canvas.create_polygon(arrow_points, fill='lime', outline='lime', width=2)
            
            self.arrow_window.geometry(f"{arrow_width}x{arrow_height}+{window_x}+{window_y}")
        except:
            pass

    def update_bar_indicators(self, left_point, middle_point, right_point):
        """Show or update vertical lines at bar positions"""
        try:
            line_width = 3
            line_height = 100
            
            # Left bar (cyan)
            if self.left_bar_window is None:
                self.left_bar_window = tk.Toplevel()
                self.left_bar_window.attributes('-topmost', True)
                self.left_bar_window.overrideredirect(True)
                self.left_bar_window.attributes('-transparentcolor', 'white')
                self.left_bar_window.configure(bg='white')
                
                canvas = tk.Canvas(self.left_bar_window, width=line_width, height=line_height,
                                 bg='white', highlightthickness=0)
                canvas.pack()
                canvas.create_line(line_width//2, 0, line_width//2, line_height,
                                 fill='cyan', width=line_width)
            
            left_x, left_y = left_point
            self.left_bar_window.geometry(f"{line_width}x{line_height}+{left_x - line_width//2}+{left_y - line_height//2}")
            
            # Middle bar (yellow)
            if self.middle_bar_window is None:
                self.middle_bar_window = tk.Toplevel()
                self.middle_bar_window.attributes('-topmost', True)
                self.middle_bar_window.overrideredirect(True)
                self.middle_bar_window.attributes('-transparentcolor', 'white')
                self.middle_bar_window.configure(bg='white')
                
                canvas = tk.Canvas(self.middle_bar_window, width=line_width, height=line_height,
                                 bg='white', highlightthickness=0)
                canvas.pack()
                canvas.create_line(line_width//2, 0, line_width//2, line_height,
                                 fill='yellow', width=line_width)
            
            middle_x, middle_y = middle_point
            self.middle_bar_window.geometry(f"{line_width}x{line_height}+{middle_x - line_width//2}+{middle_y - line_height//2}")
            
            # Right bar (magenta)
            if self.right_bar_window is None:
                self.right_bar_window = tk.Toplevel()
                self.right_bar_window.attributes('-topmost', True)
                self.right_bar_window.overrideredirect(True)
                self.right_bar_window.attributes('-transparentcolor', 'white')
                self.right_bar_window.configure(bg='white')
                
                canvas = tk.Canvas(self.right_bar_window, width=line_width, height=line_height,
                                 bg='white', highlightthickness=0)
                canvas.pack()
                canvas.create_line(line_width//2, 0, line_width//2, line_height,
                                 fill='magenta', width=line_width)
            
            right_x, right_y = right_point
            self.right_bar_window.geometry(f"{line_width}x{line_height}+{right_x - line_width//2}+{right_y - line_height//2}")
        except:
            pass

    def hide_all_indicators(self):
        """Hide all visual indicators (arrow and bar lines)"""
        try:
            if self.arrow_window is not None:
                self.arrow_window.destroy()
                self.arrow_window = None
        except:
            pass
        
        try:
            if self.left_bar_window is not None:
                self.left_bar_window.destroy()
                self.left_bar_window = None
        except:
            pass
        
        try:
            if self.middle_bar_window is not None:
                self.middle_bar_window.destroy()
                self.middle_bar_window = None
        except:
            pass
        
        try:
            if self.right_bar_window is not None:
                self.right_bar_window.destroy()
                self.right_bar_window = None
        except:
            pass

    def search_bar_points(self, img_bgr, monitor):
        """
        Search from bottom to top for five specific colors:
        - RGB(227, 244, 250) OR RGB(84, 46, 45) OR RGB(205, 205, 251) 
        - OR RGB(78, 96, 79) OR RGB(81, 71, 63)
        
        Returns:
            dict with 'left_point' and 'right_point' coordinates, or None if not found
        """
        # Define the target colors in BGR format (OpenCV uses BGR)
        # Color 1: RGB(227, 244, 250) → BGR(250, 244, 227)
        # Color 2: RGB(84, 46, 45) → BGR(45, 46, 84)
        # Color 3: RGB(205, 205, 251) → BGR(251, 205, 205)
        # Color 4: RGB(78, 96, 79) → BGR(79, 96, 78)
        # Color 5: RGB(81, 71, 63) → BGR(63, 71, 81)
        
        # Create masks for all colors with tolerance of ±5
        tolerance1 = 5
        tolerance2 = 15
        # Color 1 mask
        color1_lower = np.array([250-tolerance1, 244-tolerance1, 227-tolerance1])
        color1_upper = np.array([250+tolerance1, 244+tolerance1, 227+tolerance1])
        mask1 = cv2.inRange(img_bgr, color1_lower, color1_upper)
        
        # Color 2 mask
        color2_lower = np.array([45-tolerance2, 46-tolerance2, 84-tolerance2])
        color2_upper = np.array([45+tolerance2, 46+tolerance2, 84+tolerance2])
        mask2 = cv2.inRange(img_bgr, color2_lower, color2_upper)
        
        # Color 3 mask
        color3_lower = np.array([251-tolerance1, 205-tolerance1, 205-tolerance1])
        color3_upper = np.array([251+tolerance1, 205+tolerance1, 205+tolerance1])
        mask3 = cv2.inRange(img_bgr, color3_lower, color3_upper)
        
        # Color 4 mask - RGB(78, 96, 79)
        color4_lower = np.array([79-tolerance2, 96-tolerance2, 78-tolerance2])
        color4_upper = np.array([79+tolerance2, 96+tolerance2, 78+tolerance2])
        mask4 = cv2.inRange(img_bgr, color4_lower, color4_upper)
        
        # Color 5 mask - RGB(81, 71, 63)
        color5_lower = np.array([63-tolerance2, 71-tolerance2, 81-tolerance2])
        color5_upper = np.array([63+tolerance2, 71+tolerance2, 81+tolerance2])
        mask5 = cv2.inRange(img_bgr, color5_lower, color5_upper)
        
        # Combine all masks (OR operation)
        combined_mask = cv2.bitwise_or(mask1, mask2)
        combined_mask = cv2.bitwise_or(combined_mask, mask3)
        combined_mask = cv2.bitwise_or(combined_mask, mask4)
        combined_mask = cv2.bitwise_or(combined_mask, mask5)
        
        height, width = combined_mask.shape
        
        # Search from bottom to top
        left_point = None
        right_point = None
        
        for y in range(height - 1, -1, -1):  # Bottom to top
            row = combined_mask[y]
            
            # Find all matching pixels in this row
            matching_indices = np.where(row > 0)[0]
            
            if len(matching_indices) >= 2:
                # Search left to right for leftmost point
                leftmost_x = matching_indices[0]
                
                # Search right to left for rightmost point
                rightmost_x = matching_indices[-1]
                
                # Convert to screen coordinates
                left_screen_x = monitor['left'] + leftmost_x
                left_screen_y = monitor['top'] + y
                
                right_screen_x = monitor['left'] + rightmost_x
                right_screen_y = monitor['top'] + y
                
                left_point = (int(left_screen_x), int(left_screen_y))
                right_point = (int(right_screen_x), int(right_screen_y))
                
                # Found both points, exit the loop
                break
        
        if left_point and right_point:
            # Calculate middle point
            middle_x = (left_point[0] + right_point[0]) // 2
            middle_y = (left_point[1] + right_point[1]) // 2
            middle_point = (middle_x, middle_y)
            
            return {
                'left_point': left_point,
                'right_point': right_point,
                'middle_point': middle_point,
                'found': True
            }
        else:
            return {
                'left_point': None,
                'right_point': None,
                'middle_point': None,
                'found': False
            }

    def perform_fishing_action(self):
        """Perform standard fishing action"""
        print("🎣 Casting fishing rod...")
        
        # If area coordinates are set, move mouse to a random position within the area
        if self.area_coords:
            x1, y1, x2, y2 = self.area_coords
            # Generate random coordinates within the selected area
            random_x = random.randint(x1, x2)
            random_y = random.randint(y1, y2)
            pyautogui.moveTo(random_x, random_y)
            print(f"  → Moving to: ({random_x}, {random_y})")
        
        # Simulate pressing 'F' to cast the fishing rod (common in many Roblox games)
        pyautogui.press('f')
        
        # Wait for fish to bite (random time)
        bite_time = random.uniform(3.0, 8.0)
        time.sleep(bite_time)
        
        print("🐟 Fish biting! Reeling in...")
        
        # Simulate pressing 'F' again to reel in
        pyautogui.press('f')
        
        # Small delay after reeling
        time.sleep(0.5)

    def perform_fishing_action_alt(self):
        """Perform fishing action for alternative area"""
        print("🎣 Casting fishing rod in alternative area...")
        
        # If area coordinates are set, move mouse to a random position within the area
        if self.area_coords:
            x1, y1, x2, y2 = self.area_coords
            # Generate random coordinates within the selected area
            random_x = random.randint(x1, x2)
            random_y = random.randint(y1, y2)
            pyautogui.moveTo(random_x, random_y)
            print(f"  → Moving to: ({random_x}, {random_y})")
        
        # Different key for alternative area (could be different action)
        pyautogui.press('g')
        
        # Wait for fish to bite (different timing for variety)
        bite_time = random.uniform(2.0, 6.0)
        time.sleep(bite_time)
        
        print("🐟 Fish biting! Reeling in from alternative area...")
        
        # Different reeling key for alternative area
        pyautogui.press('g')
        
        # Small delay after reeling
        time.sleep(0.5)

    def exit_app(self):
        """Stop everything and exit the application"""
        print("👋 Exiting application...")
        
        # Stop the macro
        self.is_running = False
        
        # Stop the keyboard listener
        if self.listener:
            self.listener.stop()
        
        # Exit the program completely
        sys.exit(0)

def main():
    macro = RobloxFishingMacro()
    macro.start_listening()
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        macro.exit_app()

if __name__ == "__main__":
    main()