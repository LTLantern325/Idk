"""
Python conversion of ZLib flush type enumeration
ZLib flush types for compression
"""

from enum import IntEnum

class FlushType(IntEnum):
    """ZLib flush types"""

    NONE = 0
    PARTIAL = 1
    SYNC = 2
    FULL = 3
    FINISH = 4
    BLOCK = 5
    TREES = 6

    def __str__(self) -> str:
        """String representation"""
        flush_names = {
            0: "None",
            1: "Partial",
            2: "Sync",
            3: "Full",
            4: "Finish",
            5: "Block",
            6: "Trees"
        }
        return flush_names.get(self.value, f"Flush{self.value}")
