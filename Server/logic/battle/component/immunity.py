"""
Python conversion of Supercell.Laser.Logic.Battle.Component.Immunity.cs
Immunity component for battle status immunity
"""

from typing import Set, Optional
from enum import IntEnum

class ImmunityType(IntEnum):
    """Immunity types"""
    NONE = 0
    STUN = 1
    SLOW = 2
    POISON = 3
    FREEZE = 4
    KNOCKBACK = 5
    ALL_DEBUFFS = 6
    DAMAGE = 7

class Immunity:
    """Immunity component for battle status immunity"""

    def __init__(self):
        """Initialize immunity"""
        self.immunities = set()  # Set of ImmunityType
        self.duration = 0.0
        self.remaining_time = 0.0
        self.is_active = False
        self.source_id = 0

        # Immunity strength (0.0 = no immunity, 1.0 = full immunity)
        self.immunity_strength = 1.0

    def add_immunity(self, immunity_type: ImmunityType, duration: float = 0.0) -> None:
        """Add immunity to specific type"""
        self.immunities.add(immunity_type)
        if duration > 0:
            self.duration = max(self.duration, duration)
            self.remaining_time = max(self.remaining_time, duration)
            self.is_active = True

    def remove_immunity(self, immunity_type: ImmunityType) -> bool:
        """Remove immunity from specific type"""
        if immunity_type in self.immunities:
            self.immunities.remove(immunity_type)
            return True
        return False

    def has_immunity(self, immunity_type: ImmunityType) -> bool:
        """Check if has immunity to specific type"""
        if not self.is_active:
            return False

        return (immunity_type in self.immunities or 
                ImmunityType.ALL_DEBUFFS in self.immunities)

    def is_immune_to_stun(self) -> bool:
        """Check if immune to stun"""
        return self.has_immunity(ImmunityType.STUN)

    def is_immune_to_slow(self) -> bool:
        """Check if immune to slow"""
        return self.has_immunity(ImmunityType.SLOW)

    def is_immune_to_poison(self) -> bool:
        """Check if immune to poison"""
        return self.has_immunity(ImmunityType.POISON)

    def is_immune_to_freeze(self) -> bool:
        """Check if immune to freeze"""
        return self.has_immunity(ImmunityType.FREEZE)

    def is_immune_to_knockback(self) -> bool:
        """Check if immune to knockback"""
        return self.has_immunity(ImmunityType.KNOCKBACK)

    def is_immune_to_damage(self) -> bool:
        """Check if immune to damage"""
        return self.has_immunity(ImmunityType.DAMAGE)

    def is_immune_to_all_debuffs(self) -> bool:
        """Check if immune to all debuffs"""
        return self.has_immunity(ImmunityType.ALL_DEBUFFS)

    def get_immunity_strength(self) -> float:
        """Get immunity strength"""
        return self.immunity_strength if self.is_active else 0.0

    def set_immunity_strength(self, strength: float) -> None:
        """Set immunity strength"""
        self.immunity_strength = max(0.0, min(1.0, strength))

    def get_remaining_time(self) -> float:
        """Get remaining immunity time"""
        return self.remaining_time

    def set_duration(self, duration: float) -> None:
        """Set immunity duration"""
        self.duration = duration
        self.remaining_time = duration
        self.is_active = duration > 0

    def refresh_duration(self) -> None:
        """Refresh immunity duration to maximum"""
        self.remaining_time = self.duration
        self.is_active = True

    def update(self, delta_time: float) -> None:
        """Update immunity (called each frame)"""
        if not self.is_active:
            return

        self.remaining_time -= delta_time
        if self.remaining_time <= 0:
            self.is_active = False
            self.remaining_time = 0

    def clear_all_immunities(self) -> None:
        """Clear all immunities"""
        self.immunities.clear()
        self.is_active = False
        self.remaining_time = 0

    def get_immunity_count(self) -> int:
        """Get number of active immunities"""
        return len(self.immunities)

    def get_immunity_types(self) -> Set[ImmunityType]:
        """Get copy of immunity types"""
        return self.immunities.copy()

    def merge_with(self, other: 'Immunity') -> None:
        """Merge with another immunity"""
        self.immunities.update(other.immunities)
        self.remaining_time = max(self.remaining_time, other.remaining_time)
        self.duration = max(self.duration, other.duration)
        self.immunity_strength = max(self.immunity_strength, other.immunity_strength)
        self.is_active = self.is_active or other.is_active

    def can_apply_effect(self, effect_type: ImmunityType) -> bool:
        """Check if effect can be applied (not immune)"""
        return not self.has_immunity(effect_type)

    def get_immunity_names(self) -> list:
        """Get list of immunity names"""
        type_names = {
            ImmunityType.STUN: "Stun",
            ImmunityType.SLOW: "Slow",
            ImmunityType.POISON: "Poison",
            ImmunityType.FREEZE: "Freeze",
            ImmunityType.KNOCKBACK: "Knockback",
            ImmunityType.ALL_DEBUFFS: "All Debuffs",
            ImmunityType.DAMAGE: "Damage"
        }
        return [type_names.get(immunity, "Unknown") for immunity in self.immunities]

    def encode(self, stream) -> None:
        """Encode immunity to stream"""
        stream.write_v_int(len(self.immunities))
        for immunity_type in self.immunities:
            stream.write_v_int(int(immunity_type))

        stream.write_float(self.remaining_time)
        stream.write_float(self.immunity_strength)
        stream.write_v_int(self.source_id)
        stream.write_boolean(self.is_active)

    def decode(self, stream) -> None:
        """Decode immunity from stream"""
        immunity_count = stream.read_v_int()
        self.immunities.clear()
        for i in range(immunity_count):
            immunity_type = ImmunityType(stream.read_v_int())
            self.immunities.add(immunity_type)

        self.remaining_time = stream.read_float()
        self.immunity_strength = stream.read_float()
        self.source_id = stream.read_v_int()
        self.is_active = stream.read_boolean()

    def __str__(self) -> str:
        """String representation"""
        if not self.is_active or not self.immunities:
            return "Immunity(none)"

        names = self.get_immunity_names()
        status = f"active" if self.is_active else "inactive"
        return f"Immunity({', '.join(names)}, {self.remaining_time:.1f}s, {status})"
