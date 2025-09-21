"""
Message factory for creating game messages
"""

from typing import Optional, Dict, Type, Callable
from logic.message.game_message import GameMessage
from logic.message.account.client_hello_message import ClientHelloMessage
from logic.message.account.auth.authentication_message import AuthenticationMessage

class MessageFactory:
    """Factory for creating game messages by type"""

    instance: Optional['MessageFactory'] = None

    def __init__(self):
        """Initialize message factory"""
        self._message_types: Dict[int, Type[GameMessage]] = {}
        self._register_default_messages()

    def _register_default_messages(self) -> None:
        """Register default message types"""
        # Register core message types
        self.register_message(10100, ClientHelloMessage)
        self.register_message(10101, AuthenticationMessage)
        # Add more message types as needed

    def register_message(self, message_type: int, message_class: Type[GameMessage]) -> None:
        """Register message type"""
        self._message_types[message_type] = message_class

    def create_message_by_type(self, message_type: int) -> Optional[GameMessage]:
        """Create message instance by type"""
        try:
            message_class = self._message_types.get(message_type)
            if message_class:
                return message_class()
            return None
        except Exception as e:
            print(f"Error creating message type {message_type}: {e}")
            return None

    @classmethod
    def get_instance(cls) -> 'MessageFactory':
        """Get singleton instance"""
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

# Initialize singleton
MessageFactory.instance = MessageFactory.get_instance()
