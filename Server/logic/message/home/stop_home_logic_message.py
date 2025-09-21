"""
Python conversion of Supercell.Laser.Logic.Message.Home.StopHomeLogicMessage.cs
Stop home logic message for stopping home logic processing
"""

from ..game_message import GameMessage

class StopHomeLogicMessage(GameMessage):
    """Stop home logic message for stopping home logic processing"""

    def __init__(self):
        """Initialize stop home logic message"""
        super().__init__()

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14481  # Placeholder message type

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def encode(self) -> None:
        """Encode message to stream (empty)"""
        # Stop home logic message typically has no data
        pass

    def decode(self) -> None:
        """Decode message from stream (empty)"""
        # Stop home logic message typically has no data
        pass

    def __str__(self) -> str:
        """String representation"""
        return "StopHomeLogicMessage()"
