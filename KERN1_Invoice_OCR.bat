@echo off
REM KERN1 Invoice OCR Application Launcher for Windows
REM Double-click this file to start the application

title KERN1 Invoice OCR Application

echo.
echo ============================================================
echo KERN1 Invoice OCR Application
echo ============================================================
echo.
echo Starting application...
echo.

REM Get the directory where this script is located
cd /d "%~dp0"

REM Run the Python launcher
python launch_app.py

pause
