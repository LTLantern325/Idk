"""
Python conversion of Supercell.Laser.Titan.Json.LogicJSONNull.cs
JSON null node
"""

from .logic_json_node import LogicJSONNode, LogicJSONNodeType

class LogicJSONNull(LogicJSONNode):
    """JSON null value node"""

    def get_json_node_type(self) -> LogicJSONNodeType:
        """Get node type"""
        return LogicJSONNodeType.NULL

    def write_to_string(self, builder: list) -> None:
        """Write null to string"""
        builder.append("null")

    def __eq__(self, other) -> bool:
        """Equality comparison"""
        return isinstance(other, LogicJSONNull)

    def __hash__(self) -> int:
        """Hash for sets/dicts"""
        return hash("null")
