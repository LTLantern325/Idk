"""
Python conversion of Supercell.Laser.Logic.Data.Helper.GlobalId.cs
Global ID helper class for managing global identifiers
"""

class GlobalId:
    """Global ID helper class for managing global identifiers"""

    def __init__(self, high: int = 0, low: int = 0):
        """Initialize global ID"""
        self.high = high
        self.low = low

    def get_high(self) -> int:
        """Get high part of ID"""
        return self.high

    def set_high(self, high: int) -> None:
        """Set high part of ID"""
        self.high = high

    def get_low(self) -> int:
        """Get low part of ID"""
        return self.low

    def set_low(self, low: int) -> None:
        """Set low part of ID"""
        self.low = low

    def is_zero(self) -> bool:
        """Check if ID is zero"""
        return self.high == 0 and self.low == 0

    def is_valid(self) -> bool:
        """Check if ID is valid"""
        return not self.is_zero()

    def to_long(self) -> int:
        """Convert to long integer"""
        return (self.high << 32) | self.low

    @classmethod
    def from_long(cls, value: int) -> 'GlobalId':
        """Create GlobalId from long integer"""
        high = (value >> 32) & 0xFFFFFFFF
        low = value & 0xFFFFFFFF
        return cls(high, low)

    def copy(self) -> 'GlobalId':
        """Create copy of this ID"""
        return GlobalId(self.high, self.low)

    def equals(self, other: 'GlobalId') -> bool:
        """Check if equal to another GlobalId"""
        if not isinstance(other, GlobalId):
            return False
        return self.high == other.high and self.low == other.low

    def compare_to(self, other: 'GlobalId') -> int:
        """Compare to another GlobalId"""
        if not isinstance(other, GlobalId):
            return 1

        if self.high > other.high:
            return 1
        elif self.high < other.high:
            return -1
        elif self.low > other.low:
            return 1
        elif self.low < other.low:
            return -1
        else:
            return 0

    def __eq__(self, other) -> bool:
        """Equality operator"""
        return self.equals(other)

    def __lt__(self, other) -> bool:
        """Less than operator"""
        return self.compare_to(other) < 0

    def __le__(self, other) -> bool:
        """Less than or equal operator"""
        return self.compare_to(other) <= 0

    def __gt__(self, other) -> bool:
        """Greater than operator"""
        return self.compare_to(other) > 0

    def __ge__(self, other) -> bool:
        """Greater than or equal operator"""
        return self.compare_to(other) >= 0

    def __hash__(self) -> int:
        """Hash function"""
        return hash((self.high, self.low))

    def __str__(self) -> str:
        """String representation"""
        if self.is_zero():
            return "GlobalId(0)"
        return f"GlobalId(high={self.high}, low={self.low})"

    def __repr__(self) -> str:
        """String representation for debugging"""
        return self.__str__()

# Static helper methods
class GlobalIdHelper:
    """Helper class for GlobalId operations"""

    @staticmethod
    def create_zero() -> GlobalId:
        """Create zero GlobalId"""
        return GlobalId(0, 0)

    @staticmethod
    def create_from_parts(high: int, low: int) -> GlobalId:
        """Create GlobalId from high and low parts"""
        return GlobalId(high, low)

    @staticmethod
    def create_from_long(value: int) -> GlobalId:
        """Create GlobalId from long value"""
        return GlobalId.from_long(value)

    @staticmethod
    def is_valid_id(global_id: GlobalId) -> bool:
        """Check if GlobalId is valid"""
        return global_id is not None and global_id.is_valid()
