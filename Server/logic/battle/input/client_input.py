"""
Python conversion of Supercell.Laser.Logic.Battle.Input.ClientInput.cs
Client input handling for battle controls
"""

from typing import Tuple, Optional
from enum import IntEnum

class InputType(IntEnum):
    """Input types"""
    NONE = 0
    MOVE = 1
    ATTACK = 2
    SPECIAL = 3
    AIM = 4
    GADGET = 5

class ClientInput:
    """Client input handling for battle controls"""

    def __init__(self):
        """Initialize client input"""
        self.input_type = InputType.NONE
        self.x = 0.0
        self.y = 0.0
        self.angle = 0.0
        self.is_pressed = False
        self.timestamp = 0

        # Input state
        self.is_moving = False
        self.is_attacking = False
        self.is_aiming = False

        # Touch/mouse state
        self.touch_start_x = 0.0
        self.touch_start_y = 0.0
        self.touch_current_x = 0.0
        self.touch_current_y = 0.0

        # Joystick simulation
        self.joystick_x = 0.0
        self.joystick_y = 0.0
        self.joystick_radius = 100.0
        self.joystick_dead_zone = 10.0

    def get_input_type(self) -> InputType:
        """Get input type"""
        return self.input_type

    def set_input_type(self, input_type: InputType) -> None:
        """Set input type"""
        self.input_type = input_type

    def get_position(self) -> Tuple[float, float]:
        """Get input position"""
        return (self.x, self.y)

    def set_position(self, x: float, y: float) -> None:
        """Set input position"""
        self.x = x
        self.y = y

    def get_angle(self) -> float:
        """Get input angle"""
        return self.angle

    def set_angle(self, angle: float) -> None:
        """Set input angle"""
        self.angle = angle

    def is_input_pressed(self) -> bool:
        """Check if input is pressed"""
        return self.is_pressed

    def set_pressed(self, pressed: bool) -> None:
        """Set pressed state"""
        self.is_pressed = pressed

    def get_timestamp(self) -> int:
        """Get input timestamp"""
        return self.timestamp

    def set_timestamp(self, timestamp: int) -> None:
        """Set input timestamp"""
        self.timestamp = timestamp

    def start_touch(self, x: float, y: float) -> None:
        """Start touch input"""
        self.touch_start_x = x
        self.touch_start_y = y
        self.touch_current_x = x
        self.touch_current_y = y
        self.is_pressed = True

    def update_touch(self, x: float, y: float) -> None:
        """Update touch position"""
        self.touch_current_x = x
        self.touch_current_y = y
        self._update_joystick()

    def end_touch(self) -> None:
        """End touch input"""
        self.is_pressed = False
        self.joystick_x = 0.0
        self.joystick_y = 0.0
        self.is_moving = False
        self.is_attacking = False
        self.is_aiming = False

    def _update_joystick(self) -> None:
        """Update joystick values based on touch"""
        dx = self.touch_current_x - self.touch_start_x
        dy = self.touch_current_y - self.touch_start_y

        distance = (dx * dx + dy * dy) ** 0.5

        # Check dead zone
        if distance < self.joystick_dead_zone:
            self.joystick_x = 0.0
            self.joystick_y = 0.0
            return

        # Clamp to joystick radius
        if distance > self.joystick_radius:
            scale = self.joystick_radius / distance
            dx *= scale
            dy *= scale
            distance = self.joystick_radius

        # Normalize to -1 to 1 range
        self.joystick_x = dx / self.joystick_radius
        self.joystick_y = dy / self.joystick_radius

        # Update angle
        import math
        self.angle = math.atan2(dy, dx)

    def get_joystick_values(self) -> Tuple[float, float]:
        """Get joystick X and Y values (-1 to 1)"""
        return (self.joystick_x, self.joystick_y)

    def get_joystick_magnitude(self) -> float:
        """Get joystick magnitude (0 to 1)"""
        return min(1.0, (self.joystick_x * self.joystick_x + self.joystick_y * self.joystick_y) ** 0.5)

    def is_joystick_active(self) -> bool:
        """Check if joystick is active"""
        return self.get_joystick_magnitude() > 0.1

    def handle_move_input(self, x: float, y: float) -> None:
        """Handle movement input"""
        self.input_type = InputType.MOVE
        self.set_position(x, y)
        self.is_moving = True

    def handle_attack_input(self, target_x: float, target_y: float) -> None:
        """Handle attack input"""
        self.input_type = InputType.ATTACK
        self.set_position(target_x, target_y)
        self.is_attacking = True

        # Calculate angle to target
        import math
        dx = target_x - self.x
        dy = target_y - self.y
        self.angle = math.atan2(dy, dx)

    def handle_special_input(self, x: float, y: float) -> None:
        """Handle special ability input"""
        self.input_type = InputType.SPECIAL
        self.set_position(x, y)

    def handle_gadget_input(self) -> None:
        """Handle gadget input"""
        self.input_type = InputType.GADGET

    def clear_input(self) -> None:
        """Clear all input"""
        self.input_type = InputType.NONE
        self.is_pressed = False
        self.is_moving = False
        self.is_attacking = False
        self.is_aiming = False
        self.joystick_x = 0.0
        self.joystick_y = 0.0

    def encode(self, stream) -> None:
        """Encode input to stream"""
        stream.write_v_int(int(self.input_type))
        stream.write_float(self.x)
        stream.write_float(self.y)
        stream.write_float(self.angle)
        stream.write_boolean(self.is_pressed)
        stream.write_v_int(self.timestamp)

    def decode(self, stream) -> None:
        """Decode input from stream"""
        self.input_type = InputType(stream.read_v_int())
        self.x = stream.read_float()
        self.y = stream.read_float()
        self.angle = stream.read_float()
        self.is_pressed = stream.read_boolean()
        self.timestamp = stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        type_name = self.input_type.name
        pos = f"({self.x:.1f}, {self.y:.1f})"
        state = "pressed" if self.is_pressed else "released"
        return f"ClientInput({type_name}, {pos}, {state})"
