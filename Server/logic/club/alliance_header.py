"""
Python conversion of Supercell.Laser.Logic.Club.AllianceHeader.cs
Alliance header for basic alliance information
"""

class AllianceHeader:
    """Alliance header for basic alliance information"""

    def __init__(self):
        """Initialize alliance header"""
        self.alliance_id = 0
        self.name = ""
        self.badge_id = 0
        self.type = 1  # Open = 1, Invite Only = 2, Closed = 3
        self.member_count = 0
        self.max_members = 100
        self.trophies = 0
        self.required_trophies = 0
        self.region = "GLOBAL"
        self.is_family_friendly = True

    def get_alliance_id(self) -> int:
        """Get alliance ID"""
        return self.alliance_id

    def set_alliance_id(self, alliance_id: int) -> None:
        """Set alliance ID"""
        self.alliance_id = alliance_id

    def get_name(self) -> str:
        """Get alliance name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set alliance name"""
        self.name = name

    def get_badge_id(self) -> int:
        """Get badge ID"""
        return self.badge_id

    def set_badge_id(self, badge_id: int) -> None:
        """Set badge ID"""
        self.badge_id = badge_id

    def get_type(self) -> int:
        """Get alliance type"""
        return self.type

    def set_type(self, alliance_type: int) -> None:
        """Set alliance type"""
        self.type = alliance_type

    def get_member_count(self) -> int:
        """Get member count"""
        return self.member_count

    def set_member_count(self, count: int) -> None:
        """Set member count"""
        self.member_count = max(0, min(self.max_members, count))

    def get_trophies(self) -> int:
        """Get alliance trophies"""
        return self.trophies

    def set_trophies(self, trophies: int) -> None:
        """Set alliance trophies"""
        self.trophies = max(0, trophies)

    def get_required_trophies(self) -> int:
        """Get required trophies"""
        return self.required_trophies

    def set_required_trophies(self, required: int) -> None:
        """Set required trophies"""
        self.required_trophies = max(0, required)

    def is_open(self) -> bool:
        """Check if alliance is open"""
        return self.type == 1

    def is_invite_only(self) -> bool:
        """Check if alliance is invite only"""
        return self.type == 2

    def is_closed(self) -> bool:
        """Check if alliance is closed"""
        return self.type == 3

    def is_full(self) -> bool:
        """Check if alliance is full"""
        return self.member_count >= self.max_members

    def can_join(self, player_trophies: int) -> bool:
        """Check if player can join"""
        if self.is_full():
            return False
        if self.is_closed():
            return False
        if player_trophies < self.required_trophies:
            return False
        return True

    def get_type_name(self) -> str:
        """Get alliance type name"""
        type_names = {1: "Open", 2: "Invite Only", 3: "Closed"}
        return type_names.get(self.type, "Unknown")

    def encode(self, stream) -> None:
        """Encode alliance header to stream"""
        stream.write_v_long(self.alliance_id)
        stream.write_string(self.name)
        stream.write_v_int(self.badge_id)
        stream.write_v_int(self.type)
        stream.write_v_int(self.member_count)
        stream.write_v_int(self.trophies)
        stream.write_v_int(self.required_trophies)
        stream.write_string(self.region)
        stream.write_boolean(self.is_family_friendly)

    def decode(self, stream) -> None:
        """Decode alliance header from stream"""
        self.alliance_id = stream.read_v_long()
        self.name = stream.read_string()
        self.badge_id = stream.read_v_int()
        self.type = stream.read_v_int()
        self.member_count = stream.read_v_int()
        self.trophies = stream.read_v_int()
        self.required_trophies = stream.read_v_int()
        self.region = stream.read_string()
        self.is_family_friendly = stream.read_boolean()

    def __str__(self) -> str:
        """String representation"""
        return f"AllianceHeader('{self.name}', {self.member_count}/{self.max_members}, {self.trophies} trophies)"
