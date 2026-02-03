# Roblox Fishing Macro

An automated fishing macro for Roblox games with a user-friendly GUI, customizable keybindings, and intelligent color detection for fishing mechanics.

## ✨ Features

- 🎣 **Automated Fishing**: Automatically casts, detects fishing bar, and reels in fish
- 🎮 **Customizable Keybindings**: Rebind all hotkeys through the GUI
- 🎯 **Multiple Fishing Areas**: Save and switch between different fishing spot coordinates
- 🎨 **Visual Indicators**: Real-time display of detected fishing bar and catch indicators
- 🖱️ **Smart Detection**: Advanced color detection with tolerance for various game lighting
- ⚡ **Performance Optimized**: Uses win32api for fast, reliable input simulation
- 🔄 **Auto-Recast**: Automatically recasts after catching or missing fish

### Default Keybindings

- **F1**: Start/Stop the fishing macro
- **F2**: Toggle between saved fishing areas
- **F3**: Exit the application

All keybindings can be customized by clicking on them in the GUI.

## 📋 Prerequisites

- **OS**: Windows (required for window management and win32api)
- **Python**: 3.7 or higher
- **Roblox**: Must be running in windowed or windowed fullscreen mode

## 🚀 Installation

### Option 1: Using Pre-built Executable (Easiest)

1. Download the latest release from the [Releases](../../releases) page
2. Extract `FishingMacro.exe`
3. Run the executable - no Python installation required!

### Option 2: Using Virtual Environment (Recommended for Development)

1. Clone this repository:
```bash
git clone https://github.com/Audric-Nagata/Fisch-Macro.git
cd Fisch-Macro
```

2. Run the setup script to create a virtual environment and install dependencies:
```bash
setup_venv.bat
```

3. Run the application:
```bash
run.bat
```

### Option 3: System-wide Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python src/fishing_macro_gui.py
```

## 📖 Usage

### First Time Setup

1. Launch Roblox and open your fishing game
2. Make sure Roblox is in **windowed** or **windowed fullscreen** mode
3. Start the Fishing Macro application
4. Click **"Set Rod Location"** and click on your fishing rod in the game
5. The macro will automatically detect the fishing bar colors

### Running the Macro

1. Position your Roblox window where you want it
2. Press **F1** (or your custom keybind) to start the macro
3. The macro will:
   - Cast the fishing rod
   - Detect the fishing bar appearance
   - Track the catch indicator
   - Automatically reel in when needed
   - Recast after catching or missing

### Managing Fishing Areas

- **Save Area**: After setting a rod location, it's automatically saved
- **Switch Areas**: Press **F2** to cycle through saved fishing spots
- **Multiple Spots**: Save different locations for various fishing areas in the game

## ⚙️ Configuration

The macro saves settings in `config.json`:

```json
{
    "key_bindings": {
        "start_stop": "f1",
        "change_area": "f2",
        "exit_app": "f3"
    },
    "selected_area": null
}
```

Rod locations are saved in `config/rod_locations.json` (created automatically).

## 🔨 Building Executable

To create a standalone `.exe` file:

```bash
build_exe.bat
```

The executable will be created in the `dist/` folder. See [BUILD_EXE_GUIDE.md](BUILD_EXE_GUIDE.md) for more details.

## 🛠️ Troubleshooting

### Macro doesn't detect the fishing bar
- Ensure Roblox is in windowed mode (not fullscreen)
- Try setting the rod location again
- Check that the fishing bar colors match the game's current theme

### Keybinds not working
- Make sure the macro window has focus when setting keybinds
- Avoid using keys that conflict with Roblox controls
- Check `config.json` for correct keybind values

### Executable flagged by antivirus
- This is a common false positive for PyInstaller executables
- Add an exception in your antivirus software
- The source code is available for review

### Macro clicks in wrong location
- Roblox window must stay in the same position after setting rod location
- Don't minimize or move the Roblox window while macro is running
- Re-set the rod location if you move the window

## 📦 Dependencies

- `pynput` - Keyboard input handling
- `pygetwindow` - Window management
- `pyautogui` - Screen automation
- `Pillow` - Image processing
- `pywin32` - Windows API for input simulation
- `mss` - Fast screenshot capture
- `opencv-python` - Computer vision for detection
- `numpy` - Numerical operations

## ⚠️ Disclaimer

**This project is for educational purposes only.**

- Using macros/automation may violate Roblox's Terms of Service
- Use at your own risk - account bans are possible
- The developers are not responsible for any consequences
- This tool is meant to demonstrate automation techniques and computer vision

## 📄 License

This project is provided as-is for educational purposes only.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](../../issues).

## 📧 Support

If you encounter any issues or have questions, please [open an issue](../../issues/new).