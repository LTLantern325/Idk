"""
Python conversion of Supercell.Laser.Logic.Message.Team.TeamLeftMessage.cs
Team left message for notifying when a player left the team
"""

from ..game_message import GameMessage

class TeamLeftMessage(GameMessage):
    """Team left message for notifying when a player left the team"""

    def __init__(self):
        """Initialize team left message"""
        super().__init__()
        self.player_id = 0
        self.reason = 0  # 0=left, 1=kicked, 2=timeout

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24354  # Team left

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_player_id(self) -> int:
        """Get player ID who left"""
        return self.player_id

    def set_player_id(self, player_id: int) -> None:
        """Set player ID who left"""
        self.player_id = player_id

    def get_reason(self) -> int:
        """Get leave reason"""
        return self.reason

    def set_reason(self, reason: int) -> None:
        """Set leave reason"""
        self.reason = reason

    def is_left_voluntarily(self) -> bool:
        """Check if player left voluntarily"""
        return self.reason == 0

    def is_kicked(self) -> bool:
        """Check if player was kicked"""
        return self.reason == 1

    def is_timeout(self) -> bool:
        """Check if player left due to timeout"""
        return self.reason == 2

    def get_reason_name(self) -> str:
        """Get human-readable reason name"""
        reasons = {0: "Left", 1: "Kicked", 2: "Timeout"}
        return reasons.get(self.reason, "Unknown")

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_long(self.player_id)
        self.stream.write_v_int(self.reason)

    def decode(self) -> None:
        """Decode message from stream"""
        self.player_id = self.stream.read_v_long()
        self.reason = self.stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        return f"TeamLeftMessage(player_id={self.player_id}, {self.get_reason_name()})"
