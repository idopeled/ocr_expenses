"""
Simple launcher for KERN1 Invoice OCR Application
Double-click this file to start the application
"""
import os
import sys
import subprocess
from pathlib import Path
import webbrowser
import time


def main():
    """Launch the Streamlit application"""
    # Get the directory where this script is located
    app_dir = Path(__file__).parent

    # Change to app directory
    os.chdir(app_dir)

    print("=" * 60)
    print("KERN1 Invoice OCR Application")
    print("=" * 60)
    print()

    # Check if virtual environment exists
    venv_dir = app_dir / "venv"
    if not venv_dir.exists():
        print("⚠️  Setting up application for first time...")
        print("This may take a few minutes...")
        print()

        # Create virtual environment
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
        print("✅ Virtual environment created")
        print()

    # Get python executable from venv
    if sys.platform == "win32":
        python_exe = venv_dir / "Scripts" / "python.exe"
        pip_exe = venv_dir / "Scripts" / "pip.exe"
    else:
        python_exe = venv_dir / "bin" / "python"
        pip_exe = venv_dir / "bin" / "pip"

    # Check if dependencies are installed
    result = subprocess.run(
        [str(python_exe), "-c", "import streamlit"],
        capture_output=True
    )

    if result.returncode != 0:
        print("📦 Installing dependencies...")
        print("This may take a few minutes on first run...")
        print()
        subprocess.run([str(pip_exe), "install", "-r", "requirements.txt"], check=True)
        print()
        print("✅ Dependencies installed")
        print()

    # Create directories
    (app_dir / "uploads").mkdir(exist_ok=True)
    (app_dir / "exports").mkdir(exist_ok=True)

    # Create .env if it doesn't exist
    env_file = app_dir / ".env"
    if not env_file.exists() and (app_dir / ".env.example").exists():
        import shutil
        shutil.copy(app_dir / ".env.example", env_file)

    print("✅ Starting KERN1 Invoice OCR Application...")
    print()
    print("🌐 The application will open in your browser in a moment...")
    print("🌐 URL: http://localhost:8501")
    print()
    print("⚠️  DO NOT CLOSE THIS WINDOW while using the application")
    print("    To stop the application, press Ctrl+C or close this window")
    print()
    print("=" * 60)
    print()

    # Wait a bit then open browser
    def open_browser():
        time.sleep(3)
        webbrowser.open("http://localhost:8501")

    import threading
    threading.Thread(target=open_browser, daemon=True).start()

    # Run streamlit
    try:
        subprocess.run(
            [str(python_exe), "-m", "streamlit", "run", "app.py",
             "--server.headless", "true",
             "--browser.gatherUsageStats", "false"],
            check=True
        )
    except KeyboardInterrupt:
        print()
        print("=" * 60)
        print("Application stopped")
        print("=" * 60)
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()
