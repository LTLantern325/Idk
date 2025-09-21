"""
Python conversion of Supercell.Laser.Logic.Data.ThemeData.cs
Theme data class for map themes and environments
"""

from .data_tables import LogicData

class ThemeData(LogicData):
    """Theme data class for map themes"""

    def __init__(self):
        """Initialize theme data"""
        super().__init__()
        self.name = ""
        self.disabled = False
        self.background_texture = ""
        self.music = ""
        self.ambient_sound = ""
        self.color_scheme = ""
        self.particle_effects = ""
        self.lighting_preset = ""

    def get_name(self) -> str:
        """Get theme name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set theme name"""
        self.name = name

    def is_disabled(self) -> bool:
        """Check if theme is disabled"""
        return self.disabled

    def set_disabled(self, disabled: bool) -> None:
        """Set disabled status"""
        self.disabled = disabled

    def get_background_texture(self) -> str:
        """Get background texture"""
        return self.background_texture

    def set_background_texture(self, texture: str) -> None:
        """Set background texture"""
        self.background_texture = texture

    def get_music(self) -> str:
        """Get theme music"""
        return self.music

    def set_music(self, music: str) -> None:
        """Set theme music"""
        self.music = music

    def get_ambient_sound(self) -> str:
        """Get ambient sound"""
        return self.ambient_sound

    def set_ambient_sound(self, sound: str) -> None:
        """Set ambient sound"""
        self.ambient_sound = sound

    def has_audio(self) -> bool:
        """Check if theme has audio components"""
        return self.music != "" or self.ambient_sound != ""

    def is_available(self) -> bool:
        """Check if theme is available"""
        return not self.disabled and self.name != ""

    def __str__(self) -> str:
        """String representation"""
        status = "disabled" if self.disabled else "enabled"
        return f"ThemeData('{self.name}', {status})"
