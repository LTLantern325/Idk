"""
Python conversion of Supercell.Laser.Titan.Json.LogicJSONNode.cs
Base class for JSON nodes
"""

from abc import ABC, abstractmethod
from enum import IntEnum

class LogicJSONNodeType(IntEnum):
    """JSON node types"""
    ARRAY = 1
    OBJECT = 2
    NUMBER = 3
    STRING = 4
    BOOLEAN = 5
    NULL = 6

class LogicJSONNode(ABC):
    """Abstract base class for JSON nodes"""

    @abstractmethod
    def get_json_node_type(self) -> LogicJSONNodeType:
        """Get the JSON node type"""
        pass

    @abstractmethod
    def write_to_string(self, builder: list) -> None:
        """Write node to string builder"""
        pass

    def to_json_string(self) -> str:
        """Convert node to JSON string"""
        builder = []
        self.write_to_string(builder)
        return ''.join(builder)

    def __str__(self) -> str:
        """String representation"""
        return self.to_json_string()
