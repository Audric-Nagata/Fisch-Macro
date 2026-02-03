# Building EXE Guide

## Quick Start

Simply run:
```bash
build_exe.bat
```

This will create a standalone `FishingMacro.exe` in the `dist` folder.

## What Happens

1. PyInstaller bundles your Python code and all dependencies
2. Creates a single executable file
3. No Python installation needed to run the EXE

## Output Location

After building, you'll find:
- **`dist/FishingMacro.exe`** - Your standalone executable

## File Size

The EXE will be around **50-80 MB** because it includes:
- Python interpreter
- All libraries (OpenCV, NumPy, etc.)
- Your code

## Distribution

You can share just the `FishingMacro.exe` file with others!

They can run it on any Windows PC without installing Python.

## Important Notes

⚠️ **Config Files**: The EXE will create a `config` folder next to itself for saving rod locations.

⚠️ **First Run**: Windows Defender might flag it (false positive). You may need to allow it.

⚠️ **Antivirus**: Some antivirus software flags PyInstaller EXEs. This is normal for automation tools.

## Troubleshooting

If the build fails:
1. Make sure virtual environment is activated
2. Try: `pip install --upgrade pyinstaller`
3. Check that all dependencies are installed

## Alternative: Keep Using Python

If you prefer, you can keep using `run.bat` - it works perfectly fine!
