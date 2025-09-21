"""
Python conversion of Supercell.Laser.Logic.Data.BossData.cs
Boss data class for PvE boss encounters
"""

from .data_tables import LogicData

class BossData(LogicData):
    """Boss data class for PvE boss encounters"""

    def __init__(self):
        """Initialize boss data"""
        super().__init__()
        self.name = ""
        self.tid = ""  # Text ID for localization
        self.player_count = 1
        self.required_campaign_progress_to_unlock = 0
        self.location = ""
        self.allowed_heroes = ""
        self.reward = ""
        self.level_generation_seed = 0
        self.map = ""
        self.boss = ""
        self.boss_level = 1

    def get_name(self) -> str:
        """Get boss name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set boss name"""
        self.name = name

    def get_text_id(self) -> str:
        """Get text ID for localization"""
        return self.tid

    def set_text_id(self, tid: str) -> None:
        """Set text ID"""
        self.tid = tid

    def get_player_count(self) -> int:
        """Get required player count"""
        return self.player_count

    def set_player_count(self, count: int) -> None:
        """Set required player count"""
        self.player_count = max(1, count)

    def get_required_progress(self) -> int:
        """Get required campaign progress to unlock"""
        return self.required_campaign_progress_to_unlock

    def set_required_progress(self, progress: int) -> None:
        """Set required campaign progress"""
        self.required_campaign_progress_to_unlock = max(0, progress)

    def get_location(self) -> str:
        """Get boss location"""
        return self.location

    def set_location(self, location: str) -> None:
        """Set boss location"""
        self.location = location

    def get_allowed_heroes(self) -> str:
        """Get allowed heroes"""
        return self.allowed_heroes

    def set_allowed_heroes(self, heroes: str) -> None:
        """Set allowed heroes"""
        self.allowed_heroes = heroes

    def get_reward(self) -> str:
        """Get boss reward"""
        return self.reward

    def set_reward(self, reward: str) -> None:
        """Set boss reward"""
        self.reward = reward

    def get_level_generation_seed(self) -> int:
        """Get level generation seed"""
        return self.level_generation_seed

    def set_level_generation_seed(self, seed: int) -> None:
        """Set level generation seed"""
        self.level_generation_seed = seed

    def get_map(self) -> str:
        """Get boss map"""
        return self.map

    def set_map(self, map_name: str) -> None:
        """Set boss map"""
        self.map = map_name

    def get_boss(self) -> str:
        """Get boss character"""
        return self.boss

    def set_boss(self, boss: str) -> None:
        """Set boss character"""
        self.boss = boss

    def get_boss_level(self) -> int:
        """Get boss level"""
        return self.boss_level

    def set_boss_level(self, level: int) -> None:
        """Set boss level"""
        self.boss_level = max(1, level)

    def is_unlocked(self, campaign_progress: int) -> bool:
        """Check if boss is unlocked"""
        return campaign_progress >= self.required_campaign_progress_to_unlock

    def is_multiplayer(self) -> bool:
        """Check if boss encounter requires multiple players"""
        return self.player_count > 1

    def has_hero_restrictions(self) -> bool:
        """Check if boss has hero restrictions"""
        return self.allowed_heroes != ""

    def has_reward(self) -> bool:
        """Check if boss gives reward"""
        return self.reward != ""

    def parse_allowed_heroes(self) -> list:
        """Parse allowed heroes string into list"""
        if not self.allowed_heroes:
            return []
        return [hero.strip() for hero in self.allowed_heroes.split(',')]

    def is_hero_allowed(self, hero_name: str) -> bool:
        """Check if specific hero is allowed"""
        if not self.has_hero_restrictions():
            return True
        return hero_name in self.parse_allowed_heroes()

    def __str__(self) -> str:
        """String representation"""
        return (f"BossData('{self.name}', boss='{self.boss}', "
                f"level={self.boss_level}, players={self.player_count})")
