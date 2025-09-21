"""
Python conversion of Supercell.Laser.Logic.Message.Club.LeaveAllianceMessage.cs
Leave alliance message for leaving current alliance
"""

from ..game_message import GameMessage

class LeaveAllianceMessage(GameMessage):
    """Leave alliance message for leaving current alliance"""

    def __init__(self):
        """Initialize leave alliance message"""
        super().__init__()

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14306

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 11

    def encode(self) -> None:
        """Encode message to stream (empty)"""
        # Leave alliance message typically has no data
        pass

    def decode(self) -> None:
        """Decode message from stream (empty)"""
        # Leave alliance message typically has no data
        pass

    def __str__(self) -> str:
        """String representation"""
        return "LeaveAllianceMessage()"
