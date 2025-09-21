"""
Python conversion of Supercell.Laser.Logic.Message.Ranking.LeaderboardMessage.cs
Leaderboard message for sending leaderboard data
"""

from typing import List, Dict, Any, TYPE_CHECKING
from ..game_message import GameMessage

if TYPE_CHECKING:
    from ...avatar.client_avatar import ClientAvatar
    from ...home.client_home import ClientHome
    from ...club.alliance import Alliance

class LeaderboardMessage(GameMessage):
    """Leaderboard message for sending leaderboard data"""

    def __init__(self):
        """Initialize leaderboard message"""
        super().__init__()
        self.leaderboard_type = 1  # 0=hero, 1=global
        self.avatars = []  # List of (home, avatar) pairs
        self.alliance_list = []  # List of alliances
        self.own_avatar_id = 0
        self.region = ""
        self.hero_data_id = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24403

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def set_leaderboard_type(self, lb_type: int) -> None:
        """Set leaderboard type (0=hero, 1=global)"""
        self.leaderboard_type = lb_type

    def add_avatar(self, home: 'ClientHome', avatar: 'ClientAvatar') -> None:
        """Add avatar to leaderboard"""
        self.avatars.append((home, avatar))

    def add_alliance(self, alliance: 'Alliance') -> None:
        """Add alliance to list"""
        self.alliance_list.append(alliance)

    def set_own_avatar_id(self, avatar_id: int) -> None:
        """Set own avatar ID for highlighting"""
        self.own_avatar_id = avatar_id

    def set_region(self, region: str) -> None:
        """Set region"""
        self.region = region

    def set_hero_data_id(self, hero_id: int) -> None:
        """Set hero data ID for hero leaderboards"""
        self.hero_data_id = hero_id

    def get_player_index(self) -> int:
        """Get own player index in leaderboard"""
        for i, (home, avatar) in enumerate(self.avatars):
            if hasattr(avatar, 'account_id') and avatar.account_id == self.own_avatar_id:
                return i + 1
        return 0

    def encode(self) -> None:
        """Encode message to stream"""
        player_index = 0

        # Write header
        self.stream.write_v_int(self.leaderboard_type)
        self.stream.write_v_int(0)  # Unknown field
        # ByteStreamHelper.WriteDataReference(Stream, HeroDataId)
        self.stream.write_v_int(self.hero_data_id)  # Simplified
        self.stream.write_string(self.region)

        if self.leaderboard_type == 1:  # Global leaderboard
            self.stream.write_v_int(len(self.avatars))

            for i, (home, avatar) in enumerate(self.avatars):
                # Check if this is own avatar
                if hasattr(avatar, 'account_id') and avatar.account_id == self.own_avatar_id:
                    player_index = i + 1

                # Write avatar data (simplified)
                self.stream.write_v_long(getattr(avatar, 'account_id', 0))
                self.stream.write_v_int(1)  # Status
                self.stream.write_v_int(i)  # Rank

                self.stream.write_boolean(True)
                self.stream.write_string("")  # Empty string
                self.stream.write_string(getattr(avatar, 'name', 'NoName'))
                self.stream.write_v_int(100)  # Experience level
                self.stream.write_v_int(getattr(home, 'thumbnail_id', 43000000))
                self.stream.write_v_int(43000000)  # Default thumbnail
                self.stream.write_v_int(0)
                self.stream.write_boolean(False)

        elif self.leaderboard_type == 0:  # Hero leaderboard
            self.stream.write_v_int(len(self.avatars))

            for i, (home, avatar) in enumerate(self.avatars):
                if hasattr(avatar, 'account_id') and avatar.account_id == self.own_avatar_id:
                    player_index = i + 1

                # Write avatar data
                self.stream.write_v_long(getattr(avatar, 'account_id', 0))
                self.stream.write_v_int(1)

                # Get hero trophies (simplified)
                hero_trophies = 0
                if hasattr(avatar, 'get_hero'):
                    hero = avatar.get_hero(self.hero_data_id)
                    if hero:
                        hero_trophies = getattr(hero, 'trophies', 0)

                self.stream.write_v_int(hero_trophies)

                self.stream.write_boolean(True)
                self.stream.write_string("")
                self.stream.write_string(getattr(avatar, 'name', 'NoName'))
                self.stream.write_v_int(100)
                self.stream.write_v_int(getattr(home, 'thumbnail_id', 43000000))
                self.stream.write_v_int(43000000)
                self.stream.write_v_int(0)
                self.stream.write_boolean(False)

        # Write footer
        self.stream.write_v_int(0)
        self.stream.write_v_int(player_index)
        self.stream.write_v_int(0)
        self.stream.write_v_int(0)
        self.stream.write_string("BS")

    def decode(self) -> None:
        """Decode message from stream"""
        # Simplified decoding
        self.leaderboard_type = self.stream.read_v_int()
        self.stream.read_v_int()  # Skip unknown
        self.hero_data_id = self.stream.read_v_int()
        self.region = self.stream.read_string()

        # Skip rest of data for now

    def __str__(self) -> str:
        """String representation"""
        lb_type = "hero" if self.leaderboard_type == 0 else "global"
        return f"LeaderboardMessage({lb_type}, {len(self.avatars)} players, region='{self.region}')"
