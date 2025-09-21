"""
Python conversion of Supercell.Laser.Logic.Data.GlobalData.cs
Global data class for game-wide settings
"""

from .data_tables import LogicData

class GlobalData(LogicData):
    """Global data class for game settings"""

    def __init__(self):
        """Initialize global data"""
        super().__init__()
        self.name = ""
        self.number_value = 0
        self.boolean_value = False
        self.text_value = ""
        self.number_array = []
        self.text_array = []

    def get_name(self) -> str:
        """Get setting name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set setting name"""
        self.name = name

    def get_number_value(self) -> int:
        """Get number value"""
        return self.number_value

    def set_number_value(self, value: int) -> None:
        """Set number value"""
        self.number_value = value

    def get_boolean_value(self) -> bool:
        """Get boolean value"""
        return self.boolean_value

    def set_boolean_value(self, value: bool) -> None:
        """Set boolean value"""
        self.boolean_value = value

    def get_text_value(self) -> str:
        """Get text value"""
        return self.text_value

    def set_text_value(self, value: str) -> None:
        """Set text value"""
        self.text_value = value

    def get_number_array(self) -> list:
        """Get number array"""
        return self.number_array.copy()

    def set_number_array(self, array: list) -> None:
        """Set number array"""
        self.number_array = array.copy() if array else []

    def get_text_array(self) -> list:
        """Get text array"""
        return self.text_array.copy()

    def set_text_array(self, array: list) -> None:
        """Set text array"""
        self.text_array = array.copy() if array else []

    def has_number_array(self) -> bool:
        """Check if has number array"""
        return len(self.number_array) > 0

    def has_text_array(self) -> bool:
        """Check if has text array"""
        return len(self.text_array) > 0
