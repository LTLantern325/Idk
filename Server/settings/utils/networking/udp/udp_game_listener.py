"""
Python conversion of Supercell.Laser.Server.Networking.UDP.Game.UDPGameListener.cs
UDP game listener for battle communications
"""

from logic.listener.logic_game_listener import LogicGameListener
from logic.message.game_message import GameMessage
from networking.udp.udp_socket import UDPSocket
from networking.connection import Connection
from logger import Logger

class UDPGameListener(LogicGameListener):
    """UDP game listener implementation"""

    def __init__(self, udp_socket: UDPSocket, tcp_connection: Connection):
        """Initialize UDP game listener"""
        super().__init__()
        self.socket = udp_socket
        self.tcp_connection = tcp_connection

    def send_message(self, message: GameMessage) -> None:
        """Send message via UDP"""
        try:
            self.socket.send_message(message)
        except Exception as e:
            Logger.error(f"Error sending UDP message: {e}")

    def send_tcp_message(self, message: GameMessage) -> None:
        """Send message via TCP connection"""
        try:
            if self.tcp_connection:
                self.tcp_connection.send(message)
        except Exception as e:
            Logger.error(f"Error sending TCP message: {e}")

    def close(self) -> None:
        """Close listener"""
        try:
            if self.socket:
                self.socket.close()
        except Exception as e:
            Logger.error(f"Error closing UDP game listener: {e}")
