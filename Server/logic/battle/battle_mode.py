"""
Python conversion of Supercell.Laser.Logic.Battle.BattleMode.cs
Battle mode enumeration and utilities
"""

from enum import IntEnum
from typing import Dict, Optional

class BattleModeType(IntEnum):
    """Battle mode types"""
    GEM_GRAB = 0
    SHOWDOWN = 1
    BOUNTY = 2
    HEIST = 3
    BRAWL_BALL = 4
    SIEGE = 5
    HOT_ZONE = 6
    KNOCKOUT = 7
    BASKET_BRAWL = 8
    HOLD_THE_TROPHY = 9
    TROPHY_THIEVES = 10
    DUELS = 11
    WIPE_OUT = 12

class BattleMode:
    """Battle mode management class"""

    MODE_NAMES = {
        BattleModeType.GEM_GRAB: "Gem Grab",
        BattleModeType.SHOWDOWN: "Showdown", 
        BattleModeType.BOUNTY: "Bounty",
        BattleModeType.HEIST: "Heist",
        BattleModeType.BRAWL_BALL: "Brawl Ball",
        BattleModeType.SIEGE: "Siege",
        BattleModeType.HOT_ZONE: "Hot Zone",
        BattleModeType.KNOCKOUT: "Knockout",
        BattleModeType.BASKET_BRAWL: "Basket Brawl",
        BattleModeType.HOLD_THE_TROPHY: "Hold the Trophy",
        BattleModeType.TROPHY_THIEVES: "Trophy Thieves",
        BattleModeType.DUELS: "Duels",
        BattleModeType.WIPE_OUT: "Wipe Out"
    }

    MODE_DESCRIPTIONS = {
        BattleModeType.GEM_GRAB: "Collect gems and hold them to win",
        BattleModeType.SHOWDOWN: "Last brawler standing wins",
        BattleModeType.BOUNTY: "Eliminate enemies to collect stars",
        BattleModeType.HEIST: "Attack or defend the safe",
        BattleModeType.BRAWL_BALL: "Score goals to win",
        BattleModeType.SIEGE: "Build robots to attack the enemy base",
        BattleModeType.HOT_ZONE: "Control zones to gain percentage",
        BattleModeType.KNOCKOUT: "Eliminate all enemies to win the round"
    }

    @classmethod
    def get_mode_name(cls, mode_type: BattleModeType) -> str:
        """Get human-readable mode name"""
        return cls.MODE_NAMES.get(mode_type, f"Unknown Mode {mode_type}")

    @classmethod
    def get_mode_description(cls, mode_type: BattleModeType) -> str:
        """Get mode description"""
        return cls.MODE_DESCRIPTIONS.get(mode_type, "Unknown game mode")

    @classmethod
    def is_team_mode(cls, mode_type: BattleModeType) -> bool:
        """Check if mode is team-based"""
        return mode_type != BattleModeType.SHOWDOWN

    @classmethod
    def is_solo_mode(cls, mode_type: BattleModeType) -> bool:
        """Check if mode is solo"""
        return mode_type == BattleModeType.SHOWDOWN

    @classmethod
    def get_team_size(cls, mode_type: BattleModeType) -> int:
        """Get team size for the mode"""
        if mode_type == BattleModeType.SHOWDOWN:
            return 1
        elif mode_type == BattleModeType.DUELS:
            return 1  # 1v1 mode
        else:
            return 3  # Most modes are 3v3

    @classmethod
    def get_max_players(cls, mode_type: BattleModeType) -> int:
        """Get maximum players for the mode"""
        if mode_type == BattleModeType.SHOWDOWN:
            return 10  # Solo or Duo Showdown
        elif mode_type == BattleModeType.DUELS:
            return 2   # 1v1
        else:
            return 6   # 3v3 modes

    @classmethod
    def requires_objective(cls, mode_type: BattleModeType) -> bool:
        """Check if mode requires specific objective"""
        objective_modes = {
            BattleModeType.GEM_GRAB,
            BattleModeType.BOUNTY,
            BattleModeType.HEIST,
            BattleModeType.BRAWL_BALL,
            BattleModeType.SIEGE,
            BattleModeType.HOT_ZONE
        }
        return mode_type in objective_modes

    @classmethod
    def get_all_modes(cls) -> Dict[BattleModeType, str]:
        """Get all available modes"""
        return cls.MODE_NAMES.copy()

    def __init__(self, mode_type: BattleModeType):
        """Initialize battle mode"""
        self.mode_type = mode_type
        self.mode_name = self.get_mode_name(mode_type)
        self.description = self.get_mode_description(mode_type)
        self.team_size = self.get_team_size(mode_type)
        self.max_players = self.get_max_players(mode_type)

    def __str__(self) -> str:
        """String representation"""
        return f"BattleMode({self.mode_name})"
