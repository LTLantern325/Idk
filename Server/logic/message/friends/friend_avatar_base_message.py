"""
Python conversion of Supercell.Laser.Logic.Message.Friends.FriendAvatarBaseMessage.cs
Friend avatar base message for friend avatar data
"""

from typing import TYPE_CHECKING
from ..game_message import GameMessage

if TYPE_CHECKING:
    from ...avatar.client_avatar import ClientAvatar

class FriendAvatarBaseMessage(GameMessage):
    """Friend avatar base message for friend avatar data"""

    def __init__(self):
        """Initialize friend avatar base message"""
        super().__init__()
        self.avatar = None  # ClientAvatar

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 20105  # Base message type for friend avatars

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 1

    def get_avatar(self) -> 'ClientAvatar':
        """Get client avatar"""
        return self.avatar

    def set_avatar(self, avatar: 'ClientAvatar') -> None:
        """Set client avatar"""
        self.avatar = avatar

    def has_avatar(self) -> bool:
        """Check if has avatar data"""
        return self.avatar is not None

    def encode(self) -> None:
        """Encode message to stream"""
        if self.avatar:
            self.avatar.encode(self.stream)
        else:
            # Write empty avatar data
            self.stream.write_v_int(0)

    def decode(self) -> None:
        """Decode message from stream"""
        # In real implementation, would create and decode ClientAvatar
        # For now, just skip the data
        avatar_data_present = self.stream.read_v_int()
        if avatar_data_present > 0:
            # Skip avatar data (simplified)
            pass

    def __str__(self) -> str:
        """String representation"""
        avatar_status = "with avatar" if self.has_avatar() else "no avatar"
        return f"FriendAvatarBaseMessage({avatar_status})"
