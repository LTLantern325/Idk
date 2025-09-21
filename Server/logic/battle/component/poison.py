"""
Python conversion of Supercell.Laser.Logic.Battle.Component.Poison.cs
Poison component for damage over time effects
"""

from typing import Optional

class Poison:
    """Poison component for damage over time effects"""

    def __init__(self, damage_per_second: float = 50.0, duration: float = 5.0):
        """Initialize poison"""
        self.damage_per_second = damage_per_second
        self.duration = duration
        self.remaining_time = duration
        self.total_damage_dealt = 0.0
        self.source_id = 0
        self.is_active = True
        self.tick_interval = 1.0  # Apply damage every second
        self.time_since_last_tick = 0.0

        # Visual properties
        self.name = "Poison"
        self.description = "Deals damage over time"
        self.icon_id = 0

    def get_damage_per_second(self) -> float:
        """Get damage per second"""
        return self.damage_per_second

    def set_damage_per_second(self, dps: float) -> None:
        """Set damage per second"""
        self.damage_per_second = max(0.0, dps)

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

    def get_source_id(self) -> int:
        """Get source ID (who applied the poison)"""
        return self.source_id

    def set_source_id(self, source_id: int) -> None:
        """Set source ID"""
        self.source_id = source_id

    def get_total_damage_dealt(self) -> float:
        """Get total damage dealt so far"""
        return self.total_damage_dealt

    def get_estimated_total_damage(self) -> float:
        """Get estimated total damage over full duration"""
        return self.damage_per_second * self.duration

    def is_poison_active(self) -> bool:
        """Check if poison is active"""
        return self.is_active and self.remaining_time > 0

    def refresh_poison(self, new_duration: float = None) -> None:
        """Refresh poison duration"""
        if new_duration is not None:
            self.duration = new_duration
        self.remaining_time = self.duration
        self.is_active = True

    def stack_poison(self, additional_dps: float, additional_duration: float = 0.0) -> None:
        """Stack poison effect"""
        self.damage_per_second += additional_dps
        if additional_duration > 0:
            self.remaining_time = max(self.remaining_time, additional_duration)

    def update(self, delta_time: float) -> float:
        """Update poison and return damage to apply this frame"""
        if not self.is_active:
            return 0.0

        # Update timers
        self.remaining_time -= delta_time
        self.time_since_last_tick += delta_time

        damage_this_frame = 0.0

        # Apply damage at intervals
        if self.time_since_last_tick >= self.tick_interval:
            damage_this_frame = self.damage_per_second * self.tick_interval
            self.total_damage_dealt += damage_this_frame
            self.time_since_last_tick = 0.0

        # Deactivate if time runs out
        if self.remaining_time <= 0:
            self.is_active = False
            # Apply any remaining fractional damage
            if self.time_since_last_tick > 0:
                remaining_damage = self.damage_per_second * self.time_since_last_tick
                damage_this_frame += remaining_damage
                self.total_damage_dealt += remaining_damage

        return damage_this_frame

    def get_damage_this_tick(self) -> float:
        """Get damage for current tick"""
        if not self.is_active:
            return 0.0
        return self.damage_per_second * self.tick_interval

    def get_ticks_remaining(self) -> int:
        """Get number of damage ticks remaining"""
        if not self.is_active or self.tick_interval <= 0:
            return 0
        return int(self.remaining_time / self.tick_interval)

    def get_progress_percentage(self) -> float:
        """Get poison progress percentage"""
        if self.duration <= 0:
            return 100.0
        return max(0.0, (self.duration - self.remaining_time) / self.duration * 100.0)

    def can_kill(self, target_health: float) -> bool:
        """Check if poison can kill target with remaining damage"""
        remaining_damage = self.damage_per_second * self.remaining_time
        return remaining_damage >= target_health

    def get_time_to_kill(self, target_health: float) -> float:
        """Get time needed to kill target with current health"""
        if self.damage_per_second <= 0:
            return float('inf')
        return target_health / self.damage_per_second

    def merge_with(self, other: 'Poison') -> None:
        """Merge with another poison effect"""
        # Combine damage per second
        self.damage_per_second += other.damage_per_second

        # Use longer remaining time
        self.remaining_time = max(self.remaining_time, other.remaining_time)

        # Keep active if either is active
        self.is_active = self.is_active or other.is_active

    def encode(self, stream) -> None:
        """Encode poison to stream"""
        stream.write_float(self.damage_per_second)
        stream.write_float(self.remaining_time)
        stream.write_float(self.total_damage_dealt)
        stream.write_v_int(self.source_id)
        stream.write_boolean(self.is_active)

    def decode(self, stream) -> None:
        """Decode poison from stream"""
        self.damage_per_second = stream.read_float()
        self.remaining_time = stream.read_float()
        self.total_damage_dealt = stream.read_float()
        self.source_id = stream.read_v_int()
        self.is_active = stream.read_boolean()

    def __str__(self) -> str:
        """String representation"""
        status = "active" if self.is_active else "expired"
        return f"Poison({self.damage_per_second} DPS, {self.remaining_time:.1f}s, {status})"
