"""
Python conversion of Supercell.Laser.Logic.Command.Avatar.LogicDiamondsAddedCommand.cs
Command for adding diamonds to avatar
"""

from ..command import Command, CommandType

class LogicDiamondsAddedCommand(Command):
    """Command for adding diamonds to avatar"""

    def __init__(self):
        """Initialize diamonds added command"""
        super().__init__()
        self.command_type = CommandType.DIAMONDS_ADDED
        self.diamond_count = 0
        self.source = ""
        self.transaction_id = ""

    def get_diamond_count(self) -> int:
        """Get diamond count to add"""
        return self.diamond_count

    def set_diamond_count(self, count: int) -> None:
        """Set diamond count to add"""
        self.diamond_count = max(0, count)

    def get_source(self) -> str:
        """Get diamond source"""
        return self.source

    def set_source(self, source: str) -> None:
        """Set diamond source"""
        self.source = source

    def get_transaction_id(self) -> str:
        """Get transaction ID"""
        return self.transaction_id

    def set_transaction_id(self, transaction_id: str) -> None:
        """Set transaction ID"""
        self.transaction_id = transaction_id

    def can_execute(self, avatar: any) -> bool:
        """Check if command can be executed"""
        if not super().can_execute(avatar):
            return False

        # Check if diamond count is valid
        if self.diamond_count <= 0:
            return False

        return True

    def execute(self, avatar: any) -> int:
        """Execute diamonds added command"""
        if not self.can_execute(avatar):
            return -1

        # Add diamonds
        avatar.diamonds += self.diamond_count

        # Log transaction if ID provided
        if self.transaction_id:
            # Add to transaction history (if avatar has this feature)
            if hasattr(avatar, 'transaction_history'):
                avatar.transaction_history.append({
                    'type': 'diamonds_added',
                    'amount': self.diamond_count,
                    'source': self.source,
                    'transaction_id': self.transaction_id,
                    'timestamp': self.timestamp
                })

        return 0

    def encode(self, stream) -> None:
        """Encode command to stream"""
        super().encode(stream)
        stream.write_v_int(self.diamond_count)
        stream.write_string(self.source)
        stream.write_string(self.transaction_id)

    def decode(self, stream) -> None:
        """Decode command from stream"""
        super().decode(stream)
        self.diamond_count = stream.read_v_int()
        self.source = stream.read_string()
        self.transaction_id = stream.read_string()

    def __str__(self) -> str:
        """String representation"""
        return f"DiamondsAddedCommand(count={self.diamond_count}, source='{self.source}')"
