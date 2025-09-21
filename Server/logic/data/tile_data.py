"""
Python conversion of Supercell.Laser.Logic.Data.TileData.cs
Tile data class for map tiles
"""

from .data_tables import LogicData

class TileData(LogicData):
    """Tile data class for map tiles"""

    def __init__(self):
        """Initialize tile data"""
        super().__init__()
        self.name = ""
        self.type = ""
        self.destructible = False
        self.blocks_movement = False
        self.blocks_projectiles = False
        self.spawnable = False
        self.health = 0
        self.width = 1
        self.height = 1
        self.spawn_angle = 0

        # Visual properties
        self.file_name = ""
        self.export_name = ""
        self.animation_frames = 1
        self.collision_radius = 0

    def get_name(self) -> str:
        """Get tile name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set tile name"""
        self.name = name

    def get_type(self) -> str:
        """Get tile type"""
        return self.type

    def set_type(self, tile_type: str) -> None:
        """Set tile type"""
        self.type = tile_type

    def is_destructible(self) -> bool:
        """Check if tile is destructible"""
        return self.destructible

    def set_destructible(self, destructible: bool) -> None:
        """Set destructible status"""
        self.destructible = destructible

    def blocks_movement(self) -> bool:
        """Check if tile blocks movement"""
        return self.blocks_movement

    def blocks_projectiles(self) -> bool:
        """Check if tile blocks projectiles"""
        return self.blocks_projectiles

    def is_spawnable(self) -> bool:
        """Check if characters can spawn on tile"""
        return self.spawnable

    def get_health(self) -> int:
        """Get tile health"""
        return self.health

    def set_health(self, health: int) -> None:
        """Set tile health"""
        self.health = max(0, health)

    def get_size(self) -> tuple:
        """Get tile size"""
        return (self.width, self.height)

    def set_size(self, width: int, height: int) -> None:
        """Set tile size"""
        self.width = max(1, width)
        self.height = max(1, height)

    def is_solid(self) -> bool:
        """Check if tile is solid (blocks movement and projectiles)"""
        return self.blocks_movement and self.blocks_projectiles

    def __str__(self) -> str:
        """String representation"""
        return f"TileData('{self.name}', type='{self.type}', size={self.width}x{self.height})"
