"""
Python conversion of Supercell.Laser.Logic.Message.GameMessage.cs
Base game message class
"""

from abc import ABC, abstractmethod
from typing import Optional

class GameMessage(ABC):
    """Base class for all game messages"""

    def __init__(self):
        """Initialize game message"""
        self.version = 1
        self.account_id = 0
        self.session_id = 0

    @abstractmethod
    def get_message_type(self) -> int:
        """Get message type ID"""
        pass

    @abstractmethod
    def encode(self, stream) -> None:
        """Encode message to stream"""
        pass

    @abstractmethod
    def decode(self, stream) -> None:
        """Decode message from stream"""
        pass

    def get_message_version(self) -> int:
        """Get message version"""
        return self.version

    def set_message_version(self, version: int) -> None:
        """Set message version"""
        self.version = version

    def get_account_id(self) -> int:
        """Get account ID"""
        return self.account_id

    def set_account_id(self, account_id: int) -> None:
        """Set account ID"""
        self.account_id = account_id

    def get_session_id(self) -> int:
        """Get session ID"""
        return self.session_id

    def set_session_id(self, session_id: int) -> None:
        """Set session ID"""
        self.session_id = session_id

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 1  # Default service node

    def get_encoding_length(self) -> int:
        """Get encoding length (to be overridden)"""
        return 0

    def __str__(self) -> str:
        """String representation"""
        return f"{self.__class__.__name__}(type={self.get_message_type()}, account={self.account_id})"
