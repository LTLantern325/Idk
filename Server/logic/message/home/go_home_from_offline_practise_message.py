"""
Python conversion of Supercell.Laser.Logic.Message.Home.GoHomeFromOfflinePractiseMessage.cs
Go home from offline practise message for exiting practice mode
"""

from ..game_message import GameMessage

class GoHomeFromOfflinePractiseMessage(GameMessage):
    """Go home from offline practise message for exiting practice mode"""

    def __init__(self):
        """Initialize go home from offline practise message"""
        super().__init__()

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14480  # Placeholder message type

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def encode(self) -> None:
        """Encode message to stream (empty)"""
        # Go home from offline practise message typically has no data
        pass

    def decode(self) -> None:
        """Decode message from stream (empty)"""
        # Go home from offline practise message typically has no data
        pass

    def __str__(self) -> str:
        """String representation"""
        return "GoHomeFromOfflinePractiseMessage()"
