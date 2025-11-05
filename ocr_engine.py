"""
OCR Engine for extracting text from invoice images
Supports multiple OCR backends: Tesseract, EasyOCR, and OpenAI Vision
Enhanced with advanced preprocessing and multi-pass extraction
"""
import base64
from io import BytesIO
from typing import Optional, List, Tuple
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import cv2

from config import Config


class OCREngine:
    """Handles OCR operations with multiple backend support and advanced preprocessing"""

    def __init__(self, engine: str = None):
        """
        Initialize OCR engine

        Args:
            engine: OCR engine to use ('tesseract', 'easyocr', 'openai')
        """
        self.engine = engine or Config.OCR_ENGINE
        self.languages = Config.OCR_LANGUAGES
        self._ocr_reader = None

    def extract_text(self, image: Image.Image, multi_pass: bool = True) -> str:
        """
        Extract text from image using configured OCR engine with multi-pass for best results

        Args:
            image: PIL Image object
            multi_pass: Use multiple preprocessing techniques and combine results

        Returns:
            Extracted text as string
        """
        if self.engine == "openai":
            # OpenAI doesn't benefit from multi-pass
            return self._extract_with_openai(image)

        if multi_pass:
            return self._multi_pass_extraction(image)
        else:
            if self.engine == "tesseract":
                return self._extract_with_tesseract(image)
            elif self.engine == "easyocr":
                return self._extract_with_easyocr(image)
            else:
                raise ValueError(f"Unsupported OCR engine: {self.engine}")

    def _multi_pass_extraction(self, image: Image.Image) -> str:
        """
        Perform multiple OCR passes with different preprocessing and combine results

        Args:
            image: PIL Image object

        Returns:
            Combined text from all passes
        """
        results = []

        # Pass 1: Original image
        try:
            text = self._extract_single_pass(image)
            if text and len(text) > 10:
                results.append(text)
        except:
            pass

        # Pass 2: Enhanced contrast
        try:
            enhanced = self._enhance_contrast(image)
            text = self._extract_single_pass(enhanced)
            if text and len(text) > 10:
                results.append(text)
        except:
            pass

        # Pass 3: Advanced preprocessing (binarization + denoising)
        try:
            processed = self._advanced_preprocess(image)
            text = self._extract_single_pass(processed)
            if text and len(text) > 10:
                results.append(text)
        except:
            pass

        # Pass 4: Sharpened image
        try:
            sharpened = self._sharpen_image(image)
            text = self._extract_single_pass(sharpened)
            if text and len(text) > 10:
                results.append(text)
        except:
            pass

        # Combine results - take the longest one as it likely has the most text
        if results:
            return max(results, key=len)
        else:
            # Fallback to basic extraction
            return self._extract_single_pass(image)

    def _extract_single_pass(self, image: Image.Image) -> str:
        """Extract text in a single pass"""
        if self.engine == "tesseract":
            return self._extract_with_tesseract(image)
        elif self.engine == "easyocr":
            return self._extract_with_easyocr(image)
        else:
            raise ValueError(f"Unsupported OCR engine: {self.engine}")

    def _extract_with_tesseract(self, image: Image.Image) -> str:
        """Extract text using Tesseract OCR with optimized config"""
        try:
            import pytesseract

            # Configure language
            lang_param = '+'.join(self.languages)

            # Optimized Tesseract config for invoices
            custom_config = r'--oem 3 --psm 6'

            # Perform OCR
            text = pytesseract.image_to_string(
                image,
                lang=lang_param,
                config=custom_config
            )
            return text.strip()
        except Exception as e:
            raise RuntimeError(f"Tesseract OCR failed: {str(e)}")

    def _extract_with_easyocr(self, image: Image.Image) -> str:
        """Extract text using EasyOCR with optimized settings"""
        try:
            import easyocr

            # Initialize reader (cached)
            if self._ocr_reader is None:
                self._ocr_reader = easyocr.Reader(
                    self.languages,
                    gpu=False,
                    verbose=False
                )

            # Convert PIL image to numpy array
            img_array = np.array(image)

            # Perform OCR with detailed results
            results = self._ocr_reader.readtext(
                img_array,
                detail=1,
                paragraph=False,
                min_size=10,
                contrast_ths=0.1,
                adjust_contrast=0.5
            )

            # Extract text with newlines preserved based on y-coordinates
            if not results:
                return ""

            # Sort by y-coordinate (top to bottom), then x-coordinate (left to right)
            results_sorted = sorted(results, key=lambda x: (x[0][0][1], x[0][0][0]))

            # Combine text with proper line breaks
            lines = []
            current_line = []
            last_y = None

            for bbox, text, conf in results_sorted:
                y_coord = bbox[0][1]

                # Start new line if y-coordinate differs significantly
                if last_y is not None and abs(y_coord - last_y) > 10:
                    if current_line:
                        lines.append(' '.join(current_line))
                        current_line = []

                current_line.append(text)
                last_y = y_coord

            # Add last line
            if current_line:
                lines.append(' '.join(current_line))

            return '\n'.join(lines)
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
        Basic preprocessing for better OCR results

        Args:
            image: Input PIL Image

        Returns:
            Preprocessed PIL Image
        """
        return self._advanced_preprocess(image)

    def _enhance_contrast(self, image: Image.Image) -> Image.Image:
        """Enhance image contrast"""
        try:
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            enhanced = enhancer.enhance(2.0)

            # Enhance sharpness
            sharpness_enhancer = ImageEnhance.Sharpness(enhanced)
            enhanced = sharpness_enhancer.enhance(1.5)

            return enhanced
        except Exception as e:
            print(f"Contrast enhancement failed: {e}")
            return image

    def _sharpen_image(self, image: Image.Image) -> Image.Image:
        """Sharpen image for better text clarity"""
        try:
            # Convert to RGB
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Apply unsharp mask
            return image.filter(ImageFilter.SHARPEN)
        except Exception as e:
            print(f"Sharpening failed: {e}")
            return image

    def _advanced_preprocess(self, image: Image.Image) -> Image.Image:
        """
        Advanced preprocessing with multiple techniques

        Args:
            image: Input PIL Image

        Returns:
            Preprocessed PIL Image
        """
        try:
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Convert to numpy array
            img_array = np.array(image)

            # Resize if too small (upscale for better OCR)
            height, width = img_array.shape[:2]
            if height < 1000 or width < 1000:
                scale = max(1000 / height, 1000 / width)
                new_width = int(width * scale)
                new_height = int(height * scale)
                img_array = cv2.resize(img_array, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

            # Convert to grayscale
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

            # Denoise
            denoised = cv2.fastNlMeansDenoising(gray, None, h=10, templateWindowSize=7, searchWindowSize=21)

            # Increase contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            contrast = clahe.apply(denoised)

            # Apply adaptive thresholding
            binary = cv2.adaptiveThreshold(
                contrast,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11,
                2
            )

            # Morphological operations to remove noise
            kernel = np.ones((1, 1), np.uint8)
            morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

            # Deskew if needed
            morph = self._deskew(morph)

            # Convert back to PIL Image
            return Image.fromarray(morph)
        except Exception as e:
            # If preprocessing fails, return original
            print(f"Advanced preprocessing failed: {e}")
            return image

    def _deskew(self, image: np.ndarray) -> np.ndarray:
        """
        Deskew image to correct rotation

        Args:
            image: Input image as numpy array

        Returns:
            Deskewed image as numpy array
        """
        try:
            # Find all white pixels
            coords = np.column_stack(np.where(image > 0))

            if len(coords) < 100:
                return image

            # Find minimum area rectangle
            angle = cv2.minAreaRect(coords)[-1]

            # Correct angle
            if angle < -45:
                angle = -(90 + angle)
            else:
                angle = -angle

            # Only correct if angle is significant
            if abs(angle) < 0.5:
                return image

            # Rotate image
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(
                image,
                M,
                (w, h),
                flags=cv2.INTER_CUBIC,
                borderMode=cv2.BORDER_REPLICATE
            )

            return rotated
        except Exception as e:
            print(f"Deskewing failed: {e}")
            return image

    def get_image_quality_score(self, image: Image.Image) -> float:
        """
        Estimate image quality for OCR (0-1, higher is better)

        Args:
            image: PIL Image

        Returns:
            Quality score between 0 and 1
        """
        try:
            img_array = np.array(image.convert('L'))

            # Check resolution
            height, width = img_array.shape
            resolution_score = min(1.0, (height * width) / (1000 * 1000))

            # Check contrast
            contrast_score = img_array.std() / 128.0
            contrast_score = min(1.0, contrast_score)

            # Check sharpness using Laplacian variance
            laplacian = cv2.Laplacian(img_array, cv2.CV_64F)
            sharpness_score = min(1.0, laplacian.var() / 1000.0)

            # Combined score
            quality = (resolution_score * 0.3 + contrast_score * 0.4 + sharpness_score * 0.3)

            return quality
        except Exception as e:
            print(f"Quality estimation failed: {e}")
            return 0.5
