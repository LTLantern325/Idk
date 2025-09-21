"""
Python conversion of compression mode enumeration  
Compression/decompression mode
"""

from enum import IntEnum

class CompressionMode(IntEnum):
    """Compression mode enumeration"""

    COMPRESS = 0
    DECOMPRESS = 1

    def __str__(self) -> str:
        """String representation"""
        if self == CompressionMode.COMPRESS:
            return "Compress"
        else:
            return "Decompress"
