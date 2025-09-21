"""
Python conversion of Supercell.Laser.Logic.Message.Battle.StartLoadingMessage.cs
Start loading message for battle loading
"""

from ..game_message import GameMessage

class StartLoadingMessage(GameMessage):
    """Start loading message for battle loading"""

    def __init__(self):
        """Initialize start loading message"""
        super().__init__()
        self.map_id = 0
        self.game_mode = 0
        self.loading_stage = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 20559  # Placeholder message type

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 27

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

    def get_loading_stage(self) -> int:
        """Get loading stage"""
        return self.loading_stage

    def set_loading_stage(self, stage: int) -> None:
        """Set loading stage"""
        self.loading_stage = stage

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.map_id)
        self.stream.write_v_int(self.game_mode)
        self.stream.write_v_int(self.loading_stage)

    def decode(self) -> None:
        """Decode message from stream"""
        self.map_id = self.stream.read_v_int()
        self.game_mode = self.stream.read_v_int()
        self.loading_stage = self.stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        return (f"StartLoadingMessage(map={self.map_id}, "
                f"mode={self.game_mode}, stage={self.loading_stage})")
