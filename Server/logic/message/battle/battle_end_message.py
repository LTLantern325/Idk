"""
Python conversion of Supercell.Laser.Logic.Message.Battle.BattleEndMessage.cs
Battle end message for battle completion
"""

from ..game_message import GameMessage

class BattleEndMessage(GameMessage):
    """Battle end message for battle completion"""

    def __init__(self):
        """Initialize battle end message"""
        super().__init__()
        self.result = 0  # 0=lose, 1=win, 2=draw
        self.trophy_change = 0
        self.experience_gained = 0
        self.battle_duration = 0
        self.star_player = False

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 23456  # Placeholder message type

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 27

    def get_result(self) -> int:
        """Get battle result"""
        return self.result

    def set_result(self, result: int) -> None:
        """Set battle result"""
        self.result = result

    def is_victory(self) -> bool:
        """Check if player won"""
        return self.result == 1

    def is_defeat(self) -> bool:
        """Check if player lost"""
        return self.result == 0

    def is_draw(self) -> bool:
        """Check if battle was a draw"""
        return self.result == 2

    def get_result_name(self) -> str:
        """Get human-readable result"""
        if self.result == 0:
            return "Defeat"
        elif self.result == 1:
            return "Victory"
        elif self.result == 2:
            return "Draw"
        else:
            return "Unknown"

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.result)
        self.stream.write_v_int(self.trophy_change)
        self.stream.write_v_int(self.experience_gained)
        self.stream.write_v_int(self.battle_duration)
        self.stream.write_boolean(self.star_player)

    def decode(self) -> None:
        """Decode message from stream"""
        self.result = self.stream.read_v_int()
        self.trophy_change = self.stream.read_v_int()
        self.experience_gained = self.stream.read_v_int()
        self.battle_duration = self.stream.read_v_int()
        self.star_player = self.stream.read_boolean()

    def __str__(self) -> str:
        """String representation"""
        return (f"BattleEndMessage({self.get_result_name()}, "
                f"trophies={self.trophy_change}, star={self.star_player})")
