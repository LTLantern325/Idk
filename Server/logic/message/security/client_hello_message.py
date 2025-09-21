"""
Python conversion of Supercell.Laser.Logic.Message.Security.ClientHelloMessage.cs
Client hello message for connection initiation
"""

from ..game_message import GameMessage

class ClientHelloMessage(GameMessage):
    """Client hello message for connection initiation"""

    def __init__(self):
        """Initialize client hello message"""
        super().__init__()
        self.key_version = 0
        self.client_seed = 0
        self.major_version = 0

    def get_key_version(self) -> int:
        """Get key version"""
        return self.key_version

    def set_key_version(self, version: int) -> None:
        """Set key version"""
        self.key_version = version

    def get_client_seed(self) -> int:
        """Get client seed"""
        return self.client_seed

    def set_client_seed(self, seed: int) -> None:
        """Set client seed"""
        self.client_seed = seed

    def get_major_version(self) -> int:
        """Get major version"""
        return self.major_version

    def set_major_version(self, version: int) -> None:
        """Set major version"""
        self.major_version = version

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 10100

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 1

    def decode(self) -> None:
        """Decode message from stream"""
        # Skip first int
        self.stream.read_int()

        # Read key version
        self.key_version = self.stream.read_int()

        # Read major version  
        self.major_version = self.stream.read_int()

        # Read client seed
        self.client_seed = self.stream.read_int()

    def encode(self) -> None:
        """Encode message to stream"""
        # Write placeholder int
        self.stream.write_int(0)

        # Write key version
        self.stream.write_int(self.key_version)

        # Write major version
        self.stream.write_int(self.major_version)

        # Write client seed
        self.stream.write_int(self.client_seed)

    def is_valid_version(self) -> bool:
        """Check if version is valid"""
        return self.major_version > 0 and self.key_version >= 0

    def __str__(self) -> str:
        """String representation"""
        return (f"ClientHelloMessage(major_ver={self.major_version}, "
                f"key_ver={self.key_version}, seed={self.client_seed})")
