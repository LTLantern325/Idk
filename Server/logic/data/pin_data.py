"""
Python conversion of Supercell.Laser.Logic.Data.PinData.cs
Pin data class for player pins/badges
"""

from .data_tables import LogicData

class PinData(LogicData):
    """Pin data class for player pins"""

    def __init__(self):
        """Initialize pin data"""
        super().__init__()
        self.name = ""
        self.type = ""
        self.rarity = 0
        self.sort_order = 0
        self.icon_swf = ""
        self.icon_export_name = ""
        self.required_trophies = 0
        self.required_wins = 0
        self.seasonal = False
        self.limited_time = False

    def get_name(self) -> str:
        """Get pin name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set pin name"""
        self.name = name

    def get_type(self) -> str:
        """Get pin type"""
        return self.type

    def set_type(self, pin_type: str) -> None:
        """Set pin type"""
        self.type = pin_type

    def get_rarity(self) -> int:
        """Get pin rarity"""
        return self.rarity

    def set_rarity(self, rarity: int) -> None:
        """Set pin rarity"""
        self.rarity = max(0, rarity)

    def is_seasonal(self) -> bool:
        """Check if pin is seasonal"""
        return self.seasonal

    def set_seasonal(self, seasonal: bool) -> None:
        """Set seasonal status"""
        self.seasonal = seasonal

    def is_limited_time(self) -> bool:
        """Check if pin is limited time"""
        return self.limited_time

    def set_limited_time(self, limited: bool) -> None:
        """Set limited time status"""
        self.limited_time = limited

    def is_unlocked(self, player_trophies: int, player_wins: int) -> bool:
        """Check if pin is unlocked"""
        trophy_requirement = player_trophies >= self.required_trophies
        wins_requirement = player_wins >= self.required_wins
        return trophy_requirement and wins_requirement

    def __str__(self) -> str:
        """String representation"""
        return f"PinData('{self.name}', type='{self.type}', rarity={self.rarity})"
