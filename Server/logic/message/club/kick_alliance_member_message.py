"""
Python conversion of Supercell.Laser.Logic.Message.Club.KickAllianceMemberMessage.cs
Kick alliance member message for removing members
"""

from ..game_message import GameMessage

class KickAllianceMemberMessage(GameMessage):
    """Kick alliance member message for removing members"""

    def __init__(self):
        """Initialize kick alliance member message"""
        super().__init__()
        self.avatar_id = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14309

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 11

    def get_avatar_id(self) -> int:
        """Get avatar ID of member to kick"""
        return self.avatar_id

    def set_avatar_id(self, avatar_id: int) -> None:
        """Set avatar ID of member to kick"""
        self.avatar_id = avatar_id

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_long(self.avatar_id)

    def decode(self) -> None:
        """Decode message from stream"""
        self.avatar_id = self.stream.read_v_long()

    def is_valid_request(self) -> bool:
        """Check if request is valid"""
        return self.avatar_id > 0

    def __str__(self) -> str:
        """String representation"""
        return f"KickAllianceMemberMessage(avatar_id={self.avatar_id})"
