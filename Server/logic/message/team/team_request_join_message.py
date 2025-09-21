"""
Python conversion of Supercell.Laser.Logic.Message.Team.TeamRequestJoinMessage.cs
Team request join message for requesting to join a team
"""

from ..game_message import GameMessage

class TeamRequestJoinMessage(GameMessage):
    """Team request join message for requesting to join a team"""

    def __init__(self):
        """Initialize team request join message"""
        super().__init__()
        self.team_id = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14351

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_team_id(self) -> int:
        """Get team ID to join"""
        return self.team_id

    def set_team_id(self, team_id: int) -> None:
        """Set team ID to join"""
        self.team_id = team_id

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_long(self.team_id)

    def decode(self) -> None:
        """Decode message from stream"""
        self.team_id = self.stream.read_v_long()

    def is_valid_request(self) -> bool:
        """Check if request is valid"""
        return self.team_id > 0

    def __str__(self) -> str:
        """String representation"""
        return f"TeamRequestJoinMessage(team_id={self.team_id})"
