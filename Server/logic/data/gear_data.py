"""
Python conversion of Supercell.Laser.Logic.Data.GearData.cs
Gear data class for character equipment
"""

from .data_tables import LogicData

class GearData(LogicData):
    """Gear data class for character equipment"""

    def __init__(self):
        """Initialize gear data"""
        super().__init__()
        self.name = ""
        self.disabled = False
        self.tier = 1
        self.required_level = 1
        self.cost = 0
        self.cost_currency = ""
        self.character_requirement = ""
        self.gear_type = ""  # Type of gear (e.g., "Health", "Damage", "Speed")
        self.effect_value = 0
        self.max_level = 3

    def get_name(self) -> str:
        """Get gear name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set gear name"""
        self.name = name

    def is_disabled(self) -> bool:
        """Check if gear is disabled"""
        return self.disabled

    def set_disabled(self, disabled: bool) -> None:
        """Set disabled status"""
        self.disabled = disabled

    def get_tier(self) -> int:
        """Get gear tier"""
        return self.tier

    def set_tier(self, tier: int) -> None:
        """Set gear tier"""
        self.tier = max(1, tier)

    def get_required_level(self) -> int:
        """Get required character level"""
        return self.required_level

    def set_required_level(self, level: int) -> None:
        """Set required character level"""
        self.required_level = max(1, level)

    def get_cost(self) -> int:
        """Get gear cost"""
        return self.cost

    def set_cost(self, cost: int) -> None:
        """Set gear cost"""
        self.cost = max(0, cost)

    def get_gear_type(self) -> str:
        """Get gear type"""
        return self.gear_type

    def set_gear_type(self, gear_type: str) -> None:
        """Set gear type"""
        self.gear_type = gear_type

    def is_available(self) -> bool:
        """Check if gear is available"""
        return not self.disabled and self.name != ""

    def __str__(self) -> str:
        """String representation"""
        return f"GearData('{self.name}', tier={self.tier}, type='{self.gear_type}')"
