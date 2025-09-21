"""
Python conversion of Supercell.Laser.Logic.Message.Account.KeepAliveServerMessage.cs
Keep alive server message response (simplified version)
"""

from ..game_message import GameMessage

class KeepAliveServerMessage(GameMessage):
    """Keep alive server message response"""

    def __init__(self):
        """Initialize keep alive server message"""
        super().__init__()

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 20108  # Server response

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 1

    def encode(self) -> None:
        """Encode message to stream (empty for keep alive)"""
        # Keep alive server message typically has no data
        pass

    def decode(self) -> None:
        """Decode message from stream (empty for keep alive)"""
        # Keep alive server message typically has no data  
        pass

    def __str__(self) -> str:
        """String representation"""
        return "KeepAliveServerMessage()"
