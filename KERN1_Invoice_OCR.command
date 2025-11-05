#!/bin/bash
# KERN1 Invoice OCR Application Launcher for macOS
# Double-click this file to start the application

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo ""
echo "============================================================"
echo "KERN1 Invoice OCR Application"
echo "============================================================"
echo ""
echo "Starting application..."
echo ""

# Run the Python launcher
python3 launch_app.py

echo ""
echo "Press any key to exit..."
read -n 1
