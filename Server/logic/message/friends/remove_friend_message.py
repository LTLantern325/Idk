"""
Python conversion of Supercell.Laser.Logic.Message.Friends.RemoveFriendMessage.cs
Remove friend message for unfriending
"""

from ..game_message import GameMessage

class RemoveFriendMessage(GameMessage):
    """Remove friend message for unfriending"""

    def __init__(self):
        """Initialize remove friend message"""
        super().__init__()
        self.friend_id = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 10506

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 1

    def get_friend_id(self) -> int:
        """Get friend account ID to remove"""
        return self.friend_id

    def set_friend_id(self, friend_id: int) -> None:
        """Set friend account ID to remove"""
        self.friend_id = friend_id

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_long(self.friend_id)

    def decode(self) -> None:
        """Decode message from stream"""
        self.friend_id = self.stream.read_v_long()

    def is_valid(self) -> bool:
        """Check if message is valid"""
        return self.friend_id > 0

    def __str__(self) -> str:
        """String representation"""
        return f"RemoveFriendMessage(friend_id={self.friend_id})"
