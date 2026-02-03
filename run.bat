@echo off
echo ========================================
echo    Roblox Fishing Macro Launcher
echo ========================================
echo.

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
    if errorlevel 1 (
        echo.
        echo ERROR: Virtual environment not found!
        echo Please run setup_venv.bat first.
        echo.
        pause
        exit /b 1
    )
)

echo Starting fishing macro GUI...
echo.
python src/fishing_macro_gui.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Application closed successfully.
) else (
    echo.
    echo ERROR: Application failed to run!
    pause
)