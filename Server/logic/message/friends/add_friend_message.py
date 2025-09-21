"""
Python conversion of Supercell.Laser.Logic.Message.Friends.AddFriendMessage.cs
Add friend message for friend requests
"""

from ..game_message import GameMessage

class AddFriendMessage(GameMessage):
    """Add friend message for friend requests"""

    def __init__(self):
        """Initialize add friend message"""
        super().__init__()
        self.friend_id = 0
        self.friend_name = ""

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 10502

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 1

    def get_friend_id(self) -> int:
        """Get friend account ID"""
        return self.friend_id

    def set_friend_id(self, friend_id: int) -> None:
        """Set friend account ID"""
        self.friend_id = friend_id

    def get_friend_name(self) -> str:
        """Get friend name"""
        return self.friend_name

    def set_friend_name(self, name: str) -> None:
        """Set friend name"""
        self.friend_name = name

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_long(self.friend_id)
        self.stream.write_string(self.friend_name)

    def decode(self) -> None:
        """Decode message from stream"""
        self.friend_id = self.stream.read_v_long()
        self.friend_name = self.stream.read_string()

    def is_valid(self) -> bool:
        """Check if message is valid"""
        return self.friend_id > 0 and self.friend_name != ""

    def __str__(self) -> str:
        """String representation"""
        return f"AddFriendMessage(id={self.friend_id}, name='{self.friend_name}')"
