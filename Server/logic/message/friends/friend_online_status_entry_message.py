"""
Python conversion of Supercell.Laser.Logic.Message.Friends.FriendOnlineStatusEntryMessage.cs
Friend online status entry message for friend status updates
"""

from ..game_message import GameMessage

class FriendOnlineStatusEntryMessage(GameMessage):
    """Friend online status entry message for friend status updates"""

    def __init__(self):
        """Initialize friend online status entry message"""
        super().__init__()
        self.friend_id = 0
        self.online_status = False
        self.last_seen_timestamp = 0
        self.current_location = ""

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 20107  # Friend status entry

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 1

    def get_friend_id(self) -> int:
        """Get friend ID"""
        return self.friend_id

    def set_friend_id(self, friend_id: int) -> None:
        """Set friend ID"""
        self.friend_id = friend_id

    def is_online(self) -> bool:
        """Check if friend is online"""
        return self.online_status

    def set_online_status(self, online: bool) -> None:
        """Set online status"""
        self.online_status = online

    def get_last_seen_timestamp(self) -> int:
        """Get last seen timestamp"""
        return self.last_seen_timestamp

    def set_last_seen_timestamp(self, timestamp: int) -> None:
        """Set last seen timestamp"""
        self.last_seen_timestamp = timestamp

    def get_current_location(self) -> str:
        """Get current location/activity"""
        return self.current_location

    def set_current_location(self, location: str) -> None:
        """Set current location/activity"""
        self.current_location = location

    def has_location_info(self) -> bool:
        """Check if has location information"""
        return self.current_location != ""

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_long(self.friend_id)
        self.stream.write_boolean(self.online_status)
        self.stream.write_v_int(self.last_seen_timestamp)
        self.stream.write_string(self.current_location)

    def decode(self) -> None:
        """Decode message from stream"""
        self.friend_id = self.stream.read_v_long()
        self.online_status = self.stream.read_boolean()
        self.last_seen_timestamp = self.stream.read_v_int()
        self.current_location = self.stream.read_string()

    def __str__(self) -> str:
        """String representation"""
        status = "online" if self.online_status else "offline"
        location_info = f" at {self.current_location}" if self.has_location_info() else ""
        return f"FriendOnlineStatusEntryMessage(id={self.friend_id}, {status}{location_info})"
