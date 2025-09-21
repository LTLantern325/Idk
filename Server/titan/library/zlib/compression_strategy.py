"""
Python conversion of compression strategy enumeration
ZLib compression strategies
"""

from enum import IntEnum

class CompressionStrategy(IntEnum):
    """ZLib compression strategies"""

    DEFAULT = 0
    FILTERED = 1
    HUFFMAN_ONLY = 2
    RLE = 3
    FIXED = 4

    def __str__(self) -> str:
        """String representation"""
        strategy_names = {
            0: "Default",
            1: "Filtered",
            2: "HuffmanOnly", 
            3: "RLE",
            4: "Fixed"
        }
        return strategy_names.get(self.value, f"Strategy{self.value}")
