"""
Configuration management for KERN1 Invoice OCR Application
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""

    # Application settings
    APP_NAME = "KERN1 Invoice OCR"
    COMPANY_NAME = "KERN1"

    # Directories
    BASE_DIR = Path(__file__).parent
    UPLOAD_DIR = BASE_DIR / "uploads"
    EXPORT_DIR = BASE_DIR / "exports"

    # OCR settings
    OCR_ENGINE = os.getenv("OCR_ENGINE", "tesseract")
    OCR_LANGUAGES = os.getenv("OCR_LANGUAGES", "eng,nld").split(",")

    # OpenAI settings (optional)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Supported image formats
    SUPPORTED_IMAGE_FORMATS = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff"]

    # Supported document formats
    SUPPORTED_PDF_FORMATS = [".pdf"]

    # All supported formats
    SUPPORTED_FORMATS = SUPPORTED_IMAGE_FORMATS + SUPPORTED_PDF_FORMATS

    # Invoice fields
    INVOICE_FIELDS = [
        "invoice_date",
        "invoice_number",
        "service_description",
        "supplier_name",
        "total_amount",
        "vat_amount"
    ]

    # Excel column headers
    EXCEL_HEADERS = {
        "invoice_date": "Invoice Date",
        "invoice_number": "Invoice Number",
        "service_description": "Service Description",
        "supplier_name": "Supplier Name",
        "total_amount": "Total Amount (€)",
        "vat_amount": "VAT Amount (€)"
    }

    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        cls.UPLOAD_DIR.mkdir(exist_ok=True)
        cls.EXPORT_DIR.mkdir(exist_ok=True)

    @classmethod
    def is_openai_available(cls):
        """Check if OpenAI API key is configured"""
        return cls.OPENAI_API_KEY and cls.OPENAI_API_KEY != "your_openai_api_key_here"
