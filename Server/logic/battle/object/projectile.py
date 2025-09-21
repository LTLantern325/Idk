"""
Python conversion of Supercell.Laser.Logic.Battle.Objects.Projectile.cs
Projectile class for battle projectiles and bullets
"""

from typing import Optional, List, Tuple
from enum import IntEnum
from .game_object import GameObject

class ProjectileType(IntEnum):
    """Projectile types"""
    BULLET = 1
    SHELL = 2
    ROCKET = 3
    GRENADE = 4
    LASER = 5
    ENERGY_BALL = 6
    ARROW = 7
    BOUNCE_BALL = 8

class Projectile(GameObject):
    """Projectile class for battle projectiles and bullets"""

    def __init__(self):
        """Initialize projectile"""
        super().__init__()
        self.projectile_data_id = 0
        self.projectile_type = ProjectileType.BULLET
        self.owner_id = 0
        self.team_id = 0

        # Damage properties
        self.damage = 100
        self.damage_falloff_start = 0.0  # Distance where falloff starts
        self.damage_falloff_end = 300.0  # Distance where damage is minimum
        self.min_damage_multiplier = 0.5  # Minimum damage multiplier

        # Movement properties
        self.speed = 500.0
        self.max_travel_distance = 600.0
        self.travel_distance = 0.0
        self.direction_x = 0.0
        self.direction_y = 0.0

        # Special properties
        self.pierces_targets = False
        self.max_pierce_count = 0
        self.current_pierce_count = 0
        self.bounces = False
        self.max_bounce_count = 0
        self.current_bounce_count = 0
        self.explodes_on_impact = False
        self.explosion_radius = 0.0
        self.explosion_damage = 0

        # Target tracking
        self.hit_targets = set()  # IDs of targets already hit
        self.target_id = 0  # For homing projectiles
        self.homing_strength = 0.0

        # Trail effect
        self.leaves_trail = False
        self.trail_effect_id = 0
        self.trail_positions = []  # List of previous positions
        self.max_trail_length = 10

    def get_projectile_data_id(self) -> int:
        """Get projectile data ID"""
        return self.projectile_data_id

    def set_projectile_data_id(self, data_id: int) -> None:
        """Set projectile data ID"""
        self.projectile_data_id = data_id

    def get_projectile_type(self) -> ProjectileType:
        """Get projectile type"""
        return self.projectile_type

    def set_projectile_type(self, projectile_type: ProjectileType) -> None:
        """Set projectile type"""
        self.projectile_type = projectile_type
        self._update_projectile_properties()

    def get_owner_id(self) -> int:
        """Get owner ID"""
        return self.owner_id

    def set_owner_id(self, owner_id: int) -> None:
        """Set owner ID"""
        self.owner_id = owner_id

    def get_team_id(self) -> int:
        """Get team ID"""
        return self.team_id

    def set_team_id(self, team_id: int) -> None:
        """Set team ID"""
        self.team_id = team_id

    def get_damage(self) -> int:
        """Get base damage"""
        return self.damage

    def set_damage(self, damage: int) -> None:
        """Set base damage"""
        self.damage = max(0, damage)

    def get_speed(self) -> float:
        """Get projectile speed"""
        return self.speed

    def set_speed(self, speed: float) -> None:
        """Set projectile speed"""
        self.speed = max(0.0, speed)

    def launch(self, start_x: float, start_y: float, target_x: float, target_y: float) -> None:
        """Launch projectile towards target"""
        self.x = start_x
        self.y = start_y

        # Calculate direction
        dx = target_x - start_x
        dy = target_y - start_y
        distance = (dx * dx + dy * dy) ** 0.5

        if distance > 0:
            self.direction_x = dx / distance
            self.direction_y = dy / distance
        else:
            self.direction_x = 1.0
            self.direction_y = 0.0

        # Set velocity
        self.velocity_x = self.direction_x * self.speed
        self.velocity_y = self.direction_y * self.speed

        # Set rotation to face direction
        import math
        self.rotation = math.atan2(self.direction_y, self.direction_x)

        # Reset counters
        self.travel_distance = 0.0
        self.current_pierce_count = 0
        self.current_bounce_count = 0
        self.hit_targets.clear()

    def launch_with_angle(self, start_x: float, start_y: float, angle: float) -> None:
        """Launch projectile at specific angle"""
        import math
        target_x = start_x + math.cos(angle) * 100
        target_y = start_y + math.sin(angle) * 100
        self.launch(start_x, start_y, target_x, target_y)

    def can_hit_target(self, target_id: int, target_team_id: int) -> bool:
        """Check if can hit target"""
        if target_id == self.owner_id:
            return False  # Can't hit owner

        if target_id in self.hit_targets and not self.pierces_targets:
            return False  # Already hit this target

        if self.team_id != 0 and target_team_id == self.team_id:
            return False  # Can't hit teammates

        return True

    def hit_target(self, target_id: int) -> int:
        """Hit target and return damage dealt"""
        if not self.can_hit_target(target_id, 0):  # Simplified team check
            return 0

        # Calculate damage based on distance traveled
        damage_multiplier = self._get_damage_multiplier()
        actual_damage = int(self.damage * damage_multiplier)

        # Add to hit targets
        self.hit_targets.add(target_id)

        # Check if projectile should be destroyed
        if not self.pierces_targets:
            if self.explodes_on_impact:
                self._explode()
            else:
                self.destroy()
        else:
            self.current_pierce_count += 1
            if self.current_pierce_count >= self.max_pierce_count:
                if self.explodes_on_impact:
                    self._explode()
                else:
                    self.destroy()

        return actual_damage

    def bounce_off_surface(self, surface_normal_x: float, surface_normal_y: float) -> bool:
        """Bounce off surface"""
        if not self.bounces or self.current_bounce_count >= self.max_bounce_count:
            self.destroy()
            return False

        # Calculate reflected direction
        dot_product = (self.direction_x * surface_normal_x + 
                      self.direction_y * surface_normal_y)

        self.direction_x -= 2 * dot_product * surface_normal_x
        self.direction_y -= 2 * dot_product * surface_normal_y

        # Update velocity
        self.velocity_x = self.direction_x * self.speed
        self.velocity_y = self.direction_y * self.speed

        # Update rotation
        import math
        self.rotation = math.atan2(self.direction_y, self.direction_x)

        self.current_bounce_count += 1
        return True

    def _get_damage_multiplier(self) -> float:
        """Get damage multiplier based on distance"""
        if self.damage_falloff_start >= self.damage_falloff_end:
            return 1.0

        if self.travel_distance <= self.damage_falloff_start:
            return 1.0

        if self.travel_distance >= self.damage_falloff_end:
            return self.min_damage_multiplier

        # Linear interpolation
        falloff_range = self.damage_falloff_end - self.damage_falloff_start
        distance_in_range = self.travel_distance - self.damage_falloff_start
        falloff_factor = distance_in_range / falloff_range

        return 1.0 - falloff_factor * (1.0 - self.min_damage_multiplier)

    def _explode(self) -> None:
        """Handle explosion"""
        # Explosion damage would be handled by the battle system
        # For now, just destroy the projectile
        self.destroy()

    def _update_projectile_properties(self) -> None:
        """Update projectile properties based on type"""
        if self.projectile_type == ProjectileType.BULLET:
            self.speed = 800.0
            self.collision_radius = 3.0
            self.max_travel_distance = 600.0
        elif self.projectile_type == ProjectileType.SHELL:
            self.speed = 600.0
            self.collision_radius = 8.0
            self.max_travel_distance = 800.0
            self.damage_falloff_start = 200.0
        elif self.projectile_type == ProjectileType.ROCKET:
            self.speed = 400.0
            self.collision_radius = 12.0
            self.explodes_on_impact = True
            self.explosion_radius = 100.0
            self.explosion_damage = self.damage // 2
        elif self.projectile_type == ProjectileType.GRENADE:
            self.speed = 300.0
            self.collision_radius = 15.0
            self.explodes_on_impact = True
            self.explosion_radius = 150.0
            self.bounces = True
            self.max_bounce_count = 2
        elif self.projectile_type == ProjectileType.BOUNCE_BALL:
            self.speed = 500.0
            self.collision_radius = 10.0
            self.bounces = True
            self.max_bounce_count = 5
            self.pierces_targets = True
            self.max_pierce_count = 3

    def _update_homing(self, delta_time: float) -> None:
        """Update homing behavior"""
        if self.homing_strength <= 0 or self.target_id == 0:
            return

        # This would need access to the target object
        # For now, just a placeholder
        pass

    def update(self, delta_time: float) -> None:
        """Update projectile"""
        if not self.is_object_active():
            return

        # Update trail
        if self.leaves_trail:
            self.trail_positions.append((self.x, self.y))
            if len(self.trail_positions) > self.max_trail_length:
                self.trail_positions.pop(0)

        # Update homing
        self._update_homing(delta_time)

        # Update position and travel distance
        old_x, old_y = self.x, self.y
        super().update(delta_time)

        dx = self.x - old_x
        dy = self.y - old_y
        self.travel_distance += (dx * dx + dy * dy) ** 0.5

        # Check if reached max travel distance
        if self.travel_distance >= self.max_travel_distance:
            if self.explodes_on_impact:
                self._explode()
            else:
                self.destroy()

    def get_type_name(self) -> str:
        """Get projectile type name"""
        type_names = {
            ProjectileType.BULLET: "Bullet",
            ProjectileType.SHELL: "Shell",
            ProjectileType.ROCKET: "Rocket",
            ProjectileType.GRENADE: "Grenade",
            ProjectileType.LASER: "Laser",
            ProjectileType.ENERGY_BALL: "Energy Ball",
            ProjectileType.ARROW: "Arrow",
            ProjectileType.BOUNCE_BALL: "Bounce Ball"
        }
        return type_names.get(self.projectile_type, "Unknown Projectile")

    def encode(self, stream) -> None:
        """Encode projectile to stream"""
        super().encode(stream)
        stream.write_v_int(self.projectile_data_id)
        stream.write_v_int(int(self.projectile_type))
        stream.write_v_int(self.owner_id)
        stream.write_v_int(self.team_id)
        stream.write_v_int(self.damage)
        stream.write_float(self.speed)
        stream.write_float(self.travel_distance)
        stream.write_float(self.direction_x)
        stream.write_float(self.direction_y)

    def decode(self, stream) -> None:
        """Decode projectile from stream"""
        super().decode(stream)
        self.projectile_data_id = stream.read_v_int()
        self.projectile_type = ProjectileType(stream.read_v_int())
        self.owner_id = stream.read_v_int()
        self.team_id = stream.read_v_int()
        self.damage = stream.read_v_int()
        self.speed = stream.read_float()
        self.travel_distance = stream.read_float()
        self.direction_x = stream.read_float()
        self.direction_y = stream.read_float()
        self._update_projectile_properties()

    def __str__(self) -> str:
        """String representation"""
        return f"Projectile({self.get_type_name()}, damage={self.damage}, owner={self.owner_id})"
