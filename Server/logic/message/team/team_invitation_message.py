"""
Python conversion of Supercell.Laser.Logic.Message.Team.TeamInvitationMessage.cs
Team invitation message for team invitations
"""

from ..game_message import GameMessage

class TeamInvitationMessage(GameMessage):
    """Team invitation message for team invitations"""

    def __init__(self):
        """Initialize team invitation message"""
        super().__init__()
        self.team_id = 0
        self.team_name = ""
        self.inviter_id = 0
        self.inviter_name = ""
        self.game_mode = 0
        self.map_id = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24356  # Team invitation

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_team_id(self) -> int:
        """Get team ID"""
        return self.team_id

    def set_team_id(self, team_id: int) -> None:
        """Set team ID"""
        self.team_id = team_id

    def get_team_name(self) -> str:
        """Get team name"""
        return self.team_name

    def set_team_name(self, name: str) -> None:
        """Set team name"""
        self.team_name = name

    def get_inviter_name(self) -> str:
        """Get inviter name"""
        return self.inviter_name

    def set_inviter_name(self, name: str) -> None:
        """Set inviter name"""
        self.inviter_name = name

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_long(self.team_id)
        self.stream.write_string(self.team_name)
        self.stream.write_v_long(self.inviter_id)
        self.stream.write_string(self.inviter_name)
        self.stream.write_v_int(self.game_mode)
        self.stream.write_v_int(self.map_id)

    def decode(self) -> None:
        """Decode message from stream"""
        self.team_id = self.stream.read_v_long()
        self.team_name = self.stream.read_string()
        self.inviter_id = self.stream.read_v_long()
        self.inviter_name = self.stream.read_string()
        self.game_mode = self.stream.read_v_int()
        self.map_id = self.stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        return f"TeamInvitationMessage(team='{self.team_name}', from='{self.inviter_name}')"
