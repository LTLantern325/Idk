"""
Python conversion of Supercell.Laser.Logic.Home.Structures.PlayerMap.cs
Player map for custom map creation and sharing
"""

from ...helper.byte_stream_helper import ByteStreamHelper

class PlayerMap:
    """Player-created map data"""

    def __init__(self):
        """Initialize player map"""
        self.map_id = 0              # Unique map ID
        self.map_name = ""           # Map name
        self.gmv = 0                 # Game Mode Variation
        self.map_environment_data = 0 # Environment/theme data
        self.map_data = None         # Raw map data bytes

        # Creator information
        self.account_id = 0          # Map creator's account ID
        self.avatar_name = ""        # Map creator's name

        # Map stats and status
        self.state = 1               # Map state (1 = published, 0 = draft)
        self.update_time = 0         # Last update timestamp
        self.friendly_signoff_count = 0  # Friendly battle signoffs
        self.likes = 0               # Number of likes
        self.plays = 0               # Number of plays

    def get_map_id(self) -> int:
        """Get map ID"""
        return self.map_id

    def set_map_id(self, map_id: int) -> None:
        """Set map ID"""
        self.map_id = map_id

    def get_map_name(self) -> str:
        """Get map name"""
        return self.map_name

    def set_map_name(self, name: str) -> None:
        """Set map name"""
        self.map_name = name

    def get_game_mode_variation(self) -> int:
        """Get game mode variation"""
        return self.gmv

    def set_game_mode_variation(self, gmv: int) -> None:
        """Set game mode variation"""
        self.gmv = gmv

    def get_environment_data(self) -> int:
        """Get environment data"""
        return self.map_environment_data

    def set_environment_data(self, env_data: int) -> None:
        """Set environment data"""
        self.map_environment_data = env_data

    def get_map_data(self) -> bytes:
        """Get map data bytes"""
        return self.map_data

    def set_map_data(self, data: bytes) -> None:
        """Set map data bytes"""
        self.map_data = data

    def get_creator_id(self) -> int:
        """Get creator account ID"""
        return self.account_id

    def set_creator_id(self, account_id: int) -> None:
        """Set creator account ID"""
        self.account_id = account_id

    def get_creator_name(self) -> str:
        """Get creator name"""
        return self.avatar_name

    def set_creator_name(self, name: str) -> None:
        """Set creator name"""
        self.avatar_name = name

    def get_state(self) -> int:
        """Get map state"""
        return self.state

    def set_state(self, state: int) -> None:
        """Set map state"""
        self.state = state

    def is_published(self) -> bool:
        """Check if map is published"""
        return self.state == 1

    def is_draft(self) -> bool:
        """Check if map is draft"""
        return self.state == 0

    def get_likes(self) -> int:
        """Get number of likes"""
        return self.likes

    def add_like(self) -> None:
        """Add a like to the map"""
        self.likes += 1

    def remove_like(self) -> None:
        """Remove a like from the map"""
        self.likes = max(0, self.likes - 1)

    def get_plays(self) -> int:
        """Get number of plays"""
        return self.plays

    def add_play(self) -> None:
        """Add a play to the map"""
        self.plays += 1

    def get_friendly_signoffs(self) -> int:
        """Get friendly signoff count"""
        return self.friendly_signoff_count

    def add_friendly_signoff(self) -> None:
        """Add friendly signoff"""
        self.friendly_signoff_count += 1

    def has_map_data(self) -> bool:
        """Check if map has data"""
        return self.map_data is not None and len(self.map_data) > 0

    def get_map_size(self) -> int:
        """Get map data size in bytes"""
        return len(self.map_data) if self.map_data else 0

    def set_update_time(self, timestamp: int) -> None:
        """Set update timestamp"""
        self.update_time = timestamp

    def get_update_time(self) -> int:
        """Get update timestamp"""
        return self.update_time

    def encode(self, stream) -> None:
        """Encode player map to stream"""
        # Encode map ID as LogicLong
        ByteStreamHelper.encode_logic_long(stream, self.map_id)

        # Map basic info
        stream.write_string(self.map_name)
        stream.write_v_int(self.gmv)

        # Environment data reference (DataType 54)
        stream.write_data_reference(54, self.map_environment_data)

        # Map data bytes
        if self.map_data is not None:
            stream.write_bytes(self.map_data, len(self.map_data))
        else:
            stream.write_bytes(None, 1)

        # Creator info
        ByteStreamHelper.encode_logic_long(stream, self.account_id)
        stream.write_string(self.avatar_name)

        # Map status and stats
        stream.write_v_int(self.state)                    # State
        stream.write_long(self.update_time)               # Update time since epoch
        stream.write_v_int(0)                            # Unknown
        stream.write_v_int(self.friendly_signoff_count)   # Friendly signoff count
        stream.write_v_int(self.likes)                   # Likes
        stream.write_v_int(self.plays)                   # Plays
        stream.write_v_int(0)                            # Unknown

    def decode(self, stream) -> None:
        """Decode player map from stream"""
        # Decode map ID
        self.map_id = ByteStreamHelper.decode_logic_long(stream)

        # Map basic info
        self.map_name = stream.read_string()
        self.gmv = stream.read_v_int()

        # Environment data reference
        _, self.map_environment_data = stream.read_data_reference()

        # Map data bytes
        data_length = stream.read_v_int()
        if data_length > 1:
            self.map_data = stream.read_bytes(data_length)
        else:
            self.map_data = None

        # Creator info
        self.account_id = ByteStreamHelper.decode_logic_long(stream)
        self.avatar_name = stream.read_string()

        # Map status and stats
        self.state = stream.read_v_int()
        self.update_time = stream.read_long()
        stream.read_v_int()  # Unknown
        self.friendly_signoff_count = stream.read_v_int()
        self.likes = stream.read_v_int()
        self.plays = stream.read_v_int()
        stream.read_v_int()  # Unknown

    def __str__(self) -> str:
        """String representation"""
        return (f"PlayerMap(id={self.map_id}, name='{self.map_name}', "
                f"creator='{self.avatar_name}', likes={self.likes})")
