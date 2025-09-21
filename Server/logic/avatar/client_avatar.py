"""
Python conversion of Supercell.Laser.Logic.Avatar.ClientAvatar.cs
Client avatar class for player avatar management
"""

from typing import Dict, List, Optional, Any
from .structures.player_display_data import PlayerDisplayData

class ClientAvatar:
    """Client avatar class for player avatar management"""

    def __init__(self):
        """Initialize client avatar"""
        self.account_id = 0
        self.name = ""
        self.name_color_id = 0
        self.experience_points = 0
        self.experience_level = 1
        self.trophies = 0
        self.high_trophies = 0
        self.tokens = 0
        self.coins = 0
        self.gems = 0
        self.star_tokens = 0
        self.power_play_points = 0
        self.solo_wins = 0
        self.duo_wins = 0
        self.team_wins = 0

        # Player display data
        self.player_display_data = PlayerDisplayData()

        # Heroes (characters/brawlers)
        self.heroes = {}  # Dict[int, Hero]

        # Unlocked items
        self.unlocked_skins = []  # List of skin IDs
        self.unlocked_pins = []   # List of pin IDs

        # Season data
        self.current_season = 0
        self.current_season_trophies = 0

        # Battle pass
        self.battle_pass_tier = 0
        self.battle_pass_tokens = 0

        # Profile settings
        self.profile_icon_id = 0
        self.thumbnail_id = 0

        # Statistics
        self.battles_played = 0
        self.victory_count = 0

    def get_account_id(self) -> int:
        """Get account ID"""
        return self.account_id

    def set_account_id(self, account_id: int) -> None:
        """Set account ID"""
        self.account_id = account_id

    def get_name(self) -> str:
        """Get player name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set player name"""
        self.name = name

    def get_experience_level(self) -> int:
        """Get experience level"""
        return self.experience_level

    def set_experience_points(self, exp: int) -> None:
        """Set experience points and calculate level"""
        self.experience_points = exp
        # Calculate level from experience points
        self.experience_level = max(1, exp // 1000 + 1)

    def get_trophies(self) -> int:
        """Get current trophies"""
        return self.trophies

    def set_trophies(self, trophies: int) -> None:
        """Set current trophies"""
        self.trophies = trophies
        if trophies > self.high_trophies:
            self.high_trophies = trophies

    def get_high_trophies(self) -> int:
        """Get highest trophies achieved"""
        return self.high_trophies

    def add_trophies(self, amount: int) -> None:
        """Add trophies"""
        self.set_trophies(self.trophies + amount)

    def get_coins(self) -> int:
        """Get coins"""
        return self.coins

    def set_coins(self, coins: int) -> None:
        """Set coins"""
        self.coins = max(0, coins)

    def add_coins(self, amount: int) -> None:
        """Add coins"""
        self.set_coins(self.coins + amount)

    def get_gems(self) -> int:
        """Get gems"""
        return self.gems

    def set_gems(self, gems: int) -> None:
        """Set gems"""
        self.gems = max(0, gems)

    def add_gems(self, amount: int) -> None:
        """Add gems"""
        self.set_gems(self.gems + amount)

    def get_hero_count(self) -> int:
        """Get number of unlocked heroes"""
        return len(self.heroes)

    def add_hero(self, hero_data_id: int, hero: Any) -> None:
        """Add hero to collection"""
        self.heroes[hero_data_id] = hero

    def get_hero(self, hero_data_id: int) -> Optional[Any]:
        """Get hero by ID"""
        return self.heroes.get(hero_data_id)

    def has_hero(self, hero_data_id: int) -> bool:
        """Check if hero is unlocked"""
        return hero_data_id in self.heroes

    def get_total_wins(self) -> int:
        """Get total wins across all modes"""
        return self.solo_wins + self.duo_wins + self.team_wins

    def add_victory(self, mode: str = "solo") -> None:
        """Add victory"""
        self.victory_count += 1
        if mode == "solo":
            self.solo_wins += 1
        elif mode == "duo":
            self.duo_wins += 1
        elif mode == "team":
            self.team_wins += 1

    def unlock_skin(self, skin_id: int) -> bool:
        """Unlock skin"""
        if skin_id not in self.unlocked_skins:
            self.unlocked_skins.append(skin_id)
            return True
        return False

    def has_skin(self, skin_id: int) -> bool:
        """Check if skin is unlocked"""
        return skin_id in self.unlocked_skins

    def get_power_level_average(self) -> float:
        """Get average power level of all heroes"""
        if not self.heroes:
            return 0.0

        total_power = sum(getattr(hero, 'power_level', 1) for hero in self.heroes.values())
        return total_power / len(self.heroes)

    def encode(self, stream) -> None:
        """Encode avatar to stream"""
        # Account info
        stream.write_v_long(self.account_id)
        stream.write_string(self.name)
        stream.write_v_int(self.name_color_id)

        # Experience and trophies
        stream.write_v_int(self.experience_points)
        stream.write_v_int(self.experience_level)
        stream.write_v_int(self.trophies)
        stream.write_v_int(self.high_trophies)

        # Resources
        stream.write_v_int(self.coins)
        stream.write_v_int(self.gems)
        stream.write_v_int(self.tokens)
        stream.write_v_int(self.star_tokens)

        # Statistics
        stream.write_v_int(self.solo_wins)
        stream.write_v_int(self.duo_wins)
        stream.write_v_int(self.team_wins)

        # Heroes
        stream.write_v_int(len(self.heroes))
        for hero_id, hero in self.heroes.items():
            stream.write_v_int(hero_id)
            if hasattr(hero, 'encode'):
                hero.encode(stream)

    def decode(self, stream) -> None:
        """Decode avatar from stream"""
        # Account info
        self.account_id = stream.read_v_long()
        self.name = stream.read_string()
        self.name_color_id = stream.read_v_int()

        # Experience and trophies
        self.experience_points = stream.read_v_int()
        self.experience_level = stream.read_v_int()
        self.trophies = stream.read_v_int()
        self.high_trophies = stream.read_v_int()

        # Resources
        self.coins = stream.read_v_int()
        self.gems = stream.read_v_int()
        self.tokens = stream.read_v_int()
        self.star_tokens = stream.read_v_int()

        # Statistics
        self.solo_wins = stream.read_v_int()
        self.duo_wins = stream.read_v_int()
        self.team_wins = stream.read_v_int()

        # Heroes (simplified)
        hero_count = stream.read_v_int()
        for i in range(hero_count):
            hero_id = stream.read_v_int()
            # Skip hero data for now

    def __str__(self) -> str:
        """String representation"""
        return (f"ClientAvatar('{self.name}', level={self.experience_level}, "
                f"trophies={self.trophies}, heroes={len(self.heroes)})")
