"""
Python conversion of Supercell.Laser.Logic.Message.Home.AntiAddictionDataUpdatedMessage.cs
Anti addiction data updated message for addiction prevention system
"""

from ..game_message import GameMessage

class AntiAddictionDataUpdatedMessage(GameMessage):
    """Anti addiction data updated message for addiction prevention system"""

    def __init__(self):
        """Initialize anti addiction data updated message"""
        super().__init__()
        self.play_time_minutes = 0
        self.daily_limit_minutes = 0
        self.is_limit_reached = False
        self.warning_threshold = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24717  # Placeholder message type

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_play_time_minutes(self) -> int:
        """Get play time in minutes"""
        return self.play_time_minutes

    def set_play_time_minutes(self, minutes: int) -> None:
        """Set play time in minutes"""
        self.play_time_minutes = max(0, minutes)

    def get_daily_limit_minutes(self) -> int:
        """Get daily limit in minutes"""
        return self.daily_limit_minutes

    def set_daily_limit_minutes(self, minutes: int) -> None:
        """Set daily limit in minutes"""
        self.daily_limit_minutes = max(0, minutes)

    def is_limit_reached(self) -> bool:
        """Check if daily limit is reached"""
        return self.is_limit_reached

    def get_remaining_time_minutes(self) -> int:
        """Get remaining play time in minutes"""
        if self.daily_limit_minutes > 0:
            remaining = self.daily_limit_minutes - self.play_time_minutes
            return max(0, remaining)
        return 999999  # No limit

    def should_show_warning(self) -> bool:
        """Check if should show warning"""
        if self.warning_threshold > 0:
            return self.play_time_minutes >= self.warning_threshold
        return False

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.play_time_minutes)
        self.stream.write_v_int(self.daily_limit_minutes)
        self.stream.write_boolean(self.is_limit_reached)
        self.stream.write_v_int(self.warning_threshold)

    def decode(self) -> None:
        """Decode message from stream"""
        self.play_time_minutes = self.stream.read_v_int()
        self.daily_limit_minutes = self.stream.read_v_int()
        self.is_limit_reached = self.stream.read_boolean()
        self.warning_threshold = self.stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        return (f"AntiAddictionDataUpdatedMessage(played={self.play_time_minutes}min, "
                f"limit={self.daily_limit_minutes}min)")
