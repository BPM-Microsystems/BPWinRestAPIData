@echo off
echo ====================================
echo   DataPanel - BPWin REST API Monitor
echo ====================================
echo.
echo Starting application...
echo The browser will open automatically at http://localhost:8501
echo.
echo Press Ctrl+C in this window to stop the application
echo ====================================
echo.

REM Check if Auth.txt exists
if not exist "C:\BP\Auth.txt" (
    echo WARNING: C:\BP\Auth.txt not found!
    echo Please create an empty Auth.txt file in C:\BP folder
    echo.
    pause
    exit /b 1
)

REM Run the executable
dist\DataPanel.exe

pause
