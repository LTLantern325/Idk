"""
Python conversion of networking Connection class (simplified)
Basic connection handling for server
"""

from typing import Optional, Any
from datetime import datetime
import socket

class Connection:
    """Basic connection class for client connections"""

    def __init__(self, client_socket: socket.socket, address: tuple):
        """Initialize connection"""
        self.socket = client_socket
        self.address = address
        self.is_open = True
        self.message_manager: Optional[Any] = None
        self.messaging: Optional[Any] = None
        self.home: Optional[Any] = None
        self.avatar: Optional[Any] = None
        self.udp_session_id: int = 0
        self.matchmake_slot: int = -1
        self.matchmaking_entry: Optional[Any] = None
        self.nonce: str = ""
        self.created_time = datetime.utcnow()

    def send(self, message: Any) -> None:
        """Send message to client"""
        if self.messaging and self.is_open:
            try:
                self.messaging.encrypt_and_write(message)
            except Exception as e:
                print(f"Error sending message: {e}")
                self.close()

    def close(self) -> None:
        """Close connection"""
        self.is_open = False
        try:
            if self.socket:
                self.socket.close()
        except Exception:
            pass

    def ping_updated(self, ping: int) -> None:
        """Update ping information"""
        # Handle ping update
        pass

class Connections:
    """Static class for managing connections"""

    _connections: list = []

    @classmethod
    def init(cls) -> None:
        """Initialize connections manager"""
        cls._connections = []

    @classmethod
    def add(cls, connection: Connection) -> None:
        """Add connection"""
        cls._connections.append(connection)

    @classmethod
    def remove(cls, connection: Connection) -> None:
        """Remove connection"""
        if connection in cls._connections:
            cls._connections.remove(connection)

    @classmethod
    def get_count(cls) -> int:
        """Get connection count"""
        return len(cls._connections)

    @classmethod
    def close_all(cls) -> None:
        """Close all connections"""
        for connection in cls._connections[:]:
            connection.close()
        cls._connections.clear()
