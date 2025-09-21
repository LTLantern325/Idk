"""
Python conversion of Supercell.Laser.Logic.Message.Team.TeamToggleMemberSideMessage.cs
Team toggle member side message for toggling member side
"""

from ..game_message import GameMessage

class TeamToggleMemberSideMessage(GameMessage):
    """Team toggle member side message for toggling member side"""

    def __init__(self):
        """Initialize team toggle member side message"""
        super().__init__()
        self.member_id = 0
        self.new_side = 0  # 0=team1, 1=team2

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14365

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_member_id(self) -> int:
        """Get member ID"""
        return self.member_id

    def set_member_id(self, member_id: int) -> None:
        """Set member ID"""
        self.member_id = member_id

    def get_new_side(self) -> int:
        """Get new side"""
        return self.new_side

    def set_new_side(self, side: int) -> None:
        """Set new side"""
        self.new_side = side

    def is_team1(self) -> bool:
        """Check if member is on team 1"""
        return self.new_side == 0

    def is_team2(self) -> bool:
        """Check if member is on team 2"""
        return self.new_side == 1

    def get_side_name(self) -> str:
        """Get human-readable side name"""
        return "Team 1" if self.is_team1() else "Team 2"

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_long(self.member_id)
        self.stream.write_v_int(self.new_side)

    def decode(self) -> None:
        """Decode message from stream"""
        self.member_id = self.stream.read_v_long()
        self.new_side = self.stream.read_v_int()

    def is_valid_toggle(self) -> bool:
        """Check if toggle is valid"""
        return self.member_id > 0 and self.new_side in [0, 1]

    def __str__(self) -> str:
        """String representation"""
        return f"TeamToggleMemberSideMessage(member_id={self.member_id}, {self.get_side_name()})"
