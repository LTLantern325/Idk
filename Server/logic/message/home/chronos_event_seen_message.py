"""
Python conversion of Supercell.Laser.Logic.Message.Home.ChronosEventSeenMessage.cs
Chronos event seen message for marking events as seen
"""

from ..game_message import GameMessage

class ChronosEventSeenMessage(GameMessage):
    """Chronos event seen message for marking events as seen"""

    def __init__(self):
        """Initialize chronos event seen message"""
        super().__init__()
        self.event_id = 0
        self.event_type = 0
        self.timestamp_seen = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14770  # Placeholder message type

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_event_id(self) -> int:
        """Get event ID"""
        return self.event_id

    def set_event_id(self, event_id: int) -> None:
        """Set event ID"""
        self.event_id = event_id

    def get_event_type(self) -> int:
        """Get event type"""
        return self.event_type

    def set_event_type(self, event_type: int) -> None:
        """Set event type"""
        self.event_type = event_type

    def get_timestamp_seen(self) -> int:
        """Get timestamp when event was seen"""
        return self.timestamp_seen

    def set_timestamp_seen(self, timestamp: int) -> None:
        """Set timestamp when event was seen"""
        self.timestamp_seen = timestamp

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.event_id)
        self.stream.write_v_int(self.event_type)
        self.stream.write_v_int(self.timestamp_seen)

    def decode(self) -> None:
        """Decode message from stream"""
        self.event_id = self.stream.read_v_int()
        self.event_type = self.stream.read_v_int()
        self.timestamp_seen = self.stream.read_v_int()

    def is_valid_event(self) -> bool:
        """Check if event data is valid"""
        return self.event_id > 0 and self.timestamp_seen > 0

    def __str__(self) -> str:
        """String representation"""
        return f"ChronosEventSeenMessage(event_id={self.event_id}, type={self.event_type})"
