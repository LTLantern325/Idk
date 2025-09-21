"""
Python conversion of Supercell.Laser.Logic.Message.Team.TeamSetPlayerMapMessage.cs
Team set player map message for setting player map in team
"""

from ..game_message import GameMessage

class TeamSetPlayerMapMessage(GameMessage):
    """Team set player map message for setting player map in team"""

    def __init__(self):
        """Initialize team set player map message"""
        super().__init__()
        self.map_id = 0
        self.map_data = ""

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14364

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_map_id(self) -> int:
        """Get map ID"""
        return self.map_id

    def set_map_id(self, map_id: int) -> None:
        """Set map ID"""
        self.map_id = map_id

    def get_map_data(self) -> str:
        """Get map data"""
        return self.map_data

    def set_map_data(self, data: str) -> None:
        """Set map data"""
        self.map_data = data

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.map_id)
        self.stream.write_string(self.map_data)

    def decode(self) -> None:
        """Decode message from stream"""
        self.map_id = self.stream.read_v_int()
        self.map_data = self.stream.read_string()

    def is_valid_map(self) -> bool:
        """Check if map is valid"""
        return self.map_id > 0 or self.map_data != ""

    def __str__(self) -> str:
        """String representation"""
        return f"TeamSetPlayerMapMessage(map_id={self.map_id})"
