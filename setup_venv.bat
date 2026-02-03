@echo off
echo Setting up virtual environment for Roblox Fishing Macro...

REM Create virtual environment
python -m venv .venv

if %ERRORLEVEL% EQU 0 (
    echo Virtual environment created successfully!
    
    REM Activate virtual environment and install requirements
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    
    if %ERRORLEVEL% EQU 0 (
        echo Dependencies installed successfully!
        echo.
        echo #########################################################################
        echo To run the application:
        echo   1. Activate the virtual environment: .venv\Scripts\activate.bat
        echo   2. Run the app: python src/fishing_macro_gui.py
        echo #########################################################################
    ) else (
        echo Error installing dependencies!
        pause
    )
) else (
    echo Error creating virtual environment!
    echo Make sure Python is installed and added to your PATH.
    pause
)