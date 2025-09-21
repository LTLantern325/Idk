"""
Python conversion of Supercell.Laser.Logic.Message.Club.CreateAllianceMessage.cs
Create alliance message for creating new alliance
"""

from ..game_message import GameMessage

class CreateAllianceMessage(GameMessage):
    """Create alliance message for creating new alliance"""

    def __init__(self):
        """Initialize create alliance message"""
        super().__init__()
        self.alliance_name = ""
        self.alliance_description = ""
        self.badge_id = 0
        self.required_trophies = 0
        self.join_type = 0
        self.family_friendly = False

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14301

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 11

    def get_alliance_name(self) -> str:
        """Get alliance name"""
        return self.alliance_name

    def set_alliance_name(self, name: str) -> None:
        """Set alliance name"""
        self.alliance_name = name

    def get_alliance_description(self) -> str:
        """Get alliance description"""
        return self.alliance_description

    def set_alliance_description(self, description: str) -> None:
        """Set alliance description"""
        self.alliance_description = description

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_string(self.alliance_name)
        self.stream.write_string(self.alliance_description)
        self.stream.write_v_int(self.badge_id)
        self.stream.write_v_int(self.required_trophies)
        self.stream.write_v_int(self.join_type)
        self.stream.write_boolean(self.family_friendly)

    def decode(self) -> None:
        """Decode message from stream"""
        self.alliance_name = self.stream.read_string()
        self.alliance_description = self.stream.read_string()
        self.badge_id = self.stream.read_v_int()
        self.required_trophies = self.stream.read_v_int()
        self.join_type = self.stream.read_v_int()
        self.family_friendly = self.stream.read_boolean()

    def is_valid_alliance_data(self) -> bool:
        """Check if alliance data is valid"""
        return (self.alliance_name != "" and 
                len(self.alliance_name) <= 50 and
                len(self.alliance_description) <= 200)

    def __str__(self) -> str:
        """String representation"""
        return f"CreateAllianceMessage('{self.alliance_name}')"
