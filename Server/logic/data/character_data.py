"""
Python conversion of Supercell.Laser.Logic.Data.CharacterData.cs
Character data class
"""

from .data_tables import LogicData

class CharacterData(LogicData):
    """Character data class"""

    def __init__(self):
        """Initialize character data"""
        super().__init__()
        self.rarity = ""
        self.disabled = False
        self.locked_for_chronos = False
        self.hit_points = 100
        self.damage = 50
        self.speed = 720
        self.weapon_skill = ""
        self.super_skill = ""
        self.gadget_skill = ""
        self.star_power_skill = ""
        self.hypercharge_skill = ""
        self.type = "Brawler"

    def is_hero(self) -> bool:
        """Check if this is a hero character"""
        return self.type == "Hero" or self.type == "Brawler"

    def get_rarity(self) -> str:
        """Get character rarity"""
        return self.rarity

    def set_rarity(self, rarity: str) -> None:
        """Set character rarity"""
        self.rarity = rarity

    def is_disabled(self) -> bool:
        """Check if character is disabled"""
        return self.disabled

    def set_disabled(self, disabled: bool) -> None:
        """Set disabled status"""
        self.disabled = disabled

    def is_locked_for_chronos(self) -> bool:
        """Check if locked for Chronos"""
        return self.locked_for_chronos

    def set_locked_for_chronos(self, locked: bool) -> None:
        """Set locked for Chronos"""
        self.locked_for_chronos = locked

    def get_hit_points(self) -> int:
        """Get hit points"""
        return self.hit_points

    def set_hit_points(self, hit_points: int) -> None:
        """Set hit points"""
        self.hit_points = hit_points

    def get_damage(self) -> int:
        """Get damage"""
        return self.damage

    def set_damage(self, damage: int) -> None:
        """Set damage"""
        self.damage = damage

    def get_speed(self) -> int:
        """Get speed"""
        return self.speed

    def set_speed(self, speed: int) -> None:
        """Set speed"""
        self.speed = speed

    def get_weapon_skill(self) -> str:
        """Get weapon skill"""
        return self.weapon_skill

    def set_weapon_skill(self, weapon_skill: str) -> None:
        """Set weapon skill"""
        self.weapon_skill = weapon_skill

    def get_super_skill(self) -> str:
        """Get super skill"""
        return self.super_skill

    def set_super_skill(self, super_skill: str) -> None:
        """Set super skill"""
        self.super_skill = super_skill
