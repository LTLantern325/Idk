"""
Python conversion of Supercell.Laser.Logic.Battle.Component.Gear.cs
Gear component for brawler equipment and upgrades
"""

from typing import Dict, List, Optional
from enum import IntEnum

class GearType(IntEnum):
    """Gear types"""
    DAMAGE = 1
    HEALTH = 2
    SPEED = 3
    VISION = 4
    SHIELD = 5
    GADGET_CHARGE = 6
    SUPER_CHARGE = 7

class GearRarity(IntEnum):
    """Gear rarities"""
    COMMON = 1
    RARE = 2
    EPIC = 3
    MYTHIC = 4
    LEGENDARY = 5

class Gear:
    """Gear component for brawler equipment and upgrades"""

    def __init__(self, gear_id: int = 0):
        """Initialize gear"""
        self.gear_id = gear_id
        self.gear_type = GearType.DAMAGE
        self.level = 1
        self.rarity = GearRarity.COMMON
        self.hero_data_id = 0
        self.is_equipped = False
        self.scrap_cost = 0
        self.coins_cost = 0

        # Stat bonuses
        self.damage_bonus = 0
        self.health_bonus = 0
        self.speed_bonus = 0
        self.vision_bonus = 0
        self.shield_bonus = 0

        # Upgrade costs
        self.upgrade_scrap_cost = 0
        self.upgrade_coins_cost = 0

        # Visual properties
        self.name = ""
        self.description = ""
        self.icon_id = 0

        self._initialize_gear_stats()

    def _initialize_gear_stats(self) -> None:
        """Initialize gear stats based on type and level"""
        base_bonus = self.level * 10

        if self.gear_type == GearType.DAMAGE:
            self.damage_bonus = base_bonus
            self.name = "Damage Gear"
        elif self.gear_type == GearType.HEALTH:
            self.health_bonus = base_bonus * 5
            self.name = "Health Gear"
        elif self.gear_type == GearType.SPEED:
            self.speed_bonus = base_bonus // 5
            self.name = "Speed Gear"
        elif self.gear_type == GearType.VISION:
            self.vision_bonus = base_bonus // 2
            self.name = "Vision Gear"
        elif self.gear_type == GearType.SHIELD:
            self.shield_bonus = base_bonus * 3
            self.name = "Shield Gear"

    def get_gear_id(self) -> int:
        """Get gear ID"""
        return self.gear_id

    def set_gear_id(self, gear_id: int) -> None:
        """Set gear ID"""
        self.gear_id = gear_id

    def get_gear_type(self) -> GearType:
        """Get gear type"""
        return self.gear_type

    def set_gear_type(self, gear_type: GearType) -> None:
        """Set gear type"""
        self.gear_type = gear_type
        self._initialize_gear_stats()

    def get_level(self) -> int:
        """Get gear level"""
        return self.level

    def set_level(self, level: int) -> None:
        """Set gear level"""
        self.level = max(1, min(3, level))  # Gears have max level 3
        self._initialize_gear_stats()

    def get_rarity(self) -> GearRarity:
        """Get gear rarity"""
        return self.rarity

    def set_rarity(self, rarity: GearRarity) -> None:
        """Set gear rarity"""
        self.rarity = rarity

    def get_hero_data_id(self) -> int:
        """Get hero data ID"""
        return self.hero_data_id

    def set_hero_data_id(self, hero_id: int) -> None:
        """Set hero data ID"""
        self.hero_data_id = hero_id

    def is_gear_equipped(self) -> bool:
        """Check if gear is equipped"""
        return self.is_equipped

    def equip(self) -> None:
        """Equip gear"""
        self.is_equipped = True

    def unequip(self) -> None:
        """Unequip gear"""
        self.is_equipped = False

    def can_upgrade(self) -> bool:
        """Check if gear can be upgraded"""
        return self.level < 3  # Max level is 3

    def upgrade(self) -> bool:
        """Upgrade gear to next level"""
        if self.can_upgrade():
            self.level += 1
            self._initialize_gear_stats()
            return True
        return False

    def get_upgrade_cost(self) -> Dict[str, int]:
        """Get upgrade cost for next level"""
        if not self.can_upgrade():
            return {}

        scrap_cost = self.level * 100
        coins_cost = self.level * 500

        return {
            'scrap': scrap_cost,
            'coins': coins_cost
        }

    def get_stat_bonus(self, stat_type: str) -> int:
        """Get bonus for specific stat"""
        bonuses = {
            'damage': self.damage_bonus,
            'health': self.health_bonus,
            'speed': self.speed_bonus,
            'vision': self.vision_bonus,
            'shield': self.shield_bonus
        }
        return bonuses.get(stat_type, 0)

    def get_total_stat_bonus(self) -> int:
        """Get total stat bonus value"""
        return (self.damage_bonus + self.health_bonus + 
                self.speed_bonus + self.vision_bonus + self.shield_bonus)

    def get_power_rating(self) -> int:
        """Get gear power rating"""
        base_power = self.level * 10
        rarity_multiplier = int(self.rarity) * 0.5
        return int(base_power * (1 + rarity_multiplier))

    def get_type_name(self) -> str:
        """Get gear type name"""
        type_names = {
            GearType.DAMAGE: "Damage",
            GearType.HEALTH: "Health",
            GearType.SPEED: "Speed",
            GearType.VISION: "Vision",
            GearType.SHIELD: "Shield",
            GearType.GADGET_CHARGE: "Gadget Charge",
            GearType.SUPER_CHARGE: "Super Charge"
        }
        return type_names.get(self.gear_type, "Unknown")

    def get_rarity_name(self) -> str:
        """Get gear rarity name"""
        rarity_names = {
            GearRarity.COMMON: "Common",
            GearRarity.RARE: "Rare",
            GearRarity.EPIC: "Epic",
            GearRarity.MYTHIC: "Mythic",
            GearRarity.LEGENDARY: "Legendary"
        }
        return rarity_names.get(self.rarity, "Unknown")

    def encode(self, stream) -> None:
        """Encode gear to stream"""
        stream.write_v_int(self.gear_id)
        stream.write_v_int(int(self.gear_type))
        stream.write_v_int(self.level)
        stream.write_v_int(int(self.rarity))
        stream.write_v_int(self.hero_data_id)
        stream.write_boolean(self.is_equipped)

    def decode(self, stream) -> None:
        """Decode gear from stream"""
        self.gear_id = stream.read_v_int()
        self.gear_type = GearType(stream.read_v_int())
        self.level = stream.read_v_int()
        self.rarity = GearRarity(stream.read_v_int())
        self.hero_data_id = stream.read_v_int()
        self.is_equipped = stream.read_boolean()
        self._initialize_gear_stats()

    def __str__(self) -> str:
        """String representation"""
        status = "equipped" if self.is_equipped else "unequipped"
        return f"Gear({self.get_type_name()}, level={self.level}, {self.get_rarity_name()}, {status})"
