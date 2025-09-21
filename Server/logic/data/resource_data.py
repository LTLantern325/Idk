"""
Python conversion of Supercell.Laser.Logic.Data.ResourceData.cs
Resource data class for game currencies and items
"""

from .data_tables import LogicData

class ResourceData(LogicData):
    """Resource data class"""

    def __init__(self):
        """Initialize resource data"""
        super().__init__()
        self.name = ""
        self.currency = False
        self.premium_currency = False
        self.hard_currency = False
        self.hidden_from_client = False
        self.cap = 0
        self.starting_amount = 0
        self.rarity = ""
        self.icon_file = ""
        self.collect_effect = ""
        self.pile_count = 1

    def get_name(self) -> str:
        """Get resource name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set resource name"""
        self.name = name

    def is_currency(self) -> bool:
        """Check if resource is currency"""
        return self.currency

    def set_currency(self, currency: bool) -> None:
        """Set currency status"""
        self.currency = currency

    def is_premium_currency(self) -> bool:
        """Check if premium currency"""
        return self.premium_currency

    def set_premium_currency(self, premium: bool) -> None:
        """Set premium currency status"""
        self.premium_currency = premium

    def is_hard_currency(self) -> bool:
        """Check if hard currency"""
        return self.hard_currency

    def set_hard_currency(self, hard: bool) -> None:
        """Set hard currency status"""
        self.hard_currency = hard

    def is_hidden_from_client(self) -> bool:
        """Check if hidden from client"""
        return self.hidden_from_client

    def set_hidden_from_client(self, hidden: bool) -> None:
        """Set hidden from client"""
        self.hidden_from_client = hidden

    def get_cap(self) -> int:
        """Get resource cap"""
        return self.cap

    def set_cap(self, cap: int) -> None:
        """Set resource cap"""
        self.cap = max(0, cap)

    def get_starting_amount(self) -> int:
        """Get starting amount"""
        return self.starting_amount

    def set_starting_amount(self, amount: int) -> None:
        """Set starting amount"""
        self.starting_amount = max(0, amount)

    def has_cap(self) -> bool:
        """Check if resource has cap"""
        return self.cap > 0

    def is_capped_amount(self, amount: int) -> int:
        """Get capped amount"""
        if self.has_cap():
            return min(amount, self.cap)
        return amount
