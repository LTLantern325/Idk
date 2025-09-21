"""
Python conversion of Supercell.Laser.Logic.Message.Team.TeamSetMemberReadyMessage.cs
Team set member ready message for setting member ready status
"""

from ..game_message import GameMessage

class TeamSetMemberReadyMessage(GameMessage):
    """Team set member ready message for setting member ready status"""

    def __init__(self):
        """Initialize team set member ready message"""
        super().__init__()
        self.is_ready = False
        self.character_id = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14363

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def is_member_ready(self) -> bool:
        """Check if member is ready"""
        return self.is_ready

    def set_ready(self, ready: bool) -> None:
        """Set ready status"""
        self.is_ready = ready

    def get_character_id(self) -> int:
        """Get character ID"""
        return self.character_id

    def set_character_id(self, character_id: int) -> None:
        """Set character ID"""
        self.character_id = character_id

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_boolean(self.is_ready)
        self.stream.write_v_int(self.character_id)

    def decode(self) -> None:
        """Decode message from stream"""
        self.is_ready = self.stream.read_boolean()
        self.character_id = self.stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        status = "ready" if self.is_ready else "not ready"
        return f"TeamSetMemberReadyMessage({status}, char={self.character_id})"
