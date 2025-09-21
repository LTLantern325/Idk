"""
Python conversion of Supercell.Laser.Logic.Message.Club.AllianceOnlineStatusUpdatedMessage.cs
Alliance online status updated message for member status updates
"""

from ..game_message import GameMessage

class AllianceOnlineStatusUpdatedMessage(GameMessage):
    """Alliance online status updated message for member status updates"""

    def __init__(self):
        """Initialize alliance online status updated message"""
        super().__init__()
        self.avatar_id = 0
        self.is_online = False
        self.last_seen_timestamp = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24309  # Placeholder message type

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 11

    def get_avatar_id(self) -> int:
        """Get avatar ID"""
        return self.avatar_id

    def set_avatar_id(self, avatar_id: int) -> None:
        """Set avatar ID"""
        self.avatar_id = avatar_id

    def is_member_online(self) -> bool:
        """Check if member is online"""
        return self.is_online

    def set_online_status(self, online: bool) -> None:
        """Set online status"""
        self.is_online = online

    def get_last_seen_timestamp(self) -> int:
        """Get last seen timestamp"""
        return self.last_seen_timestamp

    def set_last_seen_timestamp(self, timestamp: int) -> None:
        """Set last seen timestamp"""
        self.last_seen_timestamp = timestamp

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_long(self.avatar_id)
        self.stream.write_boolean(self.is_online)
        self.stream.write_v_int(self.last_seen_timestamp)

    def decode(self) -> None:
        """Decode message from stream"""
        self.avatar_id = self.stream.read_v_long()
        self.is_online = self.stream.read_boolean()
        self.last_seen_timestamp = self.stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        status = "online" if self.is_online else "offline"
        return f"AllianceOnlineStatusUpdatedMessage(avatar_id={self.avatar_id}, {status})"
