"""
Python conversion of ZLib stream flavor enumeration
ZLib stream format flavors
"""

from enum import IntEnum

class ZlibStreamFlavor(IntEnum):
    """ZLib stream flavors"""

    ZLIB = 1950
    DEFLATE = 1951
    GZIP = 1952

    def __str__(self) -> str:
        """String representation"""
        flavor_names = {
            1950: "ZLib",
            1951: "Deflate",
            1952: "GZip"
        }
        return flavor_names.get(self.value, f"Flavor{self.value}")
