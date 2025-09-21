"""
Python conversion of Supercell.Laser.Logic.Battle.Component.Accessory.cs
Accessory component for battle items and equipment
"""

from typing import Dict, Optional, Any

class AccessoryType:
    """Accessory types enumeration"""
    NONE = 0
    GADGET = 1
    STAR_POWER = 2
    HYPERCHARGE = 3

class Accessory:
    """Accessory component for battle items and equipment"""

    def __init__(self, accessory_id: int = 0):
        """Initialize accessory"""
        self.accessory_id = accessory_id
        self.accessory_type = AccessoryType.NONE
        self.hero_data_id = 0
        self.level = 1
        self.is_active = False
        self.cooldown_remaining = 0
        self.max_cooldown = 0
        self.uses_remaining = 0
        self.max_uses = 0

        # Effect properties
        self.damage_modifier = 1.0
        self.speed_modifier = 1.0
        self.health_modifier = 1.0
        self.range_modifier = 1.0

        # Visual properties
        self.name = ""
        self.description = ""
        self.icon_id = 0
        self.rarity = 0

    def get_accessory_id(self) -> int:
        """Get accessory ID"""
        return self.accessory_id

    def set_accessory_id(self, accessory_id: int) -> None:
        """Set accessory ID"""
        self.accessory_id = accessory_id

    def get_accessory_type(self) -> int:
        """Get accessory type"""
        return self.accessory_type

    def set_accessory_type(self, accessory_type: int) -> None:
        """Set accessory type"""
        self.accessory_type = accessory_type

    def get_hero_data_id(self) -> int:
        """Get hero data ID this accessory belongs to"""
        return self.hero_data_id

    def set_hero_data_id(self, hero_id: int) -> None:
        """Set hero data ID"""
        self.hero_data_id = hero_id

    def get_level(self) -> int:
        """Get accessory level"""
        return self.level

    def set_level(self, level: int) -> None:
        """Set accessory level"""
        self.level = max(1, level)

    def is_accessory_active(self) -> bool:
        """Check if accessory is active"""
        return self.is_active

    def activate(self) -> bool:
        """Activate accessory"""
        if self.can_activate():
            self.is_active = True
            if self.max_uses > 0:
                self.uses_remaining = self.max_uses
            if self.max_cooldown > 0:
                self.cooldown_remaining = self.max_cooldown
            return True
        return False

    def deactivate(self) -> None:
        """Deactivate accessory"""
        self.is_active = False
        self.cooldown_remaining = 0

    def can_activate(self) -> bool:
        """Check if accessory can be activated"""
        return (self.cooldown_remaining <= 0 and 
                (self.max_uses == 0 or self.uses_remaining > 0))

    def use(self) -> bool:
        """Use accessory (consumes one use if limited)"""
        if self.is_active and (self.max_uses == 0 or self.uses_remaining > 0):
            if self.max_uses > 0:
                self.uses_remaining -= 1
                if self.uses_remaining <= 0:
                    self.deactivate()
            return True
        return False

    def update_cooldown(self, delta_time: float) -> None:
        """Update cooldown timer"""
        if self.cooldown_remaining > 0:
            self.cooldown_remaining = max(0, self.cooldown_remaining - delta_time)

    def get_damage_multiplier(self) -> float:
        """Get damage multiplier effect"""
        return self.damage_modifier if self.is_active else 1.0

    def get_speed_multiplier(self) -> float:
        """Get speed multiplier effect"""
        return self.speed_modifier if self.is_active else 1.0

    def get_health_multiplier(self) -> float:
        """Get health multiplier effect"""
        return self.health_modifier if self.is_active else 1.0

    def get_range_multiplier(self) -> float:
        """Get range multiplier effect"""
        return self.range_modifier if self.is_active else 1.0

    def is_gadget(self) -> bool:
        """Check if this is a gadget"""
        return self.accessory_type == AccessoryType.GADGET

    def is_star_power(self) -> bool:
        """Check if this is a star power"""
        return self.accessory_type == AccessoryType.STAR_POWER

    def is_hypercharge(self) -> bool:
        """Check if this is a hypercharge"""
        return self.accessory_type == AccessoryType.HYPERCHARGE

    def get_type_name(self) -> str:
        """Get accessory type name"""
        type_names = {
            AccessoryType.NONE: "None",
            AccessoryType.GADGET: "Gadget",
            AccessoryType.STAR_POWER: "Star Power",
            AccessoryType.HYPERCHARGE: "Hypercharge"
        }
        return type_names.get(self.accessory_type, "Unknown")

    def encode(self, stream) -> None:
        """Encode accessory to stream"""
        stream.write_v_int(self.accessory_id)
        stream.write_v_int(self.accessory_type)
        stream.write_v_int(self.hero_data_id)
        stream.write_v_int(self.level)
        stream.write_boolean(self.is_active)
        stream.write_v_int(self.cooldown_remaining)
        stream.write_v_int(self.uses_remaining)

    def decode(self, stream) -> None:
        """Decode accessory from stream"""
        self.accessory_id = stream.read_v_int()
        self.accessory_type = stream.read_v_int()
        self.hero_data_id = stream.read_v_int()
        self.level = stream.read_v_int()
        self.is_active = stream.read_boolean()
        self.cooldown_remaining = stream.read_v_int()
        self.uses_remaining = stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        status = "active" if self.is_active else "inactive"
        return f"Accessory({self.get_type_name()}, level={self.level}, {status})"
