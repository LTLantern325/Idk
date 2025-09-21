"""
Python conversion of Supercell.Laser.Logic.Data.Helper.LogicData.cs
Base logic data class for all data objects
"""

from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .data_table import DataTable, Row

class LogicData:
    """Base logic data class for all data objects"""

    def __init__(self):
        """Initialize logic data"""
        self.global_id = 0
        self.instance_id = 0
        self.class_id = 0
        self.data_type = 0

    def get_global_id(self) -> int:
        """Get global ID"""
        return self.global_id

    def set_global_id(self, global_id: int) -> None:
        """Set global ID"""
        self.global_id = global_id

    def get_instance_id(self) -> int:
        """Get instance ID"""
        return self.instance_id

    def set_instance_id(self, instance_id: int) -> None:
        """Set instance ID"""
        self.instance_id = instance_id

    def get_class_id(self) -> int:
        """Get class ID"""
        return self.class_id

    def set_class_id(self, class_id: int) -> None:
        """Set class ID"""
        self.class_id = class_id

    def get_data_type(self) -> int:
        """Get data type"""
        return self.data_type

    def set_data_type(self, data_type: int) -> None:
        """Set data type"""
        self.data_type = data_type

    def create_global_id(self) -> int:
        """Create global ID from class and instance ID"""
        return (self.class_id << 20) | self.instance_id

    def is_valid(self) -> bool:
        """Check if data is valid"""
        return self.instance_id >= 0 and self.class_id >= 0

    @staticmethod
    def load_data(obj: Any, obj_type: type, row: 'Row') -> None:
        """Load data from row into object (static method from C#)"""
        if obj is None or row is None:
            return

        # This is a simplified version - the original C# uses reflection
        # to automatically populate object properties from row data

        # Get all attributes that match column names
        if hasattr(row, 'get_columns'):
            for column in row.get_columns():
                if hasattr(obj, column.lower()):
                    value = row.get_value(column)
                    if value is not None:
                        try:
                            setattr(obj, column.lower(), value)
                        except:
                            pass  # Ignore conversion errors

    def load_from_row(self, row: 'Row', data_table: 'DataTable') -> None:
        """Load data from data table row"""
        if row is None:
            return

        # Load basic properties
        self.instance_id = row.get_value('InstanceId', 0)
        self.class_id = row.get_value('ClassId', 0) 
        self.data_type = row.get_value('DataType', 0)

        # Create global ID
        self.global_id = self.create_global_id()

        # Load additional data using static method
        LogicData.load_data(self, type(self), row)

    def clone(self) -> 'LogicData':
        """Create a copy of this data"""
        cloned = LogicData()
        cloned.global_id = self.global_id
        cloned.instance_id = self.instance_id
        cloned.class_id = self.class_id
        cloned.data_type = self.data_type
        return cloned

    def __str__(self) -> str:
        """String representation"""
        return (f"LogicData(global_id={self.global_id}, "
                f"class_id={self.class_id}, instance_id={self.instance_id})")

    def __eq__(self, other) -> bool:
        """Equality comparison"""
        if not isinstance(other, LogicData):
            return False
        return self.global_id == other.global_id

    def __hash__(self) -> int:
        """Hash function"""
        return hash(self.global_id)
