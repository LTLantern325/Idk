"""
Python conversion of Supercell.Laser.Titan.Library.ZLib.Adler.cs
Adler32 checksum implementation
"""

from typing import Optional

class Adler:
    """Adler32 checksum calculator"""

    # Constants from original
    BASE = 65521
    NMAX = 5552

    @staticmethod
    def adler32(adler: int, buffer: Optional[bytes], index: int = 0, length: Optional[int] = None) -> int:
        """Calculate Adler32 checksum"""
        if buffer is None:
            return 1

        if length is None:
            length = len(buffer) - index

        # Split into low and high 16-bit values
        s1 = adler & 0xFFFF
        s2 = (adler >> 16) & 0xFFFF

        while length > 0:
            # Process up to NMAX bytes at a time to avoid overflow
            k = length if length < Adler.NMAX else Adler.NMAX
            length -= k

            # Unrolled loop for better performance (16 bytes at a time)
            while k >= 16:
                s1 += buffer[index]; s2 += s1; index += 1
                s1 += buffer[index]; s2 += s1; index += 1
                s1 += buffer[index]; s2 += s1; index += 1
                s1 += buffer[index]; s2 += s1; index += 1
                s1 += buffer[index]; s2 += s1; index += 1
                s1 += buffer[index]; s2 += s1; index += 1
                s1 += buffer[index]; s2 += s1; index += 1
                s1 += buffer[index]; s2 += s1; index += 1
                s1 += buffer[index]; s2 += s1; index += 1
                s1 += buffer[index]; s2 += s1; index += 1
                s1 += buffer[index]; s2 += s1; index += 1
                s1 += buffer[index]; s2 += s1; index += 1
                s1 += buffer[index]; s2 += s1; index += 1
                s1 += buffer[index]; s2 += s1; index += 1
                s1 += buffer[index]; s2 += s1; index += 1
                s1 += buffer[index]; s2 += s1; index += 1
                k -= 16

            # Handle remaining bytes
            while k > 0:
                s1 += buffer[index]
                s2 += s1
                index += 1
                k -= 1

            # Reduce modulo BASE
            s1 %= Adler.BASE
            s2 %= Adler.BASE

        # Return combined checksum
        return (s2 << 16) | s1

    @staticmethod
    def compute_checksum(data: bytes) -> int:
        """Compute Adler32 checksum for data"""
        return Adler.adler32(1, data, 0, len(data))

    @staticmethod
    def update_checksum(current_checksum: int, data: bytes) -> int:
        """Update existing checksum with new data"""
        return Adler.adler32(current_checksum, data, 0, len(data))
