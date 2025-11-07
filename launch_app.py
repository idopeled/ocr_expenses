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
    needs_setup = False

    if not venv_dir.exists():
        print("⚠️  Setting up application for first time...")
        print("This may take a few minutes...")
        print()

        # Create virtual environment
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
        print("✅ Virtual environment created")
        print()
        needs_setup = True

    # Get python executable from venv
    if sys.platform == "win32":
        python_exe = venv_dir / "Scripts" / "python.exe"
        pip_exe = venv_dir / "Scripts" / "pip.exe"
    else:
        python_exe = venv_dir / "bin" / "python"
        pip_exe = venv_dir / "bin" / "pip"

    # Create a marker file to track if dependencies are installed
    marker_file = venv_dir / ".dependencies_installed"

    # Check if dependencies are installed (use marker file for efficiency)
    if not marker_file.exists() or needs_setup:
        print("📦 Installing dependencies...")
        print("This may take a few minutes...")
        print()

        # Upgrade pip first
        print("Upgrading pip...")
        subprocess.run([str(python_exe), "-m", "pip", "install", "--upgrade", "pip"],
                      capture_output=True, check=False)

        # Install dependencies
        result = subprocess.run([str(pip_exe), "install", "-r", "requirements.txt"],
                               capture_output=False, check=False)

        if result.returncode == 0:
            # Create marker file
            marker_file.touch()
            print()
            print("✅ Dependencies installed")
            print()
        else:
            print()
            print("⚠️  Some dependencies failed to install, but continuing anyway...")
            print("The app may still work with reduced functionality.")
            print()
    else:
        print("✅ Dependencies already installed (skipping)")
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
