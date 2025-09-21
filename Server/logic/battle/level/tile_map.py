"""
Python conversion of Supercell.Laser.Logic.Battle.Level.TileMap.cs
Tile map class for battle level management
"""

from typing import List, Tuple, Optional, Set
from .tile import Tile, TileType

class TileMap:
    """Tile map class for battle level management"""

    def __init__(self, width: int = 32, height: int = 24):
        """Initialize tile map"""
        self.width = width
        self.height = height
        self.tiles = []  # 2D array of tiles
        self.spawn_points = {}  # Dict[team_id, List[Tile]]

        # Initialize tiles
        self._initialize_tiles()

    def _initialize_tiles(self) -> None:
        """Initialize tiles grid"""
        self.tiles = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                tile = Tile(x, y, TileType.EMPTY)
                row.append(tile)
            self.tiles.append(row)

    def get_width(self) -> int:
        """Get map width"""
        return self.width

    def get_height(self) -> int:
        """Get map height"""
        return self.height

    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        """Get tile at position"""
        if not self.is_valid_position(x, y):
            return None
        return self.tiles[y][x]

    def set_tile(self, x: int, y: int, tile_type: TileType) -> bool:
        """Set tile type at position"""
        if not self.is_valid_position(x, y):
            return False

        tile = self.tiles[y][x]
        old_type = tile.get_tile_type()
        tile.set_tile_type(tile_type)

        # Update spawn points if needed
        if old_type == TileType.SPAWN:
            self._remove_spawn_point(tile)
        if tile_type == TileType.SPAWN:
            self._add_spawn_point(tile)

        return True

    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if position is valid"""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_walkable(self, x: int, y: int) -> bool:
        """Check if position is walkable"""
        tile = self.get_tile(x, y)
        return tile is not None and tile.is_tile_walkable()

    def blocks_vision(self, x: int, y: int) -> bool:
        """Check if position blocks vision"""
        tile = self.get_tile(x, y)
        return tile is not None and tile.blocks_vision()

    def blocks_projectiles(self, x: int, y: int) -> bool:
        """Check if position blocks projectiles"""
        tile = self.get_tile(x, y)
        return tile is not None and tile.blocks_projectiles()

    def get_movement_speed_modifier(self, x: int, y: int) -> float:
        """Get movement speed modifier at position"""
        tile = self.get_tile(x, y)
        return tile.get_movement_speed_modifier() if tile else 1.0

    def _add_spawn_point(self, tile: Tile) -> None:
        """Add spawn point"""
        team_id = tile.get_team_id()
        if team_id not in self.spawn_points:
            self.spawn_points[team_id] = []
        self.spawn_points[team_id].append(tile)

    def _remove_spawn_point(self, tile: Tile) -> None:
        """Remove spawn point"""
        team_id = tile.get_team_id()
        if team_id in self.spawn_points and tile in self.spawn_points[team_id]:
            self.spawn_points[team_id].remove(tile)

    def get_spawn_points(self, team_id: int) -> List[Tile]:
        """Get spawn points for team"""
        return self.spawn_points.get(team_id, [])

    def add_spawn_point(self, x: int, y: int, team_id: int) -> bool:
        """Add spawn point for team"""
        if not self.is_valid_position(x, y):
            return False

        tile = self.get_tile(x, y)
        if tile:
            tile.set_tile_type(TileType.SPAWN)
            tile.set_team_id(team_id)
            self._add_spawn_point(tile)
            return True
        return False

    def find_path(self, start_x: int, start_y: int, end_x: int, end_y: int) -> List[Tuple[int, int]]:
        """Find path between two points using A* algorithm"""
        if not self.is_valid_position(start_x, start_y) or not self.is_valid_position(end_x, end_y):
            return []

        if not self.is_walkable(end_x, end_y):
            return []

        # Simple pathfinding implementation (placeholder)
        # In a real implementation, you would use A* or similar algorithm
        path = []
        current_x, current_y = start_x, start_y

        while current_x != end_x or current_y != end_y:
            # Move towards target
            if current_x < end_x:
                current_x += 1
            elif current_x > end_x:
                current_x -= 1

            if current_y < end_y:
                current_y += 1
            elif current_y > end_y:
                current_y -= 1

            if self.is_walkable(current_x, current_y):
                path.append((current_x, current_y))
            else:
                break  # Path blocked

        return path

    def get_neighbors(self, x: int, y: int, include_diagonal: bool = False) -> List[Tile]:
        """Get neighboring tiles"""
        neighbors = []

        # Orthogonal neighbors
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        # Add diagonal neighbors
        if include_diagonal:
            directions.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            tile = self.get_tile(nx, ny)
            if tile:
                neighbors.append(tile)

        return neighbors

    def get_walkable_neighbors(self, x: int, y: int, include_diagonal: bool = False) -> List[Tile]:
        """Get walkable neighboring tiles"""
        neighbors = self.get_neighbors(x, y, include_diagonal)
        return [tile for tile in neighbors if tile.is_tile_walkable()]

    def flood_fill(self, start_x: int, start_y: int, new_type: TileType) -> int:
        """Flood fill area with new tile type"""
        if not self.is_valid_position(start_x, start_y):
            return 0

        start_tile = self.get_tile(start_x, start_y)
        if not start_tile:
            return 0

        old_type = start_tile.get_tile_type()
        if old_type == new_type:
            return 0

        # Flood fill implementation
        queue = [(start_x, start_y)]
        visited = set()
        changed_count = 0

        while queue:
            x, y = queue.pop(0)
            if (x, y) in visited:
                continue

            tile = self.get_tile(x, y)
            if not tile or tile.get_tile_type() != old_type:
                continue

            visited.add((x, y))
            tile.set_tile_type(new_type)
            changed_count += 1

            # Add neighbors
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if self.is_valid_position(nx, ny) and (nx, ny) not in visited:
                    queue.append((nx, ny))

        return changed_count

    def clear_map(self) -> None:
        """Clear all tiles to empty"""
        for y in range(self.height):
            for x in range(self.width):
                self.tiles[y][x].set_tile_type(TileType.EMPTY)
        self.spawn_points.clear()

    def count_tiles_of_type(self, tile_type: TileType) -> int:
        """Count tiles of specific type"""
        count = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.tiles[y][x].get_tile_type() == tile_type:
                    count += 1
        return count

    def get_all_tiles_of_type(self, tile_type: TileType) -> List[Tile]:
        """Get all tiles of specific type"""
        tiles = []
        for y in range(self.height):
            for x in range(self.width):
                tile = self.tiles[y][x]
                if tile.get_tile_type() == tile_type:
                    tiles.append(tile)
        return tiles

    def encode(self, stream) -> None:
        """Encode tile map to stream"""
        stream.write_v_int(self.width)
        stream.write_v_int(self.height)

        for y in range(self.height):
            for x in range(self.width):
                self.tiles[y][x].encode(stream)

    def decode(self, stream) -> None:
        """Decode tile map from stream"""
        self.width = stream.read_v_int()
        self.height = stream.read_v_int()

        self._initialize_tiles()

        for y in range(self.height):
            for x in range(self.width):
                self.tiles[y][x].decode(stream)

                # Update spawn points
                tile = self.tiles[y][x]
                if tile.get_tile_type() == TileType.SPAWN:
                    self._add_spawn_point(tile)

    def __str__(self) -> str:
        """String representation"""
        return f"TileMap({self.width}x{self.height})"
