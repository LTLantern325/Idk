"""
Python conversion of Supercell.Laser.Logic.Battle.Component.Buff.cs
Buff component for temporary battle effects
"""

from typing import Dict, List, Optional
from enum import IntEnum

class BuffType(IntEnum):
    """Buff types"""
    DAMAGE_BOOST = 1
    SPEED_BOOST = 2
    HEALTH_REGEN = 3
    SHIELD = 4
    INVISIBILITY = 5
    IMMUNITY = 6
    SLOW = 7
    STUN = 8
    POISON = 9
    FREEZE = 10

class Buff:
    """Buff component for temporary battle effects"""

    def __init__(self, buff_type: BuffType, duration: float):
        """Initialize buff"""
        self.buff_type = buff_type
        self.duration = duration
        self.remaining_time = duration
        self.strength = 1.0
        self.source_id = 0
        self.is_stackable = False
        self.max_stacks = 1
        self.current_stacks = 1
        self.is_active = True

        # Effect values
        self.damage_multiplier = 1.0
        self.speed_multiplier = 1.0
        self.health_per_second = 0.0
        self.damage_reduction = 0.0

        # Visual properties
        self.name = ""
        self.description = ""
        self.icon_id = 0

        self._initialize_buff_effects()

    def _initialize_buff_effects(self) -> None:
        """Initialize buff effects based on type"""
        if self.buff_type == BuffType.DAMAGE_BOOST:
            self.damage_multiplier = 1.25
            self.name = "Damage Boost"
        elif self.buff_type == BuffType.SPEED_BOOST:
            self.speed_multiplier = 1.3
            self.name = "Speed Boost"
        elif self.buff_type == BuffType.HEALTH_REGEN:
            self.health_per_second = 50.0
            self.name = "Health Regeneration"
        elif self.buff_type == BuffType.SHIELD:
            self.damage_reduction = 0.5
            self.name = "Shield"
        elif self.buff_type == BuffType.SLOW:
            self.speed_multiplier = 0.7
            self.name = "Slow"
        elif self.buff_type == BuffType.STUN:
            self.speed_multiplier = 0.0
            self.damage_multiplier = 0.0
            self.name = "Stun"

    def get_buff_type(self) -> BuffType:
        """Get buff type"""
        return self.buff_type

    def get_duration(self) -> float:
        """Get total duration"""
        return self.duration

    def get_remaining_time(self) -> float:
        """Get remaining time"""
        return self.remaining_time

    def set_remaining_time(self, time: float) -> None:
        """Set remaining time"""
        self.remaining_time = max(0.0, time)
        if self.remaining_time <= 0:
            self.is_active = False

    def get_strength(self) -> float:
        """Get buff strength"""
        return self.strength * self.current_stacks

    def set_strength(self, strength: float) -> None:
        """Set buff strength"""
        self.strength = max(0.0, strength)

    def get_source_id(self) -> int:
        """Get source ID (who applied the buff)"""
        return self.source_id

    def set_source_id(self, source_id: int) -> None:
        """Set source ID"""
        self.source_id = source_id

    def add_stack(self) -> bool:
        """Add stack to buff"""
        if self.is_stackable and self.current_stacks < self.max_stacks:
            self.current_stacks += 1
            return True
        return False

    def remove_stack(self) -> bool:
        """Remove stack from buff"""
        if self.current_stacks > 1:
            self.current_stacks -= 1
            return True
        else:
            self.is_active = False
            return False

    def refresh_duration(self) -> None:
        """Refresh buff duration to maximum"""
        self.remaining_time = self.duration
        self.is_active = True

    def update(self, delta_time: float) -> None:
        """Update buff (called each frame)"""
        if not self.is_active:
            return

        self.remaining_time -= delta_time
        if self.remaining_time <= 0:
            self.is_active = False

    def is_buff_active(self) -> bool:
        """Check if buff is active"""
        return self.is_active and self.remaining_time > 0

    def is_positive_buff(self) -> bool:
        """Check if this is a positive buff"""
        positive_buffs = {
            BuffType.DAMAGE_BOOST,
            BuffType.SPEED_BOOST,
            BuffType.HEALTH_REGEN,
            BuffType.SHIELD,
            BuffType.INVISIBILITY,
            BuffType.IMMUNITY
        }
        return self.buff_type in positive_buffs

    def is_negative_buff(self) -> bool:
        """Check if this is a negative buff (debuff)"""
        return not self.is_positive_buff()

    def can_stack_with(self, other_buff: 'Buff') -> bool:
        """Check if this buff can stack with another"""
        return (self.buff_type == other_buff.buff_type and 
                self.is_stackable and 
                self.current_stacks < self.max_stacks)

    def get_effective_damage_multiplier(self) -> float:
        """Get effective damage multiplier"""
        if not self.is_active:
            return 1.0
        return self.damage_multiplier ** self.get_strength()

    def get_effective_speed_multiplier(self) -> float:
        """Get effective speed multiplier"""
        if not self.is_active:
            return 1.0
        return self.speed_multiplier ** self.get_strength()

    def get_effective_health_per_second(self) -> float:
        """Get effective health regeneration per second"""
        if not self.is_active:
            return 0.0
        return self.health_per_second * self.get_strength()

    def get_effective_damage_reduction(self) -> float:
        """Get effective damage reduction"""
        if not self.is_active:
            return 0.0
        return min(0.9, self.damage_reduction * self.get_strength())  # Cap at 90%

    def get_progress_percentage(self) -> float:
        """Get buff progress percentage"""
        if self.duration <= 0:
            return 100.0
        return max(0.0, (self.duration - self.remaining_time) / self.duration * 100.0)

    def encode(self, stream) -> None:
        """Encode buff to stream"""
        stream.write_v_int(int(self.buff_type))
        stream.write_float(self.remaining_time)
        stream.write_float(self.strength)
        stream.write_v_int(self.source_id)
        stream.write_v_int(self.current_stacks)
        stream.write_boolean(self.is_active)

    def decode(self, stream) -> None:
        """Decode buff from stream"""
        self.buff_type = BuffType(stream.read_v_int())
        self.remaining_time = stream.read_float()
        self.strength = stream.read_float()
        self.source_id = stream.read_v_int()
        self.current_stacks = stream.read_v_int()
        self.is_active = stream.read_boolean()

    def __str__(self) -> str:
        """String representation"""
        status = "active" if self.is_active else "expired"
        stacks = f" x{self.current_stacks}" if self.current_stacks > 1 else ""
        return f"Buff({self.name}{stacks}, {self.remaining_time:.1f}s, {status})"
