"""
PDF Handler - Converts PDF files to images for OCR processing
"""
from pathlib import Path
from typing import List, Optional
from PIL import Image
import tempfile


class PDFHandler:
    """Handles PDF to image conversion for OCR processing"""

    def __init__(self):
        """Initialize PDF handler"""
        pass

    def pdf_to_images(self, pdf_path: Path, dpi: int = 300) -> List[Image.Image]:
        """
        Convert PDF to list of PIL Images (one per page)

        Args:
            pdf_path: Path to PDF file
            dpi: Resolution for conversion (higher = better quality, slower)

        Returns:
            List of PIL Image objects, one per page
        """
        print(f"Converting PDF: {pdf_path}")
        print(f"PDF size: {pdf_path.stat().st_size / 1024:.1f} KB")

        try:
            # Try pypdfium2 first (faster, no system dependencies)
            print("Attempting conversion with pypdfium2...")
            return self._convert_with_pypdfium2(pdf_path, dpi)
        except Exception as e1:
            print(f"pypdfium2 conversion failed: {e1}")
            try:
                # Fallback to pdf2image (requires poppler)
                print("Attempting conversion with pdf2image...")
                return self._convert_with_pdf2image(pdf_path, dpi)
            except Exception as e2:
                print(f"pdf2image conversion failed: {e2}")
                raise RuntimeError(
                    f"Failed to convert PDF to images. "
                    f"Error 1 (pypdfium2): {str(e1)[:200]}\n"
                    f"Error 2 (pdf2image): {str(e2)[:200]}\n"
                    f"The PDF may be encrypted, corrupted, or in an unsupported format."
                )

    def _convert_with_pypdfium2(self, pdf_path: Path, dpi: int) -> List[Image.Image]:
        """Convert PDF using pypdfium2 (no system dependencies)"""
        import pypdfium2 as pdfium

        images = []
        pdf = None

        try:
            pdf = pdfium.PdfDocument(str(pdf_path))
            page_count = len(pdf)
            print(f"pypdfium2: PDF has {page_count} page(s)")

            for page_num in range(page_count):
                print(f"pypdfium2: Rendering page {page_num + 1}/{page_count}...")
                page = pdf[page_num]

                # Render page to PIL Image
                # Scale factor to achieve desired DPI (default PDF is 72 DPI)
                scale = dpi / 72.0
                pil_image = page.render(
                    scale=scale,
                    rotation=0,
                    crop=(0, 0, 0, 0)
                ).to_pil()

                images.append(pil_image)
                print(f"pypdfium2: Page {page_num + 1} rendered ({pil_image.size[0]}x{pil_image.size[1]})")
                page.close()

            return images
        except Exception as e:
            print(f"pypdfium2 error details: {type(e).__name__}: {str(e)}")
            raise
        finally:
            if pdf is not None:
                try:
                    pdf.close()
                except:
                    pass

    def _convert_with_pdf2image(self, pdf_path: Path, dpi: int) -> List[Image.Image]:
        """Convert PDF using pdf2image (requires poppler)"""
        from pdf2image import convert_from_path

        images = convert_from_path(
            str(pdf_path),
            dpi=dpi,
            fmt='png',
            thread_count=2
        )

        return images

    def extract_text_from_pdf(self, pdf_path: Path) -> Optional[str]:
        """
        Try to extract text directly from PDF (for text-based PDFs)

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text if available, None otherwise
        """
        print("Attempting direct text extraction from PDF...")

        try:
            import PyPDF2

            text = []
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)

                # Check if PDF is encrypted
                if pdf_reader.is_encrypted:
                    print("PDF is encrypted, attempting to decrypt...")
                    try:
                        pdf_reader.decrypt('')
                    except:
                        print("Could not decrypt PDF with empty password")
                        return None

                print(f"PDF has {len(pdf_reader.pages)} page(s)")

                for i, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text.append(page_text)
                            print(f"Page {i+1}: Extracted {len(page_text)} characters")
                        else:
                            print(f"Page {i+1}: No text found")
                    except Exception as e:
                        print(f"Page {i+1}: Extraction failed - {e}")
                        continue

            combined_text = '\n'.join(text).strip()

            # Only return if we got meaningful text
            if combined_text and len(combined_text) > 50:
                print(f"Total extracted text: {len(combined_text)} characters")
                return combined_text

            print("Not enough text extracted (< 50 characters)")
            return None
        except Exception as e:
            print(f"Direct PDF text extraction failed: {e}")
            import traceback
            traceback.print_exc()
            return None

    def is_text_based_pdf(self, pdf_path: Path) -> bool:
        """
        Check if PDF contains extractable text (vs scanned image)

        Args:
            pdf_path: Path to PDF file

        Returns:
            True if PDF has extractable text
        """
        text = self.extract_text_from_pdf(pdf_path)
        return text is not None and len(text) > 50

    def save_uploaded_pdf(self, uploaded_file, save_dir: Path) -> Path:
        """
        Save uploaded PDF file to temporary location

        Args:
            uploaded_file: Streamlit uploaded file object
            save_dir: Directory to save file

        Returns:
            Path to saved PDF file
        """
        save_dir.mkdir(exist_ok=True, parents=True)

        # Generate unique filename
        import time
        timestamp = int(time.time() * 1000)
        filename = f"invoice_{timestamp}.pdf"
        filepath = save_dir / filename

        # Save file
        with open(filepath, 'wb') as f:
            f.write(uploaded_file.getbuffer())

        return filepath

    def get_page_count(self, pdf_path: Path) -> int:
        """
        Get number of pages in PDF

        Args:
            pdf_path: Path to PDF file

        Returns:
            Number of pages
        """
        try:
            import pypdfium2 as pdfium
            pdf = pdfium.PdfDocument(str(pdf_path))
            count = len(pdf)
            pdf.close()
            return count
        except:
            try:
                import PyPDF2
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    return len(pdf_reader.pages)
            except:
                return 1  # Default to 1 page if can't determine
