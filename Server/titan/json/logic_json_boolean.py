"""
Python conversion of Supercell.Laser.Titan.Json.LogicJSONBoolean.cs
JSON boolean node
"""

from .logic_json_node import LogicJSONNode, LogicJSONNodeType

class LogicJSONBoolean(LogicJSONNode):
    """JSON boolean value node"""

    def __init__(self, value: bool):
        """Initialize boolean node"""
        self._value = value

    def is_true(self) -> bool:
        """Check if value is true"""
        return self._value

    def get_value(self) -> bool:
        """Get boolean value"""
        return self._value

    def get_json_node_type(self) -> LogicJSONNodeType:
        """Get node type"""
        return LogicJSONNodeType.BOOLEAN

    def write_to_string(self, builder: list) -> None:
        """Write boolean to string"""
        builder.append("true" if self._value else "false")

    def __eq__(self, other) -> bool:
        """Equality comparison"""
        return isinstance(other, LogicJSONBoolean) and other._value == self._value

    def __hash__(self) -> int:
        """Hash for sets/dicts"""
        return hash(self._value)

    def __bool__(self) -> bool:
        """Boolean conversion"""
        return self._value
