"""
Python conversion of Supercell.Laser.Logic.Battle.Component.Petrol.cs
Petrol component for fuel/energy system
"""

class Petrol:
    """Petrol component for fuel/energy system"""

    def __init__(self):
        """Initialize petrol"""
        self.current_petrol = 100
        self.max_petrol = 100
        self.regeneration_rate = 1.0  # per second
        self.consumption_rate = 10.0  # per use
        self.is_regenerating = True
        self.last_use_time = 0.0
        self.regeneration_delay = 2.0  # delay after use before regen starts

    def get_current_petrol(self) -> int:
        """Get current petrol amount"""
        return self.current_petrol

    def get_max_petrol(self) -> int:
        """Get maximum petrol capacity"""
        return self.max_petrol

    def set_max_petrol(self, max_petrol: int) -> None:
        """Set maximum petrol capacity"""
        self.max_petrol = max(1, max_petrol)
        if self.current_petrol > self.max_petrol:
            self.current_petrol = self.max_petrol

    def get_petrol_percentage(self) -> float:
        """Get petrol as percentage"""
        if self.max_petrol == 0:
            return 0.0
        return (self.current_petrol / self.max_petrol) * 100.0

    def is_full(self) -> bool:
        """Check if petrol is full"""
        return self.current_petrol >= self.max_petrol

    def is_empty(self) -> bool:
        """Check if petrol is empty"""
        return self.current_petrol <= 0

    def can_use(self, amount: int = None) -> bool:
        """Check if can use petrol"""
        use_amount = amount if amount is not None else self.consumption_rate
        return self.current_petrol >= use_amount

    def use_petrol(self, amount: int = None, current_time: float = 0.0) -> bool:
        """Use petrol"""
        use_amount = amount if amount is not None else self.consumption_rate

        if self.can_use(use_amount):
            self.current_petrol = max(0, self.current_petrol - use_amount)
            self.last_use_time = current_time
            self.is_regenerating = False
            return True
        return False

    def add_petrol(self, amount: int) -> int:
        """Add petrol and return actual amount added"""
        old_petrol = self.current_petrol
        self.current_petrol = min(self.max_petrol, self.current_petrol + amount)
        return self.current_petrol - old_petrol

    def fill_petrol(self) -> None:
        """Fill petrol to maximum"""
        self.current_petrol = self.max_petrol

    def set_regeneration_rate(self, rate: float) -> None:
        """Set petrol regeneration rate"""
        self.regeneration_rate = max(0.0, rate)

    def set_consumption_rate(self, rate: float) -> None:
        """Set petrol consumption rate"""
        self.consumption_rate = max(0.0, rate)

    def set_regeneration_delay(self, delay: float) -> None:
        """Set regeneration delay after use"""
        self.regeneration_delay = max(0.0, delay)

    def update(self, delta_time: float, current_time: float = 0.0) -> None:
        """Update petrol regeneration"""
        if self.is_full():
            return

        # Check if regeneration delay has passed
        if not self.is_regenerating:
            if current_time - self.last_use_time >= self.regeneration_delay:
                self.is_regenerating = True

        # Regenerate petrol
        if self.is_regenerating and not self.is_full():
            regen_amount = self.regeneration_rate * delta_time
            self.add_petrol(int(regen_amount))

    def get_regeneration_rate(self) -> float:
        """Get regeneration rate"""
        return self.regeneration_rate

    def get_consumption_rate(self) -> float:
        """Get consumption rate"""
        return self.consumption_rate

    def is_petrol_regenerating(self) -> bool:
        """Check if petrol is currently regenerating"""
        return self.is_regenerating and not self.is_full()

    def get_time_to_full(self) -> float:
        """Get time to full petrol"""
        if self.is_full() or self.regeneration_rate <= 0:
            return 0.0

        remaining = self.max_petrol - self.current_petrol
        return remaining / self.regeneration_rate

    def get_uses_remaining(self) -> int:
        """Get number of uses remaining"""
        if self.consumption_rate <= 0:
            return float('inf')
        return int(self.current_petrol / self.consumption_rate)

    def reset(self) -> None:
        """Reset petrol to full"""
        self.current_petrol = self.max_petrol
        self.is_regenerating = True
        self.last_use_time = 0.0

    def encode(self, stream) -> None:
        """Encode petrol to stream"""
        stream.write_v_int(self.current_petrol)
        stream.write_v_int(self.max_petrol)
        stream.write_float(self.regeneration_rate)
        stream.write_float(self.consumption_rate)
        stream.write_boolean(self.is_regenerating)

    def decode(self, stream) -> None:
        """Decode petrol from stream"""
        self.current_petrol = stream.read_v_int()
        self.max_petrol = stream.read_v_int()
        self.regeneration_rate = stream.read_float()
        self.consumption_rate = stream.read_float()
        self.is_regenerating = stream.read_boolean()

    def __str__(self) -> str:
        """String representation"""
        percentage = self.get_petrol_percentage()
        status = "regenerating" if self.is_regenerating else "static"
        return f"Petrol({self.current_petrol}/{self.max_petrol}, {percentage:.1f}%, {status})"
