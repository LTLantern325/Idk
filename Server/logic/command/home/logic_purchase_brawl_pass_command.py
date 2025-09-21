"""
Python conversion of Supercell.Laser.Logic.Command.Home.LogicPurchaseBrawlPassCommand.cs
Command for purchasing brawl pass
"""

from ..command import Command

class LogicPurchaseBrawlPassCommand(Command):
    """Command for purchasing brawl pass"""

    def __init__(self):
        """Initialize purchase brawl pass command"""
        super().__init__()
        self.season_id = 0
        self.pass_type = 1  # 1=premium, 2=premium_plus
        self.cost_gems = 169  # Default cost
        self.use_gems = True

    def get_season_id(self) -> int:
        """Get season ID"""
        return self.season_id

    def set_season_id(self, season_id: int) -> None:
        """Set season ID"""
        self.season_id = season_id

    def get_pass_type(self) -> int:
        """Get pass type"""
        return self.pass_type

    def set_pass_type(self, pass_type: int) -> None:
        """Set pass type"""
        self.pass_type = pass_type
        # Set cost based on pass type
        if pass_type == 1:  # Premium
            self.cost_gems = 169
        elif pass_type == 2:  # Premium Plus
            self.cost_gems = 259

    def execute(self, avatar: any) -> int:
        """Execute purchase brawl pass command"""
        # Check if player has enough gems
        if self.use_gems and avatar.diamonds < self.cost_gems:
            return -1  # Insufficient gems

        # Check if already owns pass for this season
        if not hasattr(avatar, 'owned_passes'):
            avatar.owned_passes = {}

        if self.season_id in avatar.owned_passes:
            # Already owns a pass, check if upgrading
            current_pass = avatar.owned_passes[self.season_id]
            if current_pass >= self.pass_type:
                return -2  # Already owns same or better pass

        # Deduct cost
        if self.use_gems:
            avatar.diamonds -= self.cost_gems

        # Grant pass
        avatar.owned_passes[self.season_id] = self.pass_type

        # Initialize battle pass data if not exists
        if not hasattr(avatar, 'battle_pass_data'):
            avatar.battle_pass_data = {}

        if self.season_id not in avatar.battle_pass_data:
            avatar.battle_pass_data[self.season_id] = {
                'tokens': 0,
                'tier': 0,
                'claimed_free': [],
                'claimed_premium': []
            }

        # Grant premium tier bonuses if applicable
        battle_pass = avatar.battle_pass_data[self.season_id]
        if self.pass_type == 2:  # Premium Plus
            # Grant tier skip or bonus tokens
            battle_pass['tokens'] += 1000  # Bonus tokens

        return 0

    def encode(self, stream) -> None:
        """Encode command to stream"""
        super().encode(stream)
        stream.write_v_int(self.season_id)
        stream.write_v_int(self.pass_type)
        stream.write_v_int(self.cost_gems)
        stream.write_boolean(self.use_gems)

    def decode(self, stream) -> None:
        """Decode command from stream"""
        super().decode(stream)
        self.season_id = stream.read_v_int()
        self.pass_type = stream.read_v_int()
        self.cost_gems = stream.read_v_int()
        self.use_gems = stream.read_boolean()

    def __str__(self) -> str:
        """String representation"""
        pass_names = {1: "Premium", 2: "Premium Plus"}
        pass_name = pass_names.get(self.pass_type, "Unknown")
        return f"PurchaseBrawlPassCommand(season={self.season_id}, type={pass_name}, cost={self.cost_gems})"
