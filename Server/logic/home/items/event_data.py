"""
Python conversion of Supercell.Laser.Logic.Home.Items.EventData.cs
Event data for game events and battles
"""

from datetime import datetime
from typing import TYPE_CHECKING
from ..helper.byte_stream_helper import ByteStreamHelper

if TYPE_CHECKING:
    from ...data.location_data import LocationData
    from ...battle.structures.battle_player_map import BattlePlayerMap

class EventData:
    """Event data containing information about game events"""

    def __init__(self):
        """Initialize event data"""
        self.slot = 0              # Event slot number
        self.location_id = 0       # Location ID
        self.end_time = datetime.now()  # Event end time
        self.battle_player_map = None   # Associated battle player map

        # Additional properties for event configuration
        self.game_mode_variation = 0
        self.modifier = 0
        self.is_ranked = False
        self.map_maker_enabled = False

    def get_slot(self) -> int:
        """Get event slot"""
        return self.slot

    def set_slot(self, slot: int) -> None:
        """Set event slot"""
        self.slot = slot

    def get_location_id(self) -> int:
        """Get location ID"""
        return self.location_id

    def set_location_id(self, location_id: int) -> None:
        """Set location ID"""
        self.location_id = location_id

    def get_end_time(self) -> datetime:
        """Get event end time"""
        return self.end_time

    def set_end_time(self, end_time: datetime) -> None:
        """Set event end time"""
        self.end_time = end_time

    def get_location(self) -> 'LocationData':
        """Get location data from DataTables"""
        # This would use DataTables.Get(DataType.Location).GetDataByGlobalId(LocationId)
        # For now, simplified
        return None

    def get_battle_player_map(self) -> 'BattlePlayerMap':
        """Get battle player map"""
        return self.battle_player_map

    def set_battle_player_map(self, battle_map: 'BattlePlayerMap') -> None:
        """Set battle player map"""
        self.battle_player_map = battle_map

    def get_seconds_until_end(self) -> int:
        """Get seconds until event ends"""
        now = datetime.now()
        if self.end_time > now:
            return int((self.end_time - now).total_seconds())
        return 0

    def is_active(self) -> bool:
        """Check if event is currently active"""
        return self.get_seconds_until_end() > 0

    def is_special_slot(self) -> bool:
        """Check if event is in special slot (12 or 13)"""
        return self.slot == 12 or self.slot == 13

    def set_game_mode_variation(self, variation: int) -> None:
        """Set game mode variation"""
        self.game_mode_variation = variation

    def get_game_mode_variation(self) -> int:
        """Get game mode variation"""
        return self.game_mode_variation

    def set_modifier(self, modifier: int) -> None:
        """Set event modifier"""
        self.modifier = modifier

    def get_modifier(self) -> int:
        """Get event modifier"""
        return self.modifier

    def set_ranked(self, ranked: bool) -> None:
        """Set ranked status"""
        self.is_ranked = ranked

    def is_ranked_event(self) -> bool:
        """Check if event is ranked"""
        return self.is_ranked

    def encode(self, encoder) -> None:
        """Encode event data to stream"""
        # Write initial values
        encoder.write_v_int(-1)  # Unknown
        encoder.write_v_int(self.slot)
        encoder.write_v_int(0)   # Unknown
        encoder.write_v_int(0)   # v53 value

        # Event timing
        encoder.write_v_int(self.get_seconds_until_end())
        encoder.write_v_int(0)   # Unknown

        # Location data reference
        if self.is_special_slot():
            ByteStreamHelper.write_data_reference(encoder, None)
        else:
            location = self.get_location()
            ByteStreamHelper.write_data_reference(encoder, location)

        # Game mode and settings
        encoder.write_v_int(self.game_mode_variation)
        encoder.write_v_int(2)   # Unknown constant

        # String and additional data
        encoder.write_string(None)  # 0xacecac
        encoder.write_v_int(0)      # 0xacecc0
        encoder.write_v_int(0)      # 0xacecd4
        encoder.write_v_int(0)      # 0xacece8

        # Modifier
        encoder.write_v_int(self.modifier)

        # Additional unknowns
        encoder.write_v_int(0)  # 0xacee58
        encoder.write_v_int(0)  # 0xacee6c

        # Battle player map
        ByteStreamHelper.write_battle_player_map(encoder, self.battle_player_map)

        # Final settings
        encoder.write_v_int(0)        # Unknown
        encoder.write_boolean(self.is_ranked)  # LogicRankedSeason
        encoder.write_v_int(0)        # Unknown
        encoder.write_v_int(0)        # Unknown
        encoder.write_boolean(False)  # Unknown
        encoder.write_boolean(False)  # Unknown
        encoder.write_boolean(False)  # Unknown
        encoder.write_v_int(-1)       # Unknown
        encoder.write_boolean(False)  # Unknown
        encoder.write_boolean(False)  # Unknown
        encoder.write_v_int(-1)       # Unknown

        # v51 values
        encoder.write_v_int(0)  # v51
        encoder.write_v_int(0)  # v51
        encoder.write_v_int(0)  # v51

        # v53 value
        encoder.write_boolean(self.map_maker_enabled)  # v53

    def decode(self, decoder) -> None:
        """Decode event data from stream"""
        # Read initial values
        decoder.read_v_int()  # Unknown
        self.slot = decoder.read_v_int()
        decoder.read_v_int()  # Unknown
        decoder.read_v_int()  # v53

        # Event timing
        seconds_remaining = decoder.read_v_int()
        # Calculate end time from seconds
        self.end_time = datetime.now() + datetime.timedelta(seconds=seconds_remaining)
        decoder.read_v_int()  # Unknown

        # Location data
        location_data = ByteStreamHelper.read_data_reference(decoder)
        if location_data:
            self.location_id = location_data

        # Game mode and settings
        self.game_mode_variation = decoder.read_v_int()
        decoder.read_v_int()  # Unknown constant

        # Skip string and additional data
        decoder.read_string()  # String
        decoder.read_v_int()   # Unknown
        decoder.read_v_int()   # Unknown
        decoder.read_v_int()   # Unknown

        # Modifier
        self.modifier = decoder.read_v_int()

        # Skip additional unknowns
        decoder.read_v_int()  # Unknown
        decoder.read_v_int()  # Unknown

        # Battle player map
        self.battle_player_map = ByteStreamHelper.read_battle_player_map(decoder)

        # Final settings
        decoder.read_v_int()     # Unknown
        self.is_ranked = decoder.read_boolean()
        decoder.read_v_int()     # Unknown
        decoder.read_v_int()     # Unknown
        decoder.read_boolean()   # Unknown
        decoder.read_boolean()   # Unknown
        decoder.read_boolean()   # Unknown
        decoder.read_v_int()     # Unknown
        decoder.read_boolean()   # Unknown
        decoder.read_boolean()   # Unknown
        decoder.read_v_int()     # Unknown

        # v51 values
        decoder.read_v_int()  # v51
        decoder.read_v_int()  # v51
        decoder.read_v_int()  # v51

        # v53 value
        self.map_maker_enabled = decoder.read_boolean()

    def __str__(self) -> str:
        """String representation"""
        status = "active" if self.is_active() else "ended"
        return f"EventData(slot={self.slot}, location_id={self.location_id}, {status})"
