"""
Python conversion of Supercell.Laser.Logic.Data.AllianceBadgeData.cs
Alliance badge data class for club badges
"""

from .data_tables import LogicData

class AllianceBadgeData(LogicData):
    """Alliance badge data class for club badges"""

    def __init__(self):
        """Initialize alliance badge data"""
        super().__init__()
        self.name = ""
        self.icon_swf = ""
        self.icon_export_name = ""
        self.category = ""

    def get_name(self) -> str:
        """Get badge name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set badge name"""
        self.name = name

    def get_icon_swf(self) -> str:
        """Get icon SWF file"""
        return self.icon_swf

    def set_icon_swf(self, swf: str) -> None:
        """Set icon SWF file"""
        self.icon_swf = swf

    def get_icon_export_name(self) -> str:
        """Get icon export name"""
        return self.icon_export_name

    def set_icon_export_name(self, export_name: str) -> None:
        """Set icon export name"""
        self.icon_export_name = export_name

    def get_category(self) -> str:
        """Get badge category"""
        return self.category

    def set_category(self, category: str) -> None:
        """Set badge category"""
        self.category = category

    def has_icon(self) -> bool:
        """Check if badge has icon"""
        return self.icon_swf != "" and self.icon_export_name != ""

    def __str__(self) -> str:
        """String representation"""
        return f"AllianceBadgeData('{self.name}', category='{self.category}')"
