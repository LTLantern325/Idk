"""
Python conversion of Supercell.Laser.Server.Networking.TCPGateway.cs
TCP server gateway for client connections
"""

import socket
import threading
import select
from typing import List, Optional
import time

from networking.connection import Connection
from networking.connections import Connections
from logic.game.battles import Battles
from networking.session.sessions import Sessions
from logger import Logger

class ContentServer:
    """HTTP content server (placeholder)"""

    _http_listener = None

    @classmethod
    def init(cls, host: str, port: int) -> None:
        """Initialize HTTP content server"""
        # Placeholder implementation
        Logger.print_log(f"Content server initialized at {host}:{port}")

class TCPGateway:
    """TCP gateway for handling client connections"""

    _active_connections: List[Connection] = []
    _socket: Optional[socket.socket] = None
    _thread: Optional[threading.Thread] = None
    _running: bool = False
    _accept_event: Optional[threading.Event] = None

    @classmethod
    def init(cls, host: str, port: int) -> None:
        """Initialize TCP gateway"""
        cls._active_connections = []
        cls._running = True

        # Create server socket
        cls._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        cls._socket.bind((host, port))
        cls._socket.listen(100)
        cls._socket.setblocking(False)

        cls._accept_event = threading.Event()

        # Start accept thread
        cls._thread = threading.Thread(target=cls._update, daemon=True)
        cls._thread.start()

        Logger.print_log(f"TCP Server started at {host}:{port}")

    @classmethod
    def _update(cls) -> None:
        """Main server loop"""
        while cls._running:
            try:
                # Use select to check for incoming connections
                ready_sockets, _, _ = select.select([cls._socket], [], [], 1.0)

                if ready_sockets:
                    try:
                        client_socket, address = cls._socket.accept()
                        cls._on_accept(client_socket, address)
                    except socket.error as e:
                        if cls._running:  # Only log if we're still supposed to be running
                            Logger.error(f"Error accepting connection: {e}")

            except Exception as e:
                if cls._running:
                    Logger.error(f"Error in TCP gateway update: {e}")
                time.sleep(0.1)

    @classmethod
    def _on_accept(cls, client_socket: socket.socket, address: tuple) -> None:
        """Handle new client connection"""
        try:
            client_socket.setblocking(False)
            connection = Connection(client_socket, address)
            cls._active_connections.append(connection)

            Logger.print_log(f"New connection from {address}")
            Connections.add_connection(connection)

            # Start receiving data for this connection
            threading.Thread(target=cls._handle_connection, args=(connection,), daemon=True).start()

        except Exception as e:
            Logger.error(f"Error handling new connection: {e}")
            try:
                client_socket.close()
            except:
                pass

    @classmethod
    def _handle_connection(cls, connection: Connection) -> None:
        """Handle individual connection"""
        try:
            while connection.is_open and cls._running:
                try:
                    # Use select to check for data
                    ready_sockets, _, error_sockets = select.select([connection.socket], [], [connection.socket], 1.0)

                    if error_sockets:
                        Logger.print_log("Client disconnected (socket error)")
                        cls._disconnect_client(connection)
                        break

                    if ready_sockets:
                        # Receive data
                        data = connection.socket.recv(1024)

                        if not data:
                            Logger.print_log("Client disconnected")
                            cls._disconnect_client(connection)
                            break

                        # Write to connection memory
                        connection.memory.write(data)

                        # Process messages
                        if connection.messaging.on_receive() != 0:
                            Logger.print_log("Client disconnected (message processing error)")
                            cls._disconnect_client(connection)
                            break

                except socket.error:
                    Logger.print_log("Client disconnected (socket error)")
                    cls._disconnect_client(connection)
                    break
                except Exception as e:
                    Logger.error(f"Error handling connection: {e}")
                    cls._disconnect_client(connection)
                    break

        except Exception as e:
            Logger.error(f"Unhandled exception in connection handler: {e}")
            cls._disconnect_client(connection)

    @classmethod
    def _disconnect_client(cls, connection: Connection) -> None:
        """Handle client disconnection"""
        try:
            # Remove from active connections
            if connection in cls._active_connections:
                cls._active_connections.remove(connection)

            # Clean up session
            if connection.message_manager and connection.message_manager.home_mode:
                Sessions.remove(connection.avatar.account_id)

                # Remove from battle if in one
                if connection.home and connection.home.home_mode.avatar.battle_id > 0:
                    battle = Battles.get(connection.home.home_mode.avatar.battle_id)
                    if battle:
                        player = battle.get_player_by_session_id(connection.udp_session_id)
                        if player:
                            battle.remove_player(player)

            # Close connection
            connection.close()

        except Exception as e:
            Logger.error(f"Error during client disconnect: {e}")

    @classmethod
    def on_send(cls, socket_obj: socket.socket) -> None:
        """Handle send completion (callback)"""
        # Placeholder for send completion handling
        pass

    @classmethod
    def shutdown(cls) -> None:
        """Shutdown TCP gateway"""
        cls._running = False

        if cls._socket:
            cls._socket.close()

        if cls._thread and cls._thread.is_alive():
            cls._thread.join(timeout=5)

        # Close all connections
        for connection in cls._active_connections[:]:
            connection.close()
        cls._active_connections.clear()

        Logger.print_log("TCP Gateway shut down")
