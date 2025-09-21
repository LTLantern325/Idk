"""
Python conversion of Supercell.Laser.Logic.Message.Ranking.GetLeaderboardMessage.cs
Get leaderboard message for requesting leaderboards
"""

from ..game_message import GameMessage

class GetLeaderboardMessage(GameMessage):
    """Get leaderboard message for requesting leaderboards"""

    def __init__(self):
        """Initialize get leaderboard message"""
        super().__init__()
        self.leaderboard_type = 0  # 0=Global, 1=Local, 2=Club
        self.character_id = 0      # For character-specific leaderboards
        self.country_code = ""     # For local leaderboards

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14403

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_leaderboard_type(self) -> int:
        """Get leaderboard type"""
        return self.leaderboard_type

    def set_leaderboard_type(self, lb_type: int) -> None:
        """Set leaderboard type"""
        self.leaderboard_type = lb_type

    def get_character_id(self) -> int:
        """Get character ID"""
        return self.character_id

    def set_character_id(self, character_id: int) -> None:
        """Set character ID"""
        self.character_id = character_id

    def get_country_code(self) -> str:
        """Get country code"""
        return self.country_code

    def set_country_code(self, code: str) -> None:
        """Set country code"""
        self.country_code = code

    def is_global_leaderboard(self) -> bool:
        """Check if global leaderboard"""
        return self.leaderboard_type == 0

    def is_local_leaderboard(self) -> bool:
        """Check if local leaderboard"""
        return self.leaderboard_type == 1

    def is_club_leaderboard(self) -> bool:
        """Check if club leaderboard"""
        return self.leaderboard_type == 2

    def get_leaderboard_type_name(self) -> str:
        """Get human-readable leaderboard type"""
        if self.leaderboard_type == 0:
            return "Global"
        elif self.leaderboard_type == 1:
            return "Local"
        elif self.leaderboard_type == 2:
            return "Club"
        else:
            return "Unknown"

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.leaderboard_type)
        self.stream.write_v_int(self.character_id)
        self.stream.write_string(self.country_code)

    def decode(self) -> None:
        """Decode message from stream"""
        self.leaderboard_type = self.stream.read_v_int()
        self.character_id = self.stream.read_v_int()
        self.country_code = self.stream.read_string()

    def is_valid(self) -> bool:
        """Check if message is valid"""
        return 0 <= self.leaderboard_type <= 2

    def __str__(self) -> str:
        """String representation"""
        type_str = self.get_leaderboard_type_name()
        char_str = f", char={self.character_id}" if self.character_id > 0 else ""
        country_str = f", country={self.country_code}" if self.country_code else ""
        return f"GetLeaderboardMessage({type_str}{char_str}{country_str})"
