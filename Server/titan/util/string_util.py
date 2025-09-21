"""
Python conversion of Supercell.Laser.Titan.Util.StringUtil.cs
String utility functions
"""

import binascii
from typing import List, Optional

class StringUtil:
    """String utility functions for server"""

    @staticmethod
    def hex_to_bytes(hex_string: str) -> bytes:
        """Convert hex string to bytes"""
        if not hex_string:
            return b""

        # Remove spaces and dashes
        hex_clean = hex_string.replace(" ", "").replace("-", "")

        # Ensure even length
        if len(hex_clean) % 2 != 0:
            hex_clean = "0" + hex_clean

        try:
            return bytes.fromhex(hex_clean)
        except ValueError:
            # Try with binascii as fallback
            try:
                return binascii.unhexlify(hex_clean)
            except Exception:
                return b""

    @staticmethod
    def bytes_to_hex(data: bytes, separator: str = "") -> str:
        """Convert bytes to hex string"""
        if not data:
            return ""

        hex_str = data.hex().upper()

        if separator:
            # Insert separator between each byte
            return separator.join(hex_str[i:i+2] for i in range(0, len(hex_str), 2))

        return hex_str

    @staticmethod
    def is_valid_hex(hex_string: str) -> bool:
        """Check if string is valid hexadecimal"""
        if not hex_string:
            return False

        hex_clean = hex_string.replace(" ", "").replace("-", "")

        try:
            int(hex_clean, 16)
            return True
        except ValueError:
            return False

    @staticmethod
    def pad_hex(hex_string: str, length: int, pad_left: bool = True) -> str:
        """Pad hex string to specified length"""
        if not hex_string:
            return "0" * length

        if len(hex_string) >= length:
            return hex_string

        padding = "0" * (length - len(hex_string))

        if pad_left:
            return padding + hex_string
        else:
            return hex_string + padding

    @staticmethod
    def split_string(text: str, separator: str, max_splits: int = -1) -> List[str]:
        """Split string with optional max splits"""
        if max_splits == -1:
            return text.split(separator)
        else:
            return text.split(separator, max_splits)

    @staticmethod
    def join_strings(strings: List[str], separator: str = "") -> str:
        """Join strings with separator"""
        return separator.join(strings)

    @staticmethod
    def trim_string(text: str) -> str:
        """Trim whitespace from string"""
        return text.strip()

    @staticmethod
    def is_null_or_empty(text: Optional[str]) -> bool:
        """Check if string is null or empty"""
        return text is None or text == ""

    @staticmethod
    def is_null_or_whitespace(text: Optional[str]) -> bool:
        """Check if string is null or whitespace"""
        return text is None or text.strip() == ""

    @staticmethod
    def safe_substring(text: str, start: int, length: int = -1) -> str:
        """Safe substring that won't throw exceptions"""
        if not text or start < 0 or start >= len(text):
            return ""

        if length == -1:
            return text[start:]

        end = min(start + length, len(text))
        return text[start:end]

    @staticmethod
    def contains_any(text: str, search_strings: List[str]) -> bool:
        """Check if text contains any of the search strings"""
        if not text or not search_strings:
            return False

        return any(search in text for search in search_strings)

    @staticmethod
    def replace_multiple(text: str, replacements: dict) -> str:
        """Replace multiple strings in one pass"""
        result = text
        for old, new in replacements.items():
            result = result.replace(old, new)
        return result

    @staticmethod
    def to_title_case(text: str) -> str:
        """Convert to title case"""
        return text.title()

    @staticmethod
    def reverse_string(text: str) -> str:
        """Reverse string"""
        return text[::-1]

    @staticmethod
    def count_occurrences(text: str, substring: str) -> int:
        """Count occurrences of substring"""
        if not text or not substring:
            return 0
        return text.count(substring)

    @staticmethod
    def escape_for_json(text: str) -> str:
        """Escape string for JSON"""
        if not text:
            return ""

        replacements = {
            '\\': '\\\\',
            '"': '\\"',
            '\n': '\\n',
            '\r': '\\r',
            '\t': '\\t',
            '\b': '\\b',
            '\f': '\\f'
        }

        return StringUtil.replace_multiple(text, replacements)
