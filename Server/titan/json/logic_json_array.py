"""
Python conversion of Supercell.Laser.Titan.Json.LogicJSONArray.cs
JSON array node
"""

from typing import List, Optional
from .logic_json_node import LogicJSONNode, LogicJSONNodeType
from .logic_json_boolean import LogicJSONBoolean
from .logic_json_number import LogicJSONNumber
from .logic_json_string import LogicJSONString

class LogicJSONArray(LogicJSONNode):
    """JSON array node"""

    def __init__(self, capacity: int = 20):
        """Initialize array with optional capacity"""
        self._items: List[LogicJSONNode] = []
        if capacity > 0:
            self._items.reserve(capacity)  # Hint for performance

    def get(self, index: int) -> Optional[LogicJSONNode]:
        """Get item at index"""
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def add(self, item: LogicJSONNode) -> None:
        """Add item to array"""
        if item is not None:
            self._items.append(item)

    def get_json_array(self, index: int) -> Optional['LogicJSONArray']:
        """Get JSON array at index"""
        node = self.get(index)
        if node and node.get_json_node_type() == LogicJSONNodeType.ARRAY:
            return node
        return None

    def get_json_boolean(self, index: int) -> Optional[LogicJSONBoolean]:
        """Get JSON boolean at index"""
        node = self.get(index)
        if node and node.get_json_node_type() == LogicJSONNodeType.BOOLEAN:
            return node
        return None

    def get_json_number(self, index: int) -> Optional[LogicJSONNumber]:
        """Get JSON number at index"""
        node = self.get(index)
        if node and node.get_json_node_type() == LogicJSONNodeType.NUMBER:
            return node
        return None

    def get_json_string(self, index: int) -> Optional[LogicJSONString]:
        """Get JSON string at index"""
        node = self.get(index)
        if node and node.get_json_node_type() == LogicJSONNodeType.STRING:
            return node
        return None

    def size(self) -> int:
        """Get array size"""
        return len(self._items)

    def is_empty(self) -> bool:
        """Check if array is empty"""
        return len(self._items) == 0

    def clear(self) -> None:
        """Clear all items"""
        self._items.clear()

    def remove(self, index: int) -> bool:
        """Remove item at index"""
        if 0 <= index < len(self._items):
            del self._items[index]
            return True
        return False

    def get_json_node_type(self) -> LogicJSONNodeType:
        """Get node type"""
        return LogicJSONNodeType.ARRAY

    def write_to_string(self, builder: list) -> None:
        """Write array to string"""
        builder.append('[')

        for i, item in enumerate(self._items):
            if i > 0:
                builder.append(',')
            item.write_to_string(builder)

        builder.append(']')

    def to_python_list(self) -> list:
        """Convert to Python list"""
        result = []
        for item in self._items:
            if item.get_json_node_type() == LogicJSONNodeType.ARRAY:
                result.append(item.to_python_list())
            elif item.get_json_node_type() == LogicJSONNodeType.OBJECT:
                result.append(item.to_python_dict())
            elif item.get_json_node_type() == LogicJSONNodeType.STRING:
                result.append(item.get_string_value())
            elif item.get_json_node_type() == LogicJSONNodeType.NUMBER:
                result.append(item.get_int_value())
            elif item.get_json_node_type() == LogicJSONNodeType.BOOLEAN:
                result.append(item.is_true())
            else:  # NULL
                result.append(None)
        return result

    def __len__(self) -> int:
        """Length operator"""
        return len(self._items)

    def __getitem__(self, index: int) -> Optional[LogicJSONNode]:
        """Index operator"""
        return self.get(index)

    def __iter__(self):
        """Iterator"""
        return iter(self._items)
