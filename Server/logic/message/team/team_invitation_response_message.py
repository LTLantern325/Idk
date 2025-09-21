"""
Python conversion of Supercell.Laser.Logic.Message.Team.TeamInvitationResponseMessage.cs
Team invitation response message for responding to team invitations
"""

from ..game_message import GameMessage

class TeamInvitationResponseMessage(GameMessage):
    """Team invitation response message for responding to team invitations"""

    def __init__(self):
        """Initialize team invitation response message"""
        super().__init__()
        self.team_id = 0
        self.accepted = False

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14357

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_team_id(self) -> int:
        """Get team ID"""
        return self.team_id

    def set_team_id(self, team_id: int) -> None:
        """Set team ID"""
        self.team_id = team_id

    def is_accepted(self) -> bool:
        """Check if invitation was accepted"""
        return self.accepted

    def set_accepted(self, accepted: bool) -> None:
        """Set accepted status"""
        self.accepted = accepted

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_long(self.team_id)
        self.stream.write_boolean(self.accepted)

    def decode(self) -> None:
        """Decode message from stream"""
        self.team_id = self.stream.read_v_long()
        self.accepted = self.stream.read_boolean()

    def __str__(self) -> str:
        """String representation"""
        response = "accepted" if self.accepted else "declined"
        return f"TeamInvitationResponseMessage(team_id={self.team_id}, {response})"
