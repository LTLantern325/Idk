"""
Python conversion of Supercell.Laser.Logic.Avatar.Structures.PlayerDisplayData.cs
Player display data for visual representation
"""

class PlayerDisplayData:
    """Player display data for visual representation"""

    def __init__(self):
        """Initialize player display data"""
        self.thumbnail_id = 0
        self.name_color_id = 0
        self.name = ""
        self.experience_level = 1
        self.profile_icon_id = 0

    def get_thumbnail_id(self) -> int:
        """Get thumbnail ID"""
        return self.thumbnail_id

    def set_thumbnail_id(self, thumbnail_id: int) -> None:
        """Set thumbnail ID"""
        self.thumbnail_id = thumbnail_id

    def get_name_color_id(self) -> int:
        """Get name color ID"""
        return self.name_color_id

    def set_name_color_id(self, color_id: int) -> None:
        """Set name color ID"""
        self.name_color_id = color_id

    def get_name(self) -> str:
        """Get player name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set player name"""
        self.name = name

    def get_experience_level(self) -> int:
        """Get experience level"""
        return self.experience_level

    def set_experience_level(self, level: int) -> None:
        """Set experience level"""
        self.experience_level = max(1, level)

    def get_profile_icon_id(self) -> int:
        """Get profile icon ID"""
        return self.profile_icon_id

    def set_profile_icon_id(self, icon_id: int) -> None:
        """Set profile icon ID"""
        self.profile_icon_id = icon_id

    def encode(self, stream) -> None:
        """Encode display data to stream"""
        stream.write_string(self.name)
        stream.write_v_int(self.experience_level)
        stream.write_v_int(self.profile_icon_id)
        stream.write_v_int(self.name_color_id)
        stream.write_v_int(self.thumbnail_id)

    def decode(self, stream) -> None:
        """Decode display data from stream"""
        self.name = stream.read_string()
        self.experience_level = stream.read_v_int()
        self.profile_icon_id = stream.read_v_int()
        self.name_color_id = stream.read_v_int()
        self.thumbnail_id = stream.read_v_int()

    def copy_from(self, other: 'PlayerDisplayData') -> None:
        """Copy data from another display data object"""
        self.name = other.name
        self.experience_level = other.experience_level
        self.profile_icon_id = other.profile_icon_id
        self.name_color_id = other.name_color_id
        self.thumbnail_id = other.thumbnail_id

    def is_valid(self) -> bool:
        """Check if display data is valid"""
        return (self.name != "" and 
                self.experience_level > 0 and
                len(self.name) <= 50)

    def __str__(self) -> str:
        """String representation"""
        return f"PlayerDisplayData('{self.name}', level={self.experience_level})"
