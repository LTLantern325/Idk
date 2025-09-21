"""
Python conversion of Supercell.Laser.Titan.Library.ZLib.SharedUtils.cs
Shared utility functions for ZLib
"""

import io

class SharedUtils:
    """Shared utility functions"""

    @staticmethod
    def ur_shift(number: int, bits: int) -> int:
        """Unsigned right shift (like Java's >>>)"""
        return (number & 0xFFFFFFFF) >> bits

    @staticmethod
    def read_input(source_reader: io.TextIOBase, target: bytearray, start: int, count: int) -> int:
        """Read input from text reader to byte array"""
        if len(target) == 0:
            return 0

        try:
            # Read characters and convert to bytes
            text = source_reader.read(count)
            if not text:
                return -1

            # Convert text to bytes (UTF-8)
            text_bytes = text.encode('utf-8')
            bytes_to_copy = min(len(text_bytes), count)

            # Copy to target array
            for i in range(bytes_to_copy):
                if start + i < len(target):
                    target[start + i] = text_bytes[i]

            return bytes_to_copy

        except Exception:
            return -1

    @staticmethod
    def to_byte_array(source_string: str) -> bytes:
        """Convert string to byte array (UTF-8)"""
        return source_string.encode('utf-8')

    @staticmethod
    def to_char_array(byte_array: bytes) -> str:
        """Convert byte array to string (UTF-8)"""
        return byte_array.decode('utf-8', errors='replace')

    @staticmethod
    def copy_array(source: bytes, source_start: int, dest: bytearray, dest_start: int, length: int) -> None:
        """Copy array elements"""
        for i in range(length):
            if (source_start + i < len(source) and 
                dest_start + i < len(dest)):
                dest[dest_start + i] = source[source_start + i]
