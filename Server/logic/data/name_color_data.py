"""
Python conversion of Supercell.Laser.Logic.Data.NameColorData.cs
Name color data class for player name colors
"""

from .data_tables import LogicData

class NameColorData(LogicData):
    """Name color data class for player name colors"""

    def __init__(self):
        """Initialize name color data"""
        super().__init__()
        self.name = ""
        self.color_code = "#FFFFFF"  # Default white
        self.required_trophies = 0
        self.required_level = 0
        self.cost = 0
        self.cost_currency = "Gems"
        self.premium = False
        self.seasonal = False
        self.sort_order = 0

    def get_name(self) -> str:
        """Get color name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set color name"""
        self.name = name

    def get_color_code(self) -> str:
        """Get color code"""
        return self.color_code

    def set_color_code(self, color: str) -> None:
        """Set color code"""
        self.color_code = color

    def get_required_trophies(self) -> int:
        """Get required trophies"""
        return self.required_trophies

    def set_required_trophies(self, trophies: int) -> None:
        """Set required trophies"""
        self.required_trophies = max(0, trophies)

    def get_cost(self) -> int:
        """Get cost"""
        return self.cost

    def set_cost(self, cost: int) -> None:
        """Set cost"""
        self.cost = max(0, cost)

    def is_free(self) -> bool:
        """Check if color is free"""
        return self.cost == 0

    def is_premium(self) -> bool:
        """Check if color is premium"""
        return self.premium

    def is_seasonal(self) -> bool:
        """Check if color is seasonal"""
        return self.seasonal

    def is_unlocked(self, player_trophies: int, player_level: int) -> bool:
        """Check if color is unlocked"""
        trophy_req = player_trophies >= self.required_trophies
        level_req = player_level >= self.required_level
        return trophy_req and level_req

    def __str__(self) -> str:
        """String representation"""
        return f"NameColorData('{self.name}', color='{self.color_code}')"
