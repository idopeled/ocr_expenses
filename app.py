"""
KERN1 Invoice OCR Application
Main Streamlit application for processing invoices and generating Excel exports
Enhanced with PDF support and multi-pass OCR
"""
import streamlit as st
from pathlib import Path
from PIL import Image
from datetime import datetime
from typing import List, Dict, Optional
import time

from config import Config
from ocr_engine import OCREngine
from invoice_parser import InvoiceParser
from excel_exporter import ExcelExporter
from pdf_handler import PDFHandler


class InvoiceOCRApp:
    """Main application class"""

    def __init__(self):
        """Initialize application"""
        Config.ensure_directories()
        self.ocr_engine = OCREngine()
        self.parser = InvoiceParser()
        self.exporter = ExcelExporter()
        self.pdf_handler = PDFHandler()

        # Initialize session state
        if 'invoices' not in st.session_state:
            st.session_state.invoices = []
        if 'current_invoice' not in st.session_state:
            st.session_state.current_invoice = None
        if 'ocr_text' not in st.session_state:
            st.session_state.ocr_text = ""
        if 'current_images' not in st.session_state:
            st.session_state.current_images = []

    def run(self):
        """Main application loop"""
        # Page config
        st.set_page_config(
            page_title=Config.APP_NAME,
            page_icon="📄",
            layout="wide"
        )

        # Header
        st.title(f"📄 {Config.APP_NAME}")
        st.markdown(f"**Company:** {Config.COMPANY_NAME}")
        st.markdown("---")

        # Sidebar
        self._render_sidebar()

        # Main content
        tab1, tab2, tab3 = st.tabs(["📤 Upload & Process", "📊 Invoices", "⚙️ Settings"])

        with tab1:
            self._render_upload_tab()

        with tab2:
            self._render_invoices_tab()

        with tab3:
            self._render_settings_tab()

    def _render_sidebar(self):
        """Render sidebar with statistics and actions"""
        st.sidebar.header("📈 Statistics")

        if st.session_state.invoices:
            total_invoices = len(st.session_state.invoices)
            total_amount = sum(
                float(inv.get('total_amount', 0) or 0)
                for inv in st.session_state.invoices
            )
            total_vat = sum(
                float(inv.get('vat_amount', 0) or 0)
                for inv in st.session_state.invoices
            )

            st.sidebar.metric("Total Invoices", total_invoices)
            st.sidebar.metric("Total Amount", f"€{total_amount:.2f}")
            st.sidebar.metric("Total VAT", f"€{total_vat:.2f}")
        else:
            st.sidebar.info("No invoices processed yet")

        st.sidebar.markdown("---")

        # Quick actions
        st.sidebar.header("🚀 Quick Actions")

        if st.sidebar.button("🗑️ Clear All Invoices", use_container_width=True):
            st.session_state.invoices = []
            st.session_state.current_invoice = None
            st.rerun()

        if st.session_state.invoices:
            if st.sidebar.button("💾 Export All to Excel", use_container_width=True):
                self._export_all_invoices()

    def _render_upload_tab(self):
        """Render upload and processing tab"""
        st.header("Upload Invoice Document")

        # File uploader with PDF support
        uploaded_file = st.file_uploader(
            "Choose an invoice (Image or PDF)",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'pdf'],
            help="Upload a scanned invoice image or PDF for OCR processing"
        )

        if uploaded_file:
            # Check file type
            file_ext = Path(uploaded_file.name).suffix.lower()
            is_pdf = file_ext == '.pdf'

            col1, col2 = st.columns([1, 1])

            with col1:
                st.subheader("📄 Document Preview" if is_pdf else "📷 Image Preview")

                if is_pdf:
                    # Handle PDF
                    self._handle_pdf_upload(uploaded_file, col1)
                else:
                    # Handle image
                    image = Image.open(uploaded_file)
                    st.session_state.current_images = [image]

                    st.image(image, use_container_width=True)

                    # Show image quality
                    quality = self.ocr_engine.get_image_quality_score(image)
                    quality_color = "green" if quality > 0.6 else "orange" if quality > 0.4 else "red"
                    st.markdown(f"**Image Quality:** :{quality_color}[{'■' * int(quality * 10)}] {quality:.1%}")

                # OCR options
                st.markdown("---")

                use_multipass = st.checkbox(
                    "🚀 Multi-pass OCR (best accuracy, slower)",
                    value=True,
                    help="Process the image multiple times with different techniques for best results"
                )

                use_ai = st.checkbox(
                    "🤖 Use AI extraction (requires OpenAI API key)",
                    value=Config.is_openai_available(),
                    disabled=not Config.is_openai_available()
                )

                if st.button("🔍 Process Invoice", type="primary", use_container_width=True):
                    if st.session_state.current_images:
                        self._process_invoice(
                            st.session_state.current_images,
                            multi_pass=use_multipass,
                            use_ai=use_ai
                        )

            with col2:
                st.subheader("📝 Extracted Data")

                if st.session_state.current_invoice:
                    self._render_invoice_form(editable=True)
                else:
                    st.info("👆 Click 'Process Invoice' to extract data")

    def _handle_pdf_upload(self, uploaded_file, container):
        """Handle PDF file upload and conversion"""
        try:
            # Save PDF temporarily
            pdf_path = self.pdf_handler.save_uploaded_pdf(uploaded_file, Config.UPLOAD_DIR)

            # Get page count
            page_count = self.pdf_handler.get_page_count(pdf_path)

            container.info(f"📄 PDF Document ({page_count} page{'s' if page_count != 1 else ''})")

            # Try to extract text directly first
            if self.pdf_handler.is_text_based_pdf(pdf_path):
                container.success("✅ This is a text-based PDF. Text can be extracted directly!")
                direct_text = self.pdf_handler.extract_text_from_pdf(pdf_path)
                if direct_text:
                    st.session_state.ocr_text = direct_text
                    st.session_state.current_images = []  # No need for images
            else:
                container.info("Converting PDF to images for OCR...")

                # Convert PDF to images
                with st.spinner("Converting PDF pages to images..."):
                    images = self.pdf_handler.pdf_to_images(pdf_path, dpi=300)
                    st.session_state.current_images = images

                container.success(f"✅ Converted {len(images)} page(s) to images")

                # Show first page preview
                if images:
                    container.markdown("**Page 1 Preview:**")
                    container.image(images[0], use_container_width=True)

                    if len(images) > 1:
                        container.info(f"Will process all {len(images)} pages")

        except Exception as e:
            container.error(f"❌ Error processing PDF: {str(e)}")
            st.session_state.current_images = []

    def _render_invoices_tab(self):
        """Render invoices list tab"""
        st.header("Processed Invoices")

        if not st.session_state.invoices:
            st.info("No invoices have been processed yet. Upload an invoice in the 'Upload & Process' tab.")
            return

        # Export options
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"**Total: {len(st.session_state.invoices)} invoices**")
        with col2:
            if st.button("💾 Export to Excel", use_container_width=True):
                self._export_all_invoices()
        with col3:
            if st.button("🗑️ Clear All", use_container_width=True):
                st.session_state.invoices = []
                st.rerun()

        st.markdown("---")

        # Display invoices in a table-like format
        for idx, invoice in enumerate(st.session_state.invoices):
            with st.expander(
                f"🧾 {invoice.get('supplier_name', 'Unknown')} - "
                f"€{invoice.get('total_amount', '0.00')} - "
                f"{invoice.get('invoice_date', 'No date')}",
                expanded=False
            ):
                col1, col2 = st.columns([3, 1])

                with col1:
                    self._display_invoice_details(invoice)

                with col2:
                    st.markdown("**Actions**")
                    if st.button("🗑️ Delete", key=f"delete_{idx}", use_container_width=True):
                        st.session_state.invoices.pop(idx)
                        st.rerun()

    def _render_settings_tab(self):
        """Render settings tab"""
        st.header("⚙️ Settings")

        # OCR Engine settings
        st.subheader("OCR Engine")
        ocr_options = ['tesseract', 'easyocr']
        if Config.is_openai_available():
            ocr_options.append('openai')

        selected_engine = st.selectbox(
            "OCR Engine",
            ocr_options,
            index=ocr_options.index(Config.OCR_ENGINE),
            help="Choose the OCR engine for text extraction"
        )

        if selected_engine != Config.OCR_ENGINE:
            Config.OCR_ENGINE = selected_engine
            self.ocr_engine = OCREngine(selected_engine)
            st.success(f"OCR engine changed to: {selected_engine}")

        # Engine descriptions
        st.markdown("""
        **Engine Comparison:**
        - **Tesseract**: Fast, good for standard printed invoices
        - **EasyOCR**: Better accuracy, works well with various layouts
        - **OpenAI**: Best accuracy (requires API key and costs money)
        """)

        # Language settings
        st.subheader("Languages")
        st.info("Supported languages: English (eng), Dutch (nld)")
        st.code(f"Current languages: {', '.join(Config.OCR_LANGUAGES)}")

        # OpenAI settings
        st.subheader("OpenAI Integration")

        # Show current status
        if Config.is_openai_available():
            st.success("✅ OpenAI API key is configured")
            st.info("AI-powered extraction is available for improved accuracy")

            # Option to remove/change key
            if st.button("🔄 Change API Key"):
                Config.OPENAI_API_KEY = None
                st.rerun()
        else:
            st.warning("⚠️ OpenAI API key not configured")
            st.info("Enter your OpenAI API key below to enable AI-powered extraction")

        # API Key input form
        with st.form("openai_config"):
            st.markdown("**Configure OpenAI API Key**")

            api_key = st.text_input(
                "OpenAI API Key",
                type="password",
                placeholder="sk-...",
                help="Get your API key from https://platform.openai.com/api-keys"
            )

            col1, col2 = st.columns([1, 3])
            with col1:
                submitted = st.form_submit_button("💾 Save Key")
            with col2:
                if Config.is_openai_available():
                    if st.form_submit_button("🗑️ Remove Key"):
                        self._remove_openai_key()

            if submitted and api_key:
                if api_key.startswith('sk-'):
                    # Save to .env file
                    self._save_openai_key(api_key)
                    st.success("✅ OpenAI API key saved! Reloading...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid API key format. OpenAI keys start with 'sk-'")

        # Instructions
        with st.expander("How to get an OpenAI API key"):
            st.markdown("""
            1. Go to https://platform.openai.com/signup
            2. Sign up or log in
            3. Navigate to API Keys: https://platform.openai.com/api-keys
            4. Click "Create new secret key"
            5. Copy the key (starts with 'sk-')
            6. Paste it in the field above and click Save

            **Note:** You'll need to add billing information to use the API.
            Costs are typically $0.01-0.02 per invoice.
            """)

        # Performance settings
        st.subheader("Performance Settings")
        st.markdown("""
        **Multi-pass OCR** processes the image 4 times with different preprocessing:
        1. Original image
        2. Enhanced contrast and sharpness
        3. Advanced denoising and binarization
        4. Sharpened version

        The longest (most complete) result is used. This significantly improves accuracy
        but takes longer to process.
        """)

        # Directories
        st.subheader("Directories")
        st.text(f"Uploads: {Config.UPLOAD_DIR}")
        st.text(f"Exports: {Config.EXPORT_DIR}")

        # About
        st.markdown("---")
        st.subheader("About")
        st.markdown(f"""
        **{Config.APP_NAME}**

        Version: 2.0.0

        Features:
        - Multi-language OCR (Dutch/English)
        - Multi-pass extraction for supercharged accuracy
        - PDF support (text-based and image-based)
        - AI-powered data extraction (optional)
        - Excel export with professional formatting
        - Support for PNG, JPG, GIF, BMP, TIFF, PDF formats
        - Advanced image preprocessing (denoising, deskewing, CLAHE)

        Built with Python, Streamlit, and Tesseract/EasyOCR
        """)

    def _process_invoice(
        self,
        images: List[Image.Image],
        multi_pass: bool = True,
        use_ai: bool = False
    ):
        """Process invoice images or text"""
        with st.spinner("🔍 Processing invoice..."):
            try:
                all_text = []

                # Check if we already have extracted text (from text-based PDF)
                if st.session_state.ocr_text and not images:
                    text = st.session_state.ocr_text
                else:
                    # Process each image
                    for idx, image in enumerate(images):
                        if len(images) > 1:
                            st.info(f"Processing page {idx + 1}/{len(images)}...")

                        # Extract text with OCR
                        page_text = self.ocr_engine.extract_text(image, multi_pass=multi_pass)
                        all_text.append(page_text)

                    # Combine text from all pages
                    text = '\n\n--- PAGE BREAK ---\n\n'.join(all_text)
                    st.session_state.ocr_text = text

                # Parse invoice data
                st.info("Parsing invoice data...")
                invoice_data = self.parser.parse(text, use_ai=use_ai)

                # Validate
                errors = self.parser.validate_data(invoice_data)
                if errors:
                    st.warning(f"Validation warnings: {', '.join(errors.keys())}")

                # Store in session state
                st.session_state.current_invoice = invoice_data

                st.success("✅ Invoice processed successfully!")

            except Exception as e:
                st.error(f"❌ Error processing invoice: {str(e)}")
                import traceback
                st.error(traceback.format_exc())

    def _render_invoice_form(self, editable: bool = True):
        """Render invoice data form"""
        if not st.session_state.current_invoice:
            return

        invoice = st.session_state.current_invoice

        # Show OCR text in expander
        if st.session_state.ocr_text:
            with st.expander("📄 View OCR Text", expanded=False):
                st.text_area("Raw OCR Output", st.session_state.ocr_text, height=150, disabled=True)

        # Editable form
        st.markdown("### Invoice Details")

        invoice['invoice_date'] = st.text_input(
            "Invoice Date (YYYY-MM-DD)",
            value=invoice.get('invoice_date', ''),
            disabled=not editable
        )

        invoice['invoice_number'] = st.text_input(
            "Invoice Number",
            value=invoice.get('invoice_number', ''),
            disabled=not editable
        )

        invoice['supplier_name'] = st.text_input(
            "Supplier Name",
            value=invoice.get('supplier_name', ''),
            disabled=not editable
        )

        invoice['service_description'] = st.text_area(
            "Service Description",
            value=invoice.get('service_description', ''),
            height=100,
            disabled=not editable
        )

        col1, col2 = st.columns(2)
        with col1:
            invoice['total_amount'] = st.text_input(
                "Total Amount (€)",
                value=invoice.get('total_amount', ''),
                disabled=not editable
            )
        with col2:
            invoice['vat_amount'] = st.text_input(
                "VAT Amount (€)",
                value=invoice.get('vat_amount', ''),
                disabled=not editable
            )

        # Update session state
        st.session_state.current_invoice = invoice

        # Actions
        if editable:
            st.markdown("---")
            col1, col2 = st.columns(2)

            with col1:
                if st.button("💾 Save Invoice", type="primary", use_container_width=True):
                    self._save_current_invoice()

            with col2:
                if st.button("🗑️ Discard", use_container_width=True):
                    st.session_state.current_invoice = None
                    st.session_state.ocr_text = ""
                    st.session_state.current_images = []
                    st.rerun()

    def _display_invoice_details(self, invoice: Dict):
        """Display invoice details in read-only format"""
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Invoice Number:** {invoice.get('invoice_number', 'N/A')}")
            st.markdown(f"**Date:** {invoice.get('invoice_date', 'N/A')}")
            st.markdown(f"**Supplier:** {invoice.get('supplier_name', 'N/A')}")

        with col2:
            st.markdown(f"**Total Amount:** €{invoice.get('total_amount', '0.00')}")
            st.markdown(f"**VAT Amount:** €{invoice.get('vat_amount', '0.00')}")

        st.markdown(f"**Service:** {invoice.get('service_description', 'N/A')}")

    def _save_current_invoice(self):
        """Save current invoice to list"""
        if st.session_state.current_invoice:
            # Validate required fields
            invoice = st.session_state.current_invoice
            required_fields = ['invoice_number', 'supplier_name', 'total_amount']
            missing_fields = [f for f in required_fields if not invoice.get(f)]

            if missing_fields:
                st.error(f"❌ Missing required fields: {', '.join(missing_fields)}")
                return

            # Add to list
            st.session_state.invoices.append(invoice.copy())

            # Clear current
            st.session_state.current_invoice = None
            st.session_state.ocr_text = ""
            st.session_state.current_images = []

            st.success("✅ Invoice saved!")
            st.rerun()

    def _export_all_invoices(self):
        """Export all invoices to Excel"""
        if not st.session_state.invoices:
            st.warning("No invoices to export")
            return

        try:
            with st.spinner("📊 Creating Excel file..."):
                filepath = self.exporter.export_invoices(st.session_state.invoices)

            st.success(f"✅ Excel file created: {filepath.name}")

            # Offer download
            with open(filepath, 'rb') as f:
                st.download_button(
                    label="⬇️ Download Excel File",
                    data=f,
                    file_name=filepath.name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            # Show summary
            summary = self.exporter.create_summary(st.session_state.invoices)
            st.markdown("### 📊 Export Summary")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Invoices", summary['total_invoices'])
            with col2:
                st.metric("Total Amount", f"€{summary['total_amount']:.2f}")
            with col3:
                st.metric("Total VAT", f"€{summary['total_vat']:.2f}")

        except Exception as e:
            st.error(f"❌ Export failed: {str(e)}")

    def _save_openai_key(self, api_key: str):
        """Save OpenAI API key to .env file"""
        env_file = Config.BASE_DIR / ".env"

        # Read existing .env content
        existing_lines = []
        if env_file.exists():
            with open(env_file, 'r') as f:
                existing_lines = f.readlines()

        # Update or add OPENAI_API_KEY
        key_found = False
        new_lines = []
        for line in existing_lines:
            if line.startswith('OPENAI_API_KEY='):
                new_lines.append(f'OPENAI_API_KEY={api_key}\n')
                key_found = True
            else:
                new_lines.append(line)

        if not key_found:
            new_lines.append(f'OPENAI_API_KEY={api_key}\n')

        # Write back to file
        with open(env_file, 'w') as f:
            f.writelines(new_lines)

        # Update config
        Config.OPENAI_API_KEY = api_key

    def _remove_openai_key(self):
        """Remove OpenAI API key from .env file"""
        env_file = Config.BASE_DIR / ".env"

        if env_file.exists():
            # Read existing content
            with open(env_file, 'r') as f:
                lines = f.readlines()

            # Remove OPENAI_API_KEY line
            new_lines = [line for line in lines if not line.startswith('OPENAI_API_KEY=')]

            # Write back
            with open(env_file, 'w') as f:
                f.writelines(new_lines)

        # Update config
        Config.OPENAI_API_KEY = None
        st.success("✅ OpenAI API key removed")
        st.rerun()


def main():
    """Main entry point"""
    app = InvoiceOCRApp()
    app.run()


if __name__ == "__main__":
    main()
