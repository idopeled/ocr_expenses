"""
Test script to verify the application setup
Run this before using the application to ensure everything is configured correctly
"""
import sys


def test_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} (requires 3.8+)")
        return False


def test_dependencies():
    """Check if all required packages are installed"""
    print("\n📦 Checking dependencies...")

    required_packages = {
        'streamlit': 'Streamlit',
        'PIL': 'Pillow',
        'pandas': 'Pandas',
        'openpyxl': 'OpenPyXL',
        'pytesseract': 'PyTesseract',
        'easyocr': 'EasyOCR',
        'cv2': 'OpenCV',
        'numpy': 'NumPy',
        'dateutil': 'python-dateutil',
        'dotenv': 'python-dotenv',
    }

    missing = []
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name} (not installed)")
            missing.append(name)

    # Optional packages
    print("\n📦 Checking optional dependencies...")
    try:
        import openai
        print("   ✅ OpenAI (AI-powered extraction available)")
    except ImportError:
        print("   ⚠️  OpenAI (install for AI features: pip install openai)")

    return len(missing) == 0, missing


def test_tesseract():
    """Check if Tesseract OCR is installed"""
    print("\n🔍 Checking Tesseract OCR...")
    try:
        import pytesseract
        from PIL import Image
        import numpy as np

        # Try to get Tesseract version
        version = pytesseract.get_tesseract_version()
        print(f"   ✅ Tesseract {version}")
        return True
    except Exception as e:
        print(f"   ❌ Tesseract not found or not configured")
        print(f"      Error: {str(e)}")
        print("      Install: sudo apt-get install tesseract-ocr (Ubuntu)")
        print("               brew install tesseract (macOS)")
        return False


def test_directories():
    """Check if necessary directories exist"""
    print("\n📁 Checking directories...")
    from pathlib import Path

    base_dir = Path(__file__).parent
    dirs = ['uploads', 'exports']

    all_exist = True
    for dir_name in dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            print(f"   ✅ {dir_name}/")
        else:
            print(f"   ⚠️  {dir_name}/ (will be created automatically)")

    return True


def test_config():
    """Check configuration"""
    print("\n⚙️  Checking configuration...")
    try:
        from config import Config
        from pathlib import Path

        # Check .env file
        env_file = Path('.env')
        if env_file.exists():
            print("   ✅ .env file exists")
        else:
            print("   ⚠️  .env file not found (using defaults)")

        # Check OpenAI
        if Config.is_openai_available():
            print("   ✅ OpenAI API key configured")
        else:
            print("   ⚠️  OpenAI API key not configured (AI features disabled)")

        print(f"   ℹ️  OCR Engine: {Config.OCR_ENGINE}")
        print(f"   ℹ️  Languages: {', '.join(Config.OCR_LANGUAGES)}")

        return True
    except Exception as e:
        print(f"   ❌ Configuration error: {e}")
        return False


def test_ocr_engines():
    """Test available OCR engines"""
    print("\n🔧 Testing OCR engines...")

    engines_available = []

    # Test Tesseract
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        print("   ✅ Tesseract OCR (ready)")
        engines_available.append('tesseract')
    except:
        print("   ❌ Tesseract OCR (not available)")

    # Test EasyOCR
    try:
        import easyocr
        print("   ✅ EasyOCR (ready)")
        engines_available.append('easyocr')
    except:
        print("   ❌ EasyOCR (not installed)")

    # Test OpenAI
    try:
        from config import Config
        if Config.is_openai_available():
            print("   ✅ OpenAI Vision API (ready)")
            engines_available.append('openai')
        else:
            print("   ⚠️  OpenAI Vision API (API key not configured)")
    except:
        print("   ❌ OpenAI Vision API (not available)")

    return len(engines_available) > 0, engines_available


def main():
    """Run all tests"""
    print("=" * 60)
    print("KERN1 Invoice OCR - Setup Verification")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("Python Version", test_python_version()))

    deps_ok, missing = test_dependencies()
    results.append(("Dependencies", deps_ok))

    results.append(("Tesseract OCR", test_tesseract()))
    results.append(("Directories", test_directories()))
    results.append(("Configuration", test_config()))

    engines_ok, engines = test_ocr_engines()
    results.append(("OCR Engines", engines_ok))

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    all_passed = all(result[1] for result in results)
    critical_passed = results[0][1] and results[1][1] and results[5][1]

    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")

    print("\n" + "=" * 60)

    if all_passed:
        print("🎉 All tests passed! Your setup is complete.")
        print("\nRun the application with:")
        print("   streamlit run app.py")
    elif critical_passed:
        print("⚠️  Setup is functional but some optional features are missing.")
        print("\nYou can run the application with:")
        print("   streamlit run app.py")
        print("\nTo enable all features:")
        if not results[2][1]:  # Tesseract
            print("   - Install Tesseract OCR")
        if missing:
            print(f"   - Install missing packages: pip install -r requirements.txt")
    else:
        print("❌ Critical setup issues found. Please fix the errors above.")
        print("\nInstallation steps:")
        print("   1. Ensure Python 3.8+ is installed")
        print("   2. Run: pip install -r requirements.txt")
        print("   3. Install Tesseract OCR (see README.md)")
        return 1

    print("=" * 60)
    return 0


if __name__ == "__main__":
    exit(main())
