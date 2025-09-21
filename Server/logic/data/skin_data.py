"""
Python conversion of Supercell.Laser.Logic.Data.SkinData.cs
Skin data class for character skins
"""

from .data_tables import LogicData

class SkinData(LogicData):
    """Skin data class"""

    def __init__(self):
        """Initialize skin data"""
        super().__init__()
        self.name = ""
        self.character = ""
        self.rarity = ""
        self.cost = 0
        self.cost_currency = ""
        self.disabled = False
        self.unlocked_by_default = False
        self.campaign_unlock = ""
        self.season_unlock = 0
        self.conf_id = ""
        self.description = ""
        self.is_seasonal = False
        self.is_limited = False

    def get_name(self) -> str:
        """Get skin name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set skin name"""
        self.name = name

    def get_character(self) -> str:
        """Get associated character"""
        return self.character

    def set_character(self, character: str) -> None:
        """Set associated character"""
        self.character = character

    def get_rarity(self) -> str:
        """Get skin rarity"""
        return self.rarity

    def set_rarity(self, rarity: str) -> None:
        """Set skin rarity"""
        self.rarity = rarity

    def get_cost(self) -> int:
        """Get skin cost"""
        return self.cost

    def set_cost(self, cost: int) -> None:
        """Set skin cost"""
        self.cost = max(0, cost)

    def get_cost_currency(self) -> str:
        """Get cost currency type"""
        return self.cost_currency

    def set_cost_currency(self, currency: str) -> None:
        """Set cost currency type"""
        self.cost_currency = currency

    def is_disabled(self) -> bool:
        """Check if skin is disabled"""
        return self.disabled

    def set_disabled(self, disabled: bool) -> None:
        """Set disabled status"""
        self.disabled = disabled

    def is_unlocked_by_default(self) -> bool:
        """Check if unlocked by default"""
        return self.unlocked_by_default

    def set_unlocked_by_default(self, unlocked: bool) -> None:
        """Set unlocked by default"""
        self.unlocked_by_default = unlocked

    def has_campaign_unlock(self) -> bool:
        """Check if has campaign unlock"""
        return bool(self.campaign_unlock)

    def get_campaign_unlock(self) -> str:
        """Get campaign unlock requirement"""
        return self.campaign_unlock

    def set_campaign_unlock(self, campaign: str) -> None:
        """Set campaign unlock requirement"""
        self.campaign_unlock = campaign

    def has_season_unlock(self) -> bool:
        """Check if has season unlock"""
        return self.season_unlock > 0

    def get_season_unlock(self) -> int:
        """Get season unlock requirement"""
        return self.season_unlock

    def set_season_unlock(self, season: int) -> None:
        """Set season unlock requirement"""
        self.season_unlock = max(0, season)

    def is_free(self) -> bool:
        """Check if skin is free"""
        return self.cost == 0 or self.unlocked_by_default

    def is_purchasable(self) -> bool:
        """Check if skin can be purchased"""
        return self.cost > 0 and not self.disabled

    def is_seasonal_skin(self) -> bool:
        """Check if seasonal skin"""
        return self.is_seasonal

    def set_seasonal(self, seasonal: bool) -> None:
        """Set seasonal status"""
        self.is_seasonal = seasonal

    def is_limited_skin(self) -> bool:
        """Check if limited skin"""
        return self.is_limited

    def set_limited(self, limited: bool) -> None:
        """Set limited status"""
        self.is_limited = limited

    def is_for_character(self, character_name: str) -> bool:
        """Check if skin is for specific character"""
        return self.character == character_name
