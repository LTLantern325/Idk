"""
Python conversion of Supercell.Laser.Logic.Battle.Level.Factory.TileMapFactory.cs
Factory class for creating tile maps
"""

from typing import Dict, List, Optional
from ..tile_map import TileMap
from ..tile import TileType

class TileMapFactory:
    """Factory class for creating tile maps"""

    @staticmethod
    def create_empty_map(width: int = 32, height: int = 24) -> TileMap:
        """Create empty tile map"""
        return TileMap(width, height)

    @staticmethod
    def create_gem_grab_map() -> TileMap:
        """Create Gem Grab map layout"""
        tile_map = TileMap(32, 24)

        # Add walls around the edges
        for x in range(32):
            tile_map.set_tile(x, 0, TileType.WALL)
            tile_map.set_tile(x, 23, TileType.WALL)
        for y in range(24):
            tile_map.set_tile(0, y, TileType.WALL)
            tile_map.set_tile(31, y, TileType.WALL)

        # Add center walls
        for x in range(13, 19):
            tile_map.set_tile(x, 11, TileType.WALL)
            tile_map.set_tile(x, 12, TileType.WALL)

        # Add spawn points
        tile_map.add_spawn_point(3, 3, 1)    # Team 1
        tile_map.add_spawn_point(3, 20, 1)   # Team 1  
        tile_map.add_spawn_point(28, 3, 2)   # Team 2
        tile_map.add_spawn_point(28, 20, 2)  # Team 2

        # Add some grass cover
        for x in range(5, 10):
            for y in range(8, 16):
                tile_map.set_tile(x, y, TileType.GRASS)
        for x in range(22, 27):
            for y in range(8, 16):
                tile_map.set_tile(x, y, TileType.GRASS)

        return tile_map

    @staticmethod
    def create_heist_map() -> TileMap:
        """Create Heist map layout"""
        tile_map = TileMap(32, 24)

        # Add walls around the edges
        for x in range(32):
            tile_map.set_tile(x, 0, TileType.WALL)
            tile_map.set_tile(x, 23, TileType.WALL)
        for y in range(24):
            tile_map.set_tile(0, y, TileType.WALL)
            tile_map.set_tile(31, y, TileType.WALL)

        # Add safe areas (goals)
        tile_map.set_tile(15, 3, TileType.GOAL)
        tile_map.set_tile(16, 3, TileType.GOAL)
        tile_map.set_tile(15, 20, TileType.GOAL)
        tile_map.set_tile(16, 20, TileType.GOAL)

        # Add spawn points
        tile_map.add_spawn_point(8, 2, 1)    # Team 1
        tile_map.add_spawn_point(23, 2, 1)   # Team 1
        tile_map.add_spawn_point(8, 21, 2)   # Team 2
        tile_map.add_spawn_point(23, 21, 2)  # Team 2

        # Add defensive walls
        for x in range(12, 20):
            tile_map.set_tile(x, 6, TileType.DESTRUCTIBLE)
            tile_map.set_tile(x, 17, TileType.DESTRUCTIBLE)

        return tile_map

    @staticmethod
    def create_bounty_map() -> TileMap:
        """Create Bounty map layout"""
        tile_map = TileMap(40, 32)  # Larger map for Bounty

        # Add walls around the edges
        for x in range(40):
            tile_map.set_tile(x, 0, TileType.WALL)
            tile_map.set_tile(x, 31, TileType.WALL)
        for y in range(32):
            tile_map.set_tile(0, y, TileType.WALL)
            tile_map.set_tile(39, y, TileType.WALL)

        # Add spawn points
        tile_map.add_spawn_point(5, 5, 1)    # Team 1
        tile_map.add_spawn_point(34, 26, 2)  # Team 2

        # Add cover obstacles
        for x in range(15, 25):
            for y in range(10, 22):
                if (x + y) % 3 == 0:
                    tile_map.set_tile(x, y, TileType.WALL)

        return tile_map

    @staticmethod
    def create_showdown_map() -> TileMap:
        """Create Showdown map layout"""
        tile_map = TileMap(48, 48)  # Large map for Showdown

        # Add walls around the edges
        for x in range(48):
            tile_map.set_tile(x, 0, TileType.WALL)
            tile_map.set_tile(x, 47, TileType.WALL)
        for y in range(48):
            tile_map.set_tile(0, y, TileType.WALL)
            tile_map.set_tile(47, y, TileType.WALL)

        # Add multiple spawn points
        spawn_positions = [
            (5, 5), (42, 5), (5, 42), (42, 42),
            (23, 5), (5, 23), (42, 23), (23, 42),
            (15, 15), (32, 32)
        ]

        for i, (x, y) in enumerate(spawn_positions):
            tile_map.add_spawn_point(x, y, i)

        # Add power-up boxes
        power_up_positions = [(12, 12), (35, 12), (12, 35), (35, 35), (23, 23)]
        for x, y in power_up_positions:
            tile_map.set_tile(x, y, TileType.POWER_UP)

        # Add scattered cover
        import random
        random.seed(42)  # For consistent generation
        for _ in range(100):
            x = random.randint(3, 44)
            y = random.randint(3, 44)
            if tile_map.get_tile(x, y).get_tile_type() == TileType.EMPTY:
                tile_map.set_tile(x, y, TileType.DESTRUCTIBLE)

        return tile_map

    @staticmethod
    def create_brawl_ball_map() -> TileMap:
        """Create Brawl Ball map layout"""
        tile_map = TileMap(32, 24)

        # Add walls around the edges
        for x in range(32):
            tile_map.set_tile(x, 0, TileType.WALL)
            tile_map.set_tile(x, 23, TileType.WALL)
        for y in range(24):
            tile_map.set_tile(0, y, TileType.WALL)
            tile_map.set_tile(31, y, TileType.WALL)

        # Add goals
        for x in range(14, 18):
            tile_map.set_tile(x, 1, TileType.GOAL)
            tile_map.set_tile(x, 22, TileType.GOAL)

        # Add spawn points
        tile_map.add_spawn_point(6, 11, 1)   # Team 1
        tile_map.add_spawn_point(25, 11, 2)  # Team 2

        # Add field obstacles
        obstacles = [(10, 8), (10, 15), (21, 8), (21, 15)]
        for x, y in obstacles:
            tile_map.set_tile(x, y, TileType.WALL)

        return tile_map

    @staticmethod
    def create_map_from_string(map_data: str) -> Optional[TileMap]:
        """Create map from string representation"""
        lines = map_data.strip().split('\n')
        if not lines:
            return None

        height = len(lines)
        width = len(lines[0]) if lines else 0

        tile_map = TileMap(width, height)

        tile_mapping = {
            '.': TileType.EMPTY,
            '#': TileType.WALL,
            'g': TileType.GRASS,
            'w': TileType.WATER,
            's': TileType.SPAWN,
            'G': TileType.GOAL,
            'P': TileType.POWER_UP,
            'D': TileType.DESTRUCTIBLE
        }

        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if x < width and char in tile_mapping:
                    tile_map.set_tile(x, y, tile_mapping[char])

        return tile_map

    @staticmethod
    def get_available_maps() -> Dict[str, str]:
        """Get list of available map types"""
        return {
            "empty": "Empty Map",
            "gem_grab": "Gem Grab",
            "heist": "Heist",
            "bounty": "Bounty",
            "showdown": "Showdown",
            "brawl_ball": "Brawl Ball"
        }

    @staticmethod
    def create_map_by_name(map_name: str) -> Optional[TileMap]:
        """Create map by name"""
        map_creators = {
            "empty": TileMapFactory.create_empty_map,
            "gem_grab": TileMapFactory.create_gem_grab_map,
            "heist": TileMapFactory.create_heist_map,
            "bounty": TileMapFactory.create_bounty_map,
            "showdown": TileMapFactory.create_showdown_map,
            "brawl_ball": TileMapFactory.create_brawl_ball_map
        }

        creator = map_creators.get(map_name.lower())
        return creator() if creator else None
