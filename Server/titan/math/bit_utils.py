"""
Python conversion of bit manipulation utilities (simplified)
Bit manipulation helper functions
"""

class BitUtils:
    """Bit manipulation utilities"""

    @staticmethod
    def reverse_bits_byte(value: int) -> int:
        """Reverse bits in a byte"""
        value &= 0xFF
        result = 0
        for i in range(8):
            result = (result << 1) | ((value >> i) & 1)
        return result & 0xFF

    @staticmethod
    def reverse_bits_uint16(value: int) -> int:
        """Reverse bits in 16-bit value"""
        value &= 0xFFFF
        result = 0
        for i in range(16):
            result = (result << 1) | ((value >> i) & 1)
        return result & 0xFFFF

    @staticmethod
    def reverse_bits_uint32(value: int) -> int:
        """Reverse bits in 32-bit value"""
        value &= 0xFFFFFFFF
        result = 0
        for i in range(32):
            result = (result << 1) | ((value >> i) & 1)
        return result & 0xFFFFFFFF

    @staticmethod
    def count_bits(value: int) -> int:
        """Count number of set bits"""
        count = 0
        while value:
            count += value & 1
            value >>= 1
        return count

    @staticmethod
    def rotate_left(value: int, bits: int, width: int = 32) -> int:
        """Rotate left by bits"""
        value &= (1 << width) - 1
        bits %= width
        return ((value << bits) | (value >> (width - bits))) & ((1 << width) - 1)

    @staticmethod
    def rotate_right(value: int, bits: int, width: int = 32) -> int:
        """Rotate right by bits"""
        value &= (1 << width) - 1
        bits %= width
        return ((value >> bits) | (value << (width - bits))) & ((1 << width) - 1)
