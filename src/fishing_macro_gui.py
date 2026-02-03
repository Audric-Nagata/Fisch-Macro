import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import sys
from pynput import keyboard
from pynput.keyboard import Key, Listener
import os
import json

# Import the fishing macro module directly
from fishing_macro import RobloxFishingMacro

class RobloxFishingMacroGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Fisch Macro")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Variables to track macro state
        self.is_running = False
        self.area_toggle = False
        self.macro_instance = None
        self.output_thread = None

        # Key bindings
        self.key_bindings = {
            'start_stop': 'f1',
            'change_area': 'f2',
            'exit_app': 'f3'
        }

        # For key rebinding
        self.rebinding_key = None

        # Set up the GUI
        self.setup_gui()

    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(main_frame, text="Fisch Macro", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        self.status_var = tk.StringVar(value="Stopped")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, font=("Arial", 12))
        status_label.grid(row=0, column=0)

        # Area toggle frame
        area_frame = ttk.LabelFrame(main_frame, text="Area Settings", padding="10")
        area_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        self.area_var = tk.StringVar(value="Area: Normal")
        area_label = ttk.Label(area_frame, textvariable=self.area_var, font=("Arial", 12))
        area_label.grid(row=0, column=0)

        # Controls frame
        controls_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        controls_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        # Start/Stop binding
        start_stop_frame = ttk.Frame(controls_frame)
        start_stop_frame.grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Label(start_stop_frame, text="Start/Stop Macro:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W)
        self.start_stop_binding_btn = ttk.Button(start_stop_frame, text=f"{self.key_bindings['start_stop'].upper()}", width=15, command=lambda: self.start_rebind('start_stop'))
        self.start_stop_binding_btn.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))

        # Change Area binding
        change_area_frame = ttk.Frame(controls_frame)
        change_area_frame.grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Label(change_area_frame, text="Change Area:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W)
        self.change_area_binding_btn = ttk.Button(change_area_frame, text=f"{self.key_bindings['change_area'].upper()}", width=15, command=lambda: self.start_rebind('change_area'))
        self.change_area_binding_btn.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))

        # Exit binding
        exit_frame = ttk.Frame(controls_frame)
        exit_frame.grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Label(exit_frame, text="Exit Application:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W)
        self.exit_binding_btn = ttk.Button(exit_frame, text=f"{self.key_bindings['exit_app'].upper()}", width=15, command=lambda: self.start_rebind('exit_app'))
        self.exit_binding_btn.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))

        # Instructions
        instructions = ttk.Label(
            main_frame,
            text="Click on key bindings to rebind\nCurrent bindings shown above",
            justify=tk.CENTER
        )
        instructions.grid(row=4, column=0, columnspan=2, pady=(10, 0))

        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=5, column=0, columnspan=2, pady=(20, 0))

        # Exit button
        exit_btn = ttk.Button(buttons_frame, text="Exit App", command=self.exit_app)
        exit_btn.grid(row=0, column=0)

        # Output frame
        output_frame = ttk.LabelFrame(main_frame, text="Output Log", padding="10")
        output_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))

        # Create a text widget for displaying output
        self.output_text = tk.Text(output_frame, height=10, width=80, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=scrollbar.set)

        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)  # Give the output frame some space

    def toggle_macro_ui(self):
        """Toggle macro from the UI button"""
        if not self.is_running:
            self.start_macro()
        else:
            self.stop_macro()

    def start_rebind(self, action):
        """Start the rebind process for a specific action"""
        self.rebinding_key = action
        # Temporarily change the button text to indicate rebinding
        if action == 'start_stop':
            self.start_stop_binding_btn.config(text="Press key...")
        elif action == 'change_area':
            self.change_area_binding_btn.config(text="Press key...")
        elif action == 'exit_app':
            self.exit_binding_btn.config(text="Press key...")

        # Show a temporary message
        messagebox.showinfo("Rebind Key", f"Press the new key for '{action.replace('_', ' ').title()}'\nPress Escape to cancel")

    def update_binding_display(self):
        """Update the display of key bindings"""
        self.start_stop_binding_btn.config(text=f"{self.key_bindings['start_stop'].upper()}")
        self.change_area_binding_btn.config(text=f"{self.key_bindings['change_area'].upper()}")
        self.exit_binding_btn.config(text=f"{self.key_bindings['exit_app'].upper()}")

    def start_macro(self):
        """Start the macro instance"""
        try:
            # Create an instance of the fishing macro
            self.macro_instance = RobloxFishingMacro()

            # Override the print function to redirect to GUI
            import builtins
            original_print = builtins.print
            
            def gui_print(*args, **kwargs):
                text = " ".join(map(str, args)) + "\n"
                self.root.after(0, self.append_output, text)

            # Patch the print function globally
            builtins.print = gui_print

            # Start the macro thread
            self.macro_thread = threading.Thread(target=self.macro_instance.run_macro)
            self.macro_thread.daemon = True
            self.macro_instance.is_running = True
            self.macro_thread.start()

            self.is_running = True
            self.status_var.set("Running")
            self.append_output("=" * 50 + "\n")
            self.append_output("🎣 Macro Started\n")
            self.append_output("=" * 50 + "\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start macro: {str(e)}")

    def append_output(self, text):
        """Append text to the output text widget"""
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)  # Scroll to the end
        self.output_text.update_idletasks()  # Update the GUI

    def stop_macro(self):
        """Stop the macro instance"""
        if self.macro_instance:
            self.macro_instance.is_running = False
            self.macro_instance.release_left_click()  # Make sure mouse is released
            self.macro_instance = None

        self.is_running = False
        self.status_var.set("Stopped")
        self.append_output("=" * 50 + "\n")
        self.append_output("⏹ Macro Stopped\n")
        self.append_output("=" * 50 + "\n")

    def toggle_area(self):
        """Toggle the area selection overlay"""
        if not hasattr(self, 'area_overlay_active'):
            self.area_overlay_active = False

        if not self.area_overlay_active:
            self.show_area_selection_overlay()
        else:
            self.hide_area_selection_overlay()

    def show_area_selection_overlay(self):
        """Show a transparent overlay with a resizable rectangle for area selection"""
        # Create an overlay window that covers the entire screen
        self.area_overlay = tk.Toplevel()
        self.area_overlay.attributes('-fullscreen', True)
        self.area_overlay.attributes('-topmost', True)
        self.area_overlay.configure(bg='white', highlightthickness=0)
        self.area_overlay.overrideredirect(True)  # Remove window decorations

        # Make the window transparent using alpha channel (Windows only)
        try:
            self.area_overlay.wm_attributes("-transparentcolor", "white")
        except tk.TclError:
            pass

        # Create a canvas for drawing the semi-transparent overlay
        self.overlay_canvas = tk.Canvas(
            self.area_overlay,
            bg='white',
            highlightthickness=0,
            width=self.area_overlay.winfo_screenwidth(),
            height=self.area_overlay.winfo_screenheight()
        )
        self.overlay_canvas.pack(fill=tk.BOTH, expand=True)

        # Create a semi-transparent background
        screen_width = self.area_overlay.winfo_screenwidth()
        screen_height = self.area_overlay.winfo_screenheight()

        # Calculate initial position (centered)
        margin_x, margin_y = screen_width * 0.25, screen_height * 0.25
        x1, y1 = margin_x, margin_y
        x2, y2 = screen_width - margin_x, screen_height - margin_y

        # Draw the initial selection rectangle (red, low opacity)
        self.selection_rect = self.overlay_canvas.create_rectangle(
            x1, y1, x2, y2,
            outline='',
            width=0,
            fill='red',
            stipple='gray25'
        )

        # Draw resize handles at corners
        handle_size = 10
        self.tl_handle = self.overlay_canvas.create_rectangle(
            x1-handle_size//2, y1-handle_size//2,
            x1+handle_size//2, y1+handle_size//2,
            fill='yellow', outline='black', width=1
        )
        self.tr_handle = self.overlay_canvas.create_rectangle(
            x2-handle_size//2, y1-handle_size//2,
            x2+handle_size//2, y1+handle_size//2,
            fill='yellow', outline='black', width=1
        )
        self.bl_handle = self.overlay_canvas.create_rectangle(
            x1-handle_size//2, y2-handle_size//2,
            x1+handle_size//2, y2+handle_size//2,
            fill='yellow', outline='black', width=1
        )
        self.br_handle = self.overlay_canvas.create_rectangle(
            x2-handle_size//2, y2-handle_size//2,
            x2+handle_size//2, y2+handle_size//2,
            fill='yellow', outline='black', width=1
        )

        # Bind mouse events for resizing
        self.bind_overlay_resize_handles()

        # Bind ESC key to close the overlay
        self.area_overlay.bind('<Escape>', lambda e: self.hide_area_selection_overlay())

        # Update the area status
        self.area_overlay_active = True
        self.area_var.set("Area: Selecting...")

    def bind_overlay_resize_handles(self):
        """Bind mouse events to the resize handles for the overlay"""
        self.overlay_canvas.tag_bind(self.tl_handle, "<Button-1>", lambda e: self.start_overlay_resize(e, "tl"))
        self.overlay_canvas.tag_bind(self.tr_handle, "<Button-1>", lambda e: self.start_overlay_resize(e, "tr"))
        self.overlay_canvas.tag_bind(self.bl_handle, "<Button-1>", lambda e: self.start_overlay_resize(e, "bl"))
        self.overlay_canvas.tag_bind(self.br_handle, "<Button-1>", lambda e: self.start_overlay_resize(e, "br"))

        # Track mouse movement for resizing
        self.overlay_canvas.bind("<B1-Motion>", self.resize_overlay_rectangle)
        self.overlay_canvas.bind("<ButtonRelease-1>", self.end_overlay_resize)

    def start_overlay_resize(self, event, corner):
        """Start resizing from a corner on the overlay"""
        self.resize_corner = corner
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.orig_coords = self.overlay_canvas.coords(self.selection_rect)

    def resize_overlay_rectangle(self, event):
        """Resize the rectangle as the mouse moves on the overlay"""
        if hasattr(self, 'resize_corner'):
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y

            x1, y1, x2, y2 = self.orig_coords
            if self.resize_corner == "tl":  # Top-left
                x1 += dx
                y1 += dy
            elif self.resize_corner == "tr":  # Top-right
                x2 += dx
                y1 += dy
            elif self.resize_corner == "bl":  # Bottom-left
                x1 += dx
                y2 += dy
            elif self.resize_corner == "br":  # Bottom-right
                x2 += dx
                y2 += dy

            # Ensure rectangle stays within screen bounds
            screen_width = self.area_overlay.winfo_screenwidth()
            screen_height = self.area_overlay.winfo_screenheight()

            x1 = max(0, min(x1, screen_width))
            y1 = max(0, min(y1, screen_height))
            x2 = max(0, min(x2, screen_width))
            y2 = max(0, min(y2, screen_height))

            # Update rectangle coordinates
            self.overlay_canvas.coords(self.selection_rect, x1, y1, x2, y2)

            # Update handle positions
            handle_size = 10
            self.overlay_canvas.coords(self.tl_handle, x1-handle_size//2, y1-handle_size//2,
                                      x1+handle_size//2, y1+handle_size//2)
            self.overlay_canvas.coords(self.tr_handle, x2-handle_size//2, y1-handle_size//2,
                                      x2+handle_size//2, y1+handle_size//2)
            self.overlay_canvas.coords(self.bl_handle, x1-handle_size//2, y2-handle_size//2,
                                      x1+handle_size//2, y2+handle_size//2)
            self.overlay_canvas.coords(self.br_handle, x2-handle_size//2, y2-handle_size//2,
                                      x2+handle_size//2, y2+handle_size//2)

    def end_overlay_resize(self, event):
        """End the resize operation on the overlay"""
        if hasattr(self, 'resize_corner'):
            delattr(self, 'resize_corner')

    def hide_area_selection_overlay(self):
        """Hide the area selection overlay and save coordinates"""
        if hasattr(self, 'area_overlay_active') and self.area_overlay_active:
            # Get the final coordinates of the selection rectangle
            coords = self.overlay_canvas.coords(self.selection_rect)
            if coords:
                x1, y1, x2, y2 = coords
                saved_coords = (int(x1), int(y1), int(x2), int(y2))
                
                # Save coordinates to config file
                self.save_area_coordinates_to_config(saved_coords)

                # Update the area state
                self.area_toggle = True
                self.area_var.set("Area: Selected")

            # Destroy the overlay window
            self.area_overlay.destroy()
            self.area_overlay_active = False

    def save_area_coordinates_to_config(self, coords):
        """Save the selected area coordinates to the rod location config file"""
        # Ensure the config directory exists
        config_dir = os.path.join(os.path.dirname(__file__), "config")
        os.makedirs(config_dir, exist_ok=True)
        
        config_path = os.path.join(config_dir, "rod_location.json")

        # Create the data structure for rod location
        rod_data = {
            "rod_location": list(coords)
        }

        # Save to file
        with open(config_path, 'w') as f:
            json.dump(rod_data, f, indent=4)

        self.append_output(f"✓ Rod location saved: {coords}\n")
        self.append_output(f"  Config: {config_path}\n")

    def exit_app(self):
        """Exit the application completely"""
        # Stop the macro if it's running
        if self.is_running:
            self.stop_macro()

        # Destroy the GUI
        self.root.quit()
        self.root.destroy()

        # Exit the application completely
        sys.exit(0)

    def run(self):
        # Set up keyboard shortcuts using a separate thread
        def setup_keyboard_shortcuts():
            def on_press(key):
                try:
                    # Check if we're in the middle of rebinding a key
                    if self.rebinding_key:
                        # Handle Escape key to cancel rebinding
                        if key == Key.esc:
                            self.rebinding_key = None
                            self.update_binding_display()
                            print("Key rebinding cancelled")
                            return

                        # Get the key name
                        key_name = None
                        if hasattr(key, 'char'):
                            key_name = key.char
                        elif hasattr(key, 'name'):
                            key_name = key.name
                        else:
                            key_name = str(key).replace('Key.', '')

                        if key_name:
                            # Update the binding
                            self.key_bindings[self.rebinding_key] = key_name
                            self.rebinding_key = None
                            self.update_binding_display()
                            print(f"Key rebound successfully")
                        return

                    # Handle regular key presses based on current bindings
                    pressed_key = None
                    if hasattr(key, 'char'):
                        pressed_key = key.char
                    elif hasattr(key, 'name'):
                        pressed_key = key.name
                    else:
                        pressed_key = str(key).replace('Key.', '')

                    if pressed_key:
                        # Compare with current bindings (case-insensitive)
                        if pressed_key.lower() == self.key_bindings['start_stop'].lower():
                            self.root.after(0, self.toggle_macro_ui)
                        elif pressed_key.lower() == self.key_bindings['change_area'].lower():
                            self.root.after(0, self.toggle_area)
                        elif pressed_key.lower() == self.key_bindings['exit_app'].lower():
                            self.root.after(0, self.exit_app)
                except Exception as e:
                    print(f"Error processing key press: {e}")

            with keyboard.Listener(on_press=on_press) as listener:
                listener.join()

        # Start keyboard listener in a separate thread
        keyboard_thread = threading.Thread(target=setup_keyboard_shortcuts, daemon=True)
        keyboard_thread.start()

        # Start the GUI
        self.root.mainloop()

if __name__ == "__main__":
    app = RobloxFishingMacroGUI()
    app.run()