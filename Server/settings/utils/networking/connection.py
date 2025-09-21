"""
Python conversion of Supercell.Laser.Server.Networking.Connection.cs
Real connection class for client connections
"""

import socket
from io import BytesIO
from typing import Optional, Any

from logic.avatar.client_avatar import ClientAvatar
from logic.home.client_home import ClientHome
from logic.message.game_message import GameMessage
from networking.messaging import Messaging
from message.message_manager import MessageManager

class Connection:
    """Connection class for client connections"""

    def __init__(self, client_socket: socket.socket, address: tuple):
        """Initialize connection"""
        self.socket = client_socket
        self.address = address
        self.read_buffer = bytearray(1024)
        self.memory = BytesIO()
        self.is_open = True
        self.ping = 0

        # Connection state
        self.matchmake_slot = -1
        self.matchmaking_entry: Optional[Any] = None
        self.udp_session_id = -1
        self.nonce = ""

        # Initialize messaging and message manager
        self.messaging = Messaging(self)
        self.message_manager = MessageManager(self)

    @property
    def home(self) -> Optional[ClientHome]:
        """Get client home"""
        if self.message_manager.home_mode:
            return self.message_manager.home_mode.home
        return None

    @property
    def avatar(self) -> Optional[ClientAvatar]:
        """Get client avatar"""
        if self.message_manager.home_mode:
            return self.message_manager.home_mode.avatar
        return None

    def ping_updated(self, value: int) -> None:
        """Update ping value"""
        self.ping = value

    def send(self, message: GameMessage) -> None:
        """Send message to client"""
        self.messaging.send(message)

    def write(self, data: bytes) -> None:
        """Write raw data to socket"""
        try:
            if self.is_open:
                self.socket.send(data)
        except Exception:
            self.close()

    def close(self) -> None:
        """Close connection"""
        try:
            self.is_open = False
            if self.socket:
                self.socket.close()
        except Exception:
            pass

    def __str__(self) -> str:
        """String representation"""
        return f"Connection({self.address})"

    def __repr__(self) -> str:
        """Developer representation"""
        return f"Connection(address={self.address}, open={self.is_open})"
