"""
Python conversion of Supercell.Laser.Logic.Home.Structures.Profile.cs
Player profile for displaying player information
"""

from typing import List, TYPE_CHECKING
from ...helper.byte_stream_helper import ByteStreamHelper

if TYPE_CHECKING:
    from ...avatar.client_avatar import ClientAvatar
    from ...avatar.structures.player_display_data import PlayerDisplayData
    from ..client_home import ClientHome
    from .hero import Hero

class LogicVector2:
    """Simple vector2 for stats"""

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def encode(self, stream) -> None:
        """Encode vector2"""
        stream.write_v_int(self.x)
        stream.write_v_int(self.y)

class Profile:
    """Player profile containing display information and stats"""

    def __init__(self):
        """Initialize profile"""
        self.display_data = None  # PlayerDisplayData
        self.account_id = 0
        self.heroes: List['Hero'] = []
        self.stats: List[LogicVector2] = []

        # Selected cosmetics
        self.hero = 0          # Selected hero ID
        self.hero_skin = 0     # Selected skin ID
        self.t1 = 0           # Thumbnail 1
        self.t2 = 0           # Thumbnail 2
        self.e = 0            # Emote
        self.ti = 0           # Title

    def get_account_id(self) -> int:
        """Get account ID"""
        return self.account_id

    def set_account_id(self, account_id: int) -> None:
        """Set account ID"""
        self.account_id = account_id

    def get_display_data(self) -> 'PlayerDisplayData':
        """Get display data"""
        return self.display_data

    def set_display_data(self, display_data: 'PlayerDisplayData') -> None:
        """Set display data"""
        self.display_data = display_data

    def get_heroes(self) -> List['Hero']:
        """Get heroes list"""
        return self.heroes.copy()

    def set_heroes(self, heroes: List['Hero']) -> None:
        """Set heroes list"""
        self.heroes = heroes.copy()

    def add_hero(self, hero: 'Hero') -> None:
        """Add hero to profile"""
        self.heroes.append(hero)

    def get_hero_count(self) -> int:
        """Get number of heroes"""
        return len(self.heroes)

    def get_stats(self) -> List[LogicVector2]:
        """Get stats list"""
        return self.stats.copy()

    def add_stat(self, key: int, value: int) -> None:
        """Add stat to profile"""
        self.stats.append(LogicVector2(key, value))

    def get_stat(self, key: int) -> int:
        """Get stat value by key"""
        for stat in self.stats:
            if stat.x == key:
                return stat.y
        return 0

    def set_stat(self, key: int, value: int) -> None:
        """Set stat value"""
        for stat in self.stats:
            if stat.x == key:
                stat.y = value
                return
        self.add_stat(key, value)

    def get_selected_hero(self) -> int:
        """Get selected hero ID"""
        return self.hero

    def set_selected_hero(self, hero_id: int) -> None:
        """Set selected hero ID"""
        self.hero = hero_id

    def get_selected_skin(self) -> int:
        """Get selected skin ID"""
        return self.hero_skin

    def set_selected_skin(self, skin_id: int) -> None:
        """Set selected skin ID"""
        self.hero_skin = skin_id

    def get_cosmetics(self) -> tuple:
        """Get cosmetic IDs as tuple"""
        return (self.t1, self.t2, self.e, self.ti)

    def set_cosmetics(self, t1: int, t2: int, emote: int, title: int) -> None:
        """Set cosmetic IDs"""
        self.t1 = t1
        self.t2 = t2
        self.e = emote
        self.ti = title

    def get_trophies(self) -> int:
        """Get current trophies"""
        return self.get_stat(3)

    def get_highest_trophies(self) -> int:
        """Get highest trophies"""
        return self.get_stat(4)

    def get_experience(self) -> int:
        """Get experience points"""
        return self.get_stat(2)

    def get_trio_wins(self) -> int:
        """Get trio wins"""
        return self.get_stat(1)

    def get_solo_wins(self) -> int:
        """Get solo wins"""
        return self.get_stat(8)

    def get_total_wins(self) -> int:
        """Get total wins"""
        return self.get_trio_wins() + self.get_solo_wins()

    def encode(self, stream) -> None:
        """Encode profile to stream"""
        # Account ID
        stream.write_v_long(self.account_id)

        # Selected hero
        ByteStreamHelper.write_data_reference(stream, self.hero)

        # Heroes
        stream.write_v_int(len(self.heroes))
        for hero in self.heroes:
            hero.encode(stream)

        # Stats
        stream.write_v_int(len(self.stats))
        for stat in self.stats:
            stat.encode(stream)

        # Display data
        if self.display_data:
            self.display_data.encode(stream)
        else:
            # Write empty display data
            stream.write_string("")  # Name
            stream.write_v_int(0)    # Thumbnail

        # Additional data
        stream.write_boolean(False)  # Unknown boolean

        # Profile string and values
        stream.write_string("str")   # Profile string
        stream.write_v_int(100)      # Unknown value 1
        stream.write_v_int(200)      # Unknown value 2
        stream.write_v_int(0)        # v53 value

        # Cosmetics
        ByteStreamHelper.write_data_reference(stream, self.hero_skin)
        ByteStreamHelper.write_data_reference(stream, self.t1)
        ByteStreamHelper.write_data_reference(stream, self.t2)
        ByteStreamHelper.write_data_reference(stream, self.e)
        ByteStreamHelper.write_data_reference(stream, self.ti)

    def decode(self, stream) -> None:
        """Decode profile from stream"""
        # Account ID
        self.account_id = stream.read_v_long()

        # Selected hero
        self.hero = ByteStreamHelper.read_data_reference(stream)

        # Heroes
        hero_count = stream.read_v_int()
        self.heroes = []
        for _ in range(hero_count):
            # This would create Hero instances and decode them
            # For now, simplified
            pass

        # Stats
        stat_count = stream.read_v_int()
        self.stats = []
        for _ in range(stat_count):
            stat = LogicVector2()
            stat.x = stream.read_v_int()
            stat.y = stream.read_v_int()
            self.stats.append(stat)

        # Display data would be decoded here
        # For now, skip

        # Additional data
        stream.read_boolean()  # Unknown boolean
        stream.read_string()   # Profile string
        stream.read_v_int()    # Unknown value 1
        stream.read_v_int()    # Unknown value 2
        stream.read_v_int()    # v53 value

        # Cosmetics
        self.hero_skin = ByteStreamHelper.read_data_reference(stream)
        self.t1 = ByteStreamHelper.read_data_reference(stream)
        self.t2 = ByteStreamHelper.read_data_reference(stream)
        self.e = ByteStreamHelper.read_data_reference(stream)
        self.ti = ByteStreamHelper.read_data_reference(stream)

    @classmethod
    def create(cls, home: 'ClientHome', avatar: 'ClientAvatar') -> 'Profile':
        """Create profile from home and avatar"""
        profile = cls()

        profile.account_id = avatar.account_id

        # Set display data
        from ...avatar.structures.player_display_data import PlayerDisplayData
        player_display_data = PlayerDisplayData()
        player_display_data.thumbnail_id = home.thumbnail_id
        player_display_data.name = avatar.name
        profile.display_data = player_display_data

        # Set heroes
        profile.heroes = avatar.heroes.copy()

        # Add stats
        profile.add_stat(1, avatar.trio_wins)        # Trio wins
        profile.add_stat(2, 100)                     # Experience
        profile.add_stat(3, avatar.trophies)         # Current trophies
        profile.add_stat(4, avatar.highest_trophies) # Highest trophies
        profile.add_stat(5, len(profile.heroes))     # Hero count
        profile.add_stat(7, home.thumbnail_id)       # Thumbnail ID
        profile.add_stat(8, avatar.solo_wins)        # Solo wins

        # Set selected items
        profile.hero = home.favourite_character
        if hasattr(home, 'default_battle_card'):
            profile.t1 = home.default_battle_card.thumbnail1
            profile.t2 = home.default_battle_card.thumbnail2
            profile.e = home.default_battle_card.emote
            profile.ti = home.default_battle_card.title

        return profile

    def __str__(self) -> str:
        """String representation"""
        name = self.display_data.name if self.display_data else "Unknown"
        return (f"Profile(id={self.account_id}, name='{name}', "
                f"heroes={len(self.heroes)}, trophies={self.get_trophies()})")
