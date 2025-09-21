"""
Python conversion of Supercell.Laser.Logic.Data.Reader.Column.cs
Column class for data table column management
"""

from typing import Any, Optional

class ColumnType:
    """Column data types"""
    STRING = 0
    INTEGER = 1
    BOOLEAN = 2
    FLOAT = 3
    LONG = 4

class Column:
    """Column class for data table column management"""

    def __init__(self):
        """Initialize column"""
        self.name = ""
        self.column_type = ColumnType.STRING
        self.index = 0
        self.is_required = False
        self.default_value = None
        self.max_length = -1  # -1 for unlimited
        self.min_value = None
        self.max_value = None

    def get_name(self) -> str:
        """Get column name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set column name"""
        self.name = name

    def get_column_type(self) -> int:
        """Get column type"""
        return self.column_type

    def set_column_type(self, column_type: int) -> None:
        """Set column type"""
        self.column_type = column_type

    def get_index(self) -> int:
        """Get column index"""
        return self.index

    def set_index(self, index: int) -> None:
        """Set column index"""
        self.index = index

    def is_column_required(self) -> bool:
        """Check if column is required"""
        return self.is_required

    def set_required(self, required: bool) -> None:
        """Set column required status"""
        self.is_required = required

    def get_default_value(self) -> Any:
        """Get default value"""
        return self.default_value

    def set_default_value(self, value: Any) -> None:
        """Set default value"""
        self.default_value = value

    def validate_value(self, value: Any) -> bool:
        """Validate value against column constraints"""
        if value is None:
            return not self.is_required

        # Type validation
        if self.column_type == ColumnType.STRING:
            if not isinstance(value, str):
                return False
            if self.max_length > 0 and len(value) > self.max_length:
                return False
        elif self.column_type == ColumnType.INTEGER:
            if not isinstance(value, int):
                return False
            if self.min_value is not None and value < self.min_value:
                return False
            if self.max_value is not None and value > self.max_value:
                return False
        elif self.column_type == ColumnType.BOOLEAN:
            if not isinstance(value, bool):
                return False
        elif self.column_type == ColumnType.FLOAT:
            if not isinstance(value, (int, float)):
                return False
            if self.min_value is not None and value < self.min_value:
                return False
            if self.max_value is not None and value > self.max_value:
                return False
        elif self.column_type == ColumnType.LONG:
            if not isinstance(value, int):
                return False
            if self.min_value is not None and value < self.min_value:
                return False
            if self.max_value is not None and value > self.max_value:
                return False

        return True

    def convert_value(self, value: str) -> Any:
        """Convert string value to column type"""
        if value == "" or value is None:
            return self.default_value

        try:
            if self.column_type == ColumnType.STRING:
                return str(value)
            elif self.column_type == ColumnType.INTEGER:
                return int(value)
            elif self.column_type == ColumnType.BOOLEAN:
                return value.lower() in ('true', '1', 'yes', 'on')
            elif self.column_type == ColumnType.FLOAT:
                return float(value)
            elif self.column_type == ColumnType.LONG:
                return int(value)
        except (ValueError, TypeError):
            return self.default_value

        return self.default_value

    def get_type_name(self) -> str:
        """Get column type name"""
        type_names = {
            ColumnType.STRING: "String",
            ColumnType.INTEGER: "Integer",
            ColumnType.BOOLEAN: "Boolean",
            ColumnType.FLOAT: "Float",
            ColumnType.LONG: "Long"
        }
        return type_names.get(self.column_type, "Unknown")

    def __str__(self) -> str:
        """String representation"""
        required_str = " (Required)" if self.is_required else ""
        return f"Column('{self.name}', {self.get_type_name()}, index={self.index}{required_str})"
