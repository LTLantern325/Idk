"""
Python conversion of Supercell.Laser.Logic.Command.Home.LogicPurchaseBrawlPassProgressCommand.cs
Command for purchasing brawl pass progress (tier skips)
"""

from ..command import Command

class LogicPurchaseBrawlPassProgressCommand(Command):
    """Command for purchasing brawl pass progress (tier skips)"""

    def __init__(self):
        """Initialize purchase brawl pass progress command"""
        super().__init__()
        self.season_id = 0
        self.tiers_to_purchase = 1
        self.cost_per_tier = 150  # Gems per tier
        self.total_cost = 0

    def get_season_id(self) -> int:
        """Get season ID"""
        return self.season_id

    def set_season_id(self, season_id: int) -> None:
        """Set season ID"""
        self.season_id = season_id

    def get_tiers_to_purchase(self) -> int:
        """Get tiers to purchase"""
        return self.tiers_to_purchase

    def set_tiers_to_purchase(self, tiers: int) -> None:
        """Set tiers to purchase"""
        self.tiers_to_purchase = max(1, min(10, tiers))  # Limit 1-10 tiers
        self.total_cost = self.tiers_to_purchase * self.cost_per_tier

    def execute(self, avatar: any) -> int:
        """Execute purchase brawl pass progress command"""
        # Calculate total cost
        self.total_cost = self.tiers_to_purchase * self.cost_per_tier

        # Check if player has enough gems
        if avatar.diamonds < self.total_cost:
            return -1  # Insufficient gems

        # Get battle pass data
        if not hasattr(avatar, 'battle_pass_data'):
            avatar.battle_pass_data = {}

        if self.season_id not in avatar.battle_pass_data:
            avatar.battle_pass_data[self.season_id] = {
                'tokens': 0,
                'tier': 0,
                'claimed_free': [],
                'claimed_premium': []
            }

        battle_pass = avatar.battle_pass_data[self.season_id]
        current_tier = battle_pass['tier']
        max_tier = 30  # Maximum tier

        # Check if can purchase tiers
        if current_tier + self.tiers_to_purchase > max_tier:
            return -2  # Would exceed max tier

        # Deduct gems
        avatar.diamonds -= self.total_cost

        # Add tiers
        new_tier = current_tier + self.tiers_to_purchase
        battle_pass['tier'] = new_tier

        # Add corresponding tokens
        tokens_per_tier = 100
        battle_pass['tokens'] += self.tiers_to_purchase * tokens_per_tier

        # Auto-claim free rewards for purchased tiers
        for tier in range(current_tier + 1, new_tier + 1):
            if tier not in battle_pass['claimed_free']:
                battle_pass['claimed_free'].append(tier)
                # Apply free tier rewards
                self._apply_free_tier_reward(avatar, tier)

        return 0

    def _apply_free_tier_reward(self, avatar: any, tier: int) -> None:
        """Apply free tier reward"""
        # Simple reward system
        reward_coins = tier * 100
        reward_tokens = tier * 10

        avatar.gold += reward_coins
        if not hasattr(avatar, 'tokens'):
            avatar.tokens = 0
        avatar.tokens += reward_tokens

    def encode(self, stream) -> None:
        """Encode command to stream"""
        super().encode(stream)
        stream.write_v_int(self.season_id)
        stream.write_v_int(self.tiers_to_purchase)
        stream.write_v_int(self.cost_per_tier)
        stream.write_v_int(self.total_cost)

    def decode(self, stream) -> None:
        """Decode command from stream"""
        super().decode(stream)
        self.season_id = stream.read_v_int()
        self.tiers_to_purchase = stream.read_v_int()
        self.cost_per_tier = stream.read_v_int()
        self.total_cost = stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        return f"PurchaseBrawlPassProgressCommand(season={self.season_id}, tiers={self.tiers_to_purchase}, cost={self.total_cost})"
