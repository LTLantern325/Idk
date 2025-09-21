"""
Python conversion of Supercell.Laser.Server.Networking.Connections.cs
Connection management system
"""

import threading
import time
from typing import List, Optional
from datetime import datetime

from networking.connection import Connection
from networking.session.sessions import Sessions
from logger import Logger

class MasudaBot:
    """Simplified MasudaBot placeholder"""
    def __init__(self, *args, **kwargs):
        pass

    def log_to(self, target):
        return self

    def modify_channel_async(self, *args):
        pass

class Connections:
    """Static class for managing active connections"""

    _active_connections: List[Connection] = []
    _thread: Optional[threading.Thread] = None
    _seconds_gone: int = 0
    _running: bool = False
    bot: Optional[MasudaBot] = None

    @classmethod
    @property
    def count(cls) -> int:
        """Get active connection count"""
        return len(cls._active_connections)

    @classmethod
    def init(cls) -> None:
        """Initialize connection manager"""
        cls._active_connections = []
        cls.bot = MasudaBot(102038674, "ElazeGW3722wbRMI9StXcSJbvsRLitBm", "ElazeGW3722wbRMI9StXcSJbvsRLitBm", "Public").log_to(None)
        cls._running = True
        cls._seconds_gone = 0

        cls._thread = threading.Thread(target=cls._update, daemon=True)
        cls._thread.start()

    @classmethod
    def _update(cls) -> None:
        """Update connections in background"""
        while cls._running:
            try:
                # Check all connections
                connections_to_remove = []
                for connection in cls._active_connections[:]:
                    # Remove connections without active sessions
                    if connection.avatar and not Sessions.is_session_active(connection.avatar.account_id):
                        connection.close()
                        connections_to_remove.append(connection)

                    # Remove dead connections
                    elif not connection.message_manager.is_alive():
                        if connection.message_manager.home_mode:
                            Sessions.remove(connection.avatar.account_id)
                        connection.close()
                        connections_to_remove.append(connection)

                # Remove dead connections
                for connection in connections_to_remove:
                    if connection in cls._active_connections:
                        cls._active_connections.remove(connection)

                # Update bot status every 30 seconds
                if cls._seconds_gone % 30 == 0:
                    try:
                        cls.bot.modify_channel_async("216185176", f"服务器在线人数：{cls.count}", 0, 4, "141954264")
                    except Exception:
                        pass

                cls._seconds_gone += 1
                time.sleep(1)

            except Exception as e:
                Logger.error(f"Error in connections update: {e}")
                time.sleep(1)

    @classmethod
    def add_connection(cls, connection: Connection) -> None:
        """Add new connection"""
        cls._active_connections.append(connection)
        Logger.print_log(f"Connection added. Total: {cls.count}")

    @classmethod
    def remove_connection(cls, connection: Connection) -> None:
        """Remove connection"""
        if connection in cls._active_connections:
            cls._active_connections.remove(connection)
            Logger.print_log(f"Connection removed. Total: {cls.count}")

    @classmethod
    def get_connections(cls) -> List[Connection]:
        """Get list of active connections"""
        return cls._active_connections.copy()

    @classmethod
    def shutdown(cls) -> None:
        """Shutdown connection manager"""
        cls._running = False
        if cls._thread and cls._thread.is_alive():
            cls._thread.join(timeout=5)

        # Close all connections
        for connection in cls._active_connections[:]:
            connection.close()
        cls._active_connections.clear()
