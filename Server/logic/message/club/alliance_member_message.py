"""
Python conversion of Supercell.Laser.Logic.Message.Club.AllianceMemberMessage.cs
Alliance member message for alliance member information
"""

from typing import TYPE_CHECKING
from ..game_message import GameMessage

if TYPE_CHECKING:
    from ...club.alliance_member import AllianceMember

class AllianceMemberMessage(GameMessage):
    """Alliance member message for alliance member information"""

    def __init__(self):
        """Initialize alliance member message"""
        super().__init__()
        self.avatar_id = 0
        self.entry = None  # AllianceMember object

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24308

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 11

    def get_avatar_id(self) -> int:
        """Get avatar ID"""
        return self.avatar_id

    def set_avatar_id(self, avatar_id: int) -> None:
        """Set avatar ID"""
        self.avatar_id = avatar_id

    def get_entry(self) -> 'AllianceMember':
        """Get alliance member entry"""
        return self.entry

    def set_entry(self, entry: 'AllianceMember') -> None:
        """Set alliance member entry"""
        self.entry = entry

    def has_member_data(self) -> bool:
        """Check if has member data"""
        return self.entry is not None

    def encode(self) -> None:
        """Encode message to stream"""
        # Original C# code: Stream.WriteLong(AvatarId);
        self.stream.write_long(self.avatar_id)

        if self.entry:
            # Entry.Encode(Stream);
            self.entry.encode(self.stream)
        else:
            # Write empty member data
            self.stream.write_v_int(0)

    def decode(self) -> None:
        """Decode message from stream"""
        self.avatar_id = self.stream.read_long()

        # In real implementation, would decode AllianceMember
        # For now, just mark as having data
        member_data = self.stream.read_v_int()
        if member_data > 0:
            # Skip member data (simplified)
            pass

    def __str__(self) -> str:
        """String representation"""
        member_status = "with member" if self.has_member_data() else "no member"
        return f"AllianceMemberMessage(avatar_id={self.avatar_id}, {member_status})"
