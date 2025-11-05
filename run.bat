@echo off
REM Quick start script for KERN1 Invoice OCR Application (Windows)

echo Starting KERN1 Invoice OCR Application...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found!
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo Dependencies installed
)

REM Create directories
echo Creating necessary directories...
if not exist "uploads\" mkdir uploads
if not exist "exports\" mkdir exports

REM Check for .env file
if not exist ".env" (
    echo .env file not found. Creating from template...
    copy .env.example .env
    echo .env file created. Edit it to add your OpenAI API key (optional)
)

echo.
echo Starting application...
echo The app will open in your browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo.

REM Run the app
streamlit run app.py
