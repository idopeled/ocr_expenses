# KERN1 Invoice OCR Application

A powerful local GUI application for automated invoice processing using OCR and AI. Extract key information from scanned invoices (Dutch/English) and export to Excel with professional formatting.

## Features

- **Multi-language OCR Support**: Process invoices in Dutch and English
- **Multiple OCR Engines**: Choose between Tesseract, EasyOCR, or OpenAI Vision API
- **AI-Powered Extraction**: Intelligent data extraction using OpenAI (optional)
- **Image Preprocessing**: Automatic image enhancement for better OCR accuracy
- **Interactive GUI**: User-friendly Streamlit interface with live preview
- **Manual Editing**: Review and edit extracted data before saving
- **Excel Export**: Professional Excel files with formatting and formulas
- **Batch Processing**: Process multiple invoices and export in one file
- **Format Support**: PNG, JPG, JPEG, GIF, BMP, TIFF

## Extracted Data Fields

Each invoice captures the following information:
- **Invoice Date**: Date of invoice
- **Invoice Number**: Unique invoice identifier
- **Supplier Name**: Company/vendor name
- **Service Description**: Description of services/products
- **Total Amount**: Total invoice amount (€)
- **VAT Amount**: VAT/tax amount (€)

## Installation

### Prerequisites

1. **Python 3.8 or higher**
   ```bash
   python --version
   ```

2. **Tesseract OCR** (for Tesseract engine)

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

### Setup

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

## Usage

### Starting the Application

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

1. **Upload an invoice image** (PNG, JPG, GIF, etc.)
2. **Configure processing options:**
   - ✅ Enable image preprocessing for better OCR accuracy
   - ✅ Enable AI extraction (if OpenAI API key is configured)
3. **Click "Process Invoice"** to extract data
4. **Review extracted data** in the form
5. **Edit any fields** if needed
6. **Click "Save Invoice"** to add to your collection

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

### Tesseract (Default)
- ✅ Free and open-source
- ✅ Good accuracy for printed text
- ✅ Supports Dutch and English
- ⚠️ Requires installation
- ⚠️ May struggle with handwriting or poor quality images

### EasyOCR
- ✅ No external dependencies
- ✅ Good accuracy
- ✅ Supports multiple languages
- ⚠️ Slower than Tesseract
- ⚠️ Larger memory footprint

### OpenAI Vision API
- ✅ Best accuracy, especially with complex layouts
- ✅ Handles handwriting better
- ✅ Intelligent data extraction
- ⚠️ Requires API key and internet connection
- ⚠️ Costs per API call

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
├── app.py                 # Main Streamlit application
├── config.py              # Configuration management
├── ocr_engine.py          # OCR processing
├── invoice_parser.py      # Data extraction and parsing
├── excel_exporter.py      # Excel file generation
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── uploads/              # Uploaded images (created automatically)
└── exports/              # Excel exports (created automatically)
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

**Version:** 1.0.0
**Company:** KERN1
**License:** Private Use

## Requirements

- Python 3.8+
- Streamlit 1.31+
- Tesseract OCR (for Tesseract engine)
- OpenAI API key (optional, for AI features)

---

**Built with Python, Streamlit, Tesseract, EasyOCR, and OpenAI**
