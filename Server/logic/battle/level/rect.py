"""
Python conversion of Supercell.Laser.Logic.Battle.Level.Rect.cs
Rectangle class for battle level geometry
"""

from typing import Tuple, Optional

class Rect:
    """Rectangle class for battle level geometry"""

    def __init__(self, x: float = 0.0, y: float = 0.0, width: float = 0.0, height: float = 0.0):
        """Initialize rectangle"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_x(self) -> float:
        """Get X coordinate"""
        return self.x

    def set_x(self, x: float) -> None:
        """Set X coordinate"""
        self.x = x

    def get_y(self) -> float:
        """Get Y coordinate"""
        return self.y

    def set_y(self, y: float) -> None:
        """Set Y coordinate"""
        self.y = y

    def get_width(self) -> float:
        """Get width"""
        return self.width

    def set_width(self, width: float) -> None:
        """Set width"""
        self.width = max(0.0, width)

    def get_height(self) -> float:
        """Get height"""
        return self.height

    def set_height(self, height: float) -> None:
        """Set height"""
        self.height = max(0.0, height)

    def get_left(self) -> float:
        """Get left edge"""
        return self.x

    def get_right(self) -> float:
        """Get right edge"""
        return self.x + self.width

    def get_top(self) -> float:
        """Get top edge"""
        return self.y

    def get_bottom(self) -> float:
        """Get bottom edge"""
        return self.y + self.height

    def get_center_x(self) -> float:
        """Get center X coordinate"""
        return self.x + self.width / 2.0

    def get_center_y(self) -> float:
        """Get center Y coordinate"""
        return self.y + self.height / 2.0

    def get_center(self) -> Tuple[float, float]:
        """Get center point"""
        return (self.get_center_x(), self.get_center_y())

    def get_area(self) -> float:
        """Get rectangle area"""
        return self.width * self.height

    def get_perimeter(self) -> float:
        """Get rectangle perimeter"""
        return 2.0 * (self.width + self.height)

    def contains_point(self, x: float, y: float) -> bool:
        """Check if rectangle contains point"""
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)

    def contains_rect(self, other: 'Rect') -> bool:
        """Check if rectangle contains another rectangle"""
        return (self.x <= other.x and 
                self.y <= other.y and
                self.get_right() >= other.get_right() and
                self.get_bottom() >= other.get_bottom())

    def intersects(self, other: 'Rect') -> bool:
        """Check if rectangle intersects with another rectangle"""
        return not (self.get_right() < other.x or 
                   other.get_right() < self.x or
                   self.get_bottom() < other.y or
                   other.get_bottom() < self.y)

    def get_intersection(self, other: 'Rect') -> Optional['Rect']:
        """Get intersection rectangle with another rectangle"""
        if not self.intersects(other):
            return None

        left = max(self.x, other.x)
        top = max(self.y, other.y)
        right = min(self.get_right(), other.get_right())
        bottom = min(self.get_bottom(), other.get_bottom())

        return Rect(left, top, right - left, bottom - top)

    def expand(self, amount: float) -> 'Rect':
        """Expand rectangle by amount in all directions"""
        return Rect(self.x - amount, self.y - amount, 
                   self.width + 2 * amount, self.height + 2 * amount)

    def shrink(self, amount: float) -> 'Rect':
        """Shrink rectangle by amount in all directions"""
        return self.expand(-amount)

    def move(self, dx: float, dy: float) -> None:
        """Move rectangle by offset"""
        self.x += dx
        self.y += dy

    def move_to(self, x: float, y: float) -> None:
        """Move rectangle to position"""
        self.x = x
        self.y = y

    def resize(self, width: float, height: float) -> None:
        """Resize rectangle"""
        self.width = max(0.0, width)
        self.height = max(0.0, height)

    def is_empty(self) -> bool:
        """Check if rectangle is empty"""
        return self.width <= 0.0 or self.height <= 0.0

    def is_square(self) -> bool:
        """Check if rectangle is square"""
        return abs(self.width - self.height) < 0.001

    def get_aspect_ratio(self) -> float:
        """Get aspect ratio (width / height)"""
        if self.height <= 0.0:
            return float('inf')
        return self.width / self.height

    def distance_to_point(self, x: float, y: float) -> float:
        """Get distance from rectangle to point"""
        if self.contains_point(x, y):
            return 0.0

        dx = max(0, max(self.x - x, x - self.get_right()))
        dy = max(0, max(self.y - y, y - self.get_bottom()))

        return (dx * dx + dy * dy) ** 0.5

    def copy(self) -> 'Rect':
        """Create copy of rectangle"""
        return Rect(self.x, self.y, self.width, self.height)

    @classmethod
    def from_points(cls, x1: float, y1: float, x2: float, y2: float) -> 'Rect':
        """Create rectangle from two points"""
        left = min(x1, x2)
        top = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        return cls(left, top, width, height)

    @classmethod
    def from_center(cls, center_x: float, center_y: float, width: float, height: float) -> 'Rect':
        """Create rectangle from center point"""
        x = center_x - width / 2.0
        y = center_y - height / 2.0
        return cls(x, y, width, height)

    def encode(self, stream) -> None:
        """Encode rectangle to stream"""
        stream.write_float(self.x)
        stream.write_float(self.y)
        stream.write_float(self.width)
        stream.write_float(self.height)

    def decode(self, stream) -> None:
        """Decode rectangle from stream"""
        self.x = stream.read_float()
        self.y = stream.read_float()
        self.width = stream.read_float()
        self.height = stream.read_float()

    def __str__(self) -> str:
        """String representation"""
        return f"Rect(x={self.x}, y={self.y}, w={self.width}, h={self.height})"

    def __eq__(self, other) -> bool:
        """Check equality"""
        if not isinstance(other, Rect):
            return False
        return (abs(self.x - other.x) < 0.001 and 
                abs(self.y - other.y) < 0.001 and
                abs(self.width - other.width) < 0.001 and
                abs(self.height - other.height) < 0.001)
