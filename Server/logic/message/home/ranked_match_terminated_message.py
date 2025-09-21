"""
Python conversion of Supercell.Laser.Logic.Message.Home.RankedMatchTerminatedMessage.cs
Ranked match terminated message for ranked match termination
"""

from ..game_message import GameMessage

class RankedMatchTerminatedMessage(GameMessage):
    """Ranked match terminated message for ranked match termination"""

    def __init__(self):
        """Initialize ranked match terminated message"""
        super().__init__()
        self.reason_code = 0
        self.old_trophies = 0
        self.new_trophies = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 23458

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_reason_code(self) -> int:
        """Get termination reason code"""
        return self.reason_code

    def set_reason_code(self, code: int) -> None:
        """Set termination reason code"""
        self.reason_code = code

    def get_trophy_change(self) -> int:
        """Get trophy change"""
        return self.new_trophies - self.old_trophies

    def get_reason_name(self) -> str:
        """Get human-readable reason name"""
        reasons = {
            0: "Normal End",
            1: "Player Disconnected",
            2: "Server Error",
            3: "Match Cancelled"
        }
        return reasons.get(self.reason_code, f"Reason {self.reason_code}")

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.reason_code)
        self.stream.write_v_int(self.old_trophies)
        self.stream.write_v_int(self.new_trophies)

    def decode(self) -> None:
        """Decode message from stream"""
        self.reason_code = self.stream.read_v_int()
        self.old_trophies = self.stream.read_v_int()
        self.new_trophies = self.stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        change = self.get_trophy_change()
        change_str = f"+{change}" if change > 0 else str(change)
        return f"RankedMatchTerminatedMessage({self.get_reason_name()}, trophies={change_str})"
