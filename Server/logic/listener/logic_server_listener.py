"""
Python conversion of Supercell.Laser.Logic.Listener.LogicServerListener.cs
Server listener interface for managing players
"""

from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..avatar.client_avatar import ClientAvatar
    from ..home.home_mode import HomeMode
    from .logic_game_listener import LogicGameListener

class LogicServerListener(ABC):
    """Interface for server listener"""

    # Singleton instance
    instance: Optional['LogicServerListener'] = None

    @abstractmethod
    def get_avatar(self, player_id: int) -> Optional['ClientAvatar']:
        """Get player avatar by ID"""
        pass

    @abstractmethod
    def get_game_listener(self, player_id: int) -> Optional['LogicGameListener']:
        """Get game listener for player"""
        pass

    @abstractmethod
    def get_home_mode(self, player_id: int) -> Optional['HomeMode']:
        """Get home mode for player"""
        pass

    @abstractmethod
    def is_player_online(self, player_id: int) -> bool:
        """Check if player is online"""
        pass

    @classmethod
    def set_instance(cls, instance: 'LogicServerListener') -> None:
        """Set singleton instance"""
        cls.instance = instance

    @classmethod
    def get_instance(cls) -> Optional['LogicServerListener']:
        """Get singleton instance"""
        return cls.instance

class SimpleLogicServerListener(LogicServerListener):
    """Simple implementation of LogicServerListener"""

    def __init__(self):
        """Initialize simple server listener"""
        self.avatars = {}
        self.game_listeners = {}
        self.home_modes = {}
        self.online_players = set()

    def get_avatar(self, player_id: int) -> Optional['ClientAvatar']:
        """Get player avatar by ID"""
        return self.avatars.get(player_id)

    def get_game_listener(self, player_id: int) -> Optional['LogicGameListener']:
        """Get game listener for player"""
        return self.game_listeners.get(player_id)

    def get_home_mode(self, player_id: int) -> Optional['HomeMode']:
        """Get home mode for player"""
        return self.home_modes.get(player_id)

    def is_player_online(self, player_id: int) -> bool:
        """Check if player is online"""
        return player_id in self.online_players

    def add_player(self, player_id: int, avatar: 'ClientAvatar', 
                   game_listener: 'LogicGameListener', home_mode: 'HomeMode') -> None:
        """Add player to server"""
        self.avatars[player_id] = avatar
        self.game_listeners[player_id] = game_listener
        self.home_modes[player_id] = home_mode
        self.online_players.add(player_id)

    def remove_player(self, player_id: int) -> None:
        """Remove player from server"""
        self.avatars.pop(player_id, None)
        self.game_listeners.pop(player_id, None)
        self.home_modes.pop(player_id, None)
        self.online_players.discard(player_id)

    def set_player_online(self, player_id: int, online: bool) -> None:
        """Set player online status"""
        if online:
            self.online_players.add(player_id)
        else:
            self.online_players.discard(player_id)

    def get_online_player_count(self) -> int:
        """Get online player count"""
        return len(self.online_players)

    def get_online_players(self) -> set:
        """Get set of online player IDs"""
        return self.online_players.copy()
