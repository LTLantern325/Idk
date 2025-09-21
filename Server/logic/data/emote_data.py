"""
Python conversion of Supercell.Laser.Logic.Data.EmoteData.cs
Emote data class for player expressions
"""

from .data_tables import LogicData

class EmoteData(LogicData):
    """Emote data class"""

    def __init__(self):
        """Initialize emote data"""
        super().__init__()
        self.name = ""
        self.disabled = False
        self.character = ""
        self.skin = ""
        self.give_on_skin_unlock = False
        self.is_picto = False
        self.battle_category = ""
        self.rarity = ""
        self.emote_type = ""
        self.locked_for_chronos = False
        self.is_default_battle_emote = False

    def get_name(self) -> str:
        """Get emote name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set emote name"""
        self.name = name

    def is_disabled(self) -> bool:
        """Check if emote is disabled"""
        return self.disabled

    def set_disabled(self, disabled: bool) -> None:
        """Set disabled status"""
        self.disabled = disabled

    def get_character(self) -> str:
        """Get associated character"""
        return self.character

    def set_character(self, character: str) -> None:
        """Set associated character"""
        self.character = character

    def get_skin(self) -> str:
        """Get associated skin"""
        return self.skin

    def set_skin(self, skin: str) -> None:
        """Set associated skin"""
        self.skin = skin

    def is_give_on_skin_unlock(self) -> bool:
        """Check if given on skin unlock"""
        return self.give_on_skin_unlock

    def set_give_on_skin_unlock(self, give: bool) -> None:
        """Set give on skin unlock"""
        self.give_on_skin_unlock = give

    def is_picto(self) -> bool:
        """Check if pictogram emote"""
        return self.is_picto

    def set_picto(self, picto: bool) -> None:
        """Set pictogram status"""
        self.is_picto = picto

    def get_battle_category(self) -> str:
        """Get battle category"""
        return self.battle_category

    def set_battle_category(self, category: str) -> None:
        """Set battle category"""
        self.battle_category = category

    def get_rarity(self) -> str:
        """Get emote rarity"""
        return self.rarity

    def set_rarity(self, rarity: str) -> None:
        """Set emote rarity"""
        self.rarity = rarity

    def get_emote_type(self) -> str:
        """Get emote type"""
        return self.emote_type

    def set_emote_type(self, emote_type: str) -> None:
        """Set emote type"""
        self.emote_type = emote_type

    def is_locked_for_chronos(self) -> bool:
        """Check if locked for Chronos"""
        return self.locked_for_chronos

    def set_locked_for_chronos(self, locked: bool) -> None:
        """Set locked for Chronos"""
        self.locked_for_chronos = locked

    def is_default_battle_emote(self) -> bool:
        """Check if default battle emote"""
        return self.is_default_battle_emote

    def set_default_battle_emote(self, default: bool) -> None:
        """Set default battle emote"""
        self.is_default_battle_emote = default

    def is_available_for_character(self, character_name: str) -> bool:
        """Check if emote is available for character"""
        return self.character == character_name or self.character == ""

    def is_unlocked_with_skin(self) -> bool:
        """Check if unlocked with skin"""
        return self.give_on_skin_unlock and self.skin != ""
