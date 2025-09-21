"""
Python conversion of Supercell.Laser.Logic.Message.Home.MatchmakeRequestMessage.cs
Matchmake request message for game matching
"""

from ..game_message import GameMessage

class MatchmakeRequestMessage(GameMessage):
    """Matchmake request message for game matching"""

    def __init__(self):
        """Initialize matchmake request message"""
        super().__init__()
        self.game_mode = 0
        self.map_id = 0
        self.character_id = 0
        self.skin_id = 0
        self.team_size = 1
        self.ranked_mode = False

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 18977

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

    def get_character_id(self) -> int:
        """Get character ID"""
        return self.character_id

    def set_character_id(self, character_id: int) -> None:
        """Set character ID"""
        self.character_id = character_id

    def is_ranked(self) -> bool:
        """Check if ranked mode"""
        return self.ranked_mode

    def set_ranked(self, ranked: bool) -> None:
        """Set ranked mode"""
        self.ranked_mode = ranked

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.game_mode)
        self.stream.write_v_int(self.map_id)
        self.stream.write_v_int(self.character_id)
        self.stream.write_v_int(self.skin_id)
        self.stream.write_v_int(self.team_size)
        self.stream.write_boolean(self.ranked_mode)

    def decode(self) -> None:
        """Decode message from stream"""
        self.game_mode = self.stream.read_v_int()
        self.map_id = self.stream.read_v_int()
        self.character_id = self.stream.read_v_int()
        self.skin_id = self.stream.read_v_int()
        self.team_size = self.stream.read_v_int()
        self.ranked_mode = self.stream.read_boolean()

    def is_valid(self) -> bool:
        """Check if message is valid"""
        return (self.game_mode >= 0 and self.map_id >= 0 and 
                self.character_id > 0 and self.team_size > 0)

    def __str__(self) -> str:
        """String representation"""
        mode_str = "ranked" if self.ranked_mode else "casual"
        return (f"MatchmakeRequestMessage(mode={self.game_mode}, map={self.map_id}, "
                f"char={self.character_id}, {mode_str})")
