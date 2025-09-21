"""
Python conversion of Supercell.Laser.Titan.Library.ZLib.CRC32.cs
CRC32 checksum implementation
"""

import io
from typing import Optional

class CRC32:
    """CRC32 checksum calculator"""

    # Default polynomial (IEEE 802.3)
    DEFAULT_POLYNOMIAL = 0xEDB88320  # -306674912 as unsigned
    BUFFER_SIZE = 8192

    def __init__(self, polynomial: int = DEFAULT_POLYNOMIAL, reverse_bits: bool = False):
        """Initialize CRC32 calculator"""
        self.reverse_bits = reverse_bits
        self.dw_polynomial = polynomial & 0xFFFFFFFF
        self.m_register = 0xFFFFFFFF
        self.total_bytes_read = 0
        self.crc32_table: Optional[list] = None
        self._generate_lookup_table()

    @property
    def crc32_result(self) -> int:
        """Get current CRC32 result"""
        return (~self.m_register) & 0xFFFFFFFF

    def get_crc32(self, input_stream: io.IOBase) -> int:
        """Get CRC32 of input stream"""
        return self.get_crc32_and_copy(input_stream, None)

    def get_crc32_and_copy(self, input_stream: io.IOBase, output_stream: Optional[io.IOBase] = None) -> int:
        """Get CRC32 and optionally copy to output stream"""
        if input_stream is None:
            raise ValueError("The input stream must not be null.")

        buffer = bytearray(self.BUFFER_SIZE)
        self.total_bytes_read = 0

        bytes_read = input_stream.readinto(buffer)
        while bytes_read and bytes_read > 0:
            if output_stream is not None:
                output_stream.write(buffer[:bytes_read])

            self.total_bytes_read += bytes_read
            self.slurp_block(buffer, 0, bytes_read)
            bytes_read = input_stream.readinto(buffer)

        return self.crc32_result

    def compute_crc32(self, w: int, b: int) -> int:
        """Compute CRC32 for single byte"""
        return self._internal_compute_crc32(w & 0xFFFFFFFF, b & 0xFF)

    def _internal_compute_crc32(self, w: int, b: int) -> int:
        """Internal CRC32 computation"""
        return (self.crc32_table[(w ^ b) & 0xFF] ^ (w >> 8)) & 0xFFFFFFFF

    def slurp_block(self, block: bytes, offset: int, count: int) -> None:
        """Process block of data"""
        if block is None:
            raise ValueError("The data buffer must not be null.")

        for i in range(count):
            index = offset + i
            byte_val = block[index]

            if self.reverse_bits:
                temp = (self.m_register >> 24) ^ byte_val
                self.m_register = ((self.m_register << 8) ^ self.crc32_table[temp]) & 0xFFFFFFFF
            else:
                temp = (self.m_register & 0xFF) ^ byte_val
                self.m_register = ((self.m_register >> 8) ^ self.crc32_table[temp]) & 0xFFFFFFFF

        self.total_bytes_read += count

    def update_crc(self, byte_val: int, count: int = 1) -> None:
        """Update CRC with byte value"""
        byte_val &= 0xFF

        for _ in range(count):
            if self.reverse_bits:
                temp = (self.m_register >> 24) ^ byte_val
                self.m_register = ((self.m_register << 8) ^ self.crc32_table[temp]) & 0xFFFFFFFF
            else:
                temp = (self.m_register & 0xFF) ^ byte_val
                self.m_register = ((self.m_register >> 8) ^ self.crc32_table[temp]) & 0xFFFFFFFF

    def reset(self) -> None:
        """Reset CRC32 calculator"""
        self.m_register = 0xFFFFFFFF
        self.total_bytes_read = 0

    def _generate_lookup_table(self) -> None:
        """Generate CRC32 lookup table"""
        self.crc32_table = [0] * 256

        for b in range(256):
            temp = b

            for _ in range(8):
                if temp & 1:
                    temp = (temp >> 1) ^ self.dw_polynomial
                else:
                    temp >>= 1

            if self.reverse_bits:
                self.crc32_table[self._reverse_bits_byte(b)] = self._reverse_bits_uint(temp)
            else:
                self.crc32_table[b] = temp & 0xFFFFFFFF

    @staticmethod
    def _reverse_bits_uint(data: int) -> int:
        """Reverse bits in 32-bit unsigned integer"""
        data &= 0xFFFFFFFF
        temp = ((data & 0x55555555) << 1) | ((data >> 1) & 0x55555555)
        temp = ((temp & 0x33333333) << 2) | ((temp >> 2) & 0x33333333)
        temp = ((temp & 0x0F0F0F0F) << 4) | ((temp >> 4) & 0x0F0F0F0F)
        return (((temp << 24) | ((temp & 0xFF00) << 8) | 
                ((temp >> 8) & 0xFF00) | (temp >> 24)) & 0xFFFFFFFF)

    @staticmethod
    def _reverse_bits_byte(data: int) -> int:
        """Reverse bits in byte"""
        temp = (data & 0xFF) * 0x0202020202020202
        return ((temp & 0x010884422010) % 1023) & 0xFF

    @staticmethod
    def compute_checksum(data: bytes) -> int:
        """Compute CRC32 checksum for data"""
        crc = CRC32()
        crc.slurp_block(data, 0, len(data))
        return crc.crc32_result
