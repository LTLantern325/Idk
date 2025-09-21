"""
Python conversion of Supercell.Laser.Titan.Math.LogicLong.cs
64-bit long integer implementation
"""

import struct
from typing import Tuple

class LogicLong:
    """64-bit long integer for Brawl Stars protocol"""

    def __init__(self, high_integer: int = 0, low_integer: int = 0):
        """Initialize with high and low 32-bit integers"""
        self._high_integer = high_integer & 0xFFFFFFFF
        self._low_integer = low_integer & 0xFFFFFFFF

    @staticmethod
    def to_long(high_value: int, low_value: int) -> int:
        """Convert high/low values to Python long"""
        return (high_value << 32) | (low_value & 0xFFFFFFFF)

    @staticmethod
    def from_long(value: int) -> 'LogicLong':
        """Create LogicLong from Python long"""
        high = (value >> 32) & 0xFFFFFFFF
        low = value & 0xFFFFFFFF
        return LogicLong(high, low)

    def clone(self) -> 'LogicLong':
        """Create a copy of this LogicLong"""
        return LogicLong(self._high_integer, self._low_integer)

    def is_zero(self) -> bool:
        """Check if value is zero"""
        return self._high_integer == 0 and self._low_integer == 0

    def get_higher_int(self) -> int:
        """Get high 32-bit integer"""
        return self._high_integer

    def get_lower_int(self) -> int:
        """Get low 32-bit integer"""
        return self._low_integer

    def set_higher_int(self, value: int) -> None:
        """Set high 32-bit integer"""
        self._high_integer = value & 0xFFFFFFFF

    def set_lower_int(self, value: int) -> None:
        """Set low 32-bit integer"""
        self._low_integer = value & 0xFFFFFFFF

    def to_python_int(self) -> int:
        """Convert to Python integer"""
        return LogicLong.to_long(self._high_integer, self._low_integer)

    def encode(self, stream) -> None:
        """Encode to stream"""
        stream.write_int(self._high_integer)
        stream.write_int(self._low_integer)

    def decode(self, stream) -> None:
        """Decode from stream"""
        self._high_integer = stream.read_int()
        self._low_integer = stream.read_int()

    def __hash__(self) -> int:
        """Hash code for dictionaries"""
        return self._low_integer + 31 * self._high_integer

    def __eq__(self, other) -> bool:
        """Equality comparison"""
        if not isinstance(other, LogicLong):
            return False
        return (self._high_integer == other._high_integer and 
                self._low_integer == other._low_integer)

    def __ne__(self, other) -> bool:
        """Inequality comparison"""
        return not self.__eq__(other)

    def __str__(self) -> str:
        """String representation"""
        return f"LogicLong({self._high_integer}-{self._low_integer})"

    def __repr__(self) -> str:
        """Detailed string representation"""
        return f"LogicLong(high={self._high_integer}, low={self._low_integer})"

    def __int__(self) -> int:
        """Convert to Python int"""
        return self.to_python_int()

    def __bool__(self) -> bool:
        """Boolean conversion"""
        return not self.is_zero()
