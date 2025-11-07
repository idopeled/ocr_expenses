"""
Invoice Parser - Extracts structured data from OCR text
Uses pattern matching and optionally AI for intelligent extraction
"""
import re
from datetime import datetime
from typing import Dict, Optional
from dateutil import parser as date_parser

from config import Config


class InvoiceParser:
    """Parses invoice text to extract structured data"""

    def __init__(self):
        """Initialize parser with patterns"""
        # Patterns for invoice number
        self.invoice_patterns = [
            r'invoice\s*(?:#|no\.?|number|nr\.?)?\s*:?\s*([A-Z0-9\-\/\s]+)',
            r'factuurnummer\s*:?\s*([A-Z0-9\-\/\s]+)',
            r'factuur\s*(?:#|no\.?|nr\.?)?\s*:?\s*([A-Z0-9\-\/\s]+)',
            r'(?:^|\s)INV[-\s]?([A-Z0-9\-\/\s]+)',
        ]

        # Patterns for dates
        self.date_patterns = [
            r'date\s*(?:of\s*issue)?\s*:?\s*(\w+\s+\d{1,2}\s*,?\s*\d{4})',  # "April 9, 2025"
            r'invoice\s*date\s*:?\s*(\w+\s+\d{1,2}\s*,?\s*\d{4})',
            r'date\s*:?\s*(\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4})',
            r'datum\s*:?\s*(\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4})',
            r'invoice\s*date\s*:?\s*(\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4})',
            r'(\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4})',
        ]

        # Patterns for amounts
        self.total_patterns = [
            r'total\s*(?:amount)?\s*:?\s*€?\s*(\d+[.,]\d{2})',
            r'totaal\s*(?:bedrag)?\s*:?\s*€?\s*(\d+[.,]\d{2})',
            r'grand\s*total\s*:?\s*€?\s*(\d+[.,]\d{2})',
            r'amount\s*due\s*:?\s*€?\s*(\d+[.,]\d{2})',
        ]

        self.vat_patterns = [
            r'vat\s*(?:amount)?\s*:?\s*€?\s*(\d+[.,]\d{2})',
            r'btw\s*(?:bedrag)?\s*:?\s*€?\s*(\d+[.,]\d{2})',
            r'tax\s*(?:amount)?\s*:?\s*€?\s*(\d+[.,]\d{2})',
        ]

    def _normalize_spaced_text(self, text: str) -> str:
        """
        Normalize text that has excessive spaces between characters.
        Some PDFs extract with spaces like "I n v o i c e" instead of "Invoice".
        """
        lines = text.split('\n')
        normalized_lines = []

        for line in lines:
            words = line.split()
            merged = []
            buffer = []

            for word in words:
                # Check if word is a single character (letter, digit, or common punctuation)
                if len(word) == 1:
                    buffer.append(word)
                else:
                    # Multi-character word found
                    # If we have accumulated 3+ single chars, merge them into one word
                    if len(buffer) >= 3:
                        merged.append(''.join(buffer))
                    elif buffer:
                        # Short sequence (1-2 chars), keep with spaces
                        merged.extend(buffer)
                    buffer = []
                    merged.append(word)

            # Handle remaining buffer at end of line
            if len(buffer) >= 3:
                merged.append(''.join(buffer))
            elif buffer:
                merged.extend(buffer)

            normalized_lines.append(' '.join(merged))

        return '\n'.join(normalized_lines)

    def parse(self, text: str, use_ai: bool = False) -> Dict[str, Optional[str]]:
        """
        Parse invoice text to extract structured data

        Args:
            text: OCR-extracted text
            use_ai: Whether to use AI for extraction (if available)

        Returns:
            Dictionary with extracted invoice fields
        """
        if use_ai:
            # Try Claude first (better for structured data), then OpenAI
            if Config.is_anthropic_available():
                return self._parse_with_claude(text)
            elif Config.is_openai_available():
                return self._parse_with_openai(text)

        return self._parse_with_patterns(text)

    def _parse_with_patterns(self, text: str) -> Dict[str, Optional[str]]:
        """Extract invoice data using regex patterns"""
        # Normalize text by removing excessive spaces between characters
        # This fixes PDFs that have spaces like "I n v o i c e" instead of "Invoice"
        text = self._normalize_spaced_text(text)

        # Case-insensitive text for pattern matching
        text_lower = text.lower()

        result = {
            "invoice_number": self._extract_invoice_number(text, text_lower),
            "invoice_date": self._extract_date(text, text_lower),
            "supplier_name": self._extract_supplier_name(text),
            "service_description": self._extract_service_description(text),
            "total_amount": self._extract_total_amount(text, text_lower),
            "vat_amount": self._extract_vat_amount(text, text_lower),
        }

        return result

    def _parse_with_openai(self, text: str) -> Dict[str, Optional[str]]:
        """Extract invoice data using OpenAI"""
        try:
            from openai import OpenAI

            client = OpenAI(api_key=Config.OPENAI_API_KEY)

            prompt = f"""
Extract the following information from this invoice text:
1. Invoice number
2. Invoice date (format as YYYY-MM-DD)
3. Supplier/Company name
4. Service description (brief summary of what was invoiced)
5. Total amount (number only, without currency symbol)
6. VAT amount (number only, without currency symbol)

Invoice text:
{text}

Return the information in this exact format:
INVOICE_NUMBER: <value or UNKNOWN>
INVOICE_DATE: <value or UNKNOWN>
SUPPLIER_NAME: <value or UNKNOWN>
SERVICE_DESCRIPTION: <value or UNKNOWN>
TOTAL_AMOUNT: <value or UNKNOWN>
VAT_AMOUNT: <value or UNKNOWN>
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0
            )

            content = response.choices[0].message.content
            return self._parse_ai_response(content)

        except Exception as e:
            print(f"OpenAI parsing failed, falling back to pattern matching: {e}")
            return self._parse_with_patterns(text)

    def _parse_with_claude(self, text: str) -> Dict[str, Optional[str]]:
        """Extract invoice data using Claude (Anthropic) - Better for structured data!"""
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)

            prompt = f"""Extract the following information from this invoice text:
1. Invoice number
2. Invoice date (format as YYYY-MM-DD)
3. Supplier/Company name
4. Service description (brief summary of what was invoiced)
5. Total amount (number only, without currency symbol)
6. VAT amount (number only, without currency symbol)

Invoice text:
{text}

Return the information in this exact format:
INVOICE_NUMBER: <value or UNKNOWN>
INVOICE_DATE: <value or UNKNOWN>
SUPPLIER_NAME: <value or UNKNOWN>
SERVICE_DESCRIPTION: <value or UNKNOWN>
TOTAL_AMOUNT: <value or UNKNOWN>
VAT_AMOUNT: <value or UNKNOWN>

Be precise and extract exact values. If a field is not present, use UNKNOWN."""

            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text
            return self._parse_ai_response(content)

        except Exception as e:
            print(f"Claude parsing failed, falling back to pattern matching: {e}")
            return self._parse_with_patterns(text)

    def _parse_ai_response(self, response: str) -> Dict[str, Optional[str]]:
        """Parse the structured AI response"""
        result = {}
        lines = response.strip().split('\n')

        field_mapping = {
            'INVOICE_NUMBER': 'invoice_number',
            'INVOICE_DATE': 'invoice_date',
            'SUPPLIER_NAME': 'supplier_name',
            'SERVICE_DESCRIPTION': 'service_description',
            'TOTAL_AMOUNT': 'total_amount',
            'VAT_AMOUNT': 'vat_amount',
        }

        for line in lines:
            for ai_field, db_field in field_mapping.items():
                if line.startswith(ai_field):
                    value = line.split(':', 1)[1].strip()
                    result[db_field] = None if value == 'UNKNOWN' else value

        return result

    def _extract_invoice_number(self, text: str, text_lower: str) -> Optional[str]:
        """Extract invoice number"""
        for pattern in self.invoice_patterns:
            match = re.search(pattern, text_lower)
            if match:
                # Return from original text to preserve case
                start, end = match.span(1)
                invoice_num = text[start:end].strip()
                # Clean up extra spaces within the invoice number
                invoice_num = re.sub(r'\s+', ' ', invoice_num)
                return invoice_num
        return None

    def _extract_date(self, text: str, text_lower: str) -> Optional[str]:
        """Extract and normalize invoice date"""
        for pattern in self.date_patterns:
            match = re.search(pattern, text_lower)
            if match:
                date_str = match.group(1)
                try:
                    # Parse and normalize date
                    parsed_date = date_parser.parse(date_str, dayfirst=True)
                    return parsed_date.strftime('%Y-%m-%d')
                except:
                    continue
        return None

    def _extract_supplier_name(self, text: str) -> Optional[str]:
        """Extract supplier/company name (usually at the top of invoice)"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        # Take first non-empty line(s) as potential supplier name
        # Skip common headers
        skip_words = ['invoice', 'factuur', 'receipt', 'bon']

        for line in lines[:5]:  # Check first 5 lines
            line_lower = line.lower()
            if len(line) > 3 and not any(skip in line_lower for skip in skip_words):
                # Check if it looks like a company name (contains letters)
                if re.search(r'[a-zA-Z]{3,}', line):
                    return line
        return None

    def _extract_service_description(self, text: str) -> Optional[str]:
        """Extract service description"""
        # Look for description or service keywords
        patterns = [
            r'description\s*:?\s*(.+?)(?:\n|$)',
            r'service\s*:?\s*(.+?)(?:\n|$)',
            r'omschrijving\s*:?\s*(.+?)(?:\n|$)',
            r'details\s*:?\s*(.+?)(?:\n|$)',
        ]

        text_lower = text.lower()
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                # Get from original text
                start, end = match.span(1)
                desc = text[start:end].strip()
                if len(desc) > 3:
                    return desc[:200]  # Limit length

        # If no explicit description found, try to extract from middle section
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if len(lines) > 5:
            # Take middle lines as description
            middle_start = min(3, len(lines) // 3)
            middle_end = min(middle_start + 3, len(lines) - 2)
            desc = ' '.join(lines[middle_start:middle_end])
            return desc[:200] if desc else None

        return None

    def _extract_total_amount(self, text: str, text_lower: str) -> Optional[str]:
        """Extract total amount"""
        for pattern in self.total_patterns:
            match = re.search(pattern, text_lower)
            if match:
                amount = match.group(1).replace(',', '.')
                return amount
        return None

    def _extract_vat_amount(self, text: str, text_lower: str) -> Optional[str]:
        """Extract VAT amount"""
        for pattern in self.vat_patterns:
            match = re.search(pattern, text_lower)
            if match:
                amount = match.group(1).replace(',', '.')
                return amount
        return None

    def validate_data(self, data: Dict[str, Optional[str]]) -> Dict[str, str]:
        """
        Validate extracted data and return validation errors

        Args:
            data: Extracted invoice data

        Returns:
            Dictionary of field names to error messages
        """
        errors = {}

        # Validate date
        if data.get('invoice_date'):
            try:
                datetime.strptime(data['invoice_date'], '%Y-%m-%d')
            except ValueError:
                errors['invoice_date'] = 'Invalid date format (expected YYYY-MM-DD)'

        # Validate amounts
        for field in ['total_amount', 'vat_amount']:
            if data.get(field):
                try:
                    float(data[field])
                except (ValueError, TypeError):
                    errors[field] = 'Invalid amount format'

        return errors
