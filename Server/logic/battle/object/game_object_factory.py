"""
Python conversion of Supercell.Laser.Logic.Battle.Objects.GameObjectFactory.cs
Factory class for creating game objects
"""

from typing import Dict, Optional, Type, Any
from .game_object import GameObject
from .character import Character
from .projectile import Projectile
from .area_effect import AreaEffect
from .item import Item

class GameObjectType:
    """Game object types"""
    UNKNOWN = 0
    CHARACTER = 1
    PROJECTILE = 2
    AREA_EFFECT = 3
    ITEM = 4
    OBSTACLE = 5
    POWER_UP = 6

class GameObjectFactory:
    """Factory class for creating game objects"""

    _object_types: Dict[int, Type[GameObject]] = {}
    _next_object_id = 1

    @classmethod
    def initialize(cls) -> None:
        """Initialize factory with object types"""
        cls._object_types = {
            GameObjectType.CHARACTER: Character,
            GameObjectType.PROJECTILE: Projectile,
            GameObjectType.AREA_EFFECT: AreaEffect,
            GameObjectType.ITEM: Item,
            GameObjectType.OBSTACLE: GameObject,  # Basic game object
            GameObjectType.POWER_UP: Item
        }

    @classmethod
    def create_object(cls, object_type: int, data_id: int = 0) -> Optional[GameObject]:
        """Create game object of specified type"""
        if object_type not in cls._object_types:
            return None

        object_class = cls._object_types[object_type]
        obj = object_class()
        obj.object_id = cls._get_next_object_id()
        obj.object_type = object_type
        obj.data_id = data_id

        return obj

    @classmethod
    def create_character(cls, character_data_id: int, level: int = 1) -> Optional[Character]:
        """Create character with specific data and level"""
        character = cls.create_object(GameObjectType.CHARACTER, character_data_id)
        if isinstance(character, Character):
            character.set_character_data_id(character_data_id)
            character.set_level(level)
            return character
        return None

    @classmethod
    def create_projectile(cls, projectile_data_id: int, owner_id: int = 0) -> Optional[Projectile]:
        """Create projectile with specific data"""
        projectile = cls.create_object(GameObjectType.PROJECTILE, projectile_data_id)
        if isinstance(projectile, Projectile):
            projectile.set_projectile_data_id(projectile_data_id)
            projectile.set_owner_id(owner_id)
            return projectile
        return None

    @classmethod
    def create_area_effect(cls, effect_type: int, radius: float = 100.0, strength: float = 1.0) -> Optional[AreaEffect]:
        """Create area effect with specific parameters"""
        effect = cls.create_object(GameObjectType.AREA_EFFECT)
        if isinstance(effect, AreaEffect):
            effect.set_effect_type(effect_type)
            effect.set_radius(radius)
            effect.set_strength(strength)
            return effect
        return None

    @classmethod
    def create_item(cls, item_data_id: int, amount: int = 1) -> Optional[Item]:
        """Create item with specific data"""
        item = cls.create_object(GameObjectType.ITEM, item_data_id)
        if isinstance(item, Item):
            item.set_item_data_id(item_data_id)
            item.set_amount(amount)
            return item
        return None

    @classmethod
    def create_power_up(cls, power_up_type: int) -> Optional[Item]:
        """Create power-up item"""
        power_up = cls.create_object(GameObjectType.POWER_UP, power_up_type)
        if isinstance(power_up, Item):
            power_up.set_item_data_id(power_up_type)
            power_up.set_is_power_up(True)
            return power_up
        return None

    @classmethod
    def create_obstacle(cls, x: float, y: float, radius: float = 50.0) -> GameObject:
        """Create obstacle at position"""
        obstacle = cls.create_object(GameObjectType.OBSTACLE)
        if obstacle:
            obstacle.set_position(x, y)
            obstacle.set_collision_radius(radius)
            obstacle.is_solid = True
            obstacle.can_collide = True
        return obstacle

    @classmethod
    def create_from_template(cls, template: Dict[str, Any]) -> Optional[GameObject]:
        """Create object from template data"""
        object_type = template.get('type', GameObjectType.UNKNOWN)
        data_id = template.get('data_id', 0)

        obj = cls.create_object(object_type, data_id)
        if not obj:
            return None

        # Set common properties
        if 'x' in template:
            obj.x = float(template['x'])
        if 'y' in template:
            obj.y = float(template['y'])
        if 'rotation' in template:
            obj.rotation = float(template['rotation'])
        if 'scale' in template:
            scale = float(template['scale'])
            obj.set_uniform_scale(scale)

        # Set type-specific properties
        if isinstance(obj, Character) and 'level' in template:
            obj.set_level(int(template['level']))

        if isinstance(obj, Projectile):
            if 'damage' in template:
                obj.set_damage(int(template['damage']))
            if 'speed' in template:
                obj.set_speed(float(template['speed']))

        if isinstance(obj, AreaEffect):
            if 'radius' in template:
                obj.set_radius(float(template['radius']))
            if 'strength' in template:
                obj.set_strength(float(template['strength']))
            if 'duration' in template:
                obj.set_remaining_time(float(template['duration']))

        return obj

    @classmethod
    def clone_object(cls, original: GameObject) -> Optional[GameObject]:
        """Clone existing game object"""
        if not original:
            return None

        clone = cls.create_object(original.object_type, original.data_id)
        if not clone:
            return None

        # Copy basic properties
        clone.x = original.x
        clone.y = original.y
        clone.rotation = original.rotation
        clone.scale_x = original.scale_x
        clone.scale_y = original.scale_y
        clone.alpha = original.alpha
        clone.collision_radius = original.collision_radius
        clone.velocity_x = original.velocity_x
        clone.velocity_y = original.velocity_y

        return clone

    @classmethod
    def _get_next_object_id(cls) -> int:
        """Get next unique object ID"""
        object_id = cls._next_object_id
        cls._next_object_id += 1
        return object_id

    @classmethod
    def reset_object_ids(cls) -> None:
        """Reset object ID counter"""
        cls._next_object_id = 1

    @classmethod
    def get_object_type_name(cls, object_type: int) -> str:
        """Get human-readable object type name"""
        type_names = {
            GameObjectType.UNKNOWN: "Unknown",
            GameObjectType.CHARACTER: "Character",
            GameObjectType.PROJECTILE: "Projectile", 
            GameObjectType.AREA_EFFECT: "Area Effect",
            GameObjectType.ITEM: "Item",
            GameObjectType.OBSTACLE: "Obstacle",
            GameObjectType.POWER_UP: "Power Up"
        }
        return type_names.get(object_type, f"Type {object_type}")

    @classmethod
    def is_valid_object_type(cls, object_type: int) -> bool:
        """Check if object type is valid"""
        return object_type in cls._object_types

    @classmethod
    def get_supported_types(cls) -> Dict[int, str]:
        """Get all supported object types"""
        return {
            obj_type: cls.get_object_type_name(obj_type) 
            for obj_type in cls._object_types.keys()
        }

    @classmethod
    def register_object_type(cls, object_type: int, object_class: Type[GameObject]) -> None:
        """Register new object type"""
        cls._object_types[object_type] = object_class

# Initialize factory
GameObjectFactory.initialize()
