"""
Python conversion of Supercell.Laser.Logic.Message.Team.TeamLeaveMessage.cs
Team leave message for leaving a team
"""

from ..game_message import GameMessage

class TeamLeaveMessage(GameMessage):
    """Team leave message for leaving a team"""

    def __init__(self):
        """Initialize team leave message"""
        super().__init__()

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14353

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def encode(self) -> None:
        """Encode message to stream (empty)"""
        # Team leave message typically has no data
        pass

    def decode(self) -> None:
        """Decode message from stream (empty)"""
        # Team leave message typically has no data
        pass

    def __str__(self) -> str:
        """String representation"""
        return "TeamLeaveMessage()"
