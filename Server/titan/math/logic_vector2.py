"""
Python conversion of Supercell.Laser.Titan.Math.LogicVector2.cs
2D vector for game mathematics
"""

from typing import Tuple
from .logic_math import LogicMath

class LogicVector2:
    """2D vector for game mathematics"""

    def __init__(self, x: int = 0, y: int = 0):
        """Initialize vector"""
        self.x = x
        self.y = y

    def destruct(self) -> None:
        """Reset vector"""
        self.x = 0
        self.y = 0

    def add(self, vector2: 'LogicVector2') -> None:
        """Add another vector"""
        self.x += vector2.x
        self.y += vector2.y

    def subtract(self, vector2: 'LogicVector2') -> None:
        """Subtract another vector"""
        self.x -= vector2.x
        self.y -= vector2.y

    def multiply(self, vector2: 'LogicVector2') -> None:
        """Component-wise multiply"""
        self.x *= vector2.x
        self.y *= vector2.y

    def clone(self) -> 'LogicVector2':
        """Create a copy"""
        return LogicVector2(self.x, self.y)

    def dot(self, vector2: 'LogicVector2') -> int:
        """Dot product"""
        return self.x * vector2.x + self.y * vector2.y

    def get_angle(self) -> int:
        """Get angle in degrees"""
        return LogicMath.get_angle(self.x, self.y)

    def get_angle_between(self, x: int, y: int) -> int:
        """Get angle between this vector and point"""
        return LogicMath.get_angle_between(
            LogicMath.get_angle(self.x, self.y),
            LogicMath.get_angle(x, y)
        )

    def get_distance(self, vector2: 'LogicVector2') -> int:
        """Get distance to another vector"""
        return self.get_distance_to(vector2.x, vector2.y)

    def get_distance_to(self, x: int, y: int) -> int:
        """Get distance to point"""
        return LogicMath.sqrt(self.get_distance_squared_to(x, y))

    def get_distance_squared(self, vector2: 'LogicVector2') -> int:
        """Get squared distance to another vector"""
        return self.get_distance_squared_to(vector2.x, vector2.y)

    def get_distance_squared_to(self, x: int, y: int) -> int:
        """Get squared distance to point"""
        dx = self.x - x
        dy = self.y - y

        # Overflow protection
        if abs(dx) > 46340 or abs(dy) > 46340:
            return 0x7FFFFFFF

        dist_x = dx * dx
        dist_y = dy * dy

        # Check for overflow
        if dist_y >= (dist_x ^ 0x7FFFFFFF):
            return 0x7FFFFFFF

        return dist_x + dist_y

    def get_length(self) -> int:
        """Get vector length"""
        return LogicMath.sqrt(self.get_length_squared())

    def get_length_squared(self) -> int:
        """Get squared vector length"""
        # Overflow protection
        if abs(self.x) > 46340 or abs(self.y) > 46340:
            return 0x7FFFFFFF

        len_x = self.x * self.x
        len_y = self.y * self.y

        # Check for overflow
        if len_y >= (len_x ^ 0x7FFFFFFF):
            return 0x7FFFFFFF

        return len_x + len_y

    def is_equal(self, vector2: 'LogicVector2') -> bool:
        """Check equality"""
        return self.x == vector2.x and self.y == vector2.y

    def is_in_area(self, min_x: int, min_y: int, max_x: int, max_y: int) -> bool:
        """Check if point is in rectangular area"""
        return (min_x <= self.x < min_x + max_x and 
                min_y <= self.y < min_y + max_y)

    def normalize(self, target_length: int) -> int:
        """Normalize to target length, return original length"""
        length = self.get_length()

        if length != 0:
            self.x = self.x * target_length // length
            self.y = self.y * target_length // length

        return length

    def rotate(self, degrees: int) -> None:
        """Rotate vector by degrees"""
        new_x = LogicMath.get_rotated_x(self.x, self.y, degrees)
        new_y = LogicMath.get_rotated_y(self.x, self.y, degrees)

        self.x = new_x
        self.y = new_y

    def set(self, x: int, y: int) -> None:
        """Set coordinates"""
        self.x = x
        self.y = y

    def encode(self, stream) -> None:
        """Encode to stream"""
        stream.write_v_int(self.x)
        stream.write_v_int(self.y)

    def decode(self, stream) -> None:
        """Decode from stream"""
        self.x = stream.read_v_int()
        self.y = stream.read_v_int()

    def to_tuple(self) -> Tuple[int, int]:
        """Convert to tuple"""
        return (self.x, self.y)

    def from_tuple(self, coords: Tuple[int, int]) -> None:
        """Set from tuple"""
        self.x, self.y = coords

    def __str__(self) -> str:
        """String representation"""
        return f"LogicVector2({self.x},{self.y})"

    def __repr__(self) -> str:
        """Detailed string representation"""
        return f"LogicVector2(x={self.x}, y={self.y})"

    def __eq__(self, other) -> bool:
        """Equality operator"""
        return isinstance(other, LogicVector2) and self.is_equal(other)

    def __ne__(self, other) -> bool:
        """Inequality operator"""
        return not self.__eq__(other)

    def __add__(self, other: 'LogicVector2') -> 'LogicVector2':
        """Addition operator"""
        result = self.clone()
        result.add(other)
        return result

    def __sub__(self, other: 'LogicVector2') -> 'LogicVector2':
        """Subtraction operator"""
        result = self.clone()
        result.subtract(other)
        return result

    def __mul__(self, scalar: int) -> 'LogicVector2':
        """Scalar multiplication"""
        return LogicVector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: int) -> 'LogicVector2':
        """Scalar division"""
        if scalar == 0:
            return LogicVector2()
        return LogicVector2(self.x // scalar, self.y // scalar)
