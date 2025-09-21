"""
Python conversion of Supercell.Laser.Logic.Listener.LogicGameListener.cs
Game listener for handling messages
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..message.game_message import GameMessage

class LogicGameListener(ABC):
    """Abstract game listener for message handling"""

    def __init__(self):
        """Initialize game listener"""
        self.handled_inputs = 0

    @abstractmethod
    def send_message(self, message: 'GameMessage') -> None:
        """Send message (UDP)"""
        pass

    @abstractmethod
    def send_tcp_message(self, message: 'GameMessage') -> None:
        """Send TCP message"""
        pass

    def increment_handled_inputs(self) -> None:
        """Increment handled inputs counter"""
        self.handled_inputs += 1

    def get_handled_inputs(self) -> int:
        """Get handled inputs count"""
        return self.handled_inputs

    def reset_handled_inputs(self) -> None:
        """Reset handled inputs counter"""
        self.handled_inputs = 0

    def send_message_safe(self, message: 'GameMessage') -> bool:
        """Send message with error handling"""
        try:
            self.send_message(message)
            return True
        except Exception:
            return False

    def send_tcp_message_safe(self, message: 'GameMessage') -> bool:
        """Send TCP message with error handling"""
        try:
            self.send_tcp_message(message)
            return True
        except Exception:
            return False

    def __str__(self) -> str:
        """String representation"""
        return f"{self.__class__.__name__}(handled_inputs={self.handled_inputs})"
