"""
Python conversion of Supercell.Laser.Logic.Data.ItemData.cs
Item data class for game items
"""

from .data_tables import LogicData

class ItemData(LogicData):
    """Item data class"""

    def __init__(self):
        """Initialize item data"""
        super().__init__()
        self.name = ""
        self.type = ""
        self.rarity = ""
        self.consumable = False
        self.stackable = False
        self.max_stack = 1
        self.sell_value = 0
        self.buy_cost = 0
        self.description = ""
        self.icon_file = ""
        self.use_effect = ""
        self.level_requirement = 0
        self.character_requirement = ""

    def get_name(self) -> str:
        """Get item name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set item name"""
        self.name = name

    def get_type(self) -> str:
        """Get item type"""
        return self.type

    def set_type(self, item_type: str) -> None:
        """Set item type"""
        self.type = item_type

    def get_rarity(self) -> str:
        """Get item rarity"""
        return self.rarity

    def set_rarity(self, rarity: str) -> None:
        """Set item rarity"""
        self.rarity = rarity

    def is_consumable(self) -> bool:
        """Check if item is consumable"""
        return self.consumable

    def set_consumable(self, consumable: bool) -> None:
        """Set consumable status"""
        self.consumable = consumable

    def is_stackable(self) -> bool:
        """Check if item is stackable"""
        return self.stackable

    def set_stackable(self, stackable: bool) -> None:
        """Set stackable status"""
        self.stackable = stackable

    def get_max_stack(self) -> int:
        """Get maximum stack size"""
        return self.max_stack

    def set_max_stack(self, max_stack: int) -> None:
        """Set maximum stack size"""
        self.max_stack = max(1, max_stack)

    def get_sell_value(self) -> int:
        """Get sell value"""
        return self.sell_value

    def set_sell_value(self, value: int) -> None:
        """Set sell value"""
        self.sell_value = max(0, value)

    def get_buy_cost(self) -> int:
        """Get buy cost"""
        return self.buy_cost

    def set_buy_cost(self, cost: int) -> None:
        """Set buy cost"""
        self.buy_cost = max(0, cost)

    def get_description(self) -> str:
        """Get item description"""
        return self.description

    def set_description(self, description: str) -> None:
        """Set item description"""
        self.description = description

    def can_sell(self) -> bool:
        """Check if item can be sold"""
        return self.sell_value > 0

    def can_buy(self) -> bool:
        """Check if item can be bought"""
        return self.buy_cost > 0

    def meets_level_requirement(self, player_level: int) -> bool:
        """Check if player meets level requirement"""
        return player_level >= self.level_requirement

    def meets_character_requirement(self, character_name: str) -> bool:
        """Check if character requirement is met"""
        return not self.character_requirement or self.character_requirement == character_name
