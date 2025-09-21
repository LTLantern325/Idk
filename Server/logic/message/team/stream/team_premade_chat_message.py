"""
Python conversion of Supercell.Laser.Logic.Message.Team.Stream.TeamPremadeChatMessage.cs
Team premade chat message for predefined team messages
"""

from ...game_message import GameMessage

class TeamPremadeChatMessage(GameMessage):
    """Team premade chat message for predefined team messages"""

    def __init__(self):
        """Initialize team premade chat message"""
        super().__init__()
        self.premade_chat_id = 0
        self.player_id = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14367  # Team premade chat

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_premade_chat_id(self) -> int:
        """Get premade chat ID"""
        return self.premade_chat_id

    def set_premade_chat_id(self, chat_id: int) -> None:
        """Set premade chat ID"""
        self.premade_chat_id = chat_id

    def get_player_id(self) -> int:
        """Get sender player ID"""
        return self.player_id

    def set_player_id(self, player_id: int) -> None:
        """Set sender player ID"""
        self.player_id = player_id

    def get_premade_text(self) -> str:
        """Get premade text based on ID"""
        premade_messages = {
            1: "Attack!",
            2: "Defend!",
            3: "Retreat!",
            4: "Help!",
            5: "Good Game!",
            6: "Thanks!",
            7: "Sorry!",
            8: "Yes!",
            9: "No!"
        }
        return premade_messages.get(self.premade_chat_id, f"Message {self.premade_chat_id}")

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.premade_chat_id)
        self.stream.write_v_long(self.player_id)

    def decode(self) -> None:
        """Decode message from stream"""
        self.premade_chat_id = self.stream.read_v_int()
        self.player_id = self.stream.read_v_long()

    def is_valid_message(self) -> bool:
        """Check if message is valid"""
        return self.premade_chat_id > 0 and self.player_id > 0

    def __str__(self) -> str:
        """String representation"""
        return f"TeamPremadeChatMessage(player_id={self.player_id}, '{self.get_premade_text()}')"
