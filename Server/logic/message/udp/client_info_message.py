"""
Python conversion of Supercell.Laser.Logic.Message.Udp.ClientInfoMessage.cs
Client info message for UDP connections
"""

from ..game_message import GameMessage

class ClientInfoMessage(GameMessage):
    """Client info message for UDP connections"""

    def __init__(self):
        """Initialize client info message"""
        super().__init__()
        self.client_version = ""
        self.device_model = ""
        self.operating_system = ""
        self.advertising_id = ""
        self.device_id = ""
        self.preferred_language = "en"
        self.connection_type = 0  # 0=WiFi, 1=Mobile

    def get_message_type(self) -> int:
        """Get message type ID"""  
        return 10177

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 1

    def get_client_version(self) -> str:
        """Get client version"""
        return self.client_version

    def set_client_version(self, version: str) -> None:
        """Set client version"""
        self.client_version = version

    def get_device_model(self) -> str:
        """Get device model"""
        return self.device_model

    def set_device_model(self, model: str) -> None:
        """Set device model"""
        self.device_model = model

    def get_operating_system(self) -> str:
        """Get operating system"""
        return self.operating_system

    def set_operating_system(self, os: str) -> None:
        """Set operating system"""
        self.operating_system = os

    def is_wifi_connection(self) -> bool:
        """Check if using WiFi"""
        return self.connection_type == 0

    def is_mobile_connection(self) -> bool:
        """Check if using mobile data"""
        return self.connection_type == 1

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_string(self.client_version)
        self.stream.write_string(self.device_model)
        self.stream.write_string(self.operating_system)
        self.stream.write_string(self.advertising_id)
        self.stream.write_string(self.device_id)
        self.stream.write_string(self.preferred_language)
        self.stream.write_v_int(self.connection_type)

    def decode(self) -> None:
        """Decode message from stream"""
        self.client_version = self.stream.read_string()
        self.device_model = self.stream.read_string()
        self.operating_system = self.stream.read_string()
        self.advertising_id = self.stream.read_string()
        self.device_id = self.stream.read_string()
        self.preferred_language = self.stream.read_string()
        self.connection_type = self.stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        return (f"ClientInfoMessage(version={self.client_version}, "
                f"device={self.device_model}, os={self.operating_system})")
