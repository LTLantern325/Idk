"""
Python conversion of Supercell.Laser.Logic.Battle.Level.Tile.cs
Tile class for battle level grid system
"""

from typing import Optional, List
from enum import IntEnum

class TileType(IntEnum):
    """Tile types"""
    EMPTY = 0
    WALL = 1
    GRASS = 2
    WATER = 3
    SPAWN = 4
    GOAL = 5
    POWER_UP = 6
    DESTRUCTIBLE = 7

class Tile:
    """Tile class for battle level grid system"""

    def __init__(self, x: int = 0, y: int = 0, tile_type: TileType = TileType.EMPTY):
        """Initialize tile"""
        self.x = x
        self.y = y
        self.tile_type = tile_type
        self.is_walkable = True
        self.is_destructible = False
        self.health = 0
        self.max_health = 0

        # Visual properties
        self.sprite_id = 0
        self.animation_id = 0
        self.rotation = 0

        # Game properties
        self.movement_speed_modifier = 1.0
        self.vision_blocking = False
        self.projectile_blocking = False

        # Special properties
        self.is_spawn_point = False
        self.team_id = 0
        self.power_up_type = 0

        self._initialize_tile_properties()

    def _initialize_tile_properties(self) -> None:
        """Initialize tile properties based on type"""
        if self.tile_type == TileType.EMPTY:
            self.is_walkable = True
            self.is_destructible = False
            self.vision_blocking = False
            self.projectile_blocking = False
        elif self.tile_type == TileType.WALL:
            self.is_walkable = False
            self.is_destructible = False
            self.vision_blocking = True
            self.projectile_blocking = True
        elif self.tile_type == TileType.GRASS:
            self.is_walkable = True
            self.movement_speed_modifier = 0.8
            self.vision_blocking = True
            self.projectile_blocking = False
        elif self.tile_type == TileType.WATER:
            self.is_walkable = False
            self.vision_blocking = False
            self.projectile_blocking = False
        elif self.tile_type == TileType.SPAWN:
            self.is_walkable = True
            self.is_spawn_point = True
        elif self.tile_type == TileType.DESTRUCTIBLE:
            self.is_walkable = False
            self.is_destructible = True
            self.health = 100
            self.max_health = 100
            self.vision_blocking = True
            self.projectile_blocking = True

    def get_x(self) -> int:
        """Get X coordinate"""
        return self.x

    def get_y(self) -> int:
        """Get Y coordinate"""
        return self.y

    def set_position(self, x: int, y: int) -> None:
        """Set tile position"""
        self.x = x
        self.y = y

    def get_tile_type(self) -> TileType:
        """Get tile type"""
        return self.tile_type

    def set_tile_type(self, tile_type: TileType) -> None:
        """Set tile type"""
        self.tile_type = tile_type
        self._initialize_tile_properties()

    def is_tile_walkable(self) -> bool:
        """Check if tile is walkable"""
        return self.is_walkable and (not self.is_destructible or self.health <= 0)

    def is_tile_destructible(self) -> bool:
        """Check if tile is destructible"""
        return self.is_destructible

    def get_health(self) -> int:
        """Get tile health"""
        return self.health

    def get_max_health(self) -> int:
        """Get tile maximum health"""
        return self.max_health

    def take_damage(self, damage: int) -> bool:
        """Take damage and return true if destroyed"""
        if not self.is_destructible:
            return False

        self.health = max(0, self.health - damage)
        if self.health <= 0:
            self.is_walkable = True
            self.vision_blocking = False
            self.projectile_blocking = False
            return True
        return False

    def repair(self, amount: int) -> None:
        """Repair tile"""
        if self.is_destructible:
            old_health = self.health
            self.health = min(self.max_health, self.health + amount)

            # Restore blocking properties if repaired
            if old_health <= 0 and self.health > 0:
                self._initialize_tile_properties()

    def is_destroyed(self) -> bool:
        """Check if tile is destroyed"""
        return self.is_destructible and self.health <= 0

    def blocks_vision(self) -> bool:
        """Check if tile blocks vision"""
        return self.vision_blocking and not self.is_destroyed()

    def blocks_projectiles(self) -> bool:
        """Check if tile blocks projectiles"""
        return self.projectile_blocking and not self.is_destroyed()

    def get_movement_speed_modifier(self) -> float:
        """Get movement speed modifier"""
        return self.movement_speed_modifier

    def is_tile_spawn_point(self) -> bool:
        """Check if tile is a spawn point"""
        return self.is_spawn_point

    def get_team_id(self) -> int:
        """Get team ID for spawn points"""
        return self.team_id

    def set_team_id(self, team_id: int) -> None:
        """Set team ID for spawn points"""
        self.team_id = team_id

    def get_power_up_type(self) -> int:
        """Get power up type"""
        return self.power_up_type

    def set_power_up_type(self, power_up_type: int) -> None:
        """Set power up type"""
        self.power_up_type = power_up_type

    def get_sprite_id(self) -> int:
        """Get sprite ID"""
        return self.sprite_id

    def set_sprite_id(self, sprite_id: int) -> None:
        """Set sprite ID"""
        self.sprite_id = sprite_id

    def get_rotation(self) -> int:
        """Get rotation"""
        return self.rotation

    def set_rotation(self, rotation: int) -> None:
        """Set rotation"""
        self.rotation = rotation % 360

    def reset(self) -> None:
        """Reset tile to original state"""
        if self.is_destructible:
            self.health = self.max_health
        self._initialize_tile_properties()

    def can_place_object(self) -> bool:
        """Check if object can be placed on this tile"""
        return self.is_walkable and not self.is_spawn_point

    def get_type_name(self) -> str:
        """Get tile type name"""
        type_names = {
            TileType.EMPTY: "Empty",
            TileType.WALL: "Wall", 
            TileType.GRASS: "Grass",
            TileType.WATER: "Water",
            TileType.SPAWN: "Spawn",
            TileType.GOAL: "Goal",
            TileType.POWER_UP: "Power Up",
            TileType.DESTRUCTIBLE: "Destructible"
        }
        return type_names.get(self.tile_type, "Unknown")

    def distance_to(self, other: 'Tile') -> float:
        """Get distance to another tile"""
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx * dx + dy * dy) ** 0.5

    def manhattan_distance_to(self, other: 'Tile') -> int:
        """Get Manhattan distance to another tile"""
        return abs(self.x - other.x) + abs(self.y - other.y)

    def is_adjacent_to(self, other: 'Tile') -> bool:
        """Check if tile is adjacent to another tile"""
        return self.manhattan_distance_to(other) == 1

    def encode(self, stream) -> None:
        """Encode tile to stream"""
        stream.write_v_int(self.x)
        stream.write_v_int(self.y)
        stream.write_v_int(int(self.tile_type))
        stream.write_v_int(self.health)
        stream.write_v_int(self.sprite_id)
        stream.write_v_int(self.rotation)
        stream.write_v_int(self.team_id)

    def decode(self, stream) -> None:
        """Decode tile from stream"""
        self.x = stream.read_v_int()
        self.y = stream.read_v_int()
        self.tile_type = TileType(stream.read_v_int())
        self.health = stream.read_v_int()
        self.sprite_id = stream.read_v_int()
        self.rotation = stream.read_v_int()
        self.team_id = stream.read_v_int()
        self._initialize_tile_properties()

    def __str__(self) -> str:
        """String representation"""
        destroyed = " (destroyed)" if self.is_destroyed() else ""
        return f"Tile({self.x}, {self.y}, {self.get_type_name()}{destroyed})"

    def __eq__(self, other) -> bool:
        """Check equality"""
        if not isinstance(other, Tile):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        """Hash for use in sets/dicts"""
        return hash((self.x, self.y))
