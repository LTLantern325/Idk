"""
Python conversion of Supercell.Laser.Titan.Util.ZLibHelper.cs
ZLib compression and decompression utilities
"""

import zlib
import struct
from typing import Tuple, Optional

class ZLibHelper:
    """ZLib compression utilities"""

    @staticmethod
    def decompress_in_mysql_format(input_data: bytes) -> Tuple[int, Optional[bytes]]:
        """Decompress data in MySQL format (4-byte length prefix)"""
        if len(input_data) < 4:
            return -1, None

        try:
            # Read uncompressed length from first 4 bytes (little-endian)
            uncompressed_length = struct.unpack('<I', input_data[:4])[0]

            # Extract compressed data (skip 4-byte header)
            compressed_data = input_data[4:]

            # Decompress using zlib
            decompressed = zlib.decompress(compressed_data)

            # Verify length
            if len(decompressed) != uncompressed_length:
                from ..debugger import Debugger
                Debugger.error("ZLibHelper.decompress_in_mysql_format: decompressed byte array is corrupted")
                return -1, None

            return uncompressed_length, decompressed

        except Exception as e:
            from ..debugger import Debugger
            Debugger.error(f"ZLibHelper.decompress_in_mysql_format failed: {str(e)}")
            return -1, None

    @staticmethod
    def compress_in_zlib_format(input_data: bytes) -> Tuple[int, Optional[bytes]]:
        """Compress data in ZLib format with 4-byte length prefix"""
        if not input_data:
            return 0, b"\x00\x00\x00\x00"

        try:
            # Compress using zlib with best speed
            compressed = zlib.compress(input_data, level=zlib.Z_BEST_SPEED)

            compressed_length = len(compressed)
            uncompressed_length = len(input_data)

            # Create output with 4-byte length prefix (little-endian)
            output = bytearray()
            output.extend(struct.pack('<I', uncompressed_length))
            output.extend(compressed)

            return len(output), bytes(output)

        except Exception as e:
            from ..debugger import Debugger
            Debugger.error(f"ZLibHelper.compress_in_zlib_format failed: {str(e)}")
            return -1, None

    @staticmethod
    def decompress_raw(compressed_data: bytes) -> Optional[bytes]:
        """Decompress raw zlib data without length prefix"""
        try:
            return zlib.decompress(compressed_data)
        except Exception:
            return None

    @staticmethod
    def compress_raw(input_data: bytes, compression_level: int = zlib.Z_BEST_SPEED) -> Optional[bytes]:
        """Compress raw data without length prefix"""
        try:
            return zlib.compress(input_data, level=compression_level)
        except Exception:
            return None

    @staticmethod
    def get_compression_ratio(original_size: int, compressed_size: int) -> float:
        """Calculate compression ratio"""
        if original_size == 0:
            return 0.0
        return (1.0 - (compressed_size / original_size)) * 100.0

    @staticmethod
    def is_compressed(data: bytes) -> bool:
        """Check if data appears to be zlib compressed"""
        if len(data) < 2:
            return False

        # Check zlib header
        first_byte = data[0]
        second_byte = data[1]

        # zlib header validation
        if (first_byte & 0x0F) == 8:  # Deflate compression method
            if (first_byte >> 4) <= 7:  # Window size check
                if ((first_byte << 8) + second_byte) % 31 == 0:  # Checksum
                    return True

        return False

    @staticmethod
    def validate_compressed_data(data: bytes) -> bool:
        """Validate that compressed data can be decompressed"""
        try:
            zlib.decompress(data)
            return True
        except Exception:
            return False

    @staticmethod
    def get_uncompressed_size_estimate(compressed_data: bytes) -> int:
        """Estimate uncompressed size (not always accurate)"""
        # This is a rough estimate based on typical compression ratios
        return len(compressed_data) * 4  # Assume 4:1 ratio

    @staticmethod
    def compress_with_best_compression(input_data: bytes) -> Optional[bytes]:
        """Compress with best compression ratio"""
        try:
            return zlib.compress(input_data, level=zlib.Z_BEST_COMPRESSION)
        except Exception:
            return None

    @staticmethod
    def compress_with_best_speed(input_data: bytes) -> Optional[bytes]:
        """Compress with best speed"""
        try:
            return zlib.compress(input_data, level=zlib.Z_BEST_SPEED)
        except Exception:
            return None
