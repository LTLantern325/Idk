"""
Python conversion of Supercell.Laser.Logic.Battle.Objects.GameObjectManager.cs
Manager class for game objects in battle
"""

from typing import Dict, List, Optional, Set, Callable
from .game_object import GameObject
from .game_object_factory import GameObjectFactory
from .character import Character
from .projectile import Projectile
from .area_effect import AreaEffect

class GameObjectManager:
    """Manager class for game objects in battle"""

    def __init__(self):
        """Initialize game object manager"""
        self.objects: Dict[int, GameObject] = {}
        self.active_objects: Set[int] = set()
        self.objects_to_remove: Set[int] = set()
        self.objects_by_type: Dict[int, Set[int]] = {}

        # Spatial optimization (simple grid)
        self.grid_size = 200.0
        self.spatial_grid: Dict[tuple, Set[int]] = {}

        # Update callbacks
        self.update_callbacks: List[Callable[[GameObject, float], None]] = []

        # Statistics
        self.total_objects_created = 0
        self.total_objects_destroyed = 0

    def add_object(self, obj: GameObject) -> bool:
        """Add object to manager"""
        if not obj or obj.object_id in self.objects:
            return False

        self.objects[obj.object_id] = obj
        self.active_objects.add(obj.object_id)

        # Add to type mapping
        obj_type = obj.object_type
        if obj_type not in self.objects_by_type:
            self.objects_by_type[obj_type] = set()
        self.objects_by_type[obj_type].add(obj.object_id)

        # Add to spatial grid
        self._add_to_spatial_grid(obj)

        self.total_objects_created += 1
        return True

    def remove_object(self, object_id: int) -> bool:
        """Remove object from manager"""
        if object_id not in self.objects:
            return False

        obj = self.objects[object_id]

        # Remove from spatial grid
        self._remove_from_spatial_grid(obj)

        # Remove from type mapping
        if obj.object_type in self.objects_by_type:
            self.objects_by_type[obj.object_type].discard(object_id)

        # Remove from collections
        self.active_objects.discard(object_id)
        del self.objects[object_id]

        self.total_objects_destroyed += 1
        return True

    def get_object(self, object_id: int) -> Optional[GameObject]:
        """Get object by ID"""
        return self.objects.get(object_id)

    def get_objects_by_type(self, object_type: int) -> List[GameObject]:
        """Get all objects of specific type"""
        if object_type not in self.objects_by_type:
            return []

        result = []
        for obj_id in self.objects_by_type[object_type]:
            if obj_id in self.objects:
                result.append(self.objects[obj_id])
        return result

    def get_all_characters(self) -> List[Character]:
        """Get all character objects"""
        from .game_object_factory import GameObjectType
        characters = self.get_objects_by_type(GameObjectType.CHARACTER)
        return [obj for obj in characters if isinstance(obj, Character)]

    def get_all_projectiles(self) -> List[Projectile]:
        """Get all projectile objects"""
        from .game_object_factory import GameObjectType
        projectiles = self.get_objects_by_type(GameObjectType.PROJECTILE)
        return [obj for obj in projectiles if isinstance(obj, Projectile)]

    def get_all_area_effects(self) -> List[AreaEffect]:
        """Get all area effect objects"""
        from .game_object_factory import GameObjectType
        effects = self.get_objects_by_type(GameObjectType.AREA_EFFECT)
        return [obj for obj in effects if isinstance(obj, AreaEffect)]

    def get_objects_in_radius(self, x: float, y: float, radius: float) -> List[GameObject]:
        """Get all objects within radius of position"""
        result = []
        radius_squared = radius * radius

        # Use spatial grid for optimization
        grid_cells = self._get_grid_cells_in_radius(x, y, radius)
        candidate_objects = set()

        for cell in grid_cells:
            if cell in self.spatial_grid:
                candidate_objects.update(self.spatial_grid[cell])

        # Check distance for candidates
        for obj_id in candidate_objects:
            if obj_id in self.objects:
                obj = self.objects[obj_id]
                dx = obj.x - x
                dy = obj.y - y
                distance_squared = dx * dx + dy * dy

                if distance_squared <= radius_squared:
                    result.append(obj)

        return result

    def get_nearest_object(self, x: float, y: float, object_type: int = None) -> Optional[GameObject]:
        """Get nearest object to position"""
        nearest = None
        nearest_distance = float('inf')

        objects_to_check = (self.get_objects_by_type(object_type) 
                           if object_type is not None 
                           else self.objects.values())

        for obj in objects_to_check:
            if not obj.is_object_active():
                continue

            distance = obj.distance_to_position(x, y)
            if distance < nearest_distance:
                nearest_distance = distance
                nearest = obj

        return nearest

    def find_collisions(self, obj: GameObject) -> List[GameObject]:
        """Find all objects colliding with given object"""
        if not obj.can_object_collide():
            return []

        collisions = []
        nearby_objects = self.get_objects_in_radius(obj.x, obj.y, obj.collision_radius * 2)

        for other in nearby_objects:
            if other.object_id != obj.object_id and obj.is_colliding_with(other):
                collisions.append(other)

        return collisions

    def update(self, delta_time: float) -> None:
        """Update all game objects"""
        # Update objects
        for obj_id in list(self.active_objects):
            if obj_id not in self.objects:
                continue

            obj = self.objects[obj_id]

            # Update spatial grid position
            old_cell = self._get_grid_cell(obj.x, obj.y)

            # Update object
            obj.update(delta_time)

            # Call update callbacks
            for callback in self.update_callbacks:
                callback(obj, delta_time)

            # Update spatial grid if position changed
            new_cell = self._get_grid_cell(obj.x, obj.y)
            if old_cell != new_cell:
                self._update_spatial_grid(obj, old_cell, new_cell)

            # Mark for removal if dead
            if not obj.is_object_alive():
                self.objects_to_remove.add(obj_id)

        # Remove dead objects
        for obj_id in self.objects_to_remove:
            self.remove_object(obj_id)
        self.objects_to_remove.clear()

    def clear(self) -> None:
        """Clear all objects"""
        self.objects.clear()
        self.active_objects.clear()
        self.objects_to_remove.clear()
        self.objects_by_type.clear()
        self.spatial_grid.clear()
        GameObjectFactory.reset_object_ids()

    def get_object_count(self) -> int:
        """Get total number of objects"""
        return len(self.objects)

    def get_active_object_count(self) -> int:
        """Get number of active objects"""
        return len(self.active_objects)

    def add_update_callback(self, callback: Callable[[GameObject, float], None]) -> None:
        """Add update callback"""
        self.update_callbacks.append(callback)

    def remove_update_callback(self, callback: Callable[[GameObject, float], None]) -> None:
        """Remove update callback"""
        if callback in self.update_callbacks:
            self.update_callbacks.remove(callback)

    def _get_grid_cell(self, x: float, y: float) -> tuple:
        """Get spatial grid cell for position"""
        cell_x = int(x // self.grid_size)
        cell_y = int(y // self.grid_size)
        return (cell_x, cell_y)

    def _add_to_spatial_grid(self, obj: GameObject) -> None:
        """Add object to spatial grid"""
        cell = self._get_grid_cell(obj.x, obj.y)
        if cell not in self.spatial_grid:
            self.spatial_grid[cell] = set()
        self.spatial_grid[cell].add(obj.object_id)

    def _remove_from_spatial_grid(self, obj: GameObject) -> None:
        """Remove object from spatial grid"""
        cell = self._get_grid_cell(obj.x, obj.y)
        if cell in self.spatial_grid:
            self.spatial_grid[cell].discard(obj.object_id)
            if not self.spatial_grid[cell]:
                del self.spatial_grid[cell]

    def _update_spatial_grid(self, obj: GameObject, old_cell: tuple, new_cell: tuple) -> None:
        """Update object position in spatial grid"""
        # Remove from old cell
        if old_cell in self.spatial_grid:
            self.spatial_grid[old_cell].discard(obj.object_id)
            if not self.spatial_grid[old_cell]:
                del self.spatial_grid[old_cell]

        # Add to new cell
        if new_cell not in self.spatial_grid:
            self.spatial_grid[new_cell] = set()
        self.spatial_grid[new_cell].add(obj.object_id)

    def _get_grid_cells_in_radius(self, x: float, y: float, radius: float) -> List[tuple]:
        """Get grid cells within radius"""
        cells = []
        cell_radius = int((radius / self.grid_size) + 1)
        center_x = int(x // self.grid_size)
        center_y = int(y // self.grid_size)

        for dx in range(-cell_radius, cell_radius + 1):
            for dy in range(-cell_radius, cell_radius + 1):
                cells.append((center_x + dx, center_y + dy))

        return cells

    def get_statistics(self) -> Dict[str, int]:
        """Get manager statistics"""
        return {
            'total_objects': len(self.objects),
            'active_objects': len(self.active_objects),
            'objects_created': self.total_objects_created,
            'objects_destroyed': self.total_objects_destroyed,
            'spatial_grid_cells': len(self.spatial_grid)
        }
