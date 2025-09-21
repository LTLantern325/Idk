"""
Python conversion of Supercell.Laser.Logic.Message.Security.ServerHelloMessage.cs
Server hello message response (simplified version)
"""

from ..game_message import GameMessage

class ServerHelloMessage(GameMessage):
    """Server hello message response"""

    def __init__(self):
        """Initialize server hello message"""
        super().__init__()
        self.server_seed = 0
        self.server_build = ""
        self.content_version = ""
        self.server_environment = ""
        self.session_count = 0
        self.playbot_count = 0
        self.day_change_seconds_left = 0
        self.maintenance_remaining_seconds = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 20100  # Server hello response

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 1

    def set_server_seed(self, seed: int) -> None:
        """Set server seed"""
        self.server_seed = seed

    def get_server_seed(self) -> int:
        """Get server seed"""
        return self.server_seed

    def set_server_build(self, build: str) -> None:
        """Set server build version"""
        self.server_build = build

    def get_server_build(self) -> str:
        """Get server build version"""
        return self.server_build

    def set_content_version(self, version: str) -> None:
        """Set content version"""
        self.content_version = version

    def get_content_version(self) -> str:
        """Get content version"""
        return self.content_version

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_int(self.server_seed)
        self.stream.write_string(self.server_build)
        self.stream.write_string(self.content_version)
        self.stream.write_string(self.server_environment)
        self.stream.write_int(self.session_count)
        self.stream.write_int(self.playbot_count)
        self.stream.write_int(self.day_change_seconds_left)
        self.stream.write_int(self.maintenance_remaining_seconds)

    def decode(self) -> None:
        """Decode message from stream"""
        self.server_seed = self.stream.read_int()
        self.server_build = self.stream.read_string()
        self.content_version = self.stream.read_string()
        self.server_environment = self.stream.read_string()
        self.session_count = self.stream.read_int()
        self.playbot_count = self.stream.read_int()
        self.day_change_seconds_left = self.stream.read_int()
        self.maintenance_remaining_seconds = self.stream.read_int()

    def __str__(self) -> str:
        """String representation"""
        return (f"ServerHelloMessage(build='{self.server_build}', "
                f"content='{self.content_version}', seed={self.server_seed})")
