"""
Python conversion of Supercell.Laser.Server.Networking.UDP.UDPSocket.cs
Individual UDP socket for battle communications
"""

import socket
from typing import Optional, Any

from logic.message.game_message import GameMessage
from networking.connection import Connection
from logic.battle.battle_mode import BattleMode
from logger import Logger

class UDPSocket:
    """UDP socket for battle communications"""

    def __init__(self, session_id: int, gateway_socket: socket.socket):
        """Initialize UDP socket"""
        self.session_id = session_id
        self.gateway_socket = gateway_socket
        self.tcp_connection: Optional[Connection] = None
        self.battle: Optional[BattleMode] = None
        self.is_spectator = False
        self.client_address: Optional[tuple] = None
        self.is_active = True

    def send_message(self, message: GameMessage) -> None:
        """Send message via UDP"""
        try:
            if not self.is_active or not self.client_address:
                return

            # Encode message
            if message.get_encoding_length() == 0:
                message.encode()

            data = message.get_message_bytes()

            # Send via UDP gateway
            from networking.udp.udp_gateway import UDPGateway
            UDPGateway.send_packet(self.session_id, data, self.client_address)

        except Exception as e:
            Logger.error(f"Error sending UDP message: {e}")

    def on_receive(self, data: bytes, address: tuple) -> None:
        """Handle received UDP data"""
        try:
            # Store client address
            if not self.client_address:
                self.client_address = address

            # Process message data
            if len(data) < 7:  # Minimum message header size
                return

            # Extract message type and process
            # This would normally decode the UDP battle message
            # For now, just forward to battle if available
            if self.battle:
                self.battle.process_udp_message(self.session_id, data)

        except Exception as e:
            Logger.error(f"Error processing UDP data: {e}")

    def close(self) -> None:
        """Close UDP socket"""
        try:
            self.is_active = False

            # Remove from UDP gateway
            from networking.udp.udp_gateway import UDPGateway
            UDPGateway.remove_socket(self.session_id)

        except Exception as e:
            Logger.error(f"Error closing UDP socket: {e}")

    def __str__(self) -> str:
        """String representation"""
        return f"UDPSocket(session_id={self.session_id}, active={self.is_active})"
