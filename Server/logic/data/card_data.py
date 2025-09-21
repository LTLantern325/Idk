"""
Python conversion of Supercell.Laser.Logic.Data.CardData.cs
Card data class
"""

from .data_tables import LogicData

class CardData(LogicData):
    """Card data class"""

    def __init__(self):
        """Initialize card data"""
        super().__init__()
        self.rarity = ""
        self.meta_type = 0
        self.target = 0
        self.unlock_cost = 0
        self.upgrade_cost = 0
        self.power_level_required = 0

    def get_rarity(self) -> str:
        """Get card rarity"""
        return self.rarity

    def set_rarity(self, rarity: str) -> None:
        """Set card rarity"""
        self.rarity = rarity

    def get_meta_type(self) -> int:
        """Get meta type"""
        return self.meta_type

    def set_meta_type(self, meta_type: int) -> None:
        """Set meta type"""
        self.meta_type = meta_type

    def get_target(self) -> int:
        """Get target character"""
        return self.target

    def set_target(self, target: int) -> None:
        """Set target character"""
        self.target = target

    def get_unlock_cost(self) -> int:
        """Get unlock cost"""
        return self.unlock_cost

    def set_unlock_cost(self, cost: int) -> None:
        """Set unlock cost"""
        self.unlock_cost = cost

    def get_upgrade_cost(self) -> int:
        """Get upgrade cost"""
        return self.upgrade_cost

    def set_upgrade_cost(self, cost: int) -> None:
        """Set upgrade cost"""
        self.upgrade_cost = cost

    def get_power_level_required(self) -> int:
        """Get required power level"""
        return self.power_level_required

    def set_power_level_required(self, level: int) -> None:
        """Set required power level"""
        self.power_level_required = level

    def is_star_power(self) -> bool:
        """Check if this is a star power card"""
        return self.meta_type == 4

    def is_gadget(self) -> bool:
        """Check if this is a gadget card"""
        return self.meta_type == 5

    def is_hypercharge(self) -> bool:
        """Check if this is a hypercharge card"""
        return self.meta_type == 6
