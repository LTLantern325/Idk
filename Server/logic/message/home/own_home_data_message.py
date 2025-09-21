"""
Python conversion of Supercell.Laser.Logic.Message.Home.OwnHomeDataMessage.cs
Own home data message for sending player home data
"""

from typing import TYPE_CHECKING
from ..game_message import GameMessage

if TYPE_CHECKING:
    from ...home.client_home import ClientHome
    from ...avatar.client_avatar import ClientAvatar

class OwnHomeDataMessage(GameMessage):
    """Own home data message for sending player home data"""

    def __init__(self):
        """Initialize own home data message"""
        super().__init__()
        self.home = None  # ClientHome
        self.avatar = None  # ClientAvatar

    def get_home(self) -> 'ClientHome':
        """Get client home"""
        return self.home

    def set_home(self, home: 'ClientHome') -> None:
        """Set client home"""
        self.home = home

    def get_avatar(self) -> 'ClientAvatar':
        """Get client avatar"""
        return self.avatar

    def set_avatar(self, avatar: 'ClientAvatar') -> None:
        """Set client avatar"""
        self.avatar = avatar

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24101

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def encode(self) -> None:
        """Encode message to stream"""
        # The original C# has extensive commented-out code
        # This is a simplified version that encodes home and avatar

        if self.home:
            self.home.encode(self.stream)

        if self.avatar:
            self.avatar.encode(self.stream)

        # Write final value
        self.stream.write_v_int(0)

    def decode(self) -> None:
        """Decode message from stream"""
        # Decoding would involve reading home and avatar data
        # This is complex and would require proper ClientHome and ClientAvatar classes
        pass

    def has_home_data(self) -> bool:
        """Check if message has home data"""
        return self.home is not None

    def has_avatar_data(self) -> bool:
        """Check if message has avatar data"""
        return self.avatar is not None

    def is_complete(self) -> bool:
        """Check if message has complete data"""
        return self.home is not None and self.avatar is not None

    def __str__(self) -> str:
        """String representation"""
        home_status = "✓" if self.home else "✗"
        avatar_status = "✓" if self.avatar else "✗"
        return f"OwnHomeDataMessage(home={home_status}, avatar={avatar_status})"
