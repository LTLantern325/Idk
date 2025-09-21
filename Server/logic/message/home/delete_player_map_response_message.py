"""
Python conversion of Supercell.Laser.Logic.Message.Home.DeletePlayerMapResponseMessage.cs
Delete player map response message for map deletion responses
"""

from ..game_message import GameMessage

class DeletePlayerMapResponseMessage(GameMessage):
    """Delete player map response message for map deletion responses"""

    def __init__(self):
        """Initialize delete player map response message"""
        super().__init__()
        self.success = False
        self.map_id = 0
        self.error_code = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24461

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def is_success(self) -> bool:
        """Check if deletion was successful"""
        return self.success

    def set_success(self, success: bool) -> None:
        """Set success status"""
        self.success = success

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_boolean(self.success)
        self.stream.write_v_int(self.map_id)
        self.stream.write_v_int(self.error_code)

    def decode(self) -> None:
        """Decode message from stream"""
        self.success = self.stream.read_boolean()
        self.map_id = self.stream.read_v_int()
        self.error_code = self.stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        status = "success" if self.success else "failed"
        return f"DeletePlayerMapResponseMessage({status}, map_id={self.map_id})"
