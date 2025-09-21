"""
Python conversion of Supercell.Laser.Logic.Message.Home.PlayerProfileMessage.cs
Player profile message for sending player profile data
"""

from typing import TYPE_CHECKING
from ..game_message import GameMessage

if TYPE_CHECKING:
    from ...avatar.client_avatar import ClientAvatar

class PlayerProfileMessage(GameMessage):
    """Player profile message for sending player profile data"""

    def __init__(self):
        """Initialize player profile message"""
        super().__init__()
        self.player_id = 0
        self.player_avatar = None  # ClientAvatar

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24113  # Player profile response

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_player_id(self) -> int:
        """Get player ID"""
        return self.player_id

    def set_player_id(self, player_id: int) -> None:
        """Set player ID"""
        self.player_id = player_id

    def get_player_avatar(self) -> 'ClientAvatar':
        """Get player avatar"""
        return self.player_avatar

    def set_player_avatar(self, avatar: 'ClientAvatar') -> None:
        """Set player avatar"""
        self.player_avatar = avatar

    def has_avatar_data(self) -> bool:
        """Check if has avatar data"""
        return self.player_avatar is not None

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_long(self.player_id)

        if self.player_avatar:
            self.player_avatar.encode(self.stream)
        else:
            # Write empty avatar data
            self.stream.write_v_int(0)

    def decode(self) -> None:
        """Decode message from stream"""
        self.player_id = self.stream.read_v_long()

        # In real implementation, would decode ClientAvatar
        # For now, just mark as having data
        avatar_data = self.stream.read_v_int()
        if avatar_data > 0:
            # Skip avatar data (simplified)
            pass

    def __str__(self) -> str:
        """String representation"""
        avatar_status = "with avatar" if self.has_avatar_data() else "no avatar"
        return f"PlayerProfileMessage(player_id={self.player_id}, {avatar_status})"
