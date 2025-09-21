"""
Python conversion of Supercell.Laser.Server.Utils.Helpers.cs
Utility helper functions for server operations
"""

import random
import string

class Helpers:
    """Static helper class for server utilities"""

    STRING_CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

    @staticmethod
    def random_string(length: int) -> str:
        """Generate random string of specified length"""
        result = []
        rand = random.Random()

        for i in range(length):
            result.append(Helpers.STRING_CHARACTERS[rand.randint(0, len(Helpers.STRING_CHARACTERS) - 1)])

        return ''.join(result)

    @staticmethod
    def random_hex_string(length: int) -> str:
        """Generate random hexadecimal string"""
        hex_chars = "0123456789abcdef"
        result = []
        rand = random.Random()

        for i in range(length):
            result.append(hex_chars[rand.randint(0, len(hex_chars) - 1)])

        return ''.join(result)

    @staticmethod
    def random_bytes(length: int) -> bytes:
        """Generate random bytes"""
        return bytes([random.randint(0, 255) for _ in range(length)])
