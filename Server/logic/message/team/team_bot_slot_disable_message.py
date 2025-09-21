"""
Python conversion of Supercell.Laser.Logic.Message.Team.TeamBotSlotDisableMessage.cs
Team bot slot disable message for disabling bot slots
"""

from ..game_message import GameMessage

class TeamBotSlotDisableMessage(GameMessage):
    """Team bot slot disable message for disabling bot slots"""

    def __init__(self):
        """Initialize team bot slot disable message"""
        super().__init__()
        self.slot_id = 0
        self.disable = True

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14354

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_slot_id(self) -> int:
        """Get slot ID"""
        return self.slot_id

    def set_slot_id(self, slot_id: int) -> None:
        """Set slot ID"""
        self.slot_id = slot_id

    def is_disable(self) -> bool:
        """Check if disabling bot slot"""
        return self.disable

    def set_disable(self, disable: bool) -> None:
        """Set disable flag"""
        self.disable = disable

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.slot_id)
        self.stream.write_boolean(self.disable)

    def decode(self) -> None:
        """Decode message from stream"""
        self.slot_id = self.stream.read_v_int()
        self.disable = self.stream.read_boolean()

    def __str__(self) -> str:
        """String representation"""
        action = "disable" if self.disable else "enable"
        return f"TeamBotSlotDisableMessage(slot={self.slot_id}, {action})"
