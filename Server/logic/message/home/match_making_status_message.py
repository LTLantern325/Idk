"""
Python conversion of Supercell.Laser.Logic.Message.Home.MatchMakingStatusMessage.cs
Match making status message for matchmaking status updates
"""

from ..game_message import GameMessage

class MatchMakingStatusMessage(GameMessage):
    """Match making status message for matchmaking status updates"""

    def __init__(self):
        """Initialize match making status message"""
        super().__init__()
        self.status = 0  # 0=searching, 1=found, 2=cancelled, 3=failed
        self.estimated_wait_time = 0
        self.players_found = 0
        self.players_needed = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 20405  # Match making status

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_status(self) -> int:
        """Get matchmaking status"""
        return self.status

    def set_status(self, status: int) -> None:
        """Set matchmaking status"""
        self.status = status

    def is_searching(self) -> bool:
        """Check if currently searching"""
        return self.status == 0

    def is_found(self) -> bool:
        """Check if match found"""
        return self.status == 1

    def is_cancelled(self) -> bool:
        """Check if matchmaking was cancelled"""
        return self.status == 2

    def is_failed(self) -> bool:
        """Check if matchmaking failed"""
        return self.status == 3

    def get_status_name(self) -> str:
        """Get human-readable status name"""
        statuses = {0: "Searching", 1: "Found", 2: "Cancelled", 3: "Failed"}
        return statuses.get(self.status, "Unknown")

    def get_progress_percentage(self) -> float:
        """Get matchmaking progress percentage"""
        if self.players_needed == 0:
            return 0.0
        return (self.players_found / self.players_needed) * 100.0

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.status)
        self.stream.write_v_int(self.estimated_wait_time)
        self.stream.write_v_int(self.players_found)
        self.stream.write_v_int(self.players_needed)

    def decode(self) -> None:
        """Decode message from stream"""
        self.status = self.stream.read_v_int()
        self.estimated_wait_time = self.stream.read_v_int()
        self.players_found = self.stream.read_v_int()
        self.players_needed = self.stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        if self.is_searching():
            progress = f" ({self.players_found}/{self.players_needed})"
            return f"MatchMakingStatusMessage({self.get_status_name()}{progress})"
        else:
            return f"MatchMakingStatusMessage({self.get_status_name()})"
