"""
KERN1 Invoice OCR Application
Main Streamlit application for processing invoices and generating Excel exports
"""
import streamlit as st
from pathlib import Path
from PIL import Image
from datetime import datetime
from typing import List, Dict, Optional

from config import Config
from ocr_engine import OCREngine
from invoice_parser import InvoiceParser
from excel_exporter import ExcelExporter


class InvoiceOCRApp:
    """Main application class"""

    def __init__(self):
        """Initialize application"""
        Config.ensure_directories()
        self.ocr_engine = OCREngine()
        self.parser = InvoiceParser()
        self.exporter = ExcelExporter()

        # Initialize session state
        if 'invoices' not in st.session_state:
            st.session_state.invoices = []
        if 'current_invoice' not in st.session_state:
            st.session_state.current_invoice = None
        if 'ocr_text' not in st.session_state:
            st.session_state.ocr_text = ""

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
        st.header("Upload Invoice Image")

        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an invoice image (PNG, JPG, GIF)",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'],
            help="Upload a scanned invoice image for OCR processing"
        )

        if uploaded_file:
            col1, col2 = st.columns([1, 1])

            with col1:
                st.subheader("📷 Image Preview")
                image = Image.open(uploaded_file)
                st.image(image, use_container_width=True)

                # OCR options
                st.markdown("---")
                use_preprocessing = st.checkbox(
                    "🔧 Preprocess image (improve OCR accuracy)",
                    value=True
                )
                use_ai = st.checkbox(
                    "🤖 Use AI extraction (requires OpenAI API key)",
                    value=Config.is_openai_available(),
                    disabled=not Config.is_openai_available()
                )

                if st.button("🔍 Process Invoice", type="primary", use_container_width=True):
                    self._process_invoice(image, use_preprocessing, use_ai)

            with col2:
                st.subheader("📝 Extracted Data")

                if st.session_state.current_invoice:
                    self._render_invoice_form(editable=True)
                else:
                    st.info("👆 Click 'Process Invoice' to extract data")

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

        # Language settings
        st.subheader("Languages")
        st.info("Supported languages: English (eng), Dutch (nld)")
        st.code(f"Current languages: {', '.join(Config.OCR_LANGUAGES)}")

        # OpenAI settings
        st.subheader("OpenAI Integration")
        if Config.is_openai_available():
            st.success("✅ OpenAI API key is configured")
            st.info("AI-powered extraction is available for improved accuracy")
        else:
            st.warning("⚠️ OpenAI API key not configured")
            st.info("Add OPENAI_API_KEY to .env file to enable AI-powered extraction")

        # Directories
        st.subheader("Directories")
        st.text(f"Uploads: {Config.UPLOAD_DIR}")
        st.text(f"Exports: {Config.EXPORT_DIR}")

        # About
        st.markdown("---")
        st.subheader("About")
        st.markdown(f"""
        **{Config.APP_NAME}**

        Version: 1.0.0

        Features:
        - Multi-language OCR (Dutch/English)
        - AI-powered data extraction
        - Excel export with professional formatting
        - Support for PNG, JPG, GIF, BMP, TIFF formats

        Built with Python, Streamlit, and Tesseract/EasyOCR
        """)

    def _process_invoice(self, image: Image.Image, preprocess: bool, use_ai: bool):
        """Process invoice image"""
        with st.spinner("🔍 Processing invoice..."):
            try:
                # Step 1: Preprocess if requested
                if preprocess:
                    st.info("Preprocessing image...")
                    image = self.ocr_engine.preprocess_image(image)

                # Step 2: Extract text with OCR
                st.info(f"Extracting text with {self.ocr_engine.engine}...")
                text = self.ocr_engine.extract_text(image)
                st.session_state.ocr_text = text

                # Step 3: Parse invoice data
                st.info("Parsing invoice data...")
                invoice_data = self.parser.parse(text, use_ai=use_ai)

                # Step 4: Validate
                errors = self.parser.validate_data(invoice_data)
                if errors:
                    st.warning(f"Validation warnings: {', '.join(errors.keys())}")

                # Store in session state
                st.session_state.current_invoice = invoice_data

                st.success("✅ Invoice processed successfully!")

            except Exception as e:
                st.error(f"❌ Error processing invoice: {str(e)}")

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


def main():
    """Main entry point"""
    app = InvoiceOCRApp()
    app.run()


if __name__ == "__main__":
    main()
