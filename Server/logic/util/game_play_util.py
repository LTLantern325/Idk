"""
Python conversion of Supercell.Laser.Logic.Util.GamePlayUtil.cs
Gameplay utility functions
"""

import math
from typing import Tuple, Optional

class GamePlayUtil:
    """Gameplay utility functions"""

    @staticmethod
    def calculate_distance(x1: int, y1: int, x2: int, y2: int) -> float:
        """Calculate distance between two points"""
        dx = x2 - x1
        dy = y2 - y1
        return math.sqrt(dx * dx + dy * dy)

    @staticmethod
    def calculate_angle(x1: int, y1: int, x2: int, y2: int) -> float:
        """Calculate angle between two points in degrees"""
        dx = x2 - x1
        dy = y2 - y1
        return math.degrees(math.atan2(dy, dx))

    @staticmethod
    def is_in_range(x1: int, y1: int, x2: int, y2: int, range_distance: float) -> bool:
        """Check if two points are within range"""
        distance = GamePlayUtil.calculate_distance(x1, y1, x2, y2)
        return distance <= range_distance

    @staticmethod
    def normalize_angle(angle: float) -> float:
        """Normalize angle to 0-360 degrees"""
        while angle < 0:
            angle += 360
        while angle >= 360:
            angle -= 360
        return angle

    @staticmethod
    def angle_difference(angle1: float, angle2: float) -> float:
        """Calculate difference between two angles"""
        diff = abs(angle1 - angle2)
        if diff > 180:
            diff = 360 - diff
        return diff

    @staticmethod
    def move_towards(x: int, y: int, target_x: int, target_y: int, speed: float) -> Tuple[int, int]:
        """Move point towards target at given speed"""
        distance = GamePlayUtil.calculate_distance(x, y, target_x, target_y)
        if distance <= speed:
            return target_x, target_y

        dx = target_x - x
        dy = target_y - y

        # Normalize direction
        factor = speed / distance
        new_x = x + int(dx * factor)
        new_y = y + int(dy * factor)

        return new_x, new_y

    @staticmethod
    def clamp(value: float, min_value: float, max_value: float) -> float:
        """Clamp value between min and max"""
        return max(min_value, min(value, max_value))

    @staticmethod
    def lerp(start: float, end: float, t: float) -> float:
        """Linear interpolation between start and end"""
        return start + (end - start) * GamePlayUtil.clamp(t, 0.0, 1.0)

    @staticmethod
    def is_point_in_circle(px: int, py: int, cx: int, cy: int, radius: float) -> bool:
        """Check if point is inside circle"""
        return GamePlayUtil.calculate_distance(px, py, cx, cy) <= radius

    @staticmethod
    def is_point_in_rectangle(px: int, py: int, rx: int, ry: int, width: int, height: int) -> bool:
        """Check if point is inside rectangle"""
        return rx <= px <= rx + width and ry <= py <= ry + height
