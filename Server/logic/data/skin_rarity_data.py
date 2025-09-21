"""
Python conversion of Supercell.Laser.Logic.Data.SkinRarityData.cs
Skin rarity data class for skin pricing and rarity
"""

from .data_tables import LogicData

class SkinRarityData(LogicData):
    """Skin rarity data class for skin pricing and rarity"""

    def __init__(self):
        """Initialize skin rarity data"""
        super().__init__()
        self.name = ""
        self.price = 0
        self.rarity = 0

    def get_name(self) -> str:
        """Get rarity name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set rarity name"""
        self.name = name

    def get_price(self) -> int:
        """Get skin price"""
        return self.price

    def set_price(self, price: int) -> None:
        """Set skin price"""
        self.price = max(0, price)

    def get_rarity(self) -> int:
        """Get rarity level"""
        return self.rarity

    def set_rarity(self, rarity: int) -> None:
        """Set rarity level"""
        self.rarity = max(0, rarity)

    def is_free(self) -> bool:
        """Check if skin is free"""
        return self.price == 0

    def is_common(self) -> bool:
        """Check if rarity is common (typically 0-1)"""
        return self.rarity <= 1

    def is_rare(self) -> bool:
        """Check if rarity is rare (typically 2-3)"""
        return 2 <= self.rarity <= 3

    def is_epic(self) -> bool:
        """Check if rarity is epic (typically 4-5)"""
        return 4 <= self.rarity <= 5

    def is_legendary(self) -> bool:
        """Check if rarity is legendary (typically 6+)"""
        return self.rarity >= 6

    def get_rarity_name(self) -> str:
        """Get human-readable rarity name"""
        if self.is_common():
            return "Common"
        elif self.is_rare():
            return "Rare"
        elif self.is_epic():
            return "Epic"
        elif self.is_legendary():
            return "Legendary"
        else:
            return "Unknown"

    def __str__(self) -> str:
        """String representation"""
        return f"SkinRarityData('{self.name}', price={self.price}, rarity={self.rarity})"
