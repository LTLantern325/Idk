"""
Python conversion of Supercell.Laser.Logic.Message.Home.UpdatePlayerMapResponseMessage.cs
Update player map response message for map update responses
"""

from ..game_message import GameMessage

class UpdatePlayerMapResponseMessage(GameMessage):
    """Update player map response message for map update responses"""

    def __init__(self):
        """Initialize update player map response message"""
        super().__init__()
        self.success = False
        self.map_id = 0
        self.error_code = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24462

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

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
        return f"UpdatePlayerMapResponseMessage({status}, map_id={self.map_id})"
