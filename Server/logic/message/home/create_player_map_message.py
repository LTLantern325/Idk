"""
Python conversion of Supercell.Laser.Logic.Message.Home.CreatePlayerMapMessage.cs
Create player map message for creating custom maps
"""

from ..game_message import GameMessage

class CreatePlayerMapMessage(GameMessage):
    """Create player map message for creating custom maps"""

    def __init__(self):
        """Initialize create player map message"""
        super().__init__()
        self.map_name = ""
        self.map_data = ""
        self.game_mode = 0
        self.is_copyable = True

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14460  # Placeholder message type

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_map_name(self) -> str:
        """Get map name"""
        return self.map_name

    def set_map_name(self, name: str) -> None:
        """Set map name"""
        self.map_name = name

    def get_map_data(self) -> str:
        """Get map data"""
        return self.map_data

    def set_map_data(self, data: str) -> None:
        """Set map data"""
        self.map_data = data

    def get_game_mode(self) -> int:
        """Get game mode"""
        return self.game_mode

    def set_game_mode(self, mode: int) -> None:
        """Set game mode"""
        self.game_mode = mode

    def is_map_copyable(self) -> bool:
        """Check if map is copyable"""
        return self.is_copyable

    def set_copyable(self, copyable: bool) -> None:
        """Set if map is copyable"""
        self.is_copyable = copyable

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_string(self.map_name)
        self.stream.write_string(self.map_data)
        self.stream.write_v_int(self.game_mode)
        self.stream.write_boolean(self.is_copyable)

    def decode(self) -> None:
        """Decode message from stream"""
        self.map_name = self.stream.read_string()
        self.map_data = self.stream.read_string()
        self.game_mode = self.stream.read_v_int()
        self.is_copyable = self.stream.read_boolean()

    def is_valid_map(self) -> bool:
        """Check if map data is valid"""
        return (self.map_name != "" and self.map_data != "" and 
                len(self.map_name) <= 50)

    def __str__(self) -> str:
        """String representation"""
        copyable_status = "copyable" if self.is_copyable else "not copyable"
        return f"CreatePlayerMapMessage('{self.map_name}', mode={self.game_mode}, {copyable_status})"
