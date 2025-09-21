"""
Python conversion of Supercell.Laser.Logic.Battle.Objects.AreaEffect.cs
Area effect class for battle area-based effects
"""

from typing import List, Set, Optional, Tuple
from enum import IntEnum
from .game_object import GameObject

class AreaEffectType(IntEnum):
    """Area effect types"""
    DAMAGE_ZONE = 1
    HEALING_ZONE = 2
    SPEED_BOOST_ZONE = 3
    SLOW_ZONE = 4
    SHIELD_ZONE = 5
    POISON_ZONE = 6
    FREEZE_ZONE = 7

class AreaEffect(GameObject):
    """Area effect class for battle area-based effects"""

    def __init__(self):
        """Initialize area effect"""
        super().__init__()
        self.effect_type = AreaEffectType.DAMAGE_ZONE
        self.radius = 100.0
        self.strength = 1.0
        self.duration = 5.0
        self.remaining_time = 5.0
        self.tick_interval = 0.5  # Apply effect every 0.5 seconds
        self.time_since_last_tick = 0.0

        # Affected targets
        self.affected_targets = set()  # Set of target IDs
        self.max_targets = -1  # -1 = unlimited

        # Visual properties
        self.visual_scale = 1.0
        self.alpha = 1.0
        self.particle_effect_id = 0

        # Ownership
        self.owner_id = 0
        self.team_id = 0
        self.affects_allies = False
        self.affects_enemies = True
        self.affects_neutrals = False

    def get_effect_type(self) -> AreaEffectType:
        """Get effect type"""
        return self.effect_type

    def set_effect_type(self, effect_type: AreaEffectType) -> None:
        """Set effect type"""
        self.effect_type = effect_type

    def get_radius(self) -> float:
        """Get effect radius"""
        return self.radius

    def set_radius(self, radius: float) -> None:
        """Set effect radius"""
        self.radius = max(0.0, radius)

    def get_strength(self) -> float:
        """Get effect strength"""
        return self.strength

    def set_strength(self, strength: float) -> None:
        """Set effect strength"""
        self.strength = max(0.0, strength)

    def get_duration(self) -> float:
        """Get total duration"""
        return self.duration

    def get_remaining_time(self) -> float:
        """Get remaining time"""
        return self.remaining_time

    def set_remaining_time(self, time: float) -> None:
        """Set remaining time"""
        self.remaining_time = max(0.0, time)

    def is_effect_active(self) -> bool:
        """Check if effect is active"""
        return self.remaining_time > 0 and self.is_alive

    def get_owner_id(self) -> int:
        """Get owner ID"""
        return self.owner_id

    def set_owner_id(self, owner_id: int) -> None:
        """Set owner ID"""
        self.owner_id = owner_id

    def get_team_id(self) -> int:
        """Get team ID"""
        return self.team_id

    def set_team_id(self, team_id: int) -> None:
        """Set team ID"""
        self.team_id = team_id

    def can_affect_target(self, target_id: int, target_team_id: int) -> bool:
        """Check if can affect target"""
        if not self.is_effect_active():
            return False

        if self.max_targets > 0 and len(self.affected_targets) >= self.max_targets:
            return False

        # Check team affiliation
        if target_team_id == self.team_id:
            return self.affects_allies
        elif target_team_id == 0:
            return self.affects_neutrals
        else:
            return self.affects_enemies

    def add_affected_target(self, target_id: int) -> bool:
        """Add target to affected list"""
        if self.max_targets > 0 and len(self.affected_targets) >= self.max_targets:
            return False

        self.affected_targets.add(target_id)
        return True

    def remove_affected_target(self, target_id: int) -> bool:
        """Remove target from affected list"""
        if target_id in self.affected_targets:
            self.affected_targets.remove(target_id)
            return True
        return False

    def is_target_affected(self, target_id: int) -> bool:
        """Check if target is affected"""
        return target_id in self.affected_targets

    def get_affected_target_count(self) -> int:
        """Get number of affected targets"""
        return len(self.affected_targets)

    def is_position_in_range(self, target_x: float, target_y: float) -> bool:
        """Check if position is within effect range"""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = (dx * dx + dy * dy) ** 0.5
        return distance <= self.radius

    def get_effect_strength_at_position(self, target_x: float, target_y: float) -> float:
        """Get effect strength at position (can vary by distance)"""
        if not self.is_position_in_range(target_x, target_y):
            return 0.0

        dx = target_x - self.x
        dy = target_y - self.y
        distance = (dx * dx + dy * dy) ** 0.5

        # Linear falloff from center to edge
        falloff = 1.0 - (distance / self.radius)
        return self.strength * max(0.0, falloff)

    def update(self, delta_time: float) -> None:
        """Update area effect"""
        super().update(delta_time)

        if not self.is_effect_active():
            return

        # Update remaining time
        self.remaining_time -= delta_time
        if self.remaining_time <= 0:
            self.destroy()
            return

        # Update tick timer
        self.time_since_last_tick += delta_time

        # Update visual properties
        self.visual_scale = 0.5 + 0.5 * (self.remaining_time / self.duration)
        self.alpha = min(1.0, self.remaining_time / min(1.0, self.duration))

    def should_apply_effect(self) -> bool:
        """Check if should apply effect this frame"""
        return self.time_since_last_tick >= self.tick_interval

    def apply_effect_tick(self) -> None:
        """Apply effect tick (reset timer)"""
        self.time_since_last_tick = 0.0

    def get_damage_per_tick(self) -> float:
        """Get damage per tick for damage zones"""
        if self.effect_type == AreaEffectType.DAMAGE_ZONE:
            return self.strength * self.tick_interval
        return 0.0

    def get_healing_per_tick(self) -> float:
        """Get healing per tick for healing zones"""
        if self.effect_type == AreaEffectType.HEALING_ZONE:
            return self.strength * self.tick_interval
        return 0.0

    def get_speed_multiplier(self) -> float:
        """Get speed multiplier for speed zones"""
        if self.effect_type == AreaEffectType.SPEED_BOOST_ZONE:
            return 1.0 + self.strength * 0.5
        elif self.effect_type == AreaEffectType.SLOW_ZONE:
            return 1.0 - self.strength * 0.3
        return 1.0

    def provides_shield(self) -> bool:
        """Check if provides shield"""
        return self.effect_type == AreaEffectType.SHIELD_ZONE

    def get_shield_amount(self) -> float:
        """Get shield amount"""
        if self.provides_shield():
            return self.strength * 50.0  # Base shield amount
        return 0.0

    def get_type_name(self) -> str:
        """Get effect type name"""
        type_names = {
            AreaEffectType.DAMAGE_ZONE: "Damage Zone",
            AreaEffectType.HEALING_ZONE: "Healing Zone",
            AreaEffectType.SPEED_BOOST_ZONE: "Speed Boost Zone",
            AreaEffectType.SLOW_ZONE: "Slow Zone",
            AreaEffectType.SHIELD_ZONE: "Shield Zone",
            AreaEffectType.POISON_ZONE: "Poison Zone",
            AreaEffectType.FREEZE_ZONE: "Freeze Zone"
        }
        return type_names.get(self.effect_type, "Unknown Effect")

    def encode(self, stream) -> None:
        """Encode area effect to stream"""
        super().encode(stream)
        stream.write_v_int(int(self.effect_type))
        stream.write_float(self.radius)
        stream.write_float(self.strength)
        stream.write_float(self.remaining_time)
        stream.write_v_int(self.owner_id)
        stream.write_v_int(self.team_id)
        stream.write_boolean(self.affects_allies)
        stream.write_boolean(self.affects_enemies)

        # Write affected targets
        stream.write_v_int(len(self.affected_targets))
        for target_id in self.affected_targets:
            stream.write_v_int(target_id)

    def decode(self, stream) -> None:
        """Decode area effect from stream"""
        super().decode(stream)
        self.effect_type = AreaEffectType(stream.read_v_int())
        self.radius = stream.read_float()
        self.strength = stream.read_float()
        self.remaining_time = stream.read_float()
        self.owner_id = stream.read_v_int()
        self.team_id = stream.read_v_int()
        self.affects_allies = stream.read_boolean()
        self.affects_enemies = stream.read_boolean()

        # Read affected targets
        target_count = stream.read_v_int()
        self.affected_targets.clear()
        for i in range(target_count):
            target_id = stream.read_v_int()
            self.affected_targets.add(target_id)

    def __str__(self) -> str:
        """String representation"""
        return f"AreaEffect({self.get_type_name()}, radius={self.radius:.1f}, {self.remaining_time:.1f}s)"
