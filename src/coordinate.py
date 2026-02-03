"""
Mouse Coordinate Tracker
Displays the current mouse cursor position in real-time.
Press Ctrl+C to exit.
"""

import pyautogui
import time
import sys

def track_mouse():
    """Track and print mouse coordinates in real-time"""
    print("=" * 50)
    print("🖱️  Mouse Coordinate Tracker")
    print("=" * 50)
    print("Move your mouse to see coordinates")
    print("Press Ctrl+C to exit")
    print("-" * 50)
    
    try:
        last_x, last_y = -1, -1
        
        while True:
            # Get current mouse position
            x, y = pyautogui.position()
            
            # Only print if position changed (reduce spam)
            if x != last_x or y != last_y:
                # Clear line and print new coordinates
                print(f"\rX: {x:4d}  Y: {y:4d}  (Position: ({x}, {y}))", end='', flush=True)
                last_x, last_y = x, y
            
            # Small delay to prevent excessive CPU usage
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        print("\n" + "=" * 50)
        print("✓ Coordinate tracker stopped")
        print("=" * 50)

if __name__ == "__main__":
    track_mouse()
