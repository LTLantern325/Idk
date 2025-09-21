"""
Python conversion of Supercell.Laser.Logic.Message.Team.TeamCreateMessage.cs
Team create message for creating a team
"""

from ..game_message import GameMessage

class TeamCreateMessage(GameMessage):
    """Team create message for creating a team"""

    def __init__(self):
        """Initialize team create message"""
        super().__init__()
        self.game_mode = 0
        self.map_id = 0
        self.team_type = 0  # 0=normal, 1=ranked

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14350

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_game_mode(self) -> int:
        """Get game mode"""
        return self.game_mode

    def set_game_mode(self, mode: int) -> None:
        """Set game mode"""
        self.game_mode = mode

    def get_map_id(self) -> int:
        """Get map ID"""
        return self.map_id

    def set_map_id(self, map_id: int) -> None:
        """Set map ID"""
        self.map_id = map_id

    def get_team_type(self) -> int:
        """Get team type"""
        return self.team_type

    def set_team_type(self, team_type: int) -> None:
        """Set team type"""
        self.team_type = team_type

    def is_ranked_team(self) -> bool:
        """Check if team is ranked"""
        return self.team_type == 1

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.game_mode)
        self.stream.write_v_int(self.map_id)
        self.stream.write_v_int(self.team_type)

    def decode(self) -> None:
        """Decode message from stream"""
        self.game_mode = self.stream.read_v_int()
        self.map_id = self.stream.read_v_int()
        self.team_type = self.stream.read_v_int()

    def is_valid_team_data(self) -> bool:
        """Check if team data is valid"""
        return self.game_mode >= 0 and self.map_id > 0

    def __str__(self) -> str:
        """String representation"""
        team_type = "ranked" if self.is_ranked_team() else "normal"
        return f"TeamCreateMessage(mode={self.game_mode}, map={self.map_id}, {team_type})"
