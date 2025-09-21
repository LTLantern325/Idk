"""
Python conversion of Supercell.Laser.Logic.Data.Helper.DataTable.cs
Data table helper class for managing data tables
"""

from typing import Dict, List, Any, Optional

class DataTable:
    """Data table helper class for managing data tables"""

    def __init__(self, name: str = ""):
        """Initialize data table"""
        self.name = name
        self.rows = []  # List of Row objects
        self.columns = []  # List of column names
        self.data = {}  # Dict mapping row_id -> row_data
        self.index = 0  # Current index

    def get_name(self) -> str:
        """Get table name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set table name"""
        self.name = name

    def get_row_count(self) -> int:
        """Get number of rows"""
        return len(self.rows)

    def get_column_count(self) -> int:
        """Get number of columns"""
        return len(self.columns)

    def add_row(self, row: 'Row') -> None:
        """Add row to table"""
        self.rows.append(row)
        if hasattr(row, 'get_id'):
            self.data[row.get_id()] = row

    def get_row(self, index: int) -> Optional['Row']:
        """Get row by index"""
        if 0 <= index < len(self.rows):
            return self.rows[index]
        return None

    def get_row_by_id(self, row_id: int) -> Optional['Row']:
        """Get row by ID"""
        return self.data.get(row_id)

    def add_column(self, column_name: str) -> None:
        """Add column to table"""
        if column_name not in self.columns:
            self.columns.append(column_name)

    def get_columns(self) -> List[str]:
        """Get column names"""
        return self.columns.copy()

    def has_column(self, column_name: str) -> bool:
        """Check if column exists"""
        return column_name in self.columns

    def clear(self) -> None:
        """Clear all data"""
        self.rows.clear()
        self.columns.clear()
        self.data.clear()
        self.index = 0

    def is_empty(self) -> bool:
        """Check if table is empty"""
        return len(self.rows) == 0

    def get_next_row(self) -> Optional['Row']:
        """Get next row (iterator pattern)"""
        if self.index < len(self.rows):
            row = self.rows[self.index]
            self.index += 1
            return row
        return None

    def reset_iterator(self) -> None:
        """Reset row iterator"""
        self.index = 0

    def __str__(self) -> str:
        """String representation"""
        return f"DataTable('{self.name}', rows={len(self.rows)}, cols={len(self.columns)})"

    def __len__(self) -> int:
        """Get row count"""
        return len(self.rows)

class Row:
    """Row class for data table rows"""

    def __init__(self, row_id: int = 0):
        """Initialize row"""
        self.id = row_id
        self.data = {}  # Dict mapping column_name -> value

    def get_id(self) -> int:
        """Get row ID"""
        return self.id

    def set_id(self, row_id: int) -> None:
        """Set row ID"""
        self.id = row_id

    def set_value(self, column: str, value: Any) -> None:
        """Set value for column"""
        self.data[column] = value

    def get_value(self, column: str, default: Any = None) -> Any:
        """Get value for column"""
        return self.data.get(column, default)

    def has_column(self, column: str) -> bool:
        """Check if row has column"""
        return column in self.data

    def get_columns(self) -> List[str]:
        """Get column names in this row"""
        return list(self.data.keys())

    def __str__(self) -> str:
        """String representation"""
        return f"Row(id={self.id}, columns={len(self.data)})"
