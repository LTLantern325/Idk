"""
Python conversion of Supercell.Laser.Logic.Home.Gatcha.DeliveryUnit.cs
Delivery unit for box opening results
"""

from typing import List
from .gatcha_drop import GatchaDrop

class DeliveryUnit:
    """Delivery unit containing multiple gatcha drops"""

    def __init__(self):
        """Initialize delivery unit"""
        self.drops: List[GatchaDrop] = []
        self.unit_type = 0
        self.value = 0
        self.multiplier = 1

    def add_drop(self, drop: GatchaDrop) -> None:
        """Add drop to delivery unit"""
        self.drops.append(drop)

    def get_drops(self) -> List[GatchaDrop]:
        """Get all drops"""
        return self.drops.copy()

    def get_drop_count(self) -> int:
        """Get number of drops"""
        return len(self.drops)

    def has_hero_unlock(self) -> bool:
        """Check if unit contains hero unlock"""
        return any(drop.type == 1 for drop in self.drops)

    def get_total_gold(self) -> int:
        """Get total gold from drops"""
        return sum(drop.count for drop in self.drops if drop.type == 7)

    def get_total_gems(self) -> int:
        """Get total gems from drops"""
        return sum(drop.count for drop in self.drops if drop.type == 8)

    def execute_drops(self, home_mode) -> None:
        """Execute all drops in the unit"""
        for drop in self.drops:
            drop.do_drop(home_mode)

    def encode(self, stream) -> None:
        """Encode delivery unit to stream"""
        stream.write_v_int(len(self.drops))
        for drop in self.drops:
            drop.encode(stream)

        stream.write_v_int(self.unit_type)
        stream.write_v_int(self.value)
        stream.write_v_int(self.multiplier)
