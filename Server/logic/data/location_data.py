"""
Python conversion of Supercell.Laser.Logic.Data.LocationData.cs
Location data for game maps and environments
"""

from .data_tables import LogicData

class LocationData(LogicData):
    """Location data class for maps"""

    def __init__(self):
        """Initialize location data"""
        super().__init__()
        self.name = ""
        self.disabled = False
        self.tid = ""  # Text ID for localization
        self.game_mode_variation = ""
        self.map = ""  # Map file reference

    def get_name(self) -> str:
        """Get location name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set location name"""
        self.name = name

    def is_disabled(self) -> bool:
        """Check if location is disabled"""
        return self.disabled

    def set_disabled(self, disabled: bool) -> None:
        """Set disabled status"""
        self.disabled = disabled

    def get_text_id(self) -> str:
        """Get text ID for localization"""
        return self.tid

    def set_text_id(self, tid: str) -> None:
        """Set text ID"""
        self.tid = tid

    def get_game_mode_variation(self) -> str:
        """Get game mode variation"""
        return self.game_mode_variation

    def set_game_mode_variation(self, gmv: str) -> None:
        """Set game mode variation"""
        self.game_mode_variation = gmv

    def get_map(self) -> str:
        """Get map reference"""
        return self.map

    def set_map(self, map_ref: str) -> None:
        """Set map reference"""
        self.map = map_ref

    def is_available(self) -> bool:
        """Check if location is available"""
        return not self.disabled and self.name != ""

    def has_map(self) -> bool:
        """Check if location has map"""
        return self.map != ""

    def __str__(self) -> str:
        """String representation"""
        status = "disabled" if self.disabled else "enabled"
        return f"LocationData('{self.name}', {self.game_mode_variation}, {status})"
