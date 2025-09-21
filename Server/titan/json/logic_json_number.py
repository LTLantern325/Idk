"""
Python conversion of Supercell.Laser.Titan.Json.LogicJSONNumber.cs
JSON number node
"""

from .logic_json_node import LogicJSONNode, LogicJSONNodeType

class LogicJSONNumber(LogicJSONNode):
    """JSON number value node"""

    def __init__(self, value: int = 0):
        """Initialize number node"""
        self._value = int(value)

    def get_int_value(self) -> int:
        """Get integer value"""
        return self._value

    def set_int_value(self, value: int) -> None:
        """Set integer value"""
        self._value = int(value)

    def get_float_value(self) -> float:
        """Get float value"""
        return float(self._value)

    def get_json_node_type(self) -> LogicJSONNodeType:
        """Get node type"""
        return LogicJSONNodeType.NUMBER

    def write_to_string(self, builder: list) -> None:
        """Write number to string"""
        builder.append(str(self._value))

    def __eq__(self, other) -> bool:
        """Equality comparison"""
        return isinstance(other, LogicJSONNumber) and other._value == self._value

    def __hash__(self) -> int:
        """Hash for sets/dicts"""
        return hash(self._value)

    def __int__(self) -> int:
        """Integer conversion"""
        return self._value

    def __float__(self) -> float:
        """Float conversion"""
        return float(self._value)
