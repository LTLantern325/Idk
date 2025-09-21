"""
Python conversion of Supercell.Laser.Logic.Command.Home.LogicSetPlayerThumbnailCommand.cs
Command for setting player thumbnail
"""

from ..command import Command

class LogicSetPlayerThumbnailCommand(Command):
    """Command for setting player thumbnail"""

    def __init__(self):
        """Initialize set player thumbnail command"""
        super().__init__()
        self.thumbnail_global_id = 0
        self.thumbnail_type = 0  # 0=character, 1=custom, 2=seasonal

    def get_thumbnail_global_id(self) -> int:
        """Get thumbnail global ID"""
        return self.thumbnail_global_id

    def set_thumbnail_global_id(self, global_id: int) -> None:
        """Set thumbnail global ID"""
        self.thumbnail_global_id = global_id

    def get_thumbnail_type(self) -> int:
        """Get thumbnail type"""
        return self.thumbnail_type

    def set_thumbnail_type(self, thumbnail_type: int) -> None:
        """Set thumbnail type"""
        self.thumbnail_type = thumbnail_type

    def execute(self, avatar: any) -> int:
        """Execute set player thumbnail command"""
        # Check if thumbnail is owned
        if not hasattr(avatar, 'unlocked_thumbnails'):
            avatar.unlocked_thumbnails = []

        if self.thumbnail_global_id != 0:
            if self.thumbnail_type == 0:  # Character thumbnail
                # Check if character is owned
                if not hasattr(avatar, 'unlocked_characters'):
                    avatar.unlocked_characters = []
                if self.thumbnail_global_id not in avatar.unlocked_characters:
                    return -1  # Character not owned
            else:
                # Check if custom thumbnail is owned
                if self.thumbnail_global_id not in avatar.unlocked_thumbnails:
                    return -2  # Thumbnail not owned

        # Set player thumbnail
        avatar.player_thumbnail = self.thumbnail_global_id
        avatar.player_thumbnail_type = self.thumbnail_type

        # Update profile settings
        if not hasattr(avatar, 'profile_settings'):
            avatar.profile_settings = {}

        avatar.profile_settings['thumbnail_id'] = self.thumbnail_global_id
        avatar.profile_settings['thumbnail_type'] = self.thumbnail_type

        return 0

    def encode(self, stream) -> None:
        """Encode command to stream"""
        super().encode(stream)
        stream.write_v_int(self.thumbnail_global_id)
        stream.write_v_int(self.thumbnail_type)

    def decode(self, stream) -> None:
        """Decode command from stream"""
        super().decode(stream)
        self.thumbnail_global_id = stream.read_v_int()
        self.thumbnail_type = stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        types = ["Character", "Custom", "Seasonal"]
        type_name = types[self.thumbnail_type] if self.thumbnail_type < len(types) else "Unknown"
        return f"SetPlayerThumbnailCommand(thumbnail={self.thumbnail_global_id}, type={type_name})"
