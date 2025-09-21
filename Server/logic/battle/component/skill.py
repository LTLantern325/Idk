"""
Python conversion of Supercell.Laser.Logic.Battle.Component.Skill.cs
Skill component for special abilities and powers
"""

from typing import Dict, List, Optional
from enum import IntEnum

class SkillType(IntEnum):
    """Skill types"""
    ACTIVE = 1
    PASSIVE = 2
    ULTIMATE = 3
    GADGET = 4

class SkillTargetType(IntEnum):
    """Skill target types"""
    SELF = 1
    ALLY = 2
    ENEMY = 3
    AREA = 4
    GLOBAL = 5

class Skill:
    """Skill component for special abilities and powers"""

    def __init__(self, skill_id: int = 0):
        """Initialize skill"""
        self.skill_id = skill_id
        self.skill_type = SkillType.ACTIVE
        self.target_type = SkillTargetType.ENEMY
        self.level = 1
        self.hero_data_id = 0

        # Cooldown and charges
        self.cooldown = 10.0
        self.cooldown_remaining = 0.0
        self.max_charges = 1
        self.current_charges = 1
        self.charge_time = 10.0

        # Costs
        self.mana_cost = 0
        self.energy_cost = 0
        self.health_cost = 0

        # Effects
        self.damage = 0.0
        self.heal_amount = 0.0
        self.duration = 0.0
        self.range = 5.0
        self.area_of_effect = 1.0

        # Status
        self.is_unlocked = False
        self.is_equipped = False
        self.is_available = True

        # Visual properties
        self.name = ""
        self.description = ""
        self.icon_id = 0

    def get_skill_id(self) -> int:
        """Get skill ID"""
        return self.skill_id

    def set_skill_id(self, skill_id: int) -> None:
        """Set skill ID"""
        self.skill_id = skill_id

    def get_skill_type(self) -> SkillType:
        """Get skill type"""
        return self.skill_type

    def set_skill_type(self, skill_type: SkillType) -> None:
        """Set skill type"""
        self.skill_type = skill_type

    def get_target_type(self) -> SkillTargetType:
        """Get target type"""
        return self.target_type

    def set_target_type(self, target_type: SkillTargetType) -> None:
        """Set target type"""
        self.target_type = target_type

    def get_level(self) -> int:
        """Get skill level"""
        return self.level

    def set_level(self, level: int) -> None:
        """Set skill level"""
        self.level = max(1, level)
        self._update_stats_for_level()

    def _update_stats_for_level(self) -> None:
        """Update skill stats based on level"""
        level_multiplier = 1.0 + (self.level - 1) * 0.15
        base_damage = 100.0
        base_heal = 50.0

        self.damage = base_damage * level_multiplier
        self.heal_amount = base_heal * level_multiplier

    def get_hero_data_id(self) -> int:
        """Get hero data ID"""
        return self.hero_data_id

    def set_hero_data_id(self, hero_id: int) -> None:
        """Set hero data ID"""
        self.hero_data_id = hero_id

    def can_use_skill(self) -> bool:
        """Check if skill can be used"""
        return (self.is_unlocked and 
                self.is_available and 
                self.current_charges > 0 and 
                self.cooldown_remaining <= 0)

    def use_skill(self) -> bool:
        """Use skill"""
        if not self.can_use_skill():
            return False

        # Consume charge
        self.current_charges = max(0, self.current_charges - 1)

        # Start cooldown if no charges left
        if self.current_charges == 0:
            self.cooldown_remaining = self.cooldown

        return True

    def get_cooldown_remaining(self) -> float:
        """Get cooldown remaining"""
        return self.cooldown_remaining

    def get_cooldown_percentage(self) -> float:
        """Get cooldown as percentage"""
        if self.cooldown <= 0:
            return 0.0
        return max(0.0, self.cooldown_remaining / self.cooldown * 100.0)

    def get_current_charges(self) -> int:
        """Get current charges"""
        return self.current_charges

    def get_max_charges(self) -> int:
        """Get maximum charges"""
        return self.max_charges

    def add_charge(self) -> bool:
        """Add a charge"""
        if self.current_charges < self.max_charges:
            self.current_charges += 1
            return True
        return False

    def reset_cooldown(self) -> None:
        """Reset cooldown"""
        self.cooldown_remaining = 0.0
        self.current_charges = self.max_charges

    def update(self, delta_time: float) -> None:
        """Update skill (called each frame)"""
        # Update cooldown
        if self.cooldown_remaining > 0:
            self.cooldown_remaining = max(0.0, self.cooldown_remaining - delta_time)

            # Add charge when cooldown finishes
            if self.cooldown_remaining <= 0 and self.current_charges < self.max_charges:
                self.add_charge()

                # Start next cooldown if not at max charges
                if self.current_charges < self.max_charges:
                    self.cooldown_remaining = self.charge_time

    def unlock_skill(self) -> None:
        """Unlock skill"""
        self.is_unlocked = True

    def lock_skill(self) -> None:
        """Lock skill"""
        self.is_unlocked = False

    def equip_skill(self) -> None:
        """Equip skill"""
        if self.is_unlocked:
            self.is_equipped = True

    def unequip_skill(self) -> None:
        """Unequip skill"""
        self.is_equipped = False

    def is_skill_unlocked(self) -> bool:
        """Check if skill is unlocked"""
        return self.is_unlocked

    def is_skill_equipped(self) -> bool:
        """Check if skill is equipped"""
        return self.is_equipped

    def get_damage_at_level(self, level: int) -> float:
        """Get damage at specific level"""
        level_multiplier = 1.0 + (level - 1) * 0.15
        base_damage = 100.0
        return base_damage * level_multiplier

    def get_type_name(self) -> str:
        """Get skill type name"""
        type_names = {
            SkillType.ACTIVE: "Active",
            SkillType.PASSIVE: "Passive",
            SkillType.ULTIMATE: "Ultimate",
            SkillType.GADGET: "Gadget"
        }
        return type_names.get(self.skill_type, "Unknown")

    def get_target_type_name(self) -> str:
        """Get target type name"""
        target_names = {
            SkillTargetType.SELF: "Self",
            SkillTargetType.ALLY: "Ally",
            SkillTargetType.ENEMY: "Enemy",
            SkillTargetType.AREA: "Area",
            SkillTargetType.GLOBAL: "Global"
        }
        return target_names.get(self.target_type, "Unknown")

    def encode(self, stream) -> None:
        """Encode skill to stream"""
        stream.write_v_int(self.skill_id)
        stream.write_v_int(int(self.skill_type))
        stream.write_v_int(int(self.target_type))
        stream.write_v_int(self.level)
        stream.write_v_int(self.hero_data_id)
        stream.write_float(self.cooldown_remaining)
        stream.write_v_int(self.current_charges)
        stream.write_boolean(self.is_unlocked)
        stream.write_boolean(self.is_equipped)

    def decode(self, stream) -> None:
        """Decode skill from stream"""
        self.skill_id = stream.read_v_int()
        self.skill_type = SkillType(stream.read_v_int())
        self.target_type = SkillTargetType(stream.read_v_int())
        self.level = stream.read_v_int()
        self.hero_data_id = stream.read_v_int()
        self.cooldown_remaining = stream.read_float()
        self.current_charges = stream.read_v_int()
        self.is_unlocked = stream.read_boolean()
        self.is_equipped = stream.read_boolean()
        self._update_stats_for_level()

    def __str__(self) -> str:
        """String representation"""
        status = "equipped" if self.is_equipped else "unequipped"
        charges = f"({self.current_charges}/{self.max_charges})"
        return f"Skill({self.get_type_name()}, level={self.level}, {charges}, {status})"
