"""
Python conversion of Supercell.Laser.Logic.Message.Friends.FriendListMessage.cs
Friend list message for sending friend list data
"""

from typing import List, TYPE_CHECKING
from ..game_message import GameMessage

if TYPE_CHECKING:
    from ...avatar.client_avatar import ClientAvatar

class FriendListMessage(GameMessage):
    """Friend list message for sending friend list data"""

    def __init__(self):
        """Initialize friend list message"""
        super().__init__()
        self.friends = []  # List of friend data

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 20105  # Friend list response

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 1

    def get_friends(self) -> List[dict]:
        """Get friends list"""
        return self.friends.copy()

    def add_friend(self, friend_id: int, friend_name: str, online_status: bool = False) -> None:
        """Add friend to list"""
        friend_data = {
            'id': friend_id,
            'name': friend_name,
            'online': online_status,
            'avatar': None
        }
        self.friends.append(friend_data)

    def get_friend_count(self) -> int:
        """Get number of friends"""
        return len(self.friends)

    def get_online_friend_count(self) -> int:
        """Get number of online friends"""
        return sum(1 for friend in self.friends if friend.get('online', False))

    def clear_friends(self) -> None:
        """Clear all friends"""
        self.friends.clear()

    def encode(self) -> None:
        """Encode message to stream"""
        # Write friend count
        self.stream.write_v_int(len(self.friends))

        # Write each friend
        for friend in self.friends:
            self.stream.write_v_long(friend['id'])
            self.stream.write_string(friend['name'])
            self.stream.write_boolean(friend['online'])

            # Write avatar data (simplified)
            if friend.get('avatar'):
                self.stream.write_boolean(True)
                # friend['avatar'].encode(self.stream)
            else:
                self.stream.write_boolean(False)

    def decode(self) -> None:
        """Decode message from stream"""
        # Read friend count
        count = self.stream.read_v_int()

        # Read each friend
        self.friends.clear()
        for i in range(count):
            friend_id = self.stream.read_v_long()
            friend_name = self.stream.read_string()
            online_status = self.stream.read_boolean()

            # Read avatar data flag
            has_avatar = self.stream.read_boolean()
            if has_avatar:
                # Skip avatar data (simplified)
                pass

            self.add_friend(friend_id, friend_name, online_status)

    def __str__(self) -> str:
        """String representation"""
        online_count = self.get_online_friend_count()
        return f"FriendListMessage({len(self.friends)} friends, {online_count} online)"
