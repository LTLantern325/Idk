"""
Python conversion of Supercell.Laser.Logic.Message.Account.UnlockAccountOkMessage.cs
Unlock account OK message for account unlock confirmation
"""

from ..game_message import GameMessage

class UnlockAccountOkMessage(GameMessage):
    """Unlock account OK message for account unlock confirmation"""

    def __init__(self):
        """Initialize unlock account OK message"""
        super().__init__()
        self.account_id = 0
        self.unlock_token = ""

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 20132  # Placeholder message type

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 1

    def get_account_id(self) -> int:
        """Get unlocked account ID"""
        return self.account_id

    def set_account_id(self, account_id: int) -> None:
        """Set unlocked account ID"""
        self.account_id = account_id

    def get_unlock_token(self) -> str:
        """Get unlock token"""
        return self.unlock_token

    def set_unlock_token(self, token: str) -> None:
        """Set unlock token"""
        self.unlock_token = token

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_long(self.account_id)
        self.stream.write_string(self.unlock_token)

    def decode(self) -> None:
        """Decode message from stream"""
        self.account_id = self.stream.read_v_long()
        self.unlock_token = self.stream.read_string()

    def is_valid(self) -> bool:
        """Check if unlock is valid"""
        return self.account_id > 0 and self.unlock_token != ""

    def __str__(self) -> str:
        """String representation"""
        return f"UnlockAccountOkMessage(account_id={self.account_id})"
