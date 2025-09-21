"""
Python conversion of Supercell.Laser.Logic.Message.Home.GoHomeMessage.cs
Go home message for returning to home screen
"""

from ..game_message import GameMessage

class GoHomeMessage(GameMessage):
    """Go home message for returning to home screen"""

    def __init__(self):
        """Initialize go home message"""
        super().__init__()

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14456

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def encode(self) -> None:
        """Encode message to stream (empty for go home)"""
        # Go home message typically has no data
        pass

    def decode(self) -> None:
        """Decode message from stream (empty for go home)"""
        # Go home message typically has no data
        pass

    def __str__(self) -> str:
        """String representation"""
        return "GoHomeMessage()"
