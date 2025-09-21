"""
Python conversion of Supercell.Laser.Logic.Message.GameMessage.cs
Base game message class for all network messages
"""

from abc import ABC, abstractmethod
from typing import Optional
from ..titan.datastream.byte_stream import ByteStream

class GameMessage(ABC):
    """Base class for all game messages"""

    def __init__(self):
        """Initialize game message"""
        self.stream = ByteStream(10)
        self._version = 0

    def encode(self) -> None:
        """Encode message data to stream"""
        # Default implementation - can be overridden
        pass

    def decode(self) -> None:
        """Decode message data from stream"""
        # Default implementation - can be overridden
        pass

    @abstractmethod
    def get_message_type(self) -> int:
        """Get message type ID"""
        pass

    @abstractmethod
    def get_service_node_type(self) -> int:
        """Get service node type"""
        pass

    def set_version(self, version: int) -> None:
        """Set message version"""
        self._version = version

    def get_version(self) -> int:
        """Get message version"""
        return self._version

    def get_byte_stream(self) -> ByteStream:
        """Get underlying byte stream"""
        return self.stream

    def get_message_bytes(self) -> bytes:
        """Get message as byte array"""
        return self.stream.get_byte_array()

    def get_encoding_length(self) -> int:
        """Get encoded message length"""
        return self.stream.get_offset()

    def reset_stream(self) -> None:
        """Reset the byte stream"""
        self.stream = ByteStream(10)

    def is_encoded(self) -> bool:
        """Check if message has been encoded"""
        return self.stream.get_offset() > 0

    def __str__(self) -> str:
        """String representation"""
        return f"GameMessage(type={self.get_message_type()}, version={self._version})"
