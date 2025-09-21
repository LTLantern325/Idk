"""
Python conversion of Supercell.Laser.Logic.Data.Reader.Gamefiles.cs
Gamefiles class for loading game data files
"""

import os
import json
import csv
from typing import Dict, List, Any, Optional
from .table import Table

class Gamefiles:
    """Gamefiles class for loading game data files"""

    def __init__(self):
        """Initialize gamefiles"""
        self.tables = {}  # Dict[str, Table]
        self.base_path = "Assets/csv/"
        self.localization_tables = {}
        self.loaded_files = set()

    def get_base_path(self) -> str:
        """Get base path for data files"""
        return self.base_path

    def set_base_path(self, path: str) -> None:
        """Set base path for data files"""
        self.base_path = path

    def load_table(self, filename: str) -> Optional[Table]:
        """Load table from CSV file"""
        filepath = os.path.join(self.base_path, filename)

        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            return None

        try:
            table = Table()
            table.set_name(os.path.splitext(filename)[0])

            with open(filepath, 'r', encoding='utf-8') as file:
                # Use CSV reader to handle proper parsing
                csv_reader = csv.reader(file)

                # Load data
                for row_index, row_data in enumerate(csv_reader):
                    if row_index == 0:
                        # Header row - define columns
                        table.load_headers(row_data)
                    else:
                        # Data rows
                        table.add_row(row_data)

            self.tables[table.get_name()] = table
            self.loaded_files.add(filename)
            return table

        except Exception as e:
            print(f"Error loading table {filename}: {e}")
            return None

    def load_all_tables(self) -> int:
        """Load all CSV files in base path"""
        if not os.path.exists(self.base_path):
            print(f"Base path not found: {self.base_path}")
            return 0

        loaded_count = 0

        for filename in os.listdir(self.base_path):
            if filename.endswith('.csv'):
                table = self.load_table(filename)
                if table:
                    loaded_count += 1

        return loaded_count

    def get_table(self, table_name: str) -> Optional[Table]:
        """Get loaded table by name"""
        return self.tables.get(table_name)

    def has_table(self, table_name: str) -> bool:
        """Check if table is loaded"""
        return table_name in self.tables

    def get_table_names(self) -> List[str]:
        """Get all loaded table names"""
        return list(self.tables.keys())

    def get_table_count(self) -> int:
        """Get number of loaded tables"""
        return len(self.tables)

    def load_localization(self, language: str = "EN") -> bool:
        """Load localization data"""
        localization_path = os.path.join(self.base_path, f"localization_{language.lower()}.csv")

        if not os.path.exists(localization_path):
            return False

        try:
            localization_data = {}

            with open(localization_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)

                for row in csv_reader:
                    key = row.get('TID', '')
                    text = row.get('Text', '')
                    if key:
                        localization_data[key] = text

            self.localization_tables[language] = localization_data
            return True

        except Exception as e:
            print(f"Error loading localization {language}: {e}")
            return False

    def get_localized_text(self, key: str, language: str = "EN") -> str:
        """Get localized text"""
        if language not in self.localization_tables:
            self.load_localization(language)

        localization = self.localization_tables.get(language, {})
        return localization.get(key, key)  # Return key if not found

    def save_table(self, table_name: str, filename: str = None) -> bool:
        """Save table to CSV file"""
        if table_name not in self.tables:
            return False

        table = self.tables[table_name]
        if not filename:
            filename = f"{table_name}.csv"

        filepath = os.path.join(self.base_path, filename)

        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                # Write headers
                headers = table.get_column_names()
                writer.writerow(headers)

                # Write data rows
                for row_index in range(table.get_row_count()):
                    row_data = table.get_row_data(row_index)
                    writer.writerow(row_data)

            return True

        except Exception as e:
            print(f"Error saving table {table_name}: {e}")
            return False

    def reload_table(self, table_name: str) -> bool:
        """Reload specific table"""
        filename = f"{table_name}.csv"
        if filename in self.loaded_files:
            table = self.load_table(filename)
            return table is not None
        return False

    def clear_tables(self) -> None:
        """Clear all loaded tables"""
        self.tables.clear()
        self.loaded_files.clear()
        self.localization_tables.clear()

    def get_file_info(self, filename: str) -> Dict[str, Any]:
        """Get file information"""
        filepath = os.path.join(self.base_path, filename)

        if not os.path.exists(filepath):
            return {}

        try:
            stat = os.stat(filepath)
            return {
                'filename': filename,
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'exists': True
            }
        except Exception:
            return {'filename': filename, 'exists': False}

    def validate_all_tables(self) -> Dict[str, List[str]]:
        """Validate all loaded tables"""
        validation_results = {}

        for table_name, table in self.tables.items():
            errors = table.validate()
            if errors:
                validation_results[table_name] = errors

        return validation_results

    def __str__(self) -> str:
        """String representation"""
        return f"Gamefiles({len(self.tables)} tables loaded from '{self.base_path}')"
