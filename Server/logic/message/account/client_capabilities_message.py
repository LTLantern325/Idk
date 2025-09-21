"""
Python conversion of Supercell.Laser.Logic.Message.Account.ClientCapabilitiesMessage.cs
Client capabilities message for reporting client features
"""

from ..game_message import GameMessage

class ClientCapabilitiesMessage(GameMessage):
    """Client capabilities message for reporting client features"""

    def __init__(self):
        """Initialize client capabilities message"""
        super().__init__()
        self.ping_url = ""
        self.client_version = ""
        self.supported_compression = 0
        self.device_performance_level = 0
        self.platform = ""
        self.device_language = ""
        self.advertising_gaid = ""

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 10107

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 1

    def get_ping_url(self) -> str:
        """Get ping URL"""
        return self.ping_url

    def set_ping_url(self, url: str) -> None:
        """Set ping URL"""
        self.ping_url = url

    def get_client_version(self) -> str:
        """Get client version"""
        return self.client_version

    def set_client_version(self, version: str) -> None:
        """Set client version"""
        self.client_version = version

    def supports_compression(self) -> bool:
        """Check if client supports compression"""
        return self.supported_compression > 0

    def get_device_performance_level(self) -> int:
        """Get device performance level (0=low, 1=medium, 2=high)"""
        return self.device_performance_level

    def set_device_performance_level(self, level: int) -> None:
        """Set device performance level"""
        self.device_performance_level = max(0, min(2, level))

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_string(self.ping_url)
        self.stream.write_string(self.client_version)
        self.stream.write_v_int(self.supported_compression)
        self.stream.write_v_int(self.device_performance_level)
        self.stream.write_string(self.platform)
        self.stream.write_string(self.device_language)
        self.stream.write_string(self.advertising_gaid)

    def decode(self) -> None:
        """Decode message from stream"""
        self.ping_url = self.stream.read_string()
        self.client_version = self.stream.read_string()
        self.supported_compression = self.stream.read_v_int()
        self.device_performance_level = self.stream.read_v_int()
        self.platform = self.stream.read_string()
        self.device_language = self.stream.read_string()
        self.advertising_gaid = self.stream.read_string()

    def __str__(self) -> str:
        """String representation"""
        return (f"ClientCapabilitiesMessage(version={self.client_version}, "
                f"perf_level={self.device_performance_level})")
