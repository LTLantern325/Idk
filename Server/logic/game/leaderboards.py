"""
Python conversion of Supercell.Laser.Server.Logic.Game.Leaderboards.cs
Leaderboard management system
"""

import threading
import time
from typing import List

from logic.club.alliance import Alliance
from database.models.account import Account
from database import accounts as Accounts
from database import alliances as Alliances

class Leaderboards:
    """Static class for managing leaderboards"""

    _accounts: List[Account] = []
    _alliances: List[Alliance] = []
    _thread: threading.Thread = None
    _running: bool = False

    @classmethod
    def init(cls) -> None:
        """Initialize leaderboards"""
        cls._accounts = []
        cls._alliances = []
        cls._running = True

        # Start update thread
        cls._thread = threading.Thread(target=cls._update, daemon=True)
        cls._thread.start()

    @classmethod
    def get_avatar_ranking_list(cls) -> List[Account]:
        """Get avatar ranking list"""
        return cls._accounts.copy()

    @classmethod
    def get_brawler_ranking_list(cls, hero_data_id: int) -> List[Account]:
        """Get brawler ranking list"""
        return Accounts.get_brawler_ranking_list(hero_data_id)

    @classmethod
    def get_alliance_ranking_list(cls) -> List[Alliance]:
        """Get alliance ranking list"""
        return cls._alliances.copy()

    @classmethod
    def _update(cls) -> None:
        """Update leaderboards in background"""
        while cls._running:
            try:
                # Update account rankings
                cls._accounts = Accounts.get_ranking_list()

                # Update alliance rankings
                cls._alliances = Alliances.get_ranking_list()

                # Sleep for 20 seconds
                time.sleep(20)

            except Exception as e:
                print(f"Error updating leaderboards: {e}")
                time.sleep(20)

    @classmethod
    def shutdown(cls) -> None:
        """Shutdown leaderboards"""
        cls._running = False
        if cls._thread and cls._thread.is_alive():
            cls._thread.join(timeout=5)
