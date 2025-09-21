"""
Python conversion of Supercell.Laser.Logic.Message.Team.TeamChangeMemberSettingsMessage.cs
Team change member settings message for changing member settings
"""

from ..game_message import GameMessage

class TeamChangeMemberSettingsMessage(GameMessage):
    """Team change member settings message for changing member settings"""

    def __init__(self):
        """Initialize team change member settings message"""
        super().__init__()
        self.member_id = 0
        self.new_role = 0  # 0=member, 1=admin, 2=leader
        self.kick_member = False

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14355

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_member_id(self) -> int:
        """Get member ID"""
        return self.member_id

    def set_member_id(self, member_id: int) -> None:
        """Set member ID"""
        self.member_id = member_id

    def get_new_role(self) -> int:
        """Get new role"""
        return self.new_role

    def set_new_role(self, role: int) -> None:
        """Set new role"""
        self.new_role = role

    def is_kick_member(self) -> bool:
        """Check if kicking member"""
        return self.kick_member

    def set_kick_member(self, kick: bool) -> None:
        """Set kick member flag"""
        self.kick_member = kick

    def get_role_name(self) -> str:
        """Get human-readable role name"""
        roles = {0: "Member", 1: "Admin", 2: "Leader"}
        return roles.get(self.new_role, "Unknown")

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_long(self.member_id)
        self.stream.write_v_int(self.new_role)
        self.stream.write_boolean(self.kick_member)

    def decode(self) -> None:
        """Decode message from stream"""
        self.member_id = self.stream.read_v_long()
        self.new_role = self.stream.read_v_int()
        self.kick_member = self.stream.read_boolean()

    def __str__(self) -> str:
        """String representation"""
        if self.kick_member:
            return f"TeamChangeMemberSettingsMessage(kick member_id={self.member_id})"
        else:
            return f"TeamChangeMemberSettingsMessage(member_id={self.member_id}, role={self.get_role_name()})"
