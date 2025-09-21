"""
Python conversion of Supercell.Laser.Logic.Message.Home.AllianceWarMessage.cs
Alliance war message for alliance war information
"""

from ..game_message import GameMessage

class AllianceWarMessage(GameMessage):
    """Alliance war message for alliance war information"""

    def __init__(self):
        """Initialize alliance war message"""
        super().__init__()
        self.war_state = 1
        self.preparation_time = 0
        self.battle_day_time = 0
        self.collection_day_cards = 0
        self.war_day_wins = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24776

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def encode(self) -> None:
        """Encode message to stream"""
        # Original C# encoding
        self.stream.write_int(0)
        self.stream.write_int(1)
        self.stream.write_v_int(1)
        self.stream.write_v_int(0)
        self.stream.write_v_int(0)

    def decode(self) -> None:
        """Decode message from stream"""
        # Reverse of encoding
        self.stream.read_int()  # 0
        self.war_state = self.stream.read_int()  # 1
        self.stream.read_v_int()  # 1
        self.collection_day_cards = self.stream.read_v_int()  # 0
        self.war_day_wins = self.stream.read_v_int()  # 0

    def is_war_active(self) -> bool:
        """Check if war is active"""
        return self.war_state == 1

    def __str__(self) -> str:
        """String representation"""
        status = "active" if self.is_war_active() else "inactive"
        return f"AllianceWarMessage(status={status})"
