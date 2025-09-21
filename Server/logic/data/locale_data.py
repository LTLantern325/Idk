"""
Python conversion of Supercell.Laser.Logic.Data.LocaleData.cs
Locale data class for text localization
"""

from .data_tables import LogicData

class LocaleData(LogicData):
    """Locale data class for text localization"""

    def __init__(self):
        """Initialize locale data"""
        super().__init__()
        self.name = ""
        self.enabled = True
        self.locale_code = ""
        self.language_code = ""
        self.country_code = ""
        self.direction = "ltr"  # "ltr" or "rtl"
        self.test_language = False
        self.completeness = 100.0

    def get_name(self) -> str:
        """Get locale name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set locale name"""
        self.name = name

    def is_enabled(self) -> bool:
        """Check if locale is enabled"""
        return self.enabled

    def set_enabled(self, enabled: bool) -> None:
        """Set enabled status"""
        self.enabled = enabled

    def get_locale_code(self) -> str:
        """Get locale code (e.g., 'en_US')"""
        return self.locale_code

    def set_locale_code(self, code: str) -> None:
        """Set locale code"""
        self.locale_code = code

    def get_language_code(self) -> str:
        """Get language code (e.g., 'en')"""
        return self.language_code

    def set_language_code(self, code: str) -> None:
        """Set language code"""
        self.language_code = code

    def get_country_code(self) -> str:
        """Get country code (e.g., 'US')"""
        return self.country_code

    def set_country_code(self, code: str) -> None:
        """Set country code"""
        self.country_code = code

    def is_rtl(self) -> bool:
        """Check if locale uses right-to-left text direction"""
        return self.direction == "rtl"

    def set_rtl(self, rtl: bool) -> None:
        """Set text direction"""
        self.direction = "rtl" if rtl else "ltr"

    def is_test_language(self) -> bool:
        """Check if this is a test language"""
        return self.test_language

    def set_test_language(self, test: bool) -> None:
        """Set test language status"""
        self.test_language = test

    def get_completeness(self) -> float:
        """Get translation completeness percentage"""
        return self.completeness

    def set_completeness(self, completeness: float) -> None:
        """Set translation completeness percentage"""
        self.completeness = max(0.0, min(100.0, completeness))

    def is_complete(self) -> bool:
        """Check if locale is fully translated"""
        return self.completeness >= 100.0

    def __str__(self) -> str:
        """String representation"""
        return f"LocaleData('{self.name}', code='{self.locale_code}', {self.completeness:.1f}%)"
