# KERN1 Invoice OCR Application

A powerful local GUI application for automated invoice processing using OCR and AI. Extract key information from scanned invoices (Dutch/English) and export to Excel with professional formatting.

## 🚀 New in Version 2.0

- **Supercharged OCR**: Multi-pass extraction with 4 different preprocessing techniques for maximum accuracy
- **PDF Support**: Full support for both text-based and scanned PDFs
- **Easy Launcher**: Non-technical users can double-click to start (no terminal needed!)
- **Advanced Preprocessing**: Denoising, deskewing, CLAHE, and adaptive thresholding
- **Image Quality Detection**: Automatic assessment of image quality
- **Better Field Detection**: Enhanced pattern matching for invoice data

## Features

- **Multi-language OCR Support**: Process invoices in Dutch and English
- **Multiple OCR Engines**: Choose between Tesseract, EasyOCR, or OpenAI Vision API
- **Multi-pass OCR**: Process images 4 times with different techniques for best results
- **PDF Support**: Handle both text-based and scanned PDFs (multi-page support)
- **AI-Powered Extraction**: Intelligent data extraction using OpenAI (optional)
- **Advanced Image Preprocessing**: Denoising, deskewing, contrast enhancement, sharpening
- **Interactive GUI**: User-friendly Streamlit interface with live preview
- **Manual Editing**: Review and edit extracted data before saving
- **Excel Export**: Professional Excel files with formatting and formulas
- **Batch Processing**: Process multiple invoices and export in one file
- **Format Support**: PNG, JPG, JPEG, GIF, BMP, TIFF, PDF

## Extracted Data Fields

Each invoice captures the following information:
- **Invoice Date**: Date of invoice
- **Invoice Number**: Unique invoice identifier
- **Supplier Name**: Company/vendor name
- **Service Description**: Description of services/products
- **Total Amount**: Total invoice amount (€)
- **VAT Amount**: VAT/tax amount (€)

## Easy Installation (For Everyone!)

### 🎯 Quick Start - No Terminal Required!

**For non-technical users, we have an easy launcher:**

1. **Download/extract** the project folder
2. **Double-click** `KERN1_Invoice_OCR.command`
3. **First time only**: Right-click → Open (Mac security prompt)
4. **Wait** for automatic setup (first run only, 3-5 minutes)
5. **Browser opens automatically** - start processing invoices!
6. **Next time**: Just double-click to start instantly!

📖 **See [LAUNCHER_GUIDE.md](LAUNCHER_GUIDE.md) for detailed instructions and troubleshooting**

### Advanced Installation (For Developers)

<details>
<summary>Click to expand advanced installation steps</summary>

#### Prerequisites

1. **Python 3.8 or higher**
   ```bash
   python --version
   ```

2. **Tesseract OCR** (optional, for Tesseract engine)

   **Ubuntu/Debian:**
   ```bash
   sudo apt-get update
   sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-nld
   ```

   **macOS:**
   ```bash
   brew install tesseract tesseract-lang
   ```

   **Windows:**
   Download installer from: https://github.com/UB-Mannheim/tesseract/wiki

   **Note:** If you don't have Tesseract, use EasyOCR engine instead (no installation required)

#### Setup

1. **Clone or download the repository:**
   ```bash
   cd /path/to/ocr_expenses
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv

   # Activate on Linux/Mac:
   source venv/bin/activate

   # Activate on Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment (optional):**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your preferred editor
   ```

   Add your OpenAI API key for AI-powered extraction (optional):
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   OCR_ENGINE=tesseract
   OCR_LANGUAGES=eng,nld
   ```

</details>

## Usage

### Starting the Application

**Easy Way (Recommended):**
- **Double-click** your platform's launcher file (see Easy Installation above)

**Manual Way (Developers):**
1. **Activate virtual environment** (if not already active):
   ```bash
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. **Launch the application:**
   ```bash
   streamlit run app.py
   ```

3. **Access the GUI:**
   The application will automatically open in your browser at `http://localhost:8501`

### Processing Invoices

#### Upload & Process Tab

1. **Upload an invoice** (Image: PNG, JPG, GIF, BMP, TIFF, or PDF)
2. **For PDFs**: The app automatically detects if it's text-based or scanned
   - Text-based PDFs: Instant text extraction
   - Scanned PDFs: Converts to images for OCR
   - Multi-page PDFs: Processes all pages automatically
3. **Configure processing options:**
   - ✅ Multi-pass OCR (recommended - processes 4 times for best accuracy)
   - ✅ AI extraction (optional, requires OpenAI API key)
4. **Check image quality** indicator (for image files)
5. **Click "Process Invoice"** to extract data
6. **Review extracted data** in the form
7. **Edit any fields** if needed
8. **Click "Save Invoice"** to add to your collection

#### Invoices Tab

- **View all processed invoices** in expandable cards
- **Edit or delete** individual invoices
- **Export all invoices** to Excel with one click

#### Settings Tab

- **Switch OCR engines** (Tesseract, EasyOCR, or OpenAI)
- **View configuration** and directory locations
- **Check OpenAI integration** status

### Excel Export

The Excel export includes:
- ✅ Professional formatting with headers
- ✅ Automatic column widths
- ✅ Currency formatting (€)
- ✅ Date formatting (YYYY-MM-DD)
- ✅ Frozen header row
- ✅ Bordered cells

**Excel Columns:**
1. Invoice Date
2. Invoice Number
3. Service Description
4. Supplier Name
5. Total Amount (€)
6. VAT Amount (€)

Exported files are saved in the `exports/` directory with timestamped filenames.

## OCR Engine Comparison

### Tesseract (Default, with Multi-pass)
- ✅ Free and open-source
- ✅ **Excellent accuracy with multi-pass extraction**
- ✅ Supports Dutch and English
- ✅ Advanced preprocessing (denoising, deskewing, CLAHE)
- ⚠️ Requires Tesseract installation
- ⚠️ Slightly slower with multi-pass (but worth it!)

### EasyOCR
- ✅ No external dependencies needed
- ✅ Very good accuracy
- ✅ Supports multiple languages
- ✅ Works with multi-pass extraction
- ⚠️ Slower than Tesseract
- ⚠️ Larger memory footprint
- ⚠️ First run downloads language models

### OpenAI Vision API
- ✅ Best accuracy, especially with complex layouts
- ✅ Handles handwriting and poor quality images
- ✅ Intelligent data extraction
- ✅ No preprocessing needed
- ⚠️ Requires API key and internet connection
- ⚠️ Costs per API call (~$0.01 per invoice)

### Multi-pass Extraction (New!)

When enabled (default), the application:
1. Processes the original image
2. Processes with enhanced contrast and sharpness
3. Processes with advanced denoising and binarization
4. Processes with image sharpening

Then selects the best (longest/most complete) result. This dramatically improves accuracy for difficult invoices!

## Troubleshooting

### Tesseract Not Found Error

**Error:** `pytesseract.pytesseract.TesseractNotFoundError`

**Solution:**
1. Install Tesseract OCR (see Prerequisites)
2. Or switch to EasyOCR in Settings tab

### Poor OCR Accuracy

**Solutions:**
1. ✅ Enable "Preprocess image" option
2. ✅ Try a different OCR engine
3. ✅ Use OpenAI Vision API for best results
4. ✅ Ensure image is high quality and well-lit
5. ✅ Manually edit extracted data if needed

### OpenAI API Errors

**Error:** OpenAI authentication failed

**Solution:**
1. Verify API key in `.env` file
2. Ensure you have credits in your OpenAI account
3. Check internet connection

### Missing Data Fields

If some fields are not extracted:
1. ✅ Enable AI extraction (if available)
2. ✅ Manually fill in missing fields in the form
3. ✅ Ensure invoice has clear, readable text

## Project Structure

```
ocr_expenses/
├── app.py                        # Main Streamlit application
├── config.py                     # Configuration management
├── ocr_engine.py                 # OCR processing (multi-pass, preprocessing)
├── invoice_parser.py             # Data extraction and parsing
├── excel_exporter.py             # Excel file generation
├── pdf_handler.py                # PDF conversion and processing
├── launch_app.py                 # Easy launcher script
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
├── .gitignore                   # Git ignore rules
├── README.md                    # This file (you are here)
├── LAUNCHER_GUIDE.md            # Non-technical user guide
├── QUICKSTART.md                # 5-minute setup guide
├── test_setup.py                # Setup verification tool
├── run.sh / run.bat             # Platform-specific runners
├── KERN1_Invoice_OCR.bat        # Windows double-click launcher
├── KERN1_Invoice_OCR.command    # Mac double-click launcher
├── KERN1_Invoice_OCR.desktop    # Linux desktop entry
├── uploads/                     # Uploaded files (auto-created)
└── exports/                     # Excel exports (auto-created)
```

## Tips for Best Results

1. **Image Quality**
   - Use high-resolution scans (at least 300 DPI)
   - Ensure good lighting and contrast
   - Avoid shadows and glare

2. **Invoice Format**
   - Standard invoice layouts work best
   - Clear, printed text (not handwritten)
   - Horizontal orientation preferred

3. **Workflow**
   - Process invoices in batches
   - Review extracted data before saving
   - Export regularly to avoid data loss

4. **Data Entry**
   - Use consistent date format (YYYY-MM-DD)
   - Enter amounts without currency symbols
   - Keep descriptions concise but descriptive

## Advanced Configuration

### Custom OCR Languages

Edit `.env` file:
```bash
# Add more language codes (comma-separated)
OCR_LANGUAGES=eng,nld,deu,fra
```

### Change Default OCR Engine

Edit `.env` file:
```bash
# Options: tesseract, easyocr, openai
OCR_ENGINE=easyocr
```

## Security Notes

- ⚠️ **Never commit `.env` file** to version control
- ⚠️ Keep OpenAI API keys secure
- ⚠️ Invoice images may contain sensitive information
- ✅ All processing is done locally (except OpenAI API calls)
- ✅ No data is stored remotely

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the Settings tab in the application
3. Ensure all dependencies are installed correctly

## Version

**Version:** 2.0.0
**Company:** KERN1
**License:** Private Use

## What's New in Version 2.0

### Supercharged OCR Accuracy
- Multi-pass extraction with 4 different preprocessing techniques
- Advanced image preprocessing (denoising, deskewing, CLAHE)
- Better pattern matching for invoice fields
- Image quality assessment

### PDF Support
- Text-based PDF: Instant extraction
- Scanned PDF: Automatic conversion to images
- Multi-page support for both types

### Easy Access for Everyone
- Double-click launchers for all platforms
- Automatic setup on first run
- No terminal/command line needed
- Desktop shortcut creation guide

### Better User Experience
- Image quality indicator
- Clearer processing status
- Better error messages
- OCR engine comparison in Settings

## Requirements

- Python 3.8+
- Streamlit 1.31+
- Tesseract OCR (optional, can use EasyOCR instead)
- OpenAI API key (optional, for AI features)
- No poppler installation needed (uses pypdfium2 for PDFs)

## Quick Links

- 📖 [Non-Technical User Guide](LAUNCHER_GUIDE.md) - For easy launcher usage
- 🚀 [Quick Start Guide](QUICKSTART.md) - Get running in 5 minutes
- 🧪 Test your setup: Run `python test_setup.py`

---

**Built with Python, Streamlit, Tesseract, EasyOCR, PyPDF2, and OpenAI**
