"""
Python conversion of Supercell.Laser.Logic.Data.AccessoryData.cs
Accessory data class for gadgets and star powers
"""

from enum import IntEnum
from .data_tables import LogicData

class AccessoryType(IntEnum):
    """Accessory type enumeration"""
    HEAL = 9
    RELOAD = 16
    PLACE = 10

class AccessoryData(LogicData):
    """Accessory data class for gadgets and star powers"""

    def __init__(self):
        """Initialize accessory data"""
        super().__init__()
        self.name = ""
        self.type = ""
        self.sub_type = 0
        self.cooldown = 0

        # Effects
        self.use_effect = ""
        self.pet_use_effect = ""
        self.looping_effect = ""
        self.looping_effect_pet = ""

        # Timing
        self.activation_delay = 0
        self.active_ticks = 0
        self.show_countdown = False

        # Movement and behavior
        self.stop_movement = False
        self.stop_pet_for_delay = False
        self.animation_index = 0
        self.set_attack_angle = False

        # Aiming
        self.aim_guide_type = 0
        self.consumes_ammo = False

        # Area effects
        self.area_effect = ""
        self.pet_area_effect = ""

        # Action handling
        self.interrupts_action = False
        self.allow_stun_activation = False

        # Pet interaction
        self.require_pet_distance = 0
        self.destroy_pet = False

        # Range and targeting
        self.range = 0
        self.require_enemy_in_range = False
        self.target_friends = False
        self.target_indirect = False

        # Shield
        self.shield_percent = 0
        self.shield_ticks = 0

        # Speed boost
        self.speed_boost = 0
        self.speed_boost_ticks = 0

        # Special conditions
        self.skip_type_condition = False
        self.usable_during_charge = 0

        # Custom properties
        self.custom_object = ""
        self.custom_value1 = 0
        self.custom_value2 = 0
        self.custom_value3 = 0
        self.custom_value4 = 0
        self.custom_value5 = 0
        self.custom_value6 = 0

        # Text messages
        self.missing_target_text = ""
        self.target_too_far_text = ""
        self.target_already_active_text = ""

    def get_name(self) -> str:
        """Get accessory name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set accessory name"""
        self.name = name

    def get_type(self) -> str:
        """Get accessory type"""
        return self.type

    def set_type(self, accessory_type: str) -> None:
        """Set accessory type"""
        self.type = accessory_type

    def get_cooldown(self) -> int:
        """Get cooldown in ticks"""
        return self.cooldown

    def set_cooldown(self, cooldown: int) -> None:
        """Set cooldown"""
        self.cooldown = max(0, cooldown)

    def has_shield(self) -> bool:
        """Check if accessory provides shield"""
        return self.shield_percent > 0 and self.shield_ticks > 0

    def has_speed_boost(self) -> bool:
        """Check if accessory provides speed boost"""
        return self.speed_boost > 0 and self.speed_boost_ticks > 0

    def has_range(self) -> bool:
        """Check if accessory has range"""
        return self.range > 0

    def requires_pet(self) -> bool:
        """Check if accessory requires pet"""
        return self.require_pet_distance > 0 or self.pet_use_effect != ""

    def affects_pet(self) -> bool:
        """Check if accessory affects pet"""
        return (self.pet_use_effect != "" or self.looping_effect_pet != "" or 
                self.pet_area_effect != "" or self.destroy_pet)

    def has_area_effect(self) -> bool:
        """Check if accessory has area effect"""
        return self.area_effect != "" or self.pet_area_effect != ""

    def stops_movement(self) -> bool:
        """Check if accessory stops movement"""
        return self.stop_movement

    def consumes_ammo(self) -> bool:
        """Check if accessory consumes ammo"""
        return self.consumes_ammo

    def can_use_during_charge(self) -> bool:
        """Check if can be used during charge"""
        return self.usable_during_charge > 0

    def get_activation_delay_ms(self) -> int:
        """Get activation delay in milliseconds"""
        return self.activation_delay * 50  # Convert ticks to ms

    def get_active_duration_ms(self) -> int:
        """Get active duration in milliseconds"""
        return self.active_ticks * 50  # Convert ticks to ms

    def get_shield_duration_ms(self) -> int:
        """Get shield duration in milliseconds"""
        return self.shield_ticks * 50  # Convert ticks to ms

    def get_speed_boost_duration_ms(self) -> int:
        """Get speed boost duration in milliseconds"""
        return self.speed_boost_ticks * 50  # Convert ticks to ms

    def is_healing_accessory(self) -> bool:
        """Check if accessory is healing type"""
        return self.type == "Heal" or AccessoryType.HEAL in str(self.sub_type)

    def is_reload_accessory(self) -> bool:
        """Check if accessory is reload type"""
        return self.type == "Reload" or AccessoryType.RELOAD in str(self.sub_type)

    def is_placement_accessory(self) -> bool:
        """Check if accessory is placement type"""
        return self.type == "Place" or AccessoryType.PLACE in str(self.sub_type)

    def __str__(self) -> str:
        """String representation"""
        return f"AccessoryData('{self.name}', type='{self.type}', cooldown={self.cooldown})"
