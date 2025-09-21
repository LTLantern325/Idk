"""
Python conversion of Supercell.Laser.Logic.Data.Reader.Row.cs
Row class for data table row management
"""

from typing import List, Any, Optional, Dict

class Row:
    """Row class for data table row management"""

    def __init__(self):
        """Initialize row"""
        self.values = []  # List of cell values
        self.index = 0
        self.is_empty = True
        self.column_count = 0

    def get_index(self) -> int:
        """Get row index"""
        return self.index

    def set_index(self, index: int) -> None:
        """Set row index"""
        self.index = index

    def get_column_count(self) -> int:
        """Get number of columns"""
        return len(self.values)

    def set_column_count(self, count: int) -> None:
        """Set column count and resize values list"""
        self.column_count = count
        # Resize values list
        while len(self.values) < count:
            self.values.append("")
        while len(self.values) > count:
            self.values.pop()

    def get_value(self, column_index: int) -> Any:
        """Get value at column index"""
        if 0 <= column_index < len(self.values):
            return self.values[column_index]
        return ""

    def set_value(self, column_index: int, value: Any) -> None:
        """Set value at column index"""
        # Ensure values list is large enough
        while len(self.values) <= column_index:
            self.values.append("")

        self.values[column_index] = value
        self._update_empty_status()

    def get_string_value(self, column_index: int) -> str:
        """Get string value at column index"""
        value = self.get_value(column_index)
        return str(value) if value is not None else ""

    def get_int_value(self, column_index: int) -> int:
        """Get integer value at column index"""
        value = self.get_value(column_index)
        try:
            return int(value) if value != "" else 0
        except (ValueError, TypeError):
            return 0

    def get_float_value(self, column_index: int) -> float:
        """Get float value at column index"""
        value = self.get_value(column_index)
        try:
            return float(value) if value != "" else 0.0
        except (ValueError, TypeError):
            return 0.0

    def get_bool_value(self, column_index: int) -> bool:
        """Get boolean value at column index"""
        value = self.get_string_value(column_index).lower()
        return value in ('true', '1', 'yes', 'on')

    def get_long_value(self, column_index: int) -> int:
        """Get long value at column index"""
        return self.get_int_value(column_index)  # Python int can handle long values

    def load_from_csv_data(self, csv_data: List[str]) -> None:
        """Load row from CSV data"""
        self.values = csv_data.copy()
        self._update_empty_status()

    def get_csv_data(self) -> List[str]:
        """Get row as CSV data"""
        return [str(value) for value in self.values]

    def is_row_empty(self) -> bool:
        """Check if row is empty"""
        return self.is_empty

    def _update_empty_status(self) -> None:
        """Update empty status based on values"""
        self.is_empty = all(str(value).strip() == "" for value in self.values)

    def clear(self) -> None:
        """Clear all values"""
        self.values.clear()
        self.is_empty = True

    def copy_from(self, other_row: 'Row') -> None:
        """Copy values from another row"""
        self.values = other_row.values.copy()
        self.index = other_row.index
        self.is_empty = other_row.is_empty

    def insert_value(self, column_index: int, value: Any) -> None:
        """Insert value at column index"""
        if column_index >= len(self.values):
            # Extend list if needed
            while len(self.values) <= column_index:
                self.values.append("")

        self.values.insert(column_index, value)
        self._update_empty_status()

    def remove_value(self, column_index: int) -> Any:
        """Remove and return value at column index"""
        if 0 <= column_index < len(self.values):
            value = self.values.pop(column_index)
            self._update_empty_status()
            return value
        return ""

    def find_value(self, value: Any) -> int:
        """Find column index of value, return -1 if not found"""
        try:
            return self.values.index(value)
        except ValueError:
            return -1

    def contains_value(self, value: Any) -> bool:
        """Check if row contains value"""
        return value in self.values

    def validate(self, columns: Optional[List] = None) -> List[str]:
        """Validate row data"""
        errors = []

        if columns:
            # Validate against column definitions
            for i, column in enumerate(columns):
                if i < len(self.values):
                    value = self.values[i]
                    if not column.validate_value(value):
                        errors.append(f"Invalid value '{value}' for column '{column.get_name()}' at index {i}")
                elif column.is_column_required():
                    errors.append(f"Missing required value for column '{column.get_name()}' at index {i}")

        return errors

    def to_dict(self, column_names: List[str]) -> Dict[str, Any]:
        """Convert row to dictionary using column names"""
        result = {}
        for i, column_name in enumerate(column_names):
            if i < len(self.values):
                result[column_name] = self.values[i]
            else:
                result[column_name] = ""
        return result

    def __str__(self) -> str:
        """String representation"""
        return f"Row(index={self.index}, {len(self.values)} values, empty={self.is_empty})"

    def __len__(self) -> int:
        """Length of row (number of columns)"""
        return len(self.values)

    def __getitem__(self, index: int) -> Any:
        """Get item by index"""
        return self.get_value(index)

    def __setitem__(self, index: int, value: Any) -> None:
        """Set item by index"""
        self.set_value(index, value)
