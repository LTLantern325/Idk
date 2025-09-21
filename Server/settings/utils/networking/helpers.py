"""
Utility helper functions
"""

import random
import string
from typing import Optional

class Helpers:
    """Static helper class with utility functions"""

    @staticmethod
    def random_string(length: int) -> str:
        """Generate a random string of specified length"""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    @staticmethod
    def random_hex_string(length: int) -> str:
        """Generate a random hexadecimal string"""
        characters = string.hexdigits.lower()
        return ''.join(random.choice(characters) for _ in range(length))

    @staticmethod
    def clamp(value: int, min_val: int, max_val: int) -> int:
        """Clamp value between min and max"""
        return max(min_val, min(max_val, value))

    @staticmethod
    def safe_int_parse(value: str, default: int = 0) -> int:
        """Safely parse string to int with default fallback"""
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
