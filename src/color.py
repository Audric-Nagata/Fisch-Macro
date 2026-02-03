import pynput
from pynput import keyboard
import time
from PIL import ImageGrab
import win32gui

# Global variable to control the loop
should_stop = False

def on_press(key):
    global should_stop
    try:
        if key == keyboard.Key.esc:
            should_stop = True
            return False  # Stop the listener
    except AttributeError:
        pass

def get_pixel_color(x, y):
    """Get the color of a pixel at the given coordinates."""
    try:
        # Take a screenshot of the entire screen
        screenshot = ImageGrab.grab()
        # Get the color of the pixel at the specified coordinates
        pixel_color = screenshot.getpixel((x, y))
        return pixel_color
    except Exception as e:
        print(f"Error getting pixel color: {e}")
        return None

def main():
    global should_stop
    should_stop = False

    print("Color Picker - Press ESC to exit")
    print("Format: (X, Y) R:G:B")

    # Start the keyboard listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    try:
        while not should_stop:
            # Get current mouse position using win32gui
            x, y = win32gui.GetCursorPos()

            # Get the color at that position
            color = get_pixel_color(x, y)

            if color:
                r, g, b = color
                # Print on the same line to update continuously
                print(f"\r({x}, {y}) R:{r} G:{g} B:{b}", end='', flush=False)

            # Small delay to prevent excessive CPU usage
            time.sleep(0.05)

        # Clear the line and print exit message
        print(f"\r({x}, {y}) RGB: ({r}, {g}, {b})")
        print("\rColor picker stopped.                         ")  # Extra spaces to clear the line

    except KeyboardInterrupt:
        print("\nColor picker interrupted.")
    finally:
        # Ensure the keyboard listener is stopped
        listener.stop()

if __name__ == "__main__":
    main()