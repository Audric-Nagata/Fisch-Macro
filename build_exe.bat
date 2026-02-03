@echo off
echo ========================================
echo    Building Fishing Macro EXE
echo ========================================
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install PyInstaller if not already installed
echo Installing/Updating PyInstaller...
pip install --upgrade pyinstaller

echo.
echo Building executable...
echo This may take a few minutes...
echo.

REM Build the EXE with all necessary dependencies
pyinstaller --onefile ^
    --windowed ^
    --name "FishingMacro" ^
    --icon "assets/icon.ico" ^
    --add-data "src/config;config" ^
    --hidden-import=pynput.keyboard._win32 ^
    --hidden-import=pynput.mouse._win32 ^
    --hidden-import=win32api ^
    --hidden-import=win32con ^
    --hidden-import=tkinter ^
    --hidden-import=cv2 ^
    --hidden-import=numpy ^
    --hidden-import=mss ^
    --hidden-import=pyautogui ^
    --hidden-import=pygetwindow ^
    --collect-all pynput ^
    --collect-all cv2 ^
    --collect-all numpy ^
    src/fishing_macro_gui.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS! EXE created successfully!
    echo ========================================
    echo.
    echo Your executable is located at:
    echo   dist\FishingMacro.exe
    echo.
    echo File size: 
    dir dist\FishingMacro.exe | find "FishingMacro.exe"
    echo.
    echo You can now run it without Python installed!
    echo.
    echo IMPORTANT: The config folder will be created
    echo next to the EXE when you first run it.
    echo.
) else (
    echo.
    echo ERROR: Build failed!
    echo Check the error messages above.
    pause
)

pause
