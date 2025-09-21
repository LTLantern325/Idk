"""
Python conversion of Supercell.Laser.Logic.Message.Udp.UdpConnectionInfoMessage.cs
UDP connection info message for UDP connection details
"""

from ..game_message import GameMessage

class UdpConnectionInfoMessage(GameMessage):
    """UDP connection info message for UDP connection details"""

    def __init__(self):
        """Initialize UDP connection info message"""
        super().__init__()
        self.server_host = ""
        self.server_port = 0
        self.session_key = ""
        self.connection_id = 0
        self.udp_enabled = True

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24001  # Placeholder message type

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 1

    def get_server_host(self) -> str:
        """Get server host"""
        return self.server_host

    def set_server_host(self, host: str) -> None:
        """Set server host"""
        self.server_host = host

    def get_server_port(self) -> int:
        """Get server port"""
        return self.server_port

    def set_server_port(self, port: int) -> None:
        """Set server port"""
        self.server_port = max(0, min(65535, port))

    def get_session_key(self) -> str:
        """Get session key"""
        return self.session_key

    def set_session_key(self, key: str) -> None:
        """Set session key"""
        self.session_key = key

    def is_udp_enabled(self) -> bool:
        """Check if UDP is enabled"""
        return self.udp_enabled

    def set_udp_enabled(self, enabled: bool) -> None:
        """Set UDP enabled status"""
        self.udp_enabled = enabled

    def is_valid_connection(self) -> bool:
        """Check if connection info is valid"""
        return (self.server_host != "" and self.server_port > 0 and 
                self.session_key != "" and self.connection_id > 0)

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_string(self.server_host)
        self.stream.write_v_int(self.server_port)
        self.stream.write_string(self.session_key)
        self.stream.write_v_int(self.connection_id)
        self.stream.write_boolean(self.udp_enabled)

    def decode(self) -> None:
        """Decode message from stream"""
        self.server_host = self.stream.read_string()
        self.server_port = self.stream.read_v_int()
        self.session_key = self.stream.read_string()
        self.connection_id = self.stream.read_v_int()
        self.udp_enabled = self.stream.read_boolean()

    def __str__(self) -> str:
        """String representation"""
        return (f"UdpConnectionInfoMessage({self.server_host}:{self.server_port}, "
                f"udp={'enabled' if self.udp_enabled else 'disabled'})")
