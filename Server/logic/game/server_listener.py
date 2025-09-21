"""
Python conversion of Supercell.Laser.Server.Logic.ServerListener.cs
Server listener implementation
"""

from typing import Optional
from logic.avatar.client_avatar import ClientAvatar
from logic.home.home_mode import HomeMode
from logic.listener.logic_server_listener import LogicServerListener
from logic.listener.logic_game_listener import LogicGameListener
from database.accounts import Accounts
from networking.session.sessions import Sessions

class ServerListener(LogicServerListener):
    """Server listener implementation"""

    def get_avatar(self, account_id: int) -> Optional[ClientAvatar]:
        """Get avatar by account ID"""
        account = Accounts.load(account_id)
        return account.avatar if account else None

    def get_game_listener(self, account_id: int) -> Optional[LogicGameListener]:
        """Get game listener for account ID"""
        if Sessions.is_session_active(account_id):
            session = Sessions.get_session(account_id)
            return session.game_listener if session else None
        return None

    def get_home_mode(self, account_id: int) -> Optional[HomeMode]:
        """Get home mode for account ID"""
        if Sessions.is_session_active(account_id):
            session = Sessions.get_session(account_id)
            return session.home if session else None
        return None

    def is_player_online(self, account_id: int) -> bool:
        """Check if player is online"""
        return Sessions.is_session_active(account_id)
