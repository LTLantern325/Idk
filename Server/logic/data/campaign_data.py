"""
Python conversion of Supercell.Laser.Logic.Data.CampaignData.cs
Campaign data class for PvE campaign levels
"""

from .data_tables import LogicData

class CampaignData(LogicData):
    """Campaign data class for PvE campaign levels"""

    def __init__(self):
        """Initialize campaign data"""
        super().__init__()
        self.name = ""
        self.tid = ""  # Text ID for localization
        self.location = ""
        self.allowed_heroes = ""
        self.reward = ""
        self.level_generation_seed = 0
        self.map = ""

        # Enemy configuration
        self.enemies = ""
        self.enemy_level = 1

        # Boss configuration
        self.boss = ""
        self.boss_level = 1

        # Base configuration
        self.base = ""
        self.num_bases = 0
        self.base_level = 1

        # Tower configuration
        self.tower = ""
        self.num_towers = 0
        self.tower_level = 1

        # Requirements
        self.required_stars = 0

    def get_name(self) -> str:
        """Get campaign name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set campaign name"""
        self.name = name

    def get_text_id(self) -> str:
        """Get text ID"""
        return self.tid

    def set_text_id(self, tid: str) -> None:
        """Set text ID"""
        self.tid = tid

    def get_location(self) -> str:
        """Get campaign location"""
        return self.location

    def set_location(self, location: str) -> None:
        """Set campaign location"""
        self.location = location

    def get_map(self) -> str:
        """Get campaign map"""
        return self.map

    def set_map(self, map_name: str) -> None:
        """Set campaign map"""
        self.map = map_name

    def get_enemies(self) -> str:
        """Get enemy configuration"""
        return self.enemies

    def set_enemies(self, enemies: str) -> None:
        """Set enemy configuration"""
        self.enemies = enemies

    def get_enemy_level(self) -> int:
        """Get enemy level"""
        return self.enemy_level

    def set_enemy_level(self, level: int) -> None:
        """Set enemy level"""
        self.enemy_level = max(1, level)

    def get_boss(self) -> str:
        """Get boss configuration"""
        return self.boss

    def set_boss(self, boss: str) -> None:
        """Set boss configuration"""
        self.boss = boss

    def get_boss_level(self) -> int:
        """Get boss level"""
        return self.boss_level

    def set_boss_level(self, level: int) -> None:
        """Set boss level"""
        self.boss_level = max(1, level)

    def get_num_bases(self) -> int:
        """Get number of bases"""
        return self.num_bases

    def set_num_bases(self, count: int) -> None:
        """Set number of bases"""
        self.num_bases = max(0, count)

    def get_base_level(self) -> int:
        """Get base level"""
        return self.base_level

    def set_base_level(self, level: int) -> None:
        """Set base level"""
        self.base_level = max(1, level)

    def get_num_towers(self) -> int:
        """Get number of towers"""
        return self.num_towers

    def set_num_towers(self, count: int) -> None:
        """Set number of towers"""
        self.num_towers = max(0, count)

    def get_tower_level(self) -> int:
        """Get tower level"""
        return self.tower_level

    def set_tower_level(self, level: int) -> None:
        """Set tower level"""
        self.tower_level = max(1, level)

    def get_required_stars(self) -> int:
        """Get required stars to unlock"""
        return self.required_stars

    def set_required_stars(self, stars: int) -> None:
        """Set required stars"""
        self.required_stars = max(0, stars)

    def has_enemies(self) -> bool:
        """Check if campaign has enemies"""
        return self.enemies != ""

    def has_boss(self) -> bool:
        """Check if campaign has boss"""
        return self.boss != ""

    def has_bases(self) -> bool:
        """Check if campaign has bases"""
        return self.num_bases > 0 and self.base != ""

    def has_towers(self) -> bool:
        """Check if campaign has towers"""
        return self.num_towers > 0 and self.tower != ""

    def has_hero_restrictions(self) -> bool:
        """Check if campaign has hero restrictions"""
        return self.allowed_heroes != ""

    def has_reward(self) -> bool:
        """Check if campaign has reward"""
        return self.reward != ""

    def is_unlocked(self, player_stars: int) -> bool:
        """Check if campaign is unlocked"""
        return player_stars >= self.required_stars

    def parse_allowed_heroes(self) -> list:
        """Parse allowed heroes string into list"""
        if not self.allowed_heroes:
            return []
        return [hero.strip() for hero in self.allowed_heroes.split(',')]

    def parse_enemies(self) -> list:
        """Parse enemies string into list"""
        if not self.enemies:
            return []
        return [enemy.strip() for enemy in self.enemies.split(',')]

    def get_total_structures(self) -> int:
        """Get total number of structures (bases + towers)"""
        return self.num_bases + self.num_towers

    def get_difficulty_estimate(self) -> int:
        """Get rough difficulty estimate based on levels and structures"""
        base_difficulty = max(self.enemy_level, self.boss_level)
        structure_bonus = (self.num_bases * self.base_level + 
                          self.num_towers * self.tower_level) // 5
        return base_difficulty + structure_bonus

    def __str__(self) -> str:
        """String representation"""
        return (f"CampaignData('{self.name}', stars_req={self.required_stars}, "
                f"enemy_lvl={self.enemy_level}, bases={self.num_bases})")
