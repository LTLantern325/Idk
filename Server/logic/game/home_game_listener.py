"""
Python conversion of Supercell.Laser.Server.Logic.HomeGameListener.cs
Game listener for home mode connections
"""

from logic.listener.logic_game_listener import LogicGameListener
from networking.connection import Connection
from logic.message.game_message import GameMessage

class HomeGameListener(LogicGameListener):
    """Game listener implementation for home mode"""

    def __init__(self, connection: Connection):
        """Initialize with connection"""
        super().__init__()
        self.connection = connection

    def send_message(self, message: GameMessage) -> None:
        """Send message to client"""
        self.connection.send(message)

    def send_tcp_message(self, message: GameMessage) -> None:
        """Send TCP message to client"""
        self.connection.send(message)
