"""
Python conversion of Supercell.Laser.Titan.Library.ZLib.CompressionLevel.cs
Compression level enumeration
"""

from enum import IntEnum

class CompressionLevel(IntEnum):
    """ZLib compression levels"""

    NONE = 0
    LEVEL0 = 0
    BEST_SPEED = 1
    LEVEL1 = 1
    LEVEL2 = 2
    LEVEL3 = 3
    LEVEL4 = 4
    LEVEL5 = 5
    DEFAULT = 6
    LEVEL6 = 6
    LEVEL7 = 7
    LEVEL8 = 8
    BEST_COMPRESSION = 9
    LEVEL9 = 9

    def __str__(self) -> str:
        """String representation"""
        level_names = {
            0: "None/Level0",
            1: "BestSpeed/Level1", 
            2: "Level2",
            3: "Level3",
            4: "Level4", 
            5: "Level5",
            6: "Default/Level6",
            7: "Level7",
            8: "Level8",
            9: "BestCompression/Level9"
        }
        return level_names.get(self.value, f"Level{self.value}")
