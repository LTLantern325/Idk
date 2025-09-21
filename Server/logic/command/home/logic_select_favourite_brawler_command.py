"""
Python conversion of Supercell.Laser.Logic.Command.Home.LogicSelectFavouriteBrawlerCommand.cs
Command for selecting favourite brawler
"""

from ..command import Command

class LogicSelectFavouriteBrawlerCommand(Command):
    """Command for selecting favourite brawler"""

    def __init__(self):
        """Initialize select favourite brawler command"""
        super().__init__()
        self.brawler_global_id = 0

    def get_brawler_global_id(self) -> int:
        """Get brawler global ID"""
        return self.brawler_global_id

    def set_brawler_global_id(self, global_id: int) -> None:
        """Set brawler global ID"""
        self.brawler_global_id = global_id

    def execute(self, avatar: any) -> int:
        """Execute select favourite brawler command"""
        # Check if brawler is owned
        if not hasattr(avatar, 'unlocked_characters'):
            avatar.unlocked_characters = []

        if self.brawler_global_id != 0 and self.brawler_global_id not in avatar.unlocked_characters:
            return -1  # Brawler not owned

        # Set favourite brawler
        avatar.favourite_brawler = self.brawler_global_id

        # Update profile display
        if hasattr(avatar, 'profile_settings'):
            avatar.profile_settings['favourite_brawler'] = self.brawler_global_id

        # Track favourite brawler history
        if not hasattr(avatar, 'favourite_brawler_history'):
            avatar.favourite_brawler_history = []

        avatar.favourite_brawler_history.append({
            'brawler_id': self.brawler_global_id,
            'timestamp': self.timestamp
        })

        # Limit history size
        if len(avatar.favourite_brawler_history) > 10:
            avatar.favourite_brawler_history.pop(0)

        return 0

    def encode(self, stream) -> None:
        """Encode command to stream"""
        super().encode(stream)
        stream.write_v_int(self.brawler_global_id)

    def decode(self, stream) -> None:
        """Decode command from stream"""
        super().decode(stream)
        self.brawler_global_id = stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        return f"SelectFavouriteBrawlerCommand(brawler_id={self.brawler_global_id})"
