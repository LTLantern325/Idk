"""
Python conversion of Supercell.Laser.Logic.Data.LocationThemeData.cs
Location theme data class for map visual themes (simplified version due to complexity)
"""

from .data_tables import LogicData

class LocationThemeData(LogicData):
    """Location theme data class for map visual themes"""

    def __init__(self):
        """Initialize location theme data"""
        super().__init__()
        self.name = ""
        self.tile_set_prefix = ""

        # Environment assets
        self.masked_environment_scw = ""

        # Blocking elements (4 types)
        self.blocking1_scw = ""
        self.blocking1_mesh = ""
        self.blocking1_angle_step = 0
        self.blocking2_scw = ""
        self.blocking2_mesh = ""
        self.blocking2_angle_step = 0
        self.blocking3_scw = ""
        self.blocking3_mesh = ""
        self.blocking3_angle_step = 0
        self.blocking4_scw = ""
        self.blocking4_mesh = ""
        self.blocking4_angle_step = 0

        # Respawning elements
        self.respawning_wall_scw = ""
        self.respawning_wall_mesh = ""
        self.respawning_wall_angle_step = 0
        self.respawning_forest_scw = ""
        self.forest_scw = ""

        # Destructible elements
        self.destructable_scw = ""
        self.destructable_mesh = ""
        self.destructable_angle_step = 0
        self.destructable_scw_cn = ""  # China variant
        self.destructable_mesh_cn = ""
        self.destructable_angle_step_cn = 0

        # Fragile elements
        self.fragile_scw = ""
        self.fragile_mesh = ""
        self.fragile_angle_step = 0
        self.fragile_scw_cn = ""  # China variant
        self.fragile_mesh_cn = ""
        self.fragile_angle_step_cn = 0

        # Other elements
        self.water_tile_scw = ""
        self.fence_scw = ""
        self.indestructible_scw = ""
        self.indestructible_mesh = ""
        self.bench_scw = ""

        # Game object overrides
        self.laser_ball_skin_override = ""
        self.mine_gem_spawn_scw_override = ""
        self.loot_box_skin_override = ""
        self.showdown_boost_scw_override = ""

        # Map preview colors
        self.map_preview_bg_color_red = 0
        self.map_preview_bg_color_green = 0
        self.map_preview_bg_color_blue = 0

        # Map preview elements
        self.map_preview_gem_grab_spawn_hole_export_name = ""
        self.map_preview_ball_export_name = ""
        self.map_preview_goal1_export_name = ""
        self.map_preview_goal2_export_name = ""
        self.map_preview_cn_overrides = ""

    def get_name(self) -> str:
        """Get theme name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set theme name"""
        self.name = name

    def get_tile_set_prefix(self) -> str:
        """Get tile set prefix"""
        return self.tile_set_prefix

    def set_tile_set_prefix(self, prefix: str) -> None:
        """Set tile set prefix"""
        self.tile_set_prefix = prefix

    def has_destructible_elements(self) -> bool:
        """Check if theme has destructible elements"""
        return self.destructable_scw != ""

    def has_fragile_elements(self) -> bool:
        """Check if theme has fragile elements"""
        return self.fragile_scw != ""

    def has_china_variants(self) -> bool:
        """Check if theme has China-specific variants"""
        return (self.destructable_scw_cn != "" or self.fragile_scw_cn != "" or 
                self.map_preview_cn_overrides != "")

    def has_water_elements(self) -> bool:
        """Check if theme has water elements"""
        return self.water_tile_scw != ""

    def has_game_object_overrides(self) -> bool:
        """Check if theme has game object overrides"""
        return (self.laser_ball_skin_override != "" or 
                self.mine_gem_spawn_scw_override != "" or
                self.loot_box_skin_override != "" or
                self.showdown_boost_scw_override != "")

    def get_background_color(self) -> tuple:
        """Get background color as RGB tuple"""
        return (self.map_preview_bg_color_red, 
                self.map_preview_bg_color_green, 
                self.map_preview_bg_color_blue)

    def set_background_color(self, red: int, green: int, blue: int) -> None:
        """Set background color"""
        self.map_preview_bg_color_red = max(0, min(255, red))
        self.map_preview_bg_color_green = max(0, min(255, green))
        self.map_preview_bg_color_blue = max(0, min(255, blue))

    def has_blocking_elements(self) -> bool:
        """Check if theme has blocking elements"""
        return (self.blocking1_scw != "" or self.blocking2_scw != "" or 
                self.blocking3_scw != "" or self.blocking4_scw != "")

    def has_forest_elements(self) -> bool:
        """Check if theme has forest elements"""
        return self.forest_scw != "" or self.respawning_forest_scw != ""

    def count_blocking_types(self) -> int:
        """Count number of blocking element types"""
        count = 0
        for scw in [self.blocking1_scw, self.blocking2_scw, 
                   self.blocking3_scw, self.blocking4_scw]:
            if scw != "":
                count += 1
        return count

    def __str__(self) -> str:
        """String representation"""
        china_support = " (CN)" if self.has_china_variants() else ""
        return f"LocationThemeData('{self.name}'{china_support})"
