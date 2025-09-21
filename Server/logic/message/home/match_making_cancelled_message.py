"""
Python conversion of Supercell.Laser.Logic.Message.Home.MatchMakingCancelledMessage.cs
Match making cancelled message for matchmaking cancellation
"""

from ..game_message import GameMessage

class MatchMakingCancelledMessage(GameMessage):
    """Match making cancelled message for matchmaking cancellation"""

    def __init__(self):
        """Initialize match making cancelled message"""
        super().__init__()
        self.reason = 0  # 0=user_cancelled, 1=timeout, 2=server_error

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 20406  # Match making cancelled

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_reason(self) -> int:
        """Get cancellation reason"""
        return self.reason

    def set_reason(self, reason: int) -> None:
        """Set cancellation reason"""
        self.reason = reason

    def is_user_cancelled(self) -> bool:
        """Check if user cancelled"""
        return self.reason == 0

    def is_timeout(self) -> bool:
        """Check if cancelled due to timeout"""
        return self.reason == 1

    def is_server_error(self) -> bool:
        """Check if cancelled due to server error"""
        return self.reason == 2

    def get_reason_name(self) -> str:
        """Get human-readable reason name"""
        reasons = {0: "User Cancelled", 1: "Timeout", 2: "Server Error"}
        return reasons.get(self.reason, "Unknown")

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.reason)

    def decode(self) -> None:
        """Decode message from stream"""
        self.reason = self.stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        return f"MatchMakingCancelledMessage({self.get_reason_name()})"
