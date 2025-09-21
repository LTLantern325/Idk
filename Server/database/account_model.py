"""
Python conversion of Supercell.Laser.Server.Database.Models.Account.cs
Account model representing user account data
"""

from typing import Optional, Dict, Any
from logic.avatar.client_avatar import ClientAvatar
from logic.home.client_home import ClientHome

class Account:
    """Account model class"""

    def __init__(self):
        """Initialize new account"""
        self.account_id: int = 0
        self.pass_token: str = ""
        self.home: ClientHome = ClientHome()
        self.avatar: ClientAvatar = ClientAvatar()

    def to_dict(self) -> Dict[str, Any]:
        """Convert account to dictionary for JSON serialization"""
        return {
            "account_id": self.account_id,
            "pass_token": self.pass_token,
            "home": self.home.to_dict() if self.home else None,
            "avatar": self.avatar.to_dict() if self.avatar else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Account':
        """Create account from dictionary (JSON deserialization)"""
        account = cls()

        if "account_id" in data:
            account.account_id = data["account_id"]
        if "pass_token" in data:
            account.pass_token = data["pass_token"]

        if "home" in data and data["home"]:
            account.home = ClientHome.from_dict(data["home"])

        if "avatar" in data and data["avatar"]:
            account.avatar = ClientAvatar.from_dict(data["avatar"])

        return account

    def __str__(self) -> str:
        """String representation of account"""
        return f"Account(id={self.account_id}, token={self.pass_token[:8]}...)"

    def __repr__(self) -> str:
        """Developer representation of account"""
        return f"Account(account_id={self.account_id}, pass_token='{self.pass_token}')"
