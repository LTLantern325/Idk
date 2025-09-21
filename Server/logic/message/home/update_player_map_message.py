"""
Python conversion of Supercell.Laser.Logic.Message.Home.UpdatePlayerMapMessage.cs
Update player map message for updating custom maps
"""

from ..game_message import GameMessage

class UpdatePlayerMapMessage(GameMessage):
    """Update player map message for updating custom maps"""

    def __init__(self):
        """Initialize update player map message"""
        super().__init__()
        self.map_id = 0
        self.map_name = ""
        self.map_data = ""
        self.game_mode = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14462

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.map_id)
        self.stream.write_string(self.map_name)
        self.stream.write_string(self.map_data)
        self.stream.write_v_int(self.game_mode)

    def decode(self) -> None:
        """Decode message from stream"""
        self.map_id = self.stream.read_v_int()
        self.map_name = self.stream.read_string()
        self.map_data = self.stream.read_string()
        self.game_mode = self.stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        return f"UpdatePlayerMapMessage(id={self.map_id}, '{self.map_name}')"
