# Quick Start Guide - KERN1 Invoice OCR

Get up and running in 5 minutes!

## Step 1: Install Prerequisites

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv tesseract-ocr tesseract-ocr-eng tesseract-ocr-nld
```

### macOS
```bash
brew install python3 tesseract tesseract-lang
```

### Windows
1. Install Python 3.8+ from https://www.python.org/downloads/
2. Install Tesseract from https://github.com/UB-Mannheim/tesseract/wiki

## Step 2: Setup the Application

### Linux/macOS
```bash
cd /home/user/ocr_expenses

# One command to rule them all!
./run.sh
```

### Windows
```cmd
cd C:\path\to\ocr_expenses
run.bat
```

That's it! The application will automatically:
- Create a virtual environment
- Install all dependencies
- Create necessary directories
- Launch the web interface

## Step 3: Process Your First Invoice

1. **Open your browser** to http://localhost:8501
2. **Go to "Upload & Process" tab**
3. **Drag and drop** an invoice image
4. **Click "Process Invoice"**
5. **Review the extracted data**
6. **Edit if needed** and click "Save Invoice"
7. **Go to "Invoices" tab**
8. **Click "Export to Excel"**
9. **Download your Excel file!**

## Optional: Enable AI Features

For better accuracy with complex invoices:

1. Get an OpenAI API key from https://platform.openai.com/api-keys
2. Edit the `.env` file:
   ```bash
   nano .env  # or use any text editor
   ```
3. Add your API key:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```
4. Restart the application

Now you can use AI-powered extraction by checking the "Use AI extraction" box!

## Verify Your Setup

Run the test script to check everything:

```bash
python test_setup.py
```

This will verify:
- ✅ Python version
- ✅ All dependencies
- ✅ Tesseract installation
- ✅ OCR engines availability
- ✅ Configuration

## Common Issues

### "Tesseract not found"
→ Install Tesseract OCR (see Step 1)
→ Or switch to EasyOCR in Settings tab

### "Module not found"
→ Run: `pip install -r requirements.txt`

### "Port already in use"
→ Stop other Streamlit apps
→ Or use: `streamlit run app.py --server.port 8502`

## What's Next?

- 📖 Read the full [README.md](README.md) for detailed documentation
- ⚙️ Configure OCR engines in the Settings tab
- 🎨 Customize the `.env` file for your preferences
- 📊 Process your invoice backlog!

## Need Help?

- Check the Settings tab in the app
- Review the README.md troubleshooting section
- Run `python test_setup.py` to diagnose issues

---

**🎉 Happy invoice processing!**
