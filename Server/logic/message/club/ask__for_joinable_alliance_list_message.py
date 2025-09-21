"""
Python conversion of Supercell.Laser.Logic.Message.Club.AskForJoinableAllianceListMessage.cs
Ask for joinable alliance list message for requesting joinable alliances
"""

from ..game_message import GameMessage

class AskForJoinableAllianceListMessage(GameMessage):
    """Ask for joinable alliance list message for requesting joinable alliances"""

    def __init__(self):
        """Initialize ask for joinable alliance list message"""
        super().__init__()

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14303

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 11

    def encode(self) -> None:
        """Encode message to stream (empty)"""
        # Ask for joinable alliance list message typically has no data
        pass

    def decode(self) -> None:
        """Decode message from stream (empty)"""
        # Ask for joinable alliance list message typically has no data
        pass

    def __str__(self) -> str:
        """String representation"""
        return "AskForJoinableAllianceListMessage()"
