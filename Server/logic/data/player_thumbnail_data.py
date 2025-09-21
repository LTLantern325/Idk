"""
Python conversion of Supercell.Laser.Logic.Data.PlayerThumbnailData.cs
Player thumbnail data class (simplified)
"""

from .data_tables import LogicData

class PlayerThumbnailData(LogicData):
    """Player thumbnail data class"""

    def __init__(self):
        """Initialize player thumbnail data"""
        super().__init__()
        self.name = ""

        # Commented out in original C# - keeping for completeness
        self.required_exp_level = 0
        self.required_total_trophies = 0
        self.required_season_points = 0
        self.required_hero = ""
        self.icon_swf = ""
        self.icon_export_name = ""
        self.sort_order = 0

    def get_name(self) -> str:
        """Get thumbnail name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set thumbnail name"""
        self.name = name

    def get_required_exp_level(self) -> int:
        """Get required experience level"""
        return self.required_exp_level

    def set_required_exp_level(self, level: int) -> None:
        """Set required experience level"""
        self.required_exp_level = max(0, level)

    def get_required_trophies(self) -> int:
        """Get required total trophies"""
        return self.required_total_trophies

    def set_required_trophies(self, trophies: int) -> None:
        """Set required total trophies"""
        self.required_total_trophies = max(0, trophies)

    def is_unlocked(self, player_level: int, player_trophies: int) -> bool:
        """Check if thumbnail is unlocked for player"""
        level_requirement_met = player_level >= self.required_exp_level
        trophy_requirement_met = player_trophies >= self.required_total_trophies
        return level_requirement_met and trophy_requirement_met

    def __str__(self) -> str:
        """String representation"""
        return f"PlayerThumbnailData('{self.name}')"
