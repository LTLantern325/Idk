"""
Python conversion of Supercell.Laser.Logic.Data.Reader.Table.cs
Table class for data table management
"""

import csv
from typing import List, Dict, Any, Optional
from .column import Column, ColumnType
from .row import Row

class Table:
    """Table class for data table management"""

    def __init__(self):
        """Initialize table"""
        self.name = ""
        self.columns = []  # List[Column]
        self.rows = []     # List[Row]
        self.column_map = {}  # Dict[str, int] - column name to index
        self.primary_key_column = -1
        self.row_map = {}  # Dict[Any, int] - primary key to row index

    def get_name(self) -> str:
        """Get table name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set table name"""
        self.name = name

    def get_column_count(self) -> int:
        """Get number of columns"""
        return len(self.columns)

    def get_row_count(self) -> int:
        """Get number of rows"""
        return len(self.rows)

    def add_column(self, column: Column) -> None:
        """Add column to table"""
        column.set_index(len(self.columns))
        self.columns.append(column)
        self.column_map[column.get_name()] = column.get_index()

    def get_column(self, index: int) -> Optional[Column]:
        """Get column by index"""
        if 0 <= index < len(self.columns):
            return self.columns[index]
        return None

    def get_column_by_name(self, name: str) -> Optional[Column]:
        """Get column by name"""
        index = self.column_map.get(name, -1)
        return self.get_column(index)

    def get_column_index(self, name: str) -> int:
        """Get column index by name"""
        return self.column_map.get(name, -1)

    def get_column_names(self) -> List[str]:
        """Get all column names"""
        return [column.get_name() for column in self.columns]

    def add_row(self, row_data: List[str]) -> Row:
        """Add row to table"""
        row = Row()
        row.set_index(len(self.rows))
        row.load_from_csv_data(row_data)
        row.set_column_count(len(self.columns))

        # Convert values to proper types
        for i, column in enumerate(self.columns):
            if i < len(row_data):
                converted_value = column.convert_value(row_data[i])
                row.set_value(i, converted_value)

        self.rows.append(row)

        # Update primary key mapping if set
        if self.primary_key_column >= 0:
            pk_value = row.get_value(self.primary_key_column)
            self.row_map[pk_value] = row.get_index()

        return row

    def get_row(self, index: int) -> Optional[Row]:
        """Get row by index"""
        if 0 <= index < len(self.rows):
            return self.rows[index]
        return None

    def get_row_by_key(self, key: Any) -> Optional[Row]:
        """Get row by primary key"""
        row_index = self.row_map.get(key, -1)
        return self.get_row(row_index)

    def get_row_data(self, row_index: int) -> List[Any]:
        """Get row data as list"""
        row = self.get_row(row_index)
        if row:
            return row.get_csv_data()
        return []

    def get_cell_value(self, row_index: int, column_index: int) -> Any:
        """Get cell value"""
        row = self.get_row(row_index)
        if row:
            return row.get_value(column_index)
        return ""

    def get_cell_value_by_name(self, row_index: int, column_name: str) -> Any:
        """Get cell value by column name"""
        column_index = self.get_column_index(column_name)
        if column_index >= 0:
            return self.get_cell_value(row_index, column_index)
        return ""

    def set_cell_value(self, row_index: int, column_index: int, value: Any) -> bool:
        """Set cell value"""
        row = self.get_row(row_index)
        if row:
            row.set_value(column_index, value)
            return True
        return False

    def set_primary_key_column(self, column_name: str) -> bool:
        """Set primary key column"""
        column_index = self.get_column_index(column_name)
        if column_index >= 0:
            self.primary_key_column = column_index
            self._rebuild_row_map()
            return True
        return False

    def _rebuild_row_map(self) -> None:
        """Rebuild row mapping for primary key"""
        self.row_map.clear()
        if self.primary_key_column >= 0:
            for row in self.rows:
                pk_value = row.get_value(self.primary_key_column)
                self.row_map[pk_value] = row.get_index()

    def load_headers(self, header_data: List[str]) -> None:
        """Load column headers from CSV data"""
        self.columns.clear()
        self.column_map.clear()

        for i, header_name in enumerate(header_data):
            column = Column()
            column.set_name(header_name.strip())
            column.set_index(i)
            # Default to string type, can be changed later
            column.set_column_type(ColumnType.STRING)
            self.add_column(column)

    def find_rows(self, column_name: str, value: Any) -> List[Row]:
        """Find all rows with matching value in column"""
        column_index = self.get_column_index(column_name)
        if column_index < 0:
            return []

        matching_rows = []
        for row in self.rows:
            if row.get_value(column_index) == value:
                matching_rows.append(row)

        return matching_rows

    def find_row(self, column_name: str, value: Any) -> Optional[Row]:
        """Find first row with matching value in column"""
        rows = self.find_rows(column_name, value)
        return rows[0] if rows else None

    def sort_by_column(self, column_name: str, reverse: bool = False) -> bool:
        """Sort rows by column value"""
        column_index = self.get_column_index(column_name)
        if column_index < 0:
            return False

        try:
            self.rows.sort(key=lambda row: row.get_value(column_index), reverse=reverse)
            # Update row indices
            for i, row in enumerate(self.rows):
                row.set_index(i)
            # Rebuild row map if needed
            if self.primary_key_column >= 0:
                self._rebuild_row_map()
            return True
        except Exception:
            return False

    def filter_rows(self, column_name: str, filter_func) -> List[Row]:
        """Filter rows using custom function"""
        column_index = self.get_column_index(column_name)
        if column_index < 0:
            return []

        return [row for row in self.rows 
                if filter_func(row.get_value(column_index))]

    def to_dict_list(self) -> List[Dict[str, Any]]:
        """Convert table to list of dictionaries"""
        column_names = self.get_column_names()
        return [row.to_dict(column_names) for row in self.rows]

    def from_dict_list(self, data: List[Dict[str, Any]]) -> None:
        """Load table from list of dictionaries"""
        if not data:
            return

        # Create columns from first dictionary keys
        first_row = data[0]
        self.columns.clear()
        self.column_map.clear()

        for i, key in enumerate(first_row.keys()):
            column = Column()
            column.set_name(key)
            column.set_index(i)
            column.set_column_type(ColumnType.STRING)
            self.add_column(column)

        # Load data rows
        self.rows.clear()
        for row_data in data:
            row_values = [str(row_data.get(col_name, "")) for col_name in self.get_column_names()]
            self.add_row(row_values)

    def validate(self) -> List[str]:
        """Validate table data"""
        errors = []

        # Validate each row
        for row in self.rows:
            row_errors = row.validate(self.columns)
            errors.extend(row_errors)

        # Check for duplicate primary keys
        if self.primary_key_column >= 0:
            pk_values = [row.get_value(self.primary_key_column) for row in self.rows]
            seen = set()
            for i, pk_value in enumerate(pk_values):
                if pk_value in seen:
                    errors.append(f"Duplicate primary key '{pk_value}' at row {i}")
                seen.add(pk_value)

        return errors

    def clear(self) -> None:
        """Clear all data"""
        self.columns.clear()
        self.rows.clear()
        self.column_map.clear()
        self.row_map.clear()
        self.primary_key_column = -1

    def __str__(self) -> str:
        """String representation"""
        return f"Table('{self.name}', {len(self.columns)} columns, {len(self.rows)} rows)"
