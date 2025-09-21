"""
Python conversion of Supercell.Laser.Logic.Message.Home.GetPlayerMapsMessage.cs
Get player maps message for requesting player's custom maps
"""

from ..game_message import GameMessage

class GetPlayerMapsMessage(GameMessage):
    """Get player maps message for requesting player's custom maps"""

    def __init__(self):
        """Initialize get player maps message"""
        super().__init__()
        self.player_id = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14463

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

    def __str__(self) -> str:
        """String representation"""
        return f"GetPlayerMapsMessage(player_id={self.player_id})"
