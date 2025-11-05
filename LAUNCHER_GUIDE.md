# Easy Launcher Guide for Non-Technical Users

## Quick Start (No Terminal Required!)

### Windows Users 🪟

1. **Find the file:** `KERN1_Invoice_OCR.bat` in your project folder
2. **Double-click** the file
3. **Wait** for the application to start (may take 1-2 minutes on first run)
4. **Your browser will open automatically** with the application
5. **Start processing invoices!**

**Note:** A command window will stay open - don't close it! Closing it will stop the application.

### Mac Users 🍎

1. **Find the file:** `KERN1_Invoice_OCR.command` in your project folder
2. **Right-click** the file and select "Open" (first time only)
3. **Click "Open"** in the security dialog (Mac will ask permission first time)
4. **Wait** for the application to start
5. **Your browser will open automatically** at http://localhost:8501
6. **Start processing invoices!**

**Tip:** Next time, you can just double-click the file!

###Linux Users 🐧

**Option 1: Double-Click Launcher**
1. **Right-click** `launch_app.py` → "Properties" → "Permissions"
2. **Check** "Allow executing file as program"
3. **Double-click** `launch_app.py` to run

**Option 2: Desktop Entry**
1. Copy `KERN1_Invoice_OCR.desktop` to `~/Desktop/` or `~/.local/share/applications/`
2. Make it executable: `chmod +x KERN1_Invoice_OCR.desktop`
3. Double-click the icon on your desktop

## Creating a Desktop Shortcut

### Windows

1. **Right-click** on `KERN1_Invoice_OCR.bat`
2. Select **"Create shortcut"**
3. **Drag the shortcut** to your Desktop
4. **Rename** it to "KERN1 Invoice OCR" (optional)
5. **Right-click** the shortcut → "Properties" → "Change Icon" (optional)

### Mac

1. **Right-click** on `KERN1_Invoice_OCR.command`
2. Select **"Make Alias"**
3. **Drag the alias** to your Desktop or Applications folder
4. **Rename** it to "KERN1 Invoice OCR" (optional)

### Linux

1. **Copy** `KERN1_Invoice_OCR.desktop` to your Desktop:
   ```bash
   cp KERN1_Invoice_OCR.desktop ~/Desktop/
   chmod +x ~/Desktop/KERN1_Invoice_OCR.desktop
   ```
2. **Double-click** to run!

## First Time Setup

### What Happens on First Run?

The launcher automatically:
1. ✅ Creates a virtual environment (if needed)
2. ✅ Installs all required software packages
3. ✅ Creates necessary folders (uploads, exports)
4. ✅ Opens your web browser to the application

**This takes 3-5 minutes on first run.** Subsequent launches are instant!

### What You Need Installed

**Minimum Requirements:**
- Python 3.8 or higher ([Download here](https://www.python.org/downloads/))
- Tesseract OCR (for best results)

**Installing Tesseract:**

**Windows:**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer
3. Restart computer

**Mac:**
```bash
brew install tesseract tesseract-lang
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-nld
```

## Using the Application

Once the application opens in your browser:

1. **Upload Tab**:
   - Drag & drop or click to upload invoice (image or PDF)
   - Choose options:
     - ✅ Multi-pass OCR (recommended for best accuracy)
     - ✅ AI extraction (optional, requires OpenAI API key)
   - Click "Process Invoice"
   - Review and edit extracted data
   - Click "Save Invoice"

2. **Invoices Tab**:
   - View all processed invoices
   - Export to Excel with one click
   - Download the Excel file

3. **Settings Tab**:
   - Change OCR engine (Tesseract or EasyOCR)
   - View configuration and status

## Troubleshooting

### "Python not found" Error

**Solution:** Install Python from https://www.python.org/downloads/

Make sure to check "Add Python to PATH" during installation (Windows)

### "Tesseract not found" Warning

**Solution:**
- Install Tesseract (see above)
- OR use EasyOCR engine (no installation needed):
  - Open application → Settings tab → Select "easyocr"

### Browser Doesn't Open Automatically

**Solution:**
1. Look for this line in the terminal window:
   ```
   Local URL: http://localhost:8501
   ```
2. **Copy this URL** and **paste it into your browser**

### Application Won't Start

**Solution:**
1. Check that Python is installed: Open terminal/command prompt and type:
   ```
   python --version
   ```
2. If you see "command not found", install Python
3. Try running the test script:
   ```
   python test_setup.py
   ```

### Port Already in Use Error

**Solution:**
Another application is using port 8501. Either:
- Close the other Streamlit application
- Or edit `launch_app.py` and change `8501` to another port like `8502`

## Stopping the Application

### All Platforms

1. **Go to the terminal/command window** that opened when you started the app
2. **Press** `Ctrl+C` (Windows/Linux) or `Cmd+C` (Mac)
3. **Or simply close** the terminal window

The application will stop, but your data in the `exports/` folder is safe!

## Tips for Best Results

1. **Use high-quality scans** (300+ DPI)
2. **Enable "Multi-pass OCR"** for difficult invoices
3. **Review extracted data** before saving
4. **Export regularly** to avoid data loss
5. **Keep terminal window open** while using the app

## Getting Help

If you encounter issues:
1. Read the full [README.md](README.md)
2. Run the setup test: `python test_setup.py`
3. Check the Settings tab in the application
4. Make sure all prerequisites are installed

## Optional: OpenAI API for Best Accuracy

For maximum accuracy with complex or handwritten invoices:

1. **Get an API key** from https://platform.openai.com/api-keys
2. **Open** `.env` file in the project folder with a text editor
3. **Add** your API key:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```
4. **Save** the file
5. **Restart** the application

Now you can use AI-powered extraction for best results!

---

**🎉 You're all set! Enjoy processing your invoices with KERN1 Invoice OCR!**
