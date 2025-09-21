"""
Python conversion of Supercell.Laser.Logic.Message.Club.ChatToAllianceStreamMessage.cs
Chat to alliance stream message for alliance chat
"""

from ..game_message import GameMessage

class ChatToAllianceStreamMessage(GameMessage):
    """Chat to alliance stream message for alliance chat"""

    def __init__(self):
        """Initialize chat to alliance stream message"""
        super().__init__()
        self.chat_message = ""

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14315

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 11

    def get_chat_message(self) -> str:
        """Get chat message"""
        return self.chat_message

    def set_chat_message(self, message: str) -> None:
        """Set chat message"""
        self.chat_message = message

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_string(self.chat_message)

    def decode(self) -> None:
        """Decode message from stream"""
        self.chat_message = self.stream.read_string()

    def is_valid_message(self) -> bool:
        """Check if message is valid"""
        return self.chat_message != "" and len(self.chat_message) <= 256

    def get_message_length(self) -> int:
        """Get message length"""
        return len(self.chat_message)

    def __str__(self) -> str:
        """String representation"""
        preview = self.chat_message[:30] + "..." if len(self.chat_message) > 30 else self.chat_message
        return f"ChatToAllianceStreamMessage('{preview}')"
