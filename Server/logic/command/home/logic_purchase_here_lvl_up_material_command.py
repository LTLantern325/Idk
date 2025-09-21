"""
Python conversion of Supercell.Laser.Logic.Command.Home.LogicPurchaseHeroLvlUpMaterialCommand.cs
Command for purchasing hero level up materials (power points)
"""

from ..command import Command

class LogicPurchaseHeroLvlUpMaterialCommand(Command):
    """Command for purchasing hero level up materials (power points)"""

    def __init__(self):
        """Initialize purchase hero level up material command"""
        super().__init__()
        self.hero_global_id = 0
        self.material_type = 0  # 0=power_points, 1=coins
        self.amount = 0
        self.cost_type = 0  # 0=coins, 1=gems
        self.cost_amount = 0

    def get_hero_global_id(self) -> int:
        """Get hero global ID"""
        return self.hero_global_id

    def set_hero_global_id(self, global_id: int) -> None:
        """Set hero global ID"""
        self.hero_global_id = global_id

    def get_material_type(self) -> int:
        """Get material type"""
        return self.material_type

    def set_material_type(self, material_type: int) -> None:
        """Set material type"""
        self.material_type = material_type

    def get_amount(self) -> int:
        """Get amount to purchase"""
        return self.amount

    def set_amount(self, amount: int) -> None:
        """Set amount to purchase"""
        self.amount = amount
        self._calculate_cost()

    def _calculate_cost(self) -> None:
        """Calculate cost based on material type and amount"""
        if self.material_type == 0:  # Power points
            # Power points cost coins (1 power point = 2 coins)
            self.cost_type = 0  # Coins
            self.cost_amount = self.amount * 2
        elif self.material_type == 1:  # Additional coins
            # Bonus coins cost gems (1 gem = 100 coins)
            self.cost_type = 1  # Gems
            self.cost_amount = max(1, self.amount // 100)

    def execute(self, avatar: any) -> int:
        """Execute purchase hero level up material command"""
        # Check cost
        if self.cost_type == 0:  # Coins
            if avatar.gold < self.cost_amount:
                return -1  # Insufficient coins
        else:  # Gems
            if avatar.diamonds < self.cost_amount:
                return -1  # Insufficient gems

        # Check if hero exists
        if not hasattr(avatar, 'unlocked_characters'):
            avatar.unlocked_characters = []

        if self.hero_global_id not in avatar.unlocked_characters:
            return -2  # Hero not unlocked

        # Deduct cost
        if self.cost_type == 0:  # Coins
            avatar.gold -= self.cost_amount
        else:  # Gems
            avatar.diamonds -= self.cost_amount

        # Give materials
        if self.material_type == 0:  # Power points
            if not hasattr(avatar, 'hero_power_points'):
                avatar.hero_power_points = {}

            if self.hero_global_id not in avatar.hero_power_points:
                avatar.hero_power_points[self.hero_global_id] = 0

            avatar.hero_power_points[self.hero_global_id] += self.amount
        elif self.material_type == 1:  # Additional coins
            avatar.gold += self.amount

        return 0

    def encode(self, stream) -> None:
        """Encode command to stream"""
        super().encode(stream)
        stream.write_v_int(self.hero_global_id)
        stream.write_v_int(self.material_type)
        stream.write_v_int(self.amount)
        stream.write_v_int(self.cost_type)
        stream.write_v_int(self.cost_amount)

    def decode(self, stream) -> None:
        """Decode command from stream"""
        super().decode(stream)
        self.hero_global_id = stream.read_v_int()
        self.material_type = stream.read_v_int()
        self.amount = stream.read_v_int()
        self.cost_type = stream.read_v_int()
        self.cost_amount = stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        materials = ["Power Points", "Coins"]
        costs = ["Coins", "Gems"]
        material_name = materials[self.material_type] if self.material_type < len(materials) else "Unknown"
        cost_name = costs[self.cost_type] if self.cost_type < len(costs) else "Unknown"
        return f"PurchaseHeroLvlUpMaterialCommand(hero={self.hero_global_id}, {self.amount} {material_name} for {self.cost_amount} {cost_name})"
