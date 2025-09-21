"""
Python conversion of Supercell.Laser.Logic.Message.Home.DeletePlayerMapMessage.cs
Delete player map message for deleting custom maps
"""

from ..game_message import GameMessage

class DeletePlayerMapMessage(GameMessage):
    """Delete player map message for deleting custom maps"""

    def __init__(self):
        """Initialize delete player map message"""
        super().__init__()
        self.map_id = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14461

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_map_id(self) -> int:
        """Get map ID to delete"""
        return self.map_id

    def set_map_id(self, map_id: int) -> None:
        """Set map ID to delete"""
        self.map_id = map_id

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.map_id)

    def decode(self) -> None:
        """Decode message from stream"""
        self.map_id = self.stream.read_v_int()

    def is_valid_request(self) -> bool:
        """Check if request is valid"""
        return self.map_id > 0

    def __str__(self) -> str:
        """String representation"""
        return f"DeletePlayerMapMessage(map_id={self.map_id})"
