"""
Python conversion of Supercell.Laser.Logic.Battle.Objects.GameObject.cs
Base game object class for battle objects
"""

from typing import Optional, Tuple

class GameObject:
    """Base game object class for battle objects"""

    def __init__(self):
        """Initialize game object"""
        self.object_id = 0
        self.x = 0.0
        self.y = 0.0
        self.rotation = 0.0
        self.is_alive = True
        self.is_active = True
        self.creation_time = 0.0
        self.age = 0.0

        # Visual properties
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.alpha = 1.0
        self.z_order = 0

        # Physics properties
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.acceleration_x = 0.0
        self.acceleration_y = 0.0
        self.mass = 1.0
        self.friction = 0.98

        # Collision properties
        self.collision_radius = 10.0
        self.can_collide = True
        self.is_solid = True

        # Type information
        self.object_type = 0
        self.data_id = 0

    def get_object_id(self) -> int:
        """Get object ID"""
        return self.object_id

    def set_object_id(self, object_id: int) -> None:
        """Set object ID"""
        self.object_id = object_id

    def get_position(self) -> Tuple[float, float]:
        """Get position as tuple"""
        return (self.x, self.y)

    def set_position(self, x: float, y: float) -> None:
        """Set position"""
        self.x = x
        self.y = y

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

    def get_rotation(self) -> float:
        """Get rotation in radians"""
        return self.rotation

    def set_rotation(self, rotation: float) -> None:
        """Set rotation in radians"""
        self.rotation = rotation

    def get_rotation_degrees(self) -> float:
        """Get rotation in degrees"""
        import math
        return math.degrees(self.rotation)

    def set_rotation_degrees(self, degrees: float) -> None:
        """Set rotation in degrees"""
        import math
        self.rotation = math.radians(degrees)

    def is_object_alive(self) -> bool:
        """Check if object is alive"""
        return self.is_alive

    def is_object_active(self) -> bool:
        """Check if object is active"""
        return self.is_active and self.is_alive

    def activate(self) -> None:
        """Activate object"""
        self.is_active = True

    def deactivate(self) -> None:
        """Deactivate object"""
        self.is_active = False

    def destroy(self) -> None:
        """Destroy object"""
        self.is_alive = False
        self.is_active = False

    def get_velocity(self) -> Tuple[float, float]:
        """Get velocity as tuple"""
        return (self.velocity_x, self.velocity_y)

    def set_velocity(self, vx: float, vy: float) -> None:
        """Set velocity"""
        self.velocity_x = vx
        self.velocity_y = vy

    def add_velocity(self, vx: float, vy: float) -> None:
        """Add to velocity"""
        self.velocity_x += vx
        self.velocity_y += vy

    def get_speed(self) -> float:
        """Get current speed (magnitude of velocity)"""
        return (self.velocity_x * self.velocity_x + self.velocity_y * self.velocity_y) ** 0.5

    def get_acceleration(self) -> Tuple[float, float]:
        """Get acceleration as tuple"""
        return (self.acceleration_x, self.acceleration_y)

    def set_acceleration(self, ax: float, ay: float) -> None:
        """Set acceleration"""
        self.acceleration_x = ax
        self.acceleration_y = ay

    def get_collision_radius(self) -> float:
        """Get collision radius"""
        return self.collision_radius

    def set_collision_radius(self, radius: float) -> None:
        """Set collision radius"""
        self.collision_radius = max(0.0, radius)

    def can_object_collide(self) -> bool:
        """Check if object can collide"""
        return self.can_collide and self.is_object_active()

    def is_object_solid(self) -> bool:
        """Check if object is solid"""
        return self.is_solid

    def distance_to(self, other: 'GameObject') -> float:
        """Get distance to another object"""
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx * dx + dy * dy) ** 0.5

    def distance_to_position(self, x: float, y: float) -> float:
        """Get distance to position"""
        dx = self.x - x
        dy = self.y - y
        return (dx * dx + dy * dy) ** 0.5

    def is_colliding_with(self, other: 'GameObject') -> bool:
        """Check if colliding with another object"""
        if not self.can_object_collide() or not other.can_object_collide():
            return False

        distance = self.distance_to(other)
        return distance <= (self.collision_radius + other.collision_radius)

    def move(self, dx: float, dy: float) -> None:
        """Move by offset"""
        self.x += dx
        self.y += dy

    def move_to(self, x: float, y: float) -> None:
        """Move to position"""
        self.x = x
        self.y = y

    def rotate(self, angle: float) -> None:
        """Rotate by angle in radians"""
        self.rotation += angle

    def rotate_degrees(self, degrees: float) -> None:
        """Rotate by angle in degrees"""
        import math
        self.rotation += math.radians(degrees)

    def face_towards(self, target_x: float, target_y: float) -> None:
        """Face towards target position"""
        import math
        dx = target_x - self.x
        dy = target_y - self.y
        self.rotation = math.atan2(dy, dx)

    def face_towards_object(self, target: 'GameObject') -> None:
        """Face towards target object"""
        self.face_towards(target.x, target.y)

    def update(self, delta_time: float) -> None:
        """Update object (called each frame)"""
        if not self.is_object_active():
            return

        # Update age
        self.age += delta_time

        # Update physics
        self.velocity_x += self.acceleration_x * delta_time
        self.velocity_y += self.acceleration_y * delta_time

        # Apply friction
        self.velocity_x *= self.friction
        self.velocity_y *= self.friction

        # Update position
        self.x += self.velocity_x * delta_time
        self.y += self.velocity_y * delta_time

    def get_age(self) -> float:
        """Get object age"""
        return self.age

    def get_scale(self) -> Tuple[float, float]:
        """Get scale as tuple"""
        return (self.scale_x, self.scale_y)

    def set_scale(self, scale_x: float, scale_y: float) -> None:
        """Set scale"""
        self.scale_x = scale_x
        self.scale_y = scale_y

    def set_uniform_scale(self, scale: float) -> None:
        """Set uniform scale"""
        self.scale_x = scale
        self.scale_y = scale

    def get_alpha(self) -> float:
        """Get alpha transparency"""
        return self.alpha

    def set_alpha(self, alpha: float) -> None:
        """Set alpha transparency"""
        self.alpha = max(0.0, min(1.0, alpha))

    def get_z_order(self) -> int:
        """Get Z order (rendering order)"""
        return self.z_order

    def set_z_order(self, z_order: int) -> None:
        """Set Z order"""
        self.z_order = z_order

    def encode(self, stream) -> None:
        """Encode object to stream"""
        stream.write_v_int(self.object_id)
        stream.write_float(self.x)
        stream.write_float(self.y)
        stream.write_float(self.rotation)
        stream.write_boolean(self.is_alive)
        stream.write_boolean(self.is_active)
        stream.write_float(self.velocity_x)
        stream.write_float(self.velocity_y)

    def decode(self, stream) -> None:
        """Decode object from stream"""
        self.object_id = stream.read_v_int()
        self.x = stream.read_float()
        self.y = stream.read_float()
        self.rotation = stream.read_float()
        self.is_alive = stream.read_boolean()
        self.is_active = stream.read_boolean()
        self.velocity_x = stream.read_float()
        self.velocity_y = stream.read_float()

    def __str__(self) -> str:
        """String representation"""
        return f"GameObject(id={self.object_id}, pos=({self.x:.1f}, {self.y:.1f}))"
