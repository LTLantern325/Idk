"""
Python conversion of Supercell.Laser.Server.Networking.UDP.UDPGateway.cs
UDP gateway for battle communications
"""

import socket
import threading
import time
from typing import Dict, Optional
import struct

from networking.udp.udp_socket import UDPSocket
from logger import Logger

class UDPGateway:
    """UDP gateway for handling battle communications"""

    _socket: Optional[socket.socket] = None
    _sockets: Dict[int, UDPSocket] = {}
    _session_id_counter: int = 0
    _thread: Optional[threading.Thread] = None
    _running: bool = False
    _lock = threading.RLock()

    @classmethod
    def init(cls, host: str, port: int) -> None:
        """Initialize UDP gateway"""
        cls._running = True
        cls._sockets = {}
        cls._session_id_counter = 0

        # Create UDP socket
        cls._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cls._socket.bind((host, port))
        cls._socket.setblocking(False)

        # Start receive thread
        cls._thread = threading.Thread(target=cls._update, daemon=True)
        cls._thread.start()

        Logger.print_log(f"UDP Gateway started at {host}:{port}")

    @classmethod
    def _update(cls) -> None:
        """Main UDP receive loop"""
        while cls._running:
            try:
                import select
                ready, _, _ = select.select([cls._socket], [], [], 1.0)

                if ready:
                    data, address = cls._socket.recvfrom(2048)
                    if len(data) >= 7:
                        cls._process_packet(data, address)

            except socket.error:
                if cls._running:
                    time.sleep(0.01)
            except Exception as e:
                if cls._running:
                    Logger.error(f"Error in UDP gateway: {e}")
                time.sleep(0.01)

    @classmethod
    def _process_packet(cls, data: bytes, address: tuple) -> None:
        """Process incoming UDP packet"""
        try:
            # Extract session ID from packet header
            if len(data) < 4:
                return

            session_id = struct.unpack('>I', data[:4])[0]

            with cls._lock:
                udp_socket = cls._sockets.get(session_id)
                if udp_socket:
                    udp_socket.on_receive(data[4:], address)

        except Exception as e:
            Logger.error(f"Error processing UDP packet: {e}")

    @classmethod
    def create_socket(cls) -> UDPSocket:
        """Create new UDP socket"""
        with cls._lock:
            cls._session_id_counter += 1
            session_id = cls._session_id_counter

            udp_socket = UDPSocket(session_id, cls._socket)
            cls._sockets[session_id] = udp_socket

            return udp_socket

    @classmethod
    def remove_socket(cls, session_id: int) -> None:
        """Remove UDP socket"""
        with cls._lock:
            if session_id in cls._sockets:
                del cls._sockets[session_id]

    @classmethod
    def send_packet(cls, session_id: int, data: bytes, address: tuple) -> None:
        """Send UDP packet"""
        try:
            if cls._socket and cls._running:
                # Prepend session ID to packet
                packet = struct.pack('>I', session_id) + data
                cls._socket.sendto(packet, address)
        except Exception as e:
            Logger.error(f"Error sending UDP packet: {e}")

    @classmethod
    def get_socket_count(cls) -> int:
        """Get active socket count"""
        with cls._lock:
            return len(cls._sockets)

    @classmethod
    def shutdown(cls) -> None:
        """Shutdown UDP gateway"""
        cls._running = False

        if cls._thread and cls._thread.is_alive():
            cls._thread.join(timeout=5)

        if cls._socket:
            cls._socket.close()

        with cls._lock:
            cls._sockets.clear()

        Logger.print_log("UDP Gateway shut down")
