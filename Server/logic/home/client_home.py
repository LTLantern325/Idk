"""
Python conversion of Supercell.Laser.Logic.Home.ClientHome.cs
Client home class for home state management
"""

from typing import Dict, List, Optional, Any
from .structures.hero import Hero
from .structures.player_map import PlayerMap
from .structures.profile import Profile

class ClientHome:
    """Client home class for home state management"""

    def __init__(self):
        """Initialize client home"""
        self.account_id = 0
        self.home_id = 0

        # Player data
        self.player_name = ""
        self.experience_level = 1
        self.experience_points = 0
        self.trophies = 0
        self.highest_trophies = 0

        # Resources
        self.gold = 0
        self.diamonds = 0
        self.token_doubler = 0
        self.big_box_tokens = 0
        self.star_tokens = 0

        # Heroes/Characters
        self.heroes: Dict[int, Hero] = {}
        self.unlocked_heroes = []
        self.selected_hero = 0

        # Customization
        self.selected_skins = {}
        self.unlocked_skins = []
        self.name_color = 0
        self.player_thumbnail = 0

        # Battle pass
        self.battle_pass_season = 0
        self.battle_pass_tokens = 0
        self.battle_pass_tier = 0
        self.premium_pass_purchased = False

        # Club/Alliance
        self.alliance_id = 0
        self.alliance_name = ""
        self.alliance_role = 0

        # Quests
        self.daily_quests = []
        self.weekly_quests = []
        self.special_quests = []

        # Shop
        self.shop_offers = []
        self.featured_offers = []

        # Maps/Locations
        self.player_maps: List[PlayerMap] = []
        self.unlocked_locations = []

        # Profile
        self.profile = Profile()

        # Settings
        self.notification_settings = {}
        self.privacy_settings = {}

        # Statistics
        self.total_battles = 0
        self.victories = 0
        self.defeats = 0
        self.total_damage_dealt = 0

        # Time tracking
        self.last_online = 0
        self.session_start_time = 0
        self.total_play_time = 0

    def get_account_id(self) -> int:
        """Get account ID"""
        return self.account_id

    def set_account_id(self, account_id: int) -> None:
        """Set account ID"""
        self.account_id = account_id

    def get_home_id(self) -> int:
        """Get home ID"""
        return self.home_id

    def set_home_id(self, home_id: int) -> None:
        """Set home ID"""
        self.home_id = home_id

    def get_player_name(self) -> str:
        """Get player name"""
        return self.player_name

    def set_player_name(self, name: str) -> None:
        """Set player name"""
        self.player_name = name

    def get_experience_level(self) -> int:
        """Get experience level"""
        return self.experience_level

    def set_experience_level(self, level: int) -> None:
        """Set experience level"""
        self.experience_level = max(1, level)

    def get_trophies(self) -> int:
        """Get current trophies"""
        return self.trophies

    def set_trophies(self, trophies: int) -> None:
        """Set trophies"""
        self.trophies = max(0, trophies)
        if self.trophies > self.highest_trophies:
            self.highest_trophies = self.trophies

    def add_hero(self, hero: Hero) -> None:
        """Add hero to collection"""
        self.heroes[hero.get_hero_id()] = hero
        if hero.get_hero_id() not in self.unlocked_heroes:
            self.unlocked_heroes.append(hero.get_hero_id())

    def get_hero(self, hero_id: int) -> Optional[Hero]:
        """Get hero by ID"""
        return self.heroes.get(hero_id)

    def get_unlocked_heroes(self) -> List[int]:
        """Get list of unlocked hero IDs"""
        return self.unlocked_heroes.copy()

    def is_hero_unlocked(self, hero_id: int) -> bool:
        """Check if hero is unlocked"""
        return hero_id in self.unlocked_heroes

    def get_selected_hero(self) -> int:
        """Get selected hero ID"""
        return self.selected_hero

    def set_selected_hero(self, hero_id: int) -> None:
        """Set selected hero"""
        if self.is_hero_unlocked(hero_id):
            self.selected_hero = hero_id

    def add_resources(self, gold: int = 0, diamonds: int = 0, tokens: int = 0) -> None:
        """Add resources"""
        self.gold += gold
        self.diamonds += diamonds
        self.big_box_tokens += tokens

    def spend_resources(self, gold: int = 0, diamonds: int = 0, tokens: int = 0) -> bool:
        """Spend resources if available"""
        if (self.gold >= gold and 
            self.diamonds >= diamonds and 
            self.big_box_tokens >= tokens):

            self.gold -= gold
            self.diamonds -= diamonds
            self.big_box_tokens -= tokens
            return True
        return False

    def get_win_rate(self) -> float:
        """Get win rate percentage"""
        if self.total_battles == 0:
            return 0.0
        return (self.victories / self.total_battles) * 100

    def add_battle_result(self, victory: bool, damage_dealt: int = 0) -> None:
        """Add battle result"""
        self.total_battles += 1
        if victory:
            self.victories += 1
        else:
            self.defeats += 1
        self.total_damage_dealt += damage_dealt

    def get_battle_statistics(self) -> Dict[str, Any]:
        """Get battle statistics"""
        return {
            'total_battles': self.total_battles,
            'victories': self.victories,
            'defeats': self.defeats,
            'win_rate': self.get_win_rate(),
            'total_damage': self.total_damage_dealt,
            'average_damage': self.total_damage_dealt // max(1, self.total_battles)
        }

    def is_in_alliance(self) -> bool:
        """Check if player is in alliance"""
        return self.alliance_id != 0

    def join_alliance(self, alliance_id: int, alliance_name: str, role: int = 1) -> None:
        """Join alliance"""
        self.alliance_id = alliance_id
        self.alliance_name = alliance_name
        self.alliance_role = role

    def leave_alliance(self) -> None:
        """Leave alliance"""
        self.alliance_id = 0
        self.alliance_name = ""
        self.alliance_role = 0

    def update_session_time(self, current_time: int) -> None:
        """Update session and play time"""
        if self.session_start_time > 0:
            session_duration = current_time - self.session_start_time
            self.total_play_time += session_duration
        self.session_start_time = current_time

    def encode(self, stream) -> None:
        """Encode client home to stream"""
        stream.write_v_long(self.account_id)
        stream.write_v_int(self.home_id)
        stream.write_string(self.player_name)
        stream.write_v_int(self.experience_level)
        stream.write_v_int(self.trophies)
        stream.write_v_int(self.highest_trophies)
        stream.write_v_int(self.gold)
        stream.write_v_int(self.diamonds)
        stream.write_v_int(self.selected_hero)

        # Encode heroes
        stream.write_v_int(len(self.heroes))
        for hero in self.heroes.values():
            hero.encode(stream)

        # Encode profile
        self.profile.encode(stream)

    def decode(self, stream) -> None:
        """Decode client home from stream"""
        self.account_id = stream.read_v_long()
        self.home_id = stream.read_v_int()
        self.player_name = stream.read_string()
        self.experience_level = stream.read_v_int()
        self.trophies = stream.read_v_int()
        self.highest_trophies = stream.read_v_int()
        self.gold = stream.read_v_int()
        self.diamonds = stream.read_v_int()
        self.selected_hero = stream.read_v_int()

        # Decode heroes
        hero_count = stream.read_v_int()
        self.heroes.clear()
        for i in range(hero_count):
            hero = Hero()
            hero.decode(stream)
            self.heroes[hero.get_hero_id()] = hero

        # Decode profile
        self.profile.decode(stream)

    def __str__(self) -> str:
        """String representation"""
        return f"ClientHome('{self.player_name}', Level {self.experience_level}, {self.trophies} trophies)"
