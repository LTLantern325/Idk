"""
Python conversion of Supercell.Laser.Logic.Message.Account.AnalyticEventMessage.cs
Analytic event message for tracking user analytics
"""

from ..game_message import GameMessage

class AnalyticEventMessage(GameMessage):
    """Analytic event message for tracking user analytics"""

    def __init__(self):
        """Initialize analytic event message"""
        super().__init__()
        self.event_name = ""     # str1 in original
        self.event_data = ""     # str2 in original

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 10110

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 1

    def get_event_name(self) -> str:
        """Get event name"""
        return self.event_name

    def set_event_name(self, name: str) -> None:
        """Set event name"""
        self.event_name = name

    def get_event_data(self) -> str:
        """Get event data"""
        return self.event_data

    def set_event_data(self, data: str) -> None:
        """Set event data"""
        self.event_data = data

    def decode(self) -> None:
        """Decode message from stream"""
        self.event_name = self.stream.read_string()
        self.event_data = self.stream.read_string()

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_string(self.event_name)
        self.stream.write_string(self.event_data)

    def has_event_data(self) -> bool:
        """Check if has event data"""
        return self.event_data != ""

    def is_valid_event(self) -> bool:
        """Check if event is valid"""
        return self.event_name != ""

    def __str__(self) -> str:
        """String representation"""
        return f"AnalyticEventMessage('{self.event_name}', data_len={len(self.event_data)})"
