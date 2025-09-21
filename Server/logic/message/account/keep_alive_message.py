"""
Python conversion of Supercell.Laser.Logic.Message.Account.KeepAliveMessage.cs
Keep alive message for maintaining connection
"""

from ..game_message import GameMessage

class KeepAliveMessage(GameMessage):
    """Keep alive message for maintaining connection"""

    def __init__(self):
        """Initialize keep alive message"""
        super().__init__()

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 10108

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 1

    def encode(self) -> None:
        """Encode message to stream (empty for keep alive)"""
        # Keep alive message typically has no data
        pass

    def decode(self) -> None:
        """Decode message from stream (empty for keep alive)"""
        # Keep alive message typically has no data
        pass

    def __str__(self) -> str:
        """String representation"""
        return "KeepAliveMessage()"
