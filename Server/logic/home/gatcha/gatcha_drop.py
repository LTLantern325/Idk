"""
Python conversion of Supercell.Laser.Logic.Home.Gatcha.GatchaDrop.cs
Gatcha drop system for box rewards
"""

from typing import TYPE_CHECKING
from ..helper.byte_stream_helper import ByteStreamHelper

if TYPE_CHECKING:
    from ..home.home_mode import HomeMode

class DropType:
    """Drop type constants"""
    UNLOCK_HERO = 1
    POWER_POINTS = 6
    GOLD = 7
    GEMS = 8
    EMOTE = 10

class GatchaDrop:
    """Gatcha drop representing a reward from boxes"""

    def __init__(self, drop_type: int):
        """Initialize gatcha drop"""
        self.count = 0
        self.data_global_id = 0
        self.pin_global_id = 0
        self.type = drop_type

    def do_drop(self, home_mode: 'HomeMode') -> None:
        """Execute the drop reward"""
        avatar = home_mode.avatar

        if self.type == DropType.UNLOCK_HERO:
            if avatar and hasattr(avatar, 'unlock_hero'):
                avatar.unlock_hero(self.data_global_id)

        elif self.type == DropType.POWER_POINTS:
            if avatar and hasattr(avatar, 'get_hero'):
                hero = avatar.get_hero(self.data_global_id)
                if hero:
                    hero.power_points += self.count

        elif self.type == DropType.GOLD:
            if avatar and hasattr(avatar, 'add_gold'):
                avatar.add_gold(self.count)

        elif self.type == DropType.GEMS:
            if avatar and hasattr(avatar, 'add_diamonds'):
                avatar.add_diamonds(self.count)

        elif self.type == DropType.EMOTE:
            if home_mode.home and hasattr(home_mode.home, 'unlocked_emotes'):
                home_mode.home.unlocked_emotes.append(self.data_global_id)

    def encode(self, stream) -> None:
        """Encode drop to stream"""
        stream.write_v_int(self.count)
        ByteStreamHelper.write_data_reference(stream, self.data_global_id)
        stream.write_v_int(self.type)

        ByteStreamHelper.write_data_reference(stream, 0)
        ByteStreamHelper.write_data_reference(stream, self.pin_global_id)
        ByteStreamHelper.write_data_reference(stream, 0)
        stream.write_v_int(0)
