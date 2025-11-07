# Easy Launcher Guide for Mac Users

## Quick Start (No Terminal Required!)

### Mac Users 🍎

1. **Find the file:** `KERN1_Invoice_OCR.command` in your project folder
2. **First time:** Right-click the file and select "Open"
3. **Click "Open"** in the security dialog (Mac will ask permission first time)
4. **Wait** for the application to start (3-5 minutes on first run)
5. **Your browser will open automatically** at http://localhost:8501
6. **Start processing invoices!**

**Next Time:** Just double-click the file - instant startup!

**Note:** A Terminal window will stay open - don't close it! Closing it will stop the application.

## Creating a Desktop Shortcut (Optional)

### Mac

1. **Right-click** on `KERN1_Invoice_OCR.command`
2. Select **"Make Alias"**
3. **Drag the alias** to your Desktop or Applications folder
4. **Rename** it to "KERN1 Invoice OCR" (optional)

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

**Installing Tesseract (Mac):**

```bash
brew install tesseract tesseract-lang
```

If you don't have Homebrew, install it first:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
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
