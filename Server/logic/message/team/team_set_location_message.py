"""
Python conversion of Supercell.Laser.Logic.Message.Team.TeamSetLocationMessage.cs
Team set location message for setting team location
"""

from ..game_message import GameMessage

class TeamSetLocationMessage(GameMessage):
    """Team set location message for setting team location"""

    def __init__(self):
        """Initialize team set location message"""
        super().__init__()
        self.location_id = 0
        self.map_id = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14362

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_location_id(self) -> int:
        """Get location ID"""
        return self.location_id

    def set_location_id(self, location_id: int) -> None:
        """Set location ID"""
        self.location_id = location_id

    def get_map_id(self) -> int:
        """Get map ID"""
        return self.map_id

    def set_map_id(self, map_id: int) -> None:
        """Set map ID"""
        self.map_id = map_id

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.location_id)
        self.stream.write_v_int(self.map_id)

    def decode(self) -> None:
        """Decode message from stream"""
        self.location_id = self.stream.read_v_int()
        self.map_id = self.stream.read_v_int()

    def is_valid_location(self) -> bool:
        """Check if location is valid"""
        return self.location_id > 0 and self.map_id > 0

    def __str__(self) -> str:
        """String representation"""
        return f"TeamSetLocationMessage(location_id={self.location_id}, map_id={self.map_id})"
