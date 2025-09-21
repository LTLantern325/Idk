"""
Python conversion of Supercell.Laser.Server.Networking.Session.Sessions.cs
Session management system
"""

import threading
from typing import Dict, Optional, List
from datetime import datetime

from networking.connection import Connection
from logic.home.home_mode import HomeMode
from logic.message.team.team_chat_message import TeamChatMessage
from logger import Logger

class Session:
    """Individual session class"""

    def __init__(self, home_mode: HomeMode, connection: Connection):
        self.home_mode = home_mode
        self.connection = connection
        self.game_listener = connection.message_manager
        self.home = home_mode.home if home_mode else None
        self.created_time = datetime.utcnow()

class Sessions:
    """Static session management class"""

    _sessions: Dict[int, Session] = {}
    _lock = threading.RLock()
    _maintenance: bool = False
    _shutting_down: bool = False

    @classmethod
    @property
    def count(cls) -> int:
        """Get session count"""
        with cls._lock:
            return len(cls._sessions)

    @classmethod
    @property
    def maintenance(cls) -> bool:
        """Check if in maintenance mode"""
        return cls._maintenance

    @classmethod
    def set_maintenance(cls, value: bool) -> None:
        """Set maintenance mode"""
        cls._maintenance = value
        Logger.print_log(f"Maintenance mode: {'ON' if value else 'OFF'}")

    @classmethod
    def init(cls) -> None:
        """Initialize sessions"""
        with cls._lock:
            cls._sessions = {}
            cls._maintenance = False
            cls._shutting_down = False
        Logger.print_log("Sessions initialized")

    @classmethod
    def create(cls, home_mode: HomeMode, connection: Connection) -> Optional[Session]:
        """Create new session"""
        if not home_mode or not connection:
            return None

        account_id = home_mode.avatar.account_id

        with cls._lock:
            # Remove existing session if any
            if account_id in cls._sessions:
                old_session = cls._sessions[account_id]
                try:
                    old_session.connection.close()
                except Exception:
                    pass

            # Create new session
            session = Session(home_mode, connection)
            cls._sessions[account_id] = session

        Logger.print_log(f"Session created for account {account_id}")
        return session

    @classmethod
    def remove(cls, account_id: int) -> None:
        """Remove session"""
        with cls._lock:
            if account_id in cls._sessions:
                session = cls._sessions.pop(account_id)
                try:
                    session.connection.close()
                except Exception:
                    pass
                Logger.print_log(f"Session removed for account {account_id}")

    @classmethod
    def get_session(cls, account_id: int) -> Optional[Session]:
        """Get session by account ID"""
        with cls._lock:
            return cls._sessions.get(account_id)

    @classmethod
    def is_session_active(cls, account_id: int) -> bool:
        """Check if session is active"""
        with cls._lock:
            return account_id in cls._sessions

    @classmethod
    def get_all_sessions(cls) -> List[Session]:
        """Get all active sessions"""
        with cls._lock:
            return list(cls._sessions.values())

    @classmethod
    def send_global_message(cls, sender_id: int, sender_name: str, message: str) -> None:
        """Send global chat message to all sessions"""
        with cls._lock:
            for session in cls._sessions.values():
                try:
                    if session.connection and session.connection.is_open:
                        # Create team chat message
                        chat_msg = TeamChatMessage()
                        chat_msg.message = f"[Global] {sender_name}: {message}"
                        session.connection.send(chat_msg)
                except Exception as e:
                    Logger.error(f"Error sending global message: {e}")

    @classmethod
    def start_shutdown(cls) -> None:
        """Start server shutdown process"""
        cls._shutting_down = True
        Logger.print_log("Server shutdown initiated")

        # Disconnect all sessions
        with cls._lock:
            sessions_to_remove = list(cls._sessions.keys())
            for account_id in sessions_to_remove:
                cls.remove(account_id)

    @classmethod
    def get_sessions_by_team(cls, team_id: int) -> List[Session]:
        """Get sessions by team ID"""
        result = []
        with cls._lock:
            for session in cls._sessions.values():
                try:
                    if session.home_mode.avatar.team_id == team_id:
                        result.append(session)
                except Exception:
                    continue
        return result

    @classmethod
    def get_sessions_by_alliance(cls, alliance_id: int) -> List[Session]:
        """Get sessions by alliance ID"""
        result = []
        with cls._lock:
            for session in cls._sessions.values():
                try:
                    if session.home_mode.avatar.alliance_id == alliance_id:
                        result.append(session)
                except Exception:
                    continue
        return result

    @classmethod
    def cleanup_inactive_sessions(cls) -> None:
        """Clean up inactive sessions"""
        inactive_sessions = []

        with cls._lock:
            for account_id, session in cls._sessions.items():
                try:
                    if not session.connection.is_open or not session.connection.message_manager.is_alive():
                        inactive_sessions.append(account_id)
                except Exception:
                    inactive_sessions.append(account_id)

        # Remove inactive sessions
        for account_id in inactive_sessions:
            cls.remove(account_id)

        if inactive_sessions:
            Logger.print_log(f"Cleaned up {len(inactive_sessions)} inactive sessions")
