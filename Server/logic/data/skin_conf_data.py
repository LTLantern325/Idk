"""
Python conversion of Supercell.Laser.Logic.Data.SkinConfData.cs
Skin configuration data class (simplified version)
"""

from .data_tables import LogicData

class SkinConfData(LogicData):
    """Skin configuration data class"""

    def __init__(self):
        """Initialize skin configuration data"""
        super().__init__()
        self.name = ""
        self.character = ""
        self.skin_id = ""
        self.rarity = 0
        self.cost = 0
        self.cost_currency = "Gems"
        self.required_trophies = 0
        self.seasonal = False
        self.limited_time = False
        self.featured = False
        self.sort_order = 0

        # Visual properties
        self.file_name = ""
        self.export_name = ""
        self.icon_export_name = ""

        # Animation overrides
        self.animation_overrides = ""
        self.effect_overrides = ""

        # Sound overrides
        self.sound_overrides = ""

    def get_name(self) -> str:
        """Get skin name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set skin name"""
        self.name = name

    def get_character(self) -> str:
        """Get character this skin belongs to"""
        return self.character

    def set_character(self, character: str) -> None:
        """Set character"""
        self.character = character

    def get_skin_id(self) -> str:
        """Get skin ID"""
        return self.skin_id

    def set_skin_id(self, skin_id: str) -> None:
        """Set skin ID"""
        self.skin_id = skin_id

    def get_cost(self) -> int:
        """Get skin cost"""
        return self.cost

    def set_cost(self, cost: int) -> None:
        """Set skin cost"""
        self.cost = max(0, cost)

    def is_free(self) -> bool:
        """Check if skin is free"""
        return self.cost == 0

    def is_seasonal(self) -> bool:
        """Check if skin is seasonal"""
        return self.seasonal

    def is_limited_time(self) -> bool:
        """Check if skin is limited time"""
        return self.limited_time

    def is_featured(self) -> bool:
        """Check if skin is featured"""
        return self.featured

    def has_animation_overrides(self) -> bool:
        """Check if skin has animation overrides"""
        return self.animation_overrides != ""

    def has_effect_overrides(self) -> bool:
        """Check if skin has effect overrides"""
        return self.effect_overrides != ""

    def has_sound_overrides(self) -> bool:
        """Check if skin has sound overrides"""
        return self.sound_overrides != ""

    def has_custom_assets(self) -> bool:
        """Check if skin has custom visual assets"""
        return self.file_name != "" and self.export_name != ""

    def is_unlocked(self, player_trophies: int) -> bool:
        """Check if skin is unlocked based on trophies"""
        return player_trophies >= self.required_trophies

    def __str__(self) -> str:
        """String representation"""
        return (f"SkinConfData('{self.name}' for {self.character}, "
                f"cost={self.cost}, rarity={self.rarity})")
