"""
Python conversion of Supercell.Laser.Logic.Message.Home.AvatarNameCheckRequestMessage.cs
Avatar name check request message for validating avatar names
"""

from ..game_message import GameMessage

class AvatarNameCheckRequestMessage(GameMessage):
    """Avatar name check request message for validating avatar names"""

    def __init__(self):
        """Initialize avatar name check request message"""
        super().__init__()
        self.name = ""

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14600

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_name(self) -> str:
        """Get name to check"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set name to check"""
        self.name = name

    def decode(self) -> None:
        """Decode message from stream"""
        self.name = self.stream.read_string()

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_string(self.name)

    def is_valid_request(self) -> bool:
        """Check if request is valid"""
        return self.name != "" and len(self.name.strip()) > 0

    def get_name_length(self) -> int:
        """Get name length"""
        return len(self.name)

    def __str__(self) -> str:
        """String representation"""
        return f"AvatarNameCheckRequestMessage(name='{self.name}')"
