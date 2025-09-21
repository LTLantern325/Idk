"""
Python conversion of Supercell.Laser.Titan.Json.LogicJSONObject.cs
JSON object node
"""

from typing import List, Optional, Dict, Any
from .logic_json_node import LogicJSONNode, LogicJSONNodeType
from .logic_json_boolean import LogicJSONBoolean
from .logic_json_number import LogicJSONNumber
from .logic_json_string import LogicJSONString

class LogicJSONObject(LogicJSONNode):
    """JSON object node"""

    def __init__(self, capacity: int = 20):
        """Initialize object with optional capacity"""
        self._keys: List[str] = []
        self._items: List[LogicJSONNode] = []
        if capacity > 0:
            self._keys.reserve(capacity)
            self._items.reserve(capacity)

    def destruct(self) -> None:
        """Clean up object"""
        self._keys.clear()
        self._items.clear()

    def get(self, key: str) -> Optional[LogicJSONNode]:
        """Get item by key"""
        try:
            index = self._keys.index(key)
            return self._items[index]
        except ValueError:
            return None

    def get_json_array(self, key: str) -> Optional['LogicJSONArray']:
        """Get JSON array by key"""
        node = self.get(key)
        if node and node.get_json_node_type() == LogicJSONNodeType.ARRAY:
            return node
        return None

    def get_json_boolean(self, key: str) -> Optional[LogicJSONBoolean]:
        """Get JSON boolean by key"""
        node = self.get(key)
        if node and node.get_json_node_type() == LogicJSONNodeType.BOOLEAN:
            return node
        return None

    def get_json_number(self, key: str) -> Optional[LogicJSONNumber]:
        """Get JSON number by key"""
        node = self.get(key)
        if node and node.get_json_node_type() == LogicJSONNodeType.NUMBER:
            return node
        return None

    def get_json_object(self, key: str) -> Optional['LogicJSONObject']:
        """Get JSON object by key"""
        node = self.get(key)
        if node and node.get_json_node_type() == LogicJSONNodeType.OBJECT:
            return node
        return None

    def get_json_string(self, key: str) -> Optional[LogicJSONString]:
        """Get JSON string by key"""
        node = self.get(key)
        if node and node.get_json_node_type() == LogicJSONNodeType.STRING:
            return node
        return None

    def put(self, key: str, item: LogicJSONNode) -> None:
        """Put key-value pair"""
        try:
            # Check if key already exists
            index = self._keys.index(key)
            self._items[index] = item  # Replace existing
        except ValueError:
            # New key
            self._keys.append(key)
            self._items.append(item)

    def remove(self, key: str) -> bool:
        """Remove key-value pair"""
        try:
            index = self._keys.index(key)
            del self._keys[index]
            del self._items[index]
            return True
        except ValueError:
            return False

    def get_object_count(self) -> int:
        """Get number of key-value pairs"""
        return len(self._items)

    def get_keys(self) -> List[str]:
        """Get all keys"""
        return self._keys.copy()

    def has_key(self, key: str) -> bool:
        """Check if key exists"""
        return key in self._keys

    def clear(self) -> None:
        """Clear all items"""
        self._keys.clear()
        self._items.clear()

    def get_json_node_type(self) -> LogicJSONNodeType:
        """Get node type"""
        return LogicJSONNodeType.OBJECT

    def write_to_string(self, builder: list) -> None:
        """Write object to string"""
        from .logic_json_parser import LogicJSONParser

        builder.append('{')

        for i, (key, item) in enumerate(zip(self._keys, self._items)):
            if i > 0:
                builder.append(',')

            LogicJSONParser.write_string(key, builder)
            builder.append(':')
            item.write_to_string(builder)

        builder.append('}')

    def to_python_dict(self) -> Dict[str, Any]:
        """Convert to Python dictionary"""
        result = {}
        for key, item in zip(self._keys, self._items):
            if item.get_json_node_type() == LogicJSONNodeType.ARRAY:
                result[key] = item.to_python_list()
            elif item.get_json_node_type() == LogicJSONNodeType.OBJECT:
                result[key] = item.to_python_dict()
            elif item.get_json_node_type() == LogicJSONNodeType.STRING:
                result[key] = item.get_string_value()
            elif item.get_json_node_type() == LogicJSONNodeType.NUMBER:
                result[key] = item.get_int_value()
            elif item.get_json_node_type() == LogicJSONNodeType.BOOLEAN:
                result[key] = item.is_true()
            else:  # NULL
                result[key] = None
        return result

    def __len__(self) -> int:
        """Length operator"""
        return len(self._items)

    def __contains__(self, key: str) -> bool:
        """In operator"""
        return key in self._keys

    def __getitem__(self, key: str) -> Optional[LogicJSONNode]:
        """Index operator"""
        return self.get(key)

    def __setitem__(self, key: str, value: LogicJSONNode) -> None:
        """Index assignment operator"""
        self.put(key, value)
