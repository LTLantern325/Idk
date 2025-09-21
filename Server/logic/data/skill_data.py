"""
Python conversion of Supercell.Laser.Logic.Data.SkillData.cs
Skill data class for character abilities
"""

from .data_tables import LogicData

class SkillData(LogicData):
    """Skill data class"""

    def __init__(self):
        """Initialize skill data"""
        super().__init__()
        self.name = ""
        self.behavior_type = ""
        self.can_move_at_same_time = False
        self.targeted = False
        self.can_auto_shoot = False
        self.movement_based_autoshoot = False

        # Timing properties
        self.cooldown = 0
        self.active_time = 0
        self.casting_time = 0
        self.recharge_time = 0
        self.max_charge = 0
        self.ms_between_attacks = 0

        # Range properties
        self.casting_range = 0
        self.range_visual = 0
        self.range_input_scale = 0
        self.max_casting_range = 0
        self.allow_aim_outside_map = False
        self.force_valid_tile = 0

        # Damage properties
        self.damage = 0
        self.percent_damage = 0
        self.damage_modifier = 0

        # Attack pattern
        self.spread = 0
        self.attack_pattern = 0
        self.num_bullets_in_one_attack = 1
        self.two_guns = False
        self.execute_first_attack_immediately = False
        self.multi_shot = False

        # Charge properties
        self.charge_pushback = 0
        self.charge_speed = 0
        self.charge_type = 0
        self.charged_shot_count = 0

        # Spawn properties
        self.num_spawns = 0
        self.max_spawns = 0

        # Special properties
        self.break_invisibility_on_attack = False
        self.see_invisibility_distance = 0
        self.always_cast_at_max_range = False
        self.hold_to_shoot = False
        self.show_timer_bar = False

        # References
        self.projectile = ""
        self.summoned_character = ""
        self.area_effect_object = ""
        self.area_effect_object2 = ""
        self.spawned_item = ""

        # Effects and sounds
        self.attack_effect = ""
        self.use_effect = ""
        self.end_effect = ""
        self.loop_effect = ""
        self.loop_effect2 = ""
        self.charge_move_sound = ""

        # Skill changes
        self.skill_change_type = 0
        self.secondary_skill = ""
        self.secondary_skill2 = ""
        self.secondary_skill3 = ""
        self.secondary_skill4 = ""
        self.secondary_projectile = ""

    def is_positional_targeted(self) -> bool:
        """Check if skill is positional targeted"""
        if self.behavior_type == "Charge":
            return self._is_jump_charge(self.charge_type)

        if not self.projectile:
            return False

        # Would need to check projectile data
        # For now, simplified check
        return "Jump" in self.behavior_type or "Teleport" in self.behavior_type

    def _is_jump_charge(self, charge_type: int) -> bool:
        """Check if charge type is jump charge"""
        # Simplified implementation
        return charge_type in [1, 2, 3]  # Jump charge types

    def is_targeted_skill(self) -> bool:
        """Check if skill is targeted"""
        return self.targeted

    def is_auto_shootable(self) -> bool:
        """Check if skill can auto shoot"""
        return self.can_auto_shoot

    def can_move_while_using(self) -> bool:
        """Check if can move while using skill"""
        return self.can_move_at_same_time

    def get_total_cast_time(self) -> int:
        """Get total casting time"""
        return self.casting_time + self.active_time

    def get_effective_range(self) -> int:
        """Get effective skill range"""
        return max(self.casting_range, self.max_casting_range)

    def get_damage_per_bullet(self) -> int:
        """Get damage per bullet"""
        if self.num_bullets_in_one_attack > 0:
            return self.damage // self.num_bullets_in_one_attack
        return self.damage

    def get_total_damage_potential(self) -> int:
        """Get total damage potential"""
        base_damage = self.damage
        if self.multi_shot and self.num_bullets_in_one_attack > 1:
            base_damage *= self.num_bullets_in_one_attack

        if self.charged_shot_count > 0:
            base_damage *= self.charged_shot_count

        return base_damage

    def is_charge_skill(self) -> bool:
        """Check if skill is charge type"""
        return self.behavior_type == "Charge"

    def is_projectile_skill(self) -> bool:
        """Check if skill uses projectiles"""
        return bool(self.projectile)

    def is_area_effect_skill(self) -> bool:
        """Check if skill has area effect"""
        return bool(self.area_effect_object)

    def has_secondary_skills(self) -> bool:
        """Check if skill has secondary skills"""
        return bool(self.secondary_skill or self.secondary_skill2 or 
                   self.secondary_skill3 or self.secondary_skill4)

    def get_attack_frequency(self) -> float:
        """Get attacks per second"""
        if self.ms_between_attacks > 0:
            return 1000.0 / self.ms_between_attacks
        return 0.0

    def get_dps(self) -> float:
        """Get damage per second"""
        frequency = self.get_attack_frequency()
        if frequency > 0:
            return self.damage * frequency
        return 0.0
