"""
Python conversion of Supercell.Laser.Logic.Message.Friends.FriendListUpdateMessage.cs
Friend list update message for friend list changes
"""

from ..game_message import GameMessage

class FriendListUpdateMessage(GameMessage):
    """Friend list update message for friend list changes"""

    def __init__(self):
        """Initialize friend list update message"""
        super().__init__()
        self.update_type = 0  # 0=added, 1=removed, 2=status_changed
        self.friend_id = 0
        self.friend_name = ""
        self.online_status = False

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 20106  # Friend list update

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 1

    def get_update_type(self) -> int:
        """Get update type"""
        return self.update_type

    def set_update_type(self, update_type: int) -> None:
        """Set update type"""
        self.update_type = update_type

    def is_friend_added(self) -> bool:
        """Check if friend was added"""
        return self.update_type == 0

    def is_friend_removed(self) -> bool:
        """Check if friend was removed"""
        return self.update_type == 1

    def is_status_changed(self) -> bool:
        """Check if friend status changed"""
        return self.update_type == 2

    def get_update_type_name(self) -> str:
        """Get human-readable update type"""
        if self.update_type == 0:
            return "Added"
        elif self.update_type == 1:
            return "Removed"
        elif self.update_type == 2:
            return "Status Changed"
        else:
            return "Unknown"

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.update_type)
        self.stream.write_v_long(self.friend_id)
        self.stream.write_string(self.friend_name)
        self.stream.write_boolean(self.online_status)

    def decode(self) -> None:
        """Decode message from stream"""
        self.update_type = self.stream.read_v_int()
        self.friend_id = self.stream.read_v_long()
        self.friend_name = self.stream.read_string()
        self.online_status = self.stream.read_boolean()

    def __str__(self) -> str:
        """String representation"""
        status = "online" if self.online_status else "offline"
        return (f"FriendListUpdateMessage({self.get_update_type_name()}, "
                f"'{self.friend_name}', {status})")
