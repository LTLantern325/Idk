"""
Python conversion of Supercell.Laser.Logic.Util.LogicLongUtil.cs
Utility functions for long integer operations
"""

class LogicLongUtil:
    """Utility functions for 64-bit integer operations"""

    @staticmethod
    def get_higher_int(value: int) -> int:
        """Get higher 32-bit part of 64-bit value"""
        return (value >> 32) & 0xFFFFFFFF

    @staticmethod
    def get_lower_int(value: int) -> int:
        """Get lower 32-bit part of 64-bit value"""
        return value & 0xFFFFFFFF

    @staticmethod
    def combine_ints(higher: int, lower: int) -> int:
        """Combine two 32-bit integers into 64-bit value"""
        return ((higher & 0xFFFFFFFF) << 32) | (lower & 0xFFFFFFFF)

    @staticmethod
    def is_valid_long(value: int) -> bool:
        """Check if value is valid 64-bit integer"""
        return -(1 << 63) <= value < (1 << 63)

# Extension methods as standalone functions
def get_higher_int(value: int) -> int:
    """Extension method: Get higher 32-bit part"""
    return LogicLongUtil.get_higher_int(value)

def get_lower_int(value: int) -> int:
    """Extension method: Get lower 32-bit part"""
    return LogicLongUtil.get_lower_int(value)
