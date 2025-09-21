"""
Python conversion of Supercell.Laser.Logic.Data.MilestoneData.cs
Milestone data class for achievements and progress
"""

from .data_tables import LogicData

class MilestoneData(LogicData):
    """Milestone data class for achievements"""

    def __init__(self):
        """Initialize milestone data"""
        super().__init__()
        self.name = ""
        self.type = 0
        self.index = 0
        self.progress_start = 0
        self.progress = 0
        self.league = 0
        self.tier = 0
        self.season = 0

        # Primary reward
        self.primary_lvl_up_reward_type = 0
        self.primary_lvl_up_reward_count = 0
        self.primary_lvl_up_reward_extra_data = 0
        self.primary_lvl_up_reward_data = ""

        # Secondary reward
        self.secondary_lvl_up_reward_type = 0
        self.secondary_lvl_up_reward_count = 0
        self.secondary_lvl_up_reward_extra_data = 0
        self.secondary_lvl_up_reward_data = ""

    def get_name(self) -> str:
        """Get milestone name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set milestone name"""
        self.name = name

    def get_type(self) -> int:
        """Get milestone type"""
        return self.type

    def set_type(self, milestone_type: int) -> None:
        """Set milestone type"""
        self.type = milestone_type

    def get_required_progress(self) -> int:
        """Get required progress to complete"""
        return self.progress

    def set_required_progress(self, progress: int) -> None:
        """Set required progress"""
        self.progress = max(0, progress)

    def get_progress_start(self) -> int:
        """Get starting progress"""
        return self.progress_start

    def set_progress_start(self, start: int) -> None:
        """Set starting progress"""
        self.progress_start = max(0, start)

    def get_league(self) -> int:
        """Get league requirement"""
        return self.league

    def set_league(self, league: int) -> None:
        """Set league requirement"""
        self.league = league

    def get_tier(self) -> int:
        """Get tier"""
        return self.tier

    def set_tier(self, tier: int) -> None:
        """Set tier"""
        self.tier = tier

    def get_season(self) -> int:
        """Get season"""
        return self.season

    def set_season(self, season: int) -> None:
        """Set season"""
        self.season = season

    def has_primary_reward(self) -> bool:
        """Check if milestone has primary reward"""
        return self.primary_lvl_up_reward_type > 0 and self.primary_lvl_up_reward_count > 0

    def has_secondary_reward(self) -> bool:
        """Check if milestone has secondary reward"""
        return self.secondary_lvl_up_reward_type > 0 and self.secondary_lvl_up_reward_count > 0

    def get_primary_reward_info(self) -> tuple:
        """Get primary reward information"""
        return (self.primary_lvl_up_reward_type, self.primary_lvl_up_reward_count,
                self.primary_lvl_up_reward_extra_data, self.primary_lvl_up_reward_data)

    def get_secondary_reward_info(self) -> tuple:
        """Get secondary reward information"""
        return (self.secondary_lvl_up_reward_type, self.secondary_lvl_up_reward_count,
                self.secondary_lvl_up_reward_extra_data, self.secondary_lvl_up_reward_data)

    def is_completed(self, current_progress: int) -> bool:
        """Check if milestone is completed"""
        return current_progress >= self.progress

    def get_completion_percentage(self, current_progress: int) -> float:
        """Get completion percentage"""
        if self.progress == 0:
            return 100.0

        progress_made = max(0, current_progress - self.progress_start)
        total_required = self.progress - self.progress_start

        if total_required <= 0:
            return 100.0

        return min(100.0, (progress_made / total_required) * 100.0)

    def __str__(self) -> str:
        """String representation"""
        return (f"MilestoneData('{self.name}', type={self.type}, "
                f"progress={self.progress}, tier={self.tier})")
