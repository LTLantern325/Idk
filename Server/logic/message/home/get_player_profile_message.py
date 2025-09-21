"""
Python conversion of Supercell.Laser.Logic.Message.Home.GetPlayerProfileMessage.cs
Get player profile message for requesting player profiles
"""

from ..game_message import GameMessage

class GetPlayerProfileMessage(GameMessage):
    """Get player profile message for requesting player profiles"""

    def __init__(self):
        """Initialize get player profile message"""
        super().__init__()
        self.player_id = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14113

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_player_id(self) -> int:
        """Get player ID"""
        return self.player_id

    def set_player_id(self, player_id: int) -> None:
        """Set player ID"""
        self.player_id = player_id

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_long(self.player_id)

    def decode(self) -> None:
        """Decode message from stream"""
        self.player_id = self.stream.read_v_long()

    def is_valid_request(self) -> bool:
        """Check if request is valid"""
        return self.player_id > 0

    def __str__(self) -> str:
        """String representation"""
        return f"GetPlayerProfileMessage(player_id={self.player_id})"
