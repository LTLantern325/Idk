"""
Python conversion of Supercell.Laser.Titan.Library.ZLib.ZLibException.cs
ZLib exception class
"""

class ZLibException(Exception):
    """ZLib exception"""

    def __init__(self, message: str = ""):
        """Initialize ZLib exception"""
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        """String representation"""
        return f"ZLibException: {self.message}" if self.message else "ZLibException"
