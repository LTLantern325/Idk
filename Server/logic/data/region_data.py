"""
Python conversion of Supercell.Laser.Logic.Data.RegionData.cs
Region data for server regions
"""

from .data_tables import LogicData

class RegionData(LogicData):
    """Region data class"""

    def __init__(self):
        """Initialize region data"""
        super().__init__()
        self.name = ""
        self.display_name = ""
        self.is_country = False
        self.country_code = ""

    def get_name(self) -> str:
        """Get region name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set region name"""
        self.name = name

    def get_display_name(self) -> str:
        """Get display name"""
        return self.display_name

    def set_display_name(self, display_name: str) -> None:
        """Set display name"""
        self.display_name = display_name

    def is_country_region(self) -> bool:
        """Check if region represents a country"""
        return self.is_country

    def set_country(self, is_country: bool) -> None:
        """Set country status"""
        self.is_country = is_country

    def get_country_code(self) -> str:
        """Get country code"""
        return self.country_code

    def set_country_code(self, code: str) -> None:
        """Set country code"""
        self.country_code = code

    def __str__(self) -> str:
        """String representation"""
        return f"RegionData('{self.name}', code='{self.country_code}')"
