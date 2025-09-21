"""
Python conversion of Supercell.Laser.Logic.Message.Home.LobbyInfoMessage.cs
Lobby info message for lobby information
"""

from ..game_message import GameMessage

class LobbyInfoMessage(GameMessage):
    """Lobby info message for lobby information"""

    def __init__(self):
        """Initialize lobby info message"""
        super().__init__()
        self.player_count = 0
        self.active_events = 0
        self.server_time = 0
        self.next_shop_refresh = 0
        self.maintenance_mode = False

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 23457  # Lobby info

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_player_count(self) -> int:
        """Get online player count"""
        return self.player_count

    def set_player_count(self, count: int) -> None:
        """Set online player count"""
        self.player_count = max(0, count)

    def get_active_events(self) -> int:
        """Get number of active events"""
        return self.active_events

    def set_active_events(self, events: int) -> None:
        """Set number of active events"""
        self.active_events = max(0, events)

    def is_maintenance_mode(self) -> bool:
        """Check if server is in maintenance mode"""
        return self.maintenance_mode

    def set_maintenance_mode(self, maintenance: bool) -> None:
        """Set maintenance mode"""
        self.maintenance_mode = maintenance

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.player_count)
        self.stream.write_v_int(self.active_events)
        self.stream.write_v_int(self.server_time)
        self.stream.write_v_int(self.next_shop_refresh)
        self.stream.write_boolean(self.maintenance_mode)
        self.stream.write_string("LTBrawl v53!")

    def decode(self) -> None:
        """Decode message from stream"""
        self.player_count = self.stream.read_v_int()
        self.active_events = self.stream.read_v_int()
        self.server_time = self.stream.read_v_int()
        self.next_shop_refresh = self.stream.read_v_int()
        self.maintenance_mode = self.stream.read_boolean()

    def __str__(self) -> str:
        """String representation"""
        maintenance_info = " (maintenance)" if self.maintenance_mode else ""
        return (f"LobbyInfoMessage(players={self.player_count}, "
                f"events={self.active_events}{maintenance_info})")
