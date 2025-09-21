"""
Python conversion of Supercell.Laser.Logic.Time.GameTime.cs
Game time management
"""

class GameTime:
    """Game time tracker for ticks"""

    def __init__(self):
        """Initialize game time"""
        self.tick = 0

    def reset(self) -> None:
        """Reset tick to 0"""
        self.tick = 0

    def increase_tick(self) -> None:
        """Increment tick by 1"""
        self.tick += 1

    def get_tick(self) -> int:
        """Get current tick"""
        return self.tick

    def set_tick(self, tick: int) -> None:
        """Set current tick"""
        self.tick = tick

    def add_ticks(self, ticks: int) -> None:
        """Add multiple ticks"""
        self.tick += ticks

    def get_milliseconds(self) -> int:
        """Get time in milliseconds (assuming 50ms per tick)"""
        return self.tick * 50

    def get_seconds(self) -> float:
        """Get time in seconds"""
        return self.tick * 0.05
