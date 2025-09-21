"""
Python conversion of Supercell.Laser.Logic.Message.Club.ChangeAllianceSettingsMessage.cs
Change alliance settings message for modifying alliance settings
"""

from ..game_message import GameMessage

class ChangeAllianceSettingsMessage(GameMessage):
    """Change alliance settings message for modifying alliance settings"""

    def __init__(self):
        """Initialize change alliance settings message"""
        super().__init__()
        self.alliance_name = ""
        self.alliance_description = ""
        self.badge_id = 0
        self.required_trophies = 0
        self.join_type = 0  # 0=open, 1=invite_only, 2=closed
        self.family_friendly = False

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14305

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

    def is_open_alliance(self) -> bool:
        """Check if alliance is open"""
        return self.join_type == 0

    def is_invite_only(self) -> bool:
        """Check if alliance is invite only"""
        return self.join_type == 1

    def is_closed_alliance(self) -> bool:
        """Check if alliance is closed"""
        return self.join_type == 2

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

    def __str__(self) -> str:
        """String representation"""
        join_types = {0: "open", 1: "invite", 2: "closed"}
        join_status = join_types.get(self.join_type, "unknown")
        return f"ChangeAllianceSettingsMessage('{self.alliance_name}', {join_status})"
