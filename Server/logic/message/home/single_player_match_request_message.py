"""
Python conversion of Supercell.Laser.Logic.Message.Home.SinglePlayerMatchRequestMessage.cs
Single player match request message for single player matches
"""

from ..game_message import GameMessage

class SinglePlayerMatchRequestMessage(GameMessage):
    """Single player match request message for single player matches"""

    def __init__(self):
        """Initialize single player match request message"""
        super().__init__()
        self.map_id = 0
        self.game_mode = 0
        self.character_id = 0
        self.difficulty = 0  # 0=easy, 1=normal, 2=hard, 3=expert

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14999  # Single player match request

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_map_id(self) -> int:
        """Get map ID"""
        return self.map_id

    def set_map_id(self, map_id: int) -> None:
        """Set map ID"""
        self.map_id = map_id

    def get_game_mode(self) -> int:
        """Get game mode"""
        return self.game_mode

    def set_game_mode(self, mode: int) -> None:
        """Set game mode"""
        self.game_mode = mode

    def get_character_id(self) -> int:
        """Get character ID"""
        return self.character_id

    def set_character_id(self, character_id: int) -> None:
        """Set character ID"""
        self.character_id = character_id

    def get_difficulty(self) -> int:
        """Get difficulty level"""
        return self.difficulty

    def set_difficulty(self, difficulty: int) -> None:
        """Set difficulty level"""
        self.difficulty = max(0, min(3, difficulty))

    def get_difficulty_name(self) -> str:
        """Get human-readable difficulty name"""
        difficulties = {0: "Easy", 1: "Normal", 2: "Hard", 3: "Expert"}
        return difficulties.get(self.difficulty, "Unknown")

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.map_id)
        self.stream.write_v_int(self.game_mode)
        self.stream.write_v_int(self.character_id)
        self.stream.write_v_int(self.difficulty)

    def decode(self) -> None:
        """Decode message from stream"""
        self.map_id = self.stream.read_v_int()
        self.game_mode = self.stream.read_v_int()
        self.character_id = self.stream.read_v_int()
        self.difficulty = self.stream.read_v_int()

    def is_valid_request(self) -> bool:
        """Check if request is valid"""
        return (self.map_id > 0 and self.game_mode >= 0 and 
                self.character_id > 0 and 0 <= self.difficulty <= 3)

    def __str__(self) -> str:
        """String representation"""
        return (f"SinglePlayerMatchRequestMessage(map={self.map_id}, "
                f"mode={self.game_mode}, char={self.character_id}, "
                f"difficulty={self.get_difficulty_name()})")
