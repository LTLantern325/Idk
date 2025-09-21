"""
Python conversion of Supercell.Laser.Logic.Util.GameModeUtil.cs
Game mode utility functions
"""

class BattleMode:
    """Battle mode constants"""
    NO_TIME_TICKS = -1
    INTRO_TICKS = 600
    NORMAL_TICKS = 2400

class GameModeUtil:
    """Game mode utility functions"""

    @staticmethod
    def players_collect_power_cubes(variation: int) -> bool:
        """Check if players collect power cubes in this variation"""
        v1 = variation - 6
        if v1 <= 8:
            return ((0x119 >> v1) & 1) != 0
        else:
            return False

    @staticmethod
    def get_battle_ticks(variation: int) -> int:
        """Get battle duration in ticks for variation"""
        v2 = 2400

        if variation in [0, 5, 16, 22, 23]:
            v2 = 4200
        elif variation in [3, 7, 8]:
            v2 = 2400  # Default value
        elif variation in [6, 9, 10, 12, 13, 18, 20]:
            return BattleMode.NO_TIME_TICKS
        elif variation == 14:
            v2 = 9600
        elif variation in [17, 21]:
            v2 = 3600
        else:
            v2 = 20 * ((BattleMode.NORMAL_TICKS - BattleMode.INTRO_TICKS) // 20)

        return BattleMode.INTRO_TICKS + v2

    @staticmethod
    def get_respawn_seconds(variation: int) -> int:
        """Get respawn time in seconds for variation"""
        if variation in [0, 2]:
            return 3
        elif variation == 3:
            return 1
        elif variation == 7:
            return 3
        else:
            return 5

    @staticmethod
    def players_collect_bounty_stars(variation: int) -> bool:
        """Check if players collect bounty stars"""
        return variation == 3 or variation == 15

    @staticmethod
    def has_two_teams(variation: int) -> bool:
        """Check if game mode has two teams"""
        return variation != 6

    @staticmethod
    def has_two_bases(variation: int) -> bool:
        """Check if game mode has two bases"""
        return variation == 2 or variation == 11

    @staticmethod
    def get_game_mode_variation(mode: str) -> int:
        """Get variation number for game mode string"""
        mode_map = {
            "CoinRush": 0,
            "GemGrab": 0,
            "Heist": 2,
            "BossFight": 7,
            "Bounty": 3,
            "Artifact": 4,
            "LaserBall": 5,
            "Showdown": 6,
            "BigGame": 7,
            "BattleRoyaleTeam": 9,
            "Survival": 8,
            "Raid": 10,
            "RoboWars": 11,
            "Tutorial": 12,
            "Training": 13,
            "TagTeam": 24,
            "ReachExit": 30,
            "MapPrint": 99
        }

        if mode in mode_map:
            return mode_map[mode]
        else:
            print(f"Error: Wrong game mode '{mode}'!")
            return -1

    @staticmethod
    def is_team_vs_team_mode(variation: int) -> bool:
        """Check if mode is team vs team"""
        return GameModeUtil.has_two_teams(variation)

    @staticmethod
    def is_battle_royale_mode(variation: int) -> bool:
        """Check if mode is battle royale"""
        return variation in [6, 9]  # Showdown, BattleRoyaleTeam

    @staticmethod
    def is_boss_fight_mode(variation: int) -> bool:
        """Check if mode is boss fight"""
        return variation == 7

    @staticmethod
    def is_infinite_time_mode(variation: int) -> bool:
        """Check if mode has infinite time"""
        return GameModeUtil.get_battle_ticks(variation) == BattleMode.NO_TIME_TICKS
