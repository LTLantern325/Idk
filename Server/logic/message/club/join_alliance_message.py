"""
Python conversion of Supercell.Laser.Logic.Message.Club.JoinAllianceMessage.cs
Join alliance message for joining an alliance
"""

from ..game_message import GameMessage

class JoinAllianceMessage(GameMessage):
    """Join alliance message for joining an alliance"""

    def __init__(self):
        """Initialize join alliance message"""
        super().__init__()
        self.alliance_id = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14308

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 11

    def get_alliance_id(self) -> int:
        """Get alliance ID"""
        return self.alliance_id

    def set_alliance_id(self, alliance_id: int) -> None:
        """Set alliance ID"""
        self.alliance_id = alliance_id

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_long(self.alliance_id)

    def decode(self) -> None:
        """Decode message from stream"""
        self.alliance_id = self.stream.read_v_long()

    def is_valid_request(self) -> bool:
        """Check if request is valid"""
        return self.alliance_id > 0

    def __str__(self) -> str:
        """String representation"""
        return f"JoinAllianceMessage(alliance_id={self.alliance_id})"
