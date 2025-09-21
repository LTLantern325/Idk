"""
Python conversion of Supercell.Laser.Logic.Message.Friends.AcceptFriendMessage.cs
Accept friend message for accepting friend requests
"""

from ..game_message import GameMessage

class AcceptFriendMessage(GameMessage):
    """Accept friend message for accepting friend requests"""

    def __init__(self):
        """Initialize accept friend message"""
        super().__init__()
        self.friend_id = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 10501

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 1

    def get_friend_id(self) -> int:
        """Get friend ID to accept"""
        return self.friend_id

    def set_friend_id(self, friend_id: int) -> None:
        """Set friend ID to accept"""
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
        return f"AcceptFriendMessage(friend_id={self.friend_id})"
