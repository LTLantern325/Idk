"""
Python conversion of Supercell.Laser.Logic.Message.Home.CancelMatchmakingMessage.cs
Cancel matchmaking message for cancelling game search
"""

from ..game_message import GameMessage

class CancelMatchmakingMessage(GameMessage):
    """Cancel matchmaking message for cancelling game search"""

    def __init__(self):
        """Initialize cancel matchmaking message"""
        super().__init__()

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14106

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def encode(self) -> None:
        """Encode message to stream (empty for cancel matchmaking)"""
        # Cancel matchmaking message typically has no data
        pass

    def decode(self) -> None:
        """Decode message from stream (empty for cancel matchmaking)"""
        # Cancel matchmaking message typically has no data
        pass

    def __str__(self) -> str:
        """String representation"""
        return "CancelMatchmakingMessage()"
