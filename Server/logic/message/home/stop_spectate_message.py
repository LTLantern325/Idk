"""
Python conversion of Supercell.Laser.Logic.Message.Home.StopSpectateMessage.cs
Stop spectate message for stopping spectating
"""

from ..game_message import GameMessage

class StopSpectateMessage(GameMessage):
    """Stop spectate message for stopping spectating"""

    def __init__(self):
        """Initialize stop spectate message"""
        super().__init__()

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14105

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def encode(self) -> None:
        """Encode message to stream (empty)"""
        # Stop spectate message typically has no data
        pass

    def decode(self) -> None:
        """Decode message from stream (empty)"""
        # Stop spectate message typically has no data
        pass

    def __str__(self) -> str:
        """String representation"""
        return "StopSpectateMessage()"
