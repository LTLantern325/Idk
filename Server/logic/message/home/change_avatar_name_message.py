"""
Python conversion of Supercell.Laser.Logic.Message.Home.ChangeAvatarNameMessage.cs
Change avatar name message for renaming avatars
"""

from ..game_message import GameMessage

class ChangeAvatarNameMessage(GameMessage):
    """Change avatar name message for renaming avatars"""

    def __init__(self):
        """Initialize change avatar name message"""
        super().__init__()
        self.name = ""

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 10212

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_name(self) -> str:
        """Get new avatar name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set new avatar name"""
        self.name = name

    def decode(self) -> None:
        """Decode message from stream"""
        self.name = self.stream.read_string()

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_string(self.name)

    def is_valid_name(self) -> bool:
        """Check if name is valid"""
        return self.name != "" and len(self.name) <= 50

    def __str__(self) -> str:
        """String representation"""
        return f"ChangeAvatarNameMessage(name='{self.name}')"
