"""
Python conversion of Supercell.Laser.Logic.Message.Home.GoHomeFromMapEditorMessage.cs
Go home from map editor message for exiting map editor
"""

from ..game_message import GameMessage

class GoHomeFromMapEditorMessage(GameMessage):
    """Go home from map editor message for exiting map editor"""

    def __init__(self):
        """Initialize go home from map editor message"""
        super().__init__()

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14479

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def encode(self) -> None:
        """Encode message to stream (empty)"""
        # Go home from map editor message typically has no data
        pass

    def decode(self) -> None:
        """Decode message from stream (empty)"""
        # Go home from map editor message typically has no data
        pass

    def __str__(self) -> str:
        """String representation"""
        return "GoHomeFromMapEditorMessage()"
