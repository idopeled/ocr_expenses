"""
OCR Engine for extracting text from invoice images
Supports multiple OCR backends: Tesseract, EasyOCR, and OpenAI Vision
"""
import base64
from io import BytesIO
from typing import Optional
from PIL import Image
import numpy as np

from config import Config


class OCREngine:
    """Handles OCR operations with multiple backend support"""

    def __init__(self, engine: str = None):
        """
        Initialize OCR engine

        Args:
            engine: OCR engine to use ('tesseract', 'easyocr', 'openai')
        """
        self.engine = engine or Config.OCR_ENGINE
        self.languages = Config.OCR_LANGUAGES
        self._ocr_reader = None

    def extract_text(self, image: Image.Image) -> str:
        """
        Extract text from image using configured OCR engine

        Args:
            image: PIL Image object

        Returns:
            Extracted text as string
        """
        if self.engine == "tesseract":
            return self._extract_with_tesseract(image)
        elif self.engine == "easyocr":
            return self._extract_with_easyocr(image)
        elif self.engine == "openai":
            return self._extract_with_openai(image)
        else:
            raise ValueError(f"Unsupported OCR engine: {self.engine}")

    def _extract_with_tesseract(self, image: Image.Image) -> str:
        """Extract text using Tesseract OCR"""
        try:
            import pytesseract

            # Configure language
            lang_param = '+'.join(self.languages)

            # Perform OCR
            text = pytesseract.image_to_string(image, lang=lang_param)
            return text.strip()
        except Exception as e:
            raise RuntimeError(f"Tesseract OCR failed: {str(e)}")

    def _extract_with_easyocr(self, image: Image.Image) -> str:
        """Extract text using EasyOCR"""
        try:
            import easyocr

            # Initialize reader (cached)
            if self._ocr_reader is None:
                self._ocr_reader = easyocr.Reader(self.languages, gpu=False)

            # Convert PIL image to numpy array
            img_array = np.array(image)

            # Perform OCR
            results = self._ocr_reader.readtext(img_array)

            # Extract text from results
            text = ' '.join([result[1] for result in results])
            return text.strip()
        except Exception as e:
            raise RuntimeError(f"EasyOCR failed: {str(e)}")

    def _extract_with_openai(self, image: Image.Image) -> str:
        """Extract text using OpenAI Vision API"""
        try:
            from openai import OpenAI

            if not Config.is_openai_available():
                raise ValueError("OpenAI API key not configured")

            client = OpenAI(api_key=Config.OPENAI_API_KEY)

            # Convert image to base64
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()

            # Call OpenAI Vision API
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Extract all text from this invoice image. Return the raw text exactly as it appears."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{img_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=2000
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"OpenAI Vision API failed: {str(e)}")

    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for better OCR results

        Args:
            image: Input PIL Image

        Returns:
            Preprocessed PIL Image
        """
        try:
            import cv2

            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Convert to numpy array
            img_array = np.array(image)

            # Convert to grayscale
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

            # Apply thresholding to make text clearer
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Convert back to PIL Image
            return Image.fromarray(thresh)
        except Exception as e:
            # If preprocessing fails, return original
            print(f"Image preprocessing failed: {e}")
            return image
