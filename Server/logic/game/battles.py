"""
Python conversion of Supercell.Laser.Server.Logic.Game.Battles.cs
Battle management system
"""

import threading
import time
from typing import Dict, Optional
from concurrent.futures import ThreadPoolExecutor
from logic.battle.battle_mode import BattleMode

class Battles:
    """Static class for managing battles"""

    _battle_id_counter: int = 0
    _battles: Dict[int, BattleMode] = {}
    _update_thread: Optional[threading.Thread] = None
    _running: bool = False

    @classmethod
    def init(cls) -> None:
        """Initialize battle manager"""
        cls._battles = {}
        cls._battle_id_counter = 0
        cls._running = True

        # Start update thread
        cls._update_thread = threading.Thread(target=cls._update, daemon=True)
        cls._update_thread.start()

    @classmethod
    def _update(cls) -> None:
        """Update battles loop"""
        while cls._running:
            try:
                # Get battles to check (copy to avoid modification during iteration)
                battles_to_check = list(cls._battles.items())

                for battle_id, battle in battles_to_check:
                    if battle.is_game_over:
                        cls._battles.pop(battle_id, None)

                time.sleep(1)  # Sleep for 1 second

            except Exception as e:
                print(f"Error in battles update loop: {e}")
                time.sleep(1)

    @classmethod
    def add(cls, battle: BattleMode) -> int:
        """Add battle and return ID"""
        cls._battle_id_counter += 1
        battle_id = cls._battle_id_counter
        cls._battles[battle_id] = battle
        return battle_id

    @classmethod
    def get(cls, battle_id: int) -> Optional[BattleMode]:
        """Get battle by ID"""
        return cls._battles.get(battle_id)

    @classmethod
    def remove(cls, battle_id: int) -> None:
        """Remove battle by ID"""
        cls._battles.pop(battle_id, None)

    @classmethod
    def get_count(cls) -> int:
        """Get active battle count"""
        return len(cls._battles)

    @classmethod
    def shutdown(cls) -> None:
        """Shutdown battle manager"""
        cls._running = False
        if cls._update_thread and cls._update_thread.is_alive():
            cls._update_thread.join(timeout=5)
