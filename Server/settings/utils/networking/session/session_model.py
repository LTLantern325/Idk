"""
Python conversion of Session model class (renamed to avoid conflict)
Individual session representation
"""

from datetime import datetime
from typing import Optional

from networking.connection import Connection
from logic.home.home_mode import HomeMode

class SessionModel:
    """Individual session model"""

    def __init__(self, home_mode: HomeMode, connection: Connection):
        """Initialize session"""
        self.home_mode = home_mode
        self.connection = connection
        self.game_listener = connection.message_manager if connection else None
        self.home = home_mode.home if home_mode else None
        self.created_time = datetime.utcnow()
        self.last_activity = datetime.utcnow()

    def is_active(self) -> bool:
        """Check if session is still active"""
        try:
            return (self.connection and 
                    self.connection.is_open and 
                    self.connection.message_manager.is_alive())
        except Exception:
            return False

    def update_activity(self) -> None:
        """Update last activity timestamp"""
        self.last_activity = datetime.utcnow()

    def get_account_id(self) -> Optional[int]:
        """Get account ID from session"""
        try:
            return self.home_mode.avatar.account_id if self.home_mode and self.home_mode.avatar else None
        except Exception:
            return None

    def close(self) -> None:
        """Close session"""
        try:
            if self.connection:
                self.connection.close()
        except Exception:
            pass

    def __str__(self) -> str:
        """String representation"""
        account_id = self.get_account_id()
        return f"Session(account_id={account_id}, active={self.is_active()})"
