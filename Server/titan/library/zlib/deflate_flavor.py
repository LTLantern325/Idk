"""
Python conversion of deflate flavor enumeration
Different deflate algorithm flavors
"""

from enum import IntEnum

class DeflateFlavor(IntEnum):
    """Deflate algorithm flavors"""

    STORE = 0
    FAST = 1
    SLOW = 2

    def __str__(self) -> str:
        """String representation"""
        flavor_names = {
            0: "Store",
            1: "Fast", 
            2: "Slow"
        }
        return flavor_names.get(self.value, f"Flavor{self.value}")
