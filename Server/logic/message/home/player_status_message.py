"""
Python conversion of Supercell.Laser.Logic.Message.Home.PlayerStatusMessage.cs
Player status message for player status updates
"""

from ..game_message import GameMessage

class PlayerStatusMessage(GameMessage):
    """Player status message for player status updates"""

    def __init__(self):
        """Initialize player status message"""
        super().__init__()
        self.player_id = 0
        self.status = 0  # 0=offline, 1=online, 2=away, 3=in_battle
        self.location = ""
        self.last_seen_timestamp = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24114  # Player status

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_player_id(self) -> int:
        """Get player ID"""
        return self.player_id

    def set_player_id(self, player_id: int) -> None:
        """Set player ID"""
        self.player_id = player_id

    def get_status(self) -> int:
        """Get player status"""
        return self.status

    def set_status(self, status: int) -> None:
        """Set player status"""
        self.status = status

    def is_online(self) -> bool:
        """Check if player is online"""
        return self.status == 1

    def is_offline(self) -> bool:
        """Check if player is offline"""
        return self.status == 0

    def is_away(self) -> bool:
        """Check if player is away"""
        return self.status == 2

    def is_in_battle(self) -> bool:
        """Check if player is in battle"""
        return self.status == 3

    def get_status_name(self) -> str:
        """Get human-readable status name"""
        statuses = {0: "Offline", 1: "Online", 2: "Away", 3: "In Battle"}
        return statuses.get(self.status, "Unknown")

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_long(self.player_id)
        self.stream.write_v_int(self.status)
        self.stream.write_string(self.location)
        self.stream.write_v_int(self.last_seen_timestamp)

    def decode(self) -> None:
        """Decode message from stream"""
        self.player_id = self.stream.read_v_long()
        self.status = self.stream.read_v_int()
        self.location = self.stream.read_string()
        self.last_seen_timestamp = self.stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        location_info = f" at {self.location}" if self.location else ""
        return f"PlayerStatusMessage(id={self.player_id}, {self.get_status_name()}{location_info})"
