"""
Python conversion of Supercell.Laser.Logic.Data.AreaEffectData.cs
Area effect data class for environmental effects
"""

from .data_tables import LogicData

class AreaEffectData(LogicData):
    """Area effect data class for environmental effects"""

    def __init__(self):
        """Initialize area effect data"""
        super().__init__()
        self.name = ""
        self.parent_area_effect_for_skin = ""

        # Visual properties
        self.file_name = ""
        self.own_export_name = ""
        self.blue_export_name = ""
        self.red_export_name = ""
        self.neutral_export_name = ""
        self.layer = ""
        self.export_name_top = ""
        self.export_name_object = ""

        # Effects
        self.effect = ""
        self.looping_effect = ""
        self.allow_effect_interrupt = False

        # Physical properties
        self.scale = 0
        self.time_ms = 0
        self.radius = 0
        self.damage = 0
        self.custom_value = 0
        self.type = ""

        # Behavior
        self.delay_first_tick = False
        self.is_personal = False

        # Bullet explosion
        self.bullet_explosion_bullet = ""
        self.bullet_explosion_bullet_distance = 0
        self.bullet_explosion_item = ""

        # Environment interaction
        self.destroys_environment = False

        # Pushback
        self.pushback_strength = 0
        self.pushback_strength_self = 0
        self.pushback_deadzone = 0
        self.can_stop_grapple = False

        # Status effects
        self.slow_strength = 0
        self.freeze_ticks = 0

        # Visibility and targeting
        self.should_show_even_if_outside_screen = False
        self.same_area_effect_can_not_damage_ms = 0
        self.dont_show_to_enemy = False
        self.require_line_of_sight = False

        # Chaining
        self.chain_area_effect = ""

        # Skinning
        self.skinned_custom_value = 0

    def get_name(self) -> str:
        """Get area effect name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set area effect name"""
        self.name = name

    def get_radius(self) -> int:
        """Get effect radius"""
        return self.radius

    def set_radius(self, radius: int) -> None:
        """Set effect radius"""
        self.radius = max(0, radius)

    def get_damage(self) -> int:
        """Get damage amount"""
        return self.damage

    def set_damage(self, damage: int) -> None:
        """Set damage amount"""
        self.damage = damage

    def get_duration_ms(self) -> int:
        """Get duration in milliseconds"""
        return self.time_ms

    def set_duration_ms(self, duration: int) -> None:
        """Set duration in milliseconds"""
        self.time_ms = max(0, duration)

    def get_duration_ticks(self) -> int:
        """Get duration in ticks"""
        return self.time_ms // 50  # Convert ms to ticks

    def has_damage(self) -> bool:
        """Check if area effect deals damage"""
        return self.damage != 0

    def has_pushback(self) -> bool:
        """Check if area effect has pushback"""
        return self.pushback_strength > 0 or self.pushback_strength_self > 0

    def has_slow_effect(self) -> bool:
        """Check if area effect slows targets"""
        return self.slow_strength > 0

    def has_freeze_effect(self) -> bool:
        """Check if area effect freezes targets"""
        return self.freeze_ticks > 0

    def is_environmental_destructive(self) -> bool:
        """Check if destroys environment"""
        return self.destroys_environment

    def is_visible_to_enemy(self) -> bool:
        """Check if visible to enemy"""
        return not self.dont_show_to_enemy

    def requires_line_of_sight(self) -> bool:
        """Check if requires line of sight"""
        return self.require_line_of_sight

    def has_bullet_explosion(self) -> bool:
        """Check if has bullet explosion"""
        return self.bullet_explosion_bullet != ""

    def has_chain_effect(self) -> bool:
        """Check if has chain effect"""
        return self.chain_area_effect != ""

    def is_personal_effect(self) -> bool:
        """Check if effect is personal"""
        return self.is_personal

    def can_interrupt_effects(self) -> bool:
        """Check if can interrupt other effects"""
        return self.allow_effect_interrupt

    def get_freeze_duration_ms(self) -> int:
        """Get freeze duration in milliseconds"""
        return self.freeze_ticks * 50  # Convert ticks to ms

    def get_damage_immunity_ms(self) -> int:
        """Get damage immunity duration"""
        return self.same_area_effect_can_not_damage_ms

    def has_visual_effects(self) -> bool:
        """Check if has visual effects"""
        return (self.effect != "" or self.looping_effect != "" or 
                self.own_export_name != "")

    def get_team_export_name(self, is_blue_team: bool) -> str:
        """Get export name for team color"""
        if is_blue_team:
            return self.blue_export_name if self.blue_export_name else self.neutral_export_name
        else:
            return self.red_export_name if self.red_export_name else self.neutral_export_name

    def __str__(self) -> str:
        """String representation"""
        return (f"AreaEffectData('{self.name}', radius={self.radius}, "
                f"damage={self.damage}, duration={self.time_ms}ms)")
