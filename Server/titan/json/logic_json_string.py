"""
Python conversion of Supercell.Laser.Titan.Json.LogicJSONString.cs
JSON string node
"""

from .logic_json_node import LogicJSONNode, LogicJSONNodeType

class LogicJSONString(LogicJSONNode):
    """JSON string value node"""

    def __init__(self, value: str):
        """Initialize string node"""
        self._value = str(value) if value is not None else ""

    def get_string_value(self) -> str:
        """Get string value"""
        return self._value

    def set_string_value(self, value: str) -> None:
        """Set string value"""
        self._value = str(value) if value is not None else ""

    def get_json_node_type(self) -> LogicJSONNodeType:
        """Get node type"""
        return LogicJSONNodeType.STRING

    def write_to_string(self, builder: list) -> None:
        """Write string to string builder"""
        # Use the parser's write_string method for proper escaping
        from .logic_json_parser import LogicJSONParser
        LogicJSONParser.write_string(self._value, builder)

    def __eq__(self, other) -> bool:
        """Equality comparison"""
        return isinstance(other, LogicJSONString) and other._value == self._value

    def __hash__(self) -> int:
        """Hash for sets/dicts"""
        return hash(self._value)

    def __str__(self) -> str:
        """String conversion"""
        return self._value
