"""
Python conversion of Supercell.Laser.Logic.Command.Home.LogicHeroSeenCommand.cs
Command for marking hero as seen
"""

from ..command import Command

class LogicHeroSeenCommand(Command):
    """Command for marking hero as seen"""

    def __init__(self):
        """Initialize hero seen command"""
        super().__init__()
        self.hero_global_id = 0

    def get_hero_global_id(self) -> int:
        """Get hero global ID"""
        return self.hero_global_id

    def set_hero_global_id(self, global_id: int) -> None:
        """Set hero global ID"""
        self.hero_global_id = global_id

    def execute(self, avatar: any) -> int:
        """Execute hero seen command"""
        # Mark hero as seen
        if not hasattr(avatar, 'seen_heroes'):
            avatar.seen_heroes = set()

        avatar.seen_heroes.add(self.hero_global_id)

        # Also mark any new notifications for this hero as seen
        if hasattr(avatar, 'hero_notifications'):
            hero_notifications = avatar.hero_notifications.get(self.hero_global_id, [])
            for notification in hero_notifications:
                notification['seen'] = True

        return 0

    def encode(self, stream) -> None:
        """Encode command to stream"""
        super().encode(stream)
        stream.write_v_int(self.hero_global_id)

    def decode(self, stream) -> None:
        """Decode command from stream"""
        super().decode(stream)
        self.hero_global_id = stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        return f"HeroSeenCommand(hero_id={self.hero_global_id})"
