"""
Python conversion of Supercell.Laser.Server.Database.Cache.AllianceCache.cs
Caching system for alliances with periodic saving
"""

import threading
import time
from typing import Dict, Optional
from logic.club.alliance import Alliance
from database.alliances import Alliances

class AllianceCache:
    """Static class for caching alliances"""

    _cached_alliances: Dict[int, Alliance] = {}
    _thread: Optional[threading.Thread] = None
    _started: bool = True

    @classmethod
    @property
    def count(cls) -> int:
        """Get count of cached alliances"""
        return len(cls._cached_alliances)

    @classmethod
    def init(cls) -> None:
        """Initialize alliance cache and start save thread"""
        cls._cached_alliances = {}
        cls._thread = threading.Thread(target=cls._update, daemon=True)
        cls._thread.start()

    @classmethod
    def _update(cls) -> None:
        """Background thread that periodically saves cached alliances"""
        while cls._started:
            try:
                cls.save_all()
                time.sleep(30)  # Sleep for 30 seconds
            except Exception as e:
                print(f"Error in AllianceCache update thread: {e}")
                time.sleep(30)

    @classmethod
    def save_all(cls) -> None:
        """Save all cached alliances to database"""
        try:
            for alliance in cls._cached_alliances.values():
                try:
                    Alliances.save(alliance)
                except Exception as ex:
                    print(f"Unhandled exception while saving alliance: {ex}")
        except Exception:
            pass  # Ignore exceptions in save_all

    @classmethod
    def is_alliance_cached(cls, alliance_id: int) -> bool:
        """Check if alliance is in cache"""
        return alliance_id in cls._cached_alliances

    @classmethod
    def get_alliance(cls, alliance_id: int) -> Optional[Alliance]:
        """Get alliance from cache"""
        return cls._cached_alliances.get(alliance_id)

    @classmethod
    def cache(cls, alliance: Alliance) -> None:
        """Cache an alliance"""
        if alliance and hasattr(alliance, 'id'):
            cls._cached_alliances[alliance.id] = alliance

    @classmethod
    def remove(cls, alliance_id: int) -> None:
        """Remove alliance from cache"""
        if alliance_id in cls._cached_alliances:
            del cls._cached_alliances[alliance_id]

    @classmethod
    def shutdown(cls) -> None:
        """Shutdown the cache system"""
        cls._started = False
        if cls._thread and cls._thread.is_alive():
            cls._thread.join(timeout=5)
        cls.save_all()  # Final save before shutdown
