"""
Python conversion of Supercell.Laser.Logic.Message.Team.TeamInviteMessage.cs
Team invite message for inviting players to team
"""

from ..game_message import GameMessage

class TeamInviteMessage(GameMessage):
    """Team invite message for inviting players to team"""

    def __init__(self):
        """Initialize team invite message"""
        super().__init__()
        self.player_id = 0
        self.player_name = ""

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14358

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_player_id(self) -> int:
        """Get player ID to invite"""
        return self.player_id

    def set_player_id(self, player_id: int) -> None:
        """Set player ID to invite"""
        self.player_id = player_id

    def get_player_name(self) -> str:
        """Get player name to invite"""
        return self.player_name

    def set_player_name(self, name: str) -> None:
        """Set player name to invite"""
        self.player_name = name

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_long(self.player_id)
        self.stream.write_string(self.player_name)

    def decode(self) -> None:
        """Decode message from stream"""
        self.player_id = self.stream.read_v_long()
        self.player_name = self.stream.read_string()

    def is_valid_invite(self) -> bool:
        """Check if invite is valid"""
        return self.player_id > 0 or self.player_name != ""

    def __str__(self) -> str:
        """String representation"""
        if self.player_name:
            return f"TeamInviteMessage('{self.player_name}')"
        else:
            return f"TeamInviteMessage(player_id={self.player_id})"
