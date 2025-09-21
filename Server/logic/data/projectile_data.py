"""
Python conversion of Supercell.Laser.Logic.Data.ProjectileData.cs
Projectile data class for bullets and missiles (simplified version)
"""

from .data_tables import LogicData

class ProjectileData(LogicData):
    """Projectile data class for bullets and missiles"""

    def __init__(self):
        """Initialize projectile data"""
        super().__init__()
        # Basic properties
        self.name = ""
        self.parent_projectile_for_skin = ""
        self.speed = 0

        # Visual properties
        self.file_name = ""
        self.blue_scw = ""
        self.red_scw = ""
        self.blue_export_name = ""
        self.red_export_name = ""
        self.shadow_export_name = ""
        self.blue_ground_glow_export_name = ""
        self.red_ground_glow_export_name = ""

        # Pre-explosion
        self.pre_explosion_blue_export_name = ""
        self.pre_explosion_red_export_name = ""
        self.pre_explosion_time_ms = 0

        # Effects
        self.hit_effect_env = ""
        self.hit_effect_char = ""
        self.max_range_reached_effect = ""
        self.cancel_effect = ""
        self.trail_effect = ""
        self.special_trail_effect = ""

        # Physical properties
        self.radius = 0
        self.indirect = False
        self.constant_fly_time = False
        self.trigger_with_delay_ms = 0
        self.bounce_percent = 0
        self.gravity = 0
        self.early_ticks = 0
        self.hide_time = 0
        self.scale = 0
        self.random_start_frame = 0

        # Spawn effects
        self.spawn_area_effect_object = ""
        self.spawn_area_effect_object2 = ""
        self.area_effect2_damage_percent = 0
        self.spawn_character = ""
        self.spawn_item = ""
        self.spawn_area_effect_trail = ""

        # Behavior flags
        self.shot_by_hero = False
        self.is_beam = False
        self.is_bouncing = False
        self.distance_add_from_bounce = 0
        self.rendering = ""

        # Piercing
        self.pierces_characters = False
        self.pierces_environment = False
        self.pierces_environment_like_butter = False

        # Pushback
        self.pushback_strength = 0
        self.pushback_type = 0

        # Chaining
        self.chains_to_enemies = 0
        self.chain_bullets = 0
        self.chain_spread = 0
        self.chain_travel_distance = 0
        self.chain_bullet = ""
        self.execute_chain_special_case = 0

        # Damage scaling
        self.damage_percent_start = 0
        self.damage_percent_end = 0
        self.damages_constantly_tick_delay = 0

        # Status effects
        self.freeze_strength = 0
        self.freeze_duration_ms = 0
        self.partial_stun_promille = 0
        self.stun_length_ms = 0
        self.life_steal_percent = 0
        self.poison_damage_percent = 0
        self.suppress_healing = 0
        self.suppress_healing_ticks = 0
        self.consumable_shield = 0
        self.consumable_shield_ticks = 0
        self.heal_own_percent = 0

        # Scale properties
        self.scale_start = 0
        self.scale_end = 0

        # Special properties
        self.attracts_pet = False
        self.passes_environment = False
        self.damage_only_with_one_proj = False
        self.special_visual_state = False
        self.hide_faster = False
        self.grapples_enemy = False
        self.kick_back = 0

        # Color modulation
        self.use_color_mod = False
        self.red_add = 0
        self.green_add = 0
        self.blue_add = 0
        self.red_mul = 0
        self.green_mul = 0
        self.blue_mul = 0

        # Advanced behavior
        self.ground_basis = False
        self.min_distance_for_spread = 0
        self.is_friendly_homing_missile = False
        self.is_boomerang = False
        self.can_hit_again_after_bounce = False
        self.is_homing_missile = False
        self.ulti_charge_change_percent = 0
        self.poison_type = 0
        self.applied_effect_visual_type = 0
        self.travel_type = 0
        self.travel_type_variable = 0
        self.ignore_level_boarder = False
        self.steer_strength = 0
        self.steer_ignore_ticks = 0
        self.home_distance = 0
        self.steer_life_time = 0
        self.unique_property = 0

    # Helper methods from original C#
    def get_scale_start(self) -> int:
        """Get scale start value"""
        return self.scale_start if self.scale_start != 0 else 100

    def get_scale_end(self) -> int:
        """Get scale end value"""
        return self.scale_end if self.scale_end != 0 else 100

    def get_damage_percent_start(self) -> int:
        """Get damage percent start"""
        return self.damage_percent_start if self.damage_percent_start != 0 else 100

    def get_damage_percent_end(self) -> int:
        """Get damage percent end"""
        return self.damage_percent_end if self.damage_percent_end != 0 else 100

    def get_freeze_duration(self) -> int:
        """Get freeze duration in ticks"""
        return self.freeze_duration_ms // 50

    def get_stun_length_ticks(self) -> int:
        """Get stun length in ticks"""
        return self.stun_length_ms // 50

    def execute_chain_on_no_hit(self) -> bool:
        """Check if chain executes on no hit"""
        return self.execute_chain_special_case == 1

    def execute_chain_always(self) -> bool:
        """Check if chain always executes"""
        return self.execute_chain_special_case == 2

    def execute_chain_on_object_hit(self) -> bool:
        """Check if chain executes on object hit"""
        return self.execute_chain_special_case == 0 and self.chain_bullet != ""

    def execute_chain_on_any_hit(self) -> bool:
        """Check if chain executes on any hit"""
        return self.execute_chain_special_case == 3

    def damages_constantly(self) -> bool:
        """Check if damages constantly"""
        return self.damages_constantly_tick_delay != 0

    # Additional utility methods
    def is_explosive(self) -> bool:
        """Check if projectile is explosive"""
        return self.spawn_area_effect_object != ""

    def has_trail_effect(self) -> bool:
        """Check if has trail effect"""
        return self.trail_effect != "" or self.special_trail_effect != ""

    def can_pierce(self) -> bool:
        """Check if projectile can pierce"""
        return self.pierces_characters or self.pierces_environment

    def has_chain_ability(self) -> bool:
        """Check if projectile can chain"""
        return self.chains_to_enemies > 0 or self.chain_bullet != ""

    def has_status_effects(self) -> bool:
        """Check if projectile applies status effects"""
        return (self.freeze_strength > 0 or self.stun_length_ms > 0 or
                self.poison_damage_percent > 0 or self.suppress_healing > 0)

    def is_homing(self) -> bool:
        """Check if projectile homes to targets"""
        return self.is_homing_missile or self.is_friendly_homing_missile

    def __str__(self) -> str:
        """String representation"""
        return f"ProjectileData('{self.name}', speed={self.speed}, radius={self.radius})"
