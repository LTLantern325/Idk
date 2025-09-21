"""
Python conversion of Supercell.Laser.Logic.Message.Friends.AskForFriendListMessage.cs
Ask for friend list message for requesting friend list
"""

from ..game_message import GameMessage

class AskForFriendListMessage(GameMessage):
    """Ask for friend list message for requesting friend list"""

    def __init__(self):
        """Initialize ask for friend list message"""
        super().__init__()

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 10504

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 1

    def encode(self) -> None:
        """Encode message to stream (empty for ask friend list)"""
        # Ask for friend list message typically has no data
        pass

    def decode(self) -> None:
        """Decode message from stream (empty for ask friend list)"""
        # Ask for friend list message typically has no data
        pass

    def __str__(self) -> str:
        """String representation"""
        return "AskForFriendListMessage()"
