"""
Python conversion of Supercell.Laser.Server.Database.Cache.AccountCache.cs
Caching system for user accounts with periodic saving
"""

import threading
import time
from typing import Dict, Optional
from database.models.account import Account
from database.accounts import Accounts

class AccountCache:
    """Static class for caching user accounts"""

    _cached_accounts: Dict[int, Account] = {}
    _thread: Optional[threading.Thread] = None
    _started: bool = True

    @classmethod
    @property
    def count(cls) -> int:
        """Get count of cached accounts"""
        return len(cls._cached_accounts)

    @classmethod
    def init(cls) -> None:
        """Initialize account cache and start save thread"""
        cls._cached_accounts = {}
        cls._thread = threading.Thread(target=cls._update, daemon=True)
        cls._thread.start()

    @classmethod
    def _update(cls) -> None:
        """Background thread that periodically saves cached accounts"""
        while cls._started:
            try:
                cls.save_all()
                time.sleep(30)  # Sleep for 30 seconds
            except Exception as e:
                print(f"Error in AccountCache update thread: {e}")
                time.sleep(30)

    @classmethod
    def save_all(cls) -> None:
        """Save all cached accounts to database"""
        try:
            for account in cls._cached_accounts.values():
                try:
                    Accounts.save(account)
                except Exception as ex:
                    print(f"Unhandled exception while saving account: {ex}")
        except Exception:
            pass  # Ignore exceptions in save_all

    @classmethod
    def is_account_cached(cls, account_id: int) -> bool:
        """Check if account is in cache"""
        return account_id in cls._cached_accounts

    @classmethod
    def get_account(cls, account_id: int) -> Optional[Account]:
        """Get account from cache"""
        return cls._cached_accounts.get(account_id)

    @classmethod
    def cache(cls, account: Account) -> None:
        """Cache an account"""
        if account and hasattr(account, 'account_id'):
            try:
                cls._cached_accounts[account.account_id] = account
            except Exception:
                pass  # Ignore exceptions when caching

    @classmethod
    def remove(cls, account_id: int) -> None:
        """Remove account from cache"""
        if account_id in cls._cached_accounts:
            del cls._cached_accounts[account_id]

    @classmethod
    def shutdown(cls) -> None:
        """Shutdown the cache system"""
        cls._started = False
        if cls._thread and cls._thread.is_alive():
            cls._thread.join(timeout=5)
        cls.save_all()  # Final save before shutdown
