import time
import json
import os
from PIL import Image
from PIL import ImageGrab

def take_screenshot_of_area():
    """Take a screenshot of the defined area from rod_location.json and save it"""

    # Load coordinates from rod_location.json
    config_path = os.path.join(os.path.dirname(__file__), "config/rod_location.json")

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            area_coords = config.get('rod_location', None)

            if not area_coords:
                print("No rod location coordinates found in rod_location.json")
                return
    except FileNotFoundError:
        print("rod_location.json file not found")
        return
    except json.JSONDecodeError:
        print("rod_location.json file is invalid")
        return

    # Extract coordinates
    if len(area_coords) != 4:
        print("Invalid coordinates format in rod_location.json. Expected [x1, y1, x2, y2]")
        return

    x1, y1, x2, y2 = area_coords

    # Calculate the region dimensions
    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    # Wait 1 second before taking the screenshot
    print("Waiting 1 second before taking screenshot...")
    time.sleep(1)

    # Take screenshot of the specific region using PIL
    full_screenshot = ImageGrab.grab()
    screenshot = full_screenshot.crop((left, top, left + width, top + height))

    # Create screenshots directory if it doesn't exist
    screenshots_dir = os.path.join(os.path.dirname(__file__), "..", "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    # Generate filename with timestamp
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    filepath = os.path.join(screenshots_dir, filename)

    # Save the screenshot
    screenshot.save(filepath)
    print(f"Screenshot saved: {filepath}")

if __name__ == "__main__":
    take_screenshot_of_area()