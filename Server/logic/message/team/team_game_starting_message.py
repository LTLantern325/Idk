"""
Python conversion of Supercell.Laser.Logic.Message.Team.TeamGameStartingMessage.cs
Team game starting message for notifying game start
"""

from ..game_message import GameMessage

class TeamGameStartingMessage(GameMessage):
    """Team game starting message for notifying game start"""

    def __init__(self):
        """Initialize team game starting message"""
        super().__init__()
        self.countdown_seconds = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24360  # Team game starting

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_countdown_seconds(self) -> int:
        """Get countdown seconds"""
        return self.countdown_seconds

    def set_countdown_seconds(self, seconds: int) -> None:
        """Set countdown seconds"""
        self.countdown_seconds = max(0, seconds)

    def is_immediate_start(self) -> bool:
        """Check if game starts immediately"""
        return self.countdown_seconds == 0

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.countdown_seconds)

    def decode(self) -> None:
        """Decode message from stream"""
        self.countdown_seconds = self.stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        if self.is_immediate_start():
            return "TeamGameStartingMessage(immediate)"
        else:
            return f"TeamGameStartingMessage(countdown={self.countdown_seconds}s)"
