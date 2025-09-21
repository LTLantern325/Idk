"""
Python conversion of Supercell.Laser.Logic.Message.Team.Stream.TeamChatMessage.cs
Team chat message for team chat functionality
"""

from ...game_message import GameMessage

class TeamChatMessage(GameMessage):
    """Team chat message for team chat functionality"""

    def __init__(self):
        """Initialize team chat message"""
        super().__init__()
        self.message_text = ""
        self.player_id = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14366  # Team chat

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_message_text(self) -> str:
        """Get message text"""
        return self.message_text

    def set_message_text(self, text: str) -> None:
        """Set message text"""
        self.message_text = text

    def get_player_id(self) -> int:
        """Get sender player ID"""
        return self.player_id

    def set_player_id(self, player_id: int) -> None:
        """Set sender player ID"""
        self.player_id = player_id

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_string(self.message_text)
        self.stream.write_v_long(self.player_id)

    def decode(self) -> None:
        """Decode message from stream"""
        self.message_text = self.stream.read_string()
        self.player_id = self.stream.read_v_long()

    def is_valid_message(self) -> bool:
        """Check if message is valid"""
        return (self.message_text != "" and 
                len(self.message_text) <= 256 and
                self.player_id > 0)

    def get_message_length(self) -> int:
        """Get message length"""
        return len(self.message_text)

    def __str__(self) -> str:
        """String representation"""
        preview = self.message_text[:30] + "..." if len(self.message_text) > 30 else self.message_text
        return f"TeamChatMessage(player_id={self.player_id}, '{preview}')"
