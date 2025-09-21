"""
Python conversion of Supercell.Laser.Logic.Command.Command.cs
Base command class for game commands
"""

from typing import Optional, Any

class CommandType:
    """Command types"""
    UNKNOWN = 0
    AVATAR_CHANGE_NAME = 1
    DIAMONDS_ADDED = 2
    LEVEL_UP = 3
    PURCHASE_OFFER = 4
    SELECT_CHARACTER = 5

class Command:
    """Base command class for game commands"""

    def __init__(self):
        """Initialize command"""
        self.command_type = CommandType.UNKNOWN
        self.account_id = 0
        self.timestamp = 0
        self.execution_time = 0.0
        self.is_executed = False
        self.success = False
        self.error_code = 0
        self.error_message = ""

    def get_command_type(self) -> int:
        """Get command type"""
        return self.command_type

    def set_command_type(self, command_type: int) -> None:
        """Set command type"""
        self.command_type = command_type

    def get_account_id(self) -> int:
        """Get account ID"""
        return self.account_id

    def set_account_id(self, account_id: int) -> None:
        """Set account ID"""
        self.account_id = account_id

    def execute(self, avatar: Any) -> int:
        """Execute command (to be overridden by subclasses)"""
        # Base implementation
        self.is_executed = True
        self.success = True
        return 0

    def can_execute(self, avatar: Any) -> bool:
        """Check if command can be executed"""
        return not self.is_executed

    def is_command_executed(self) -> bool:
        """Check if command was executed"""
        return self.is_executed

    def was_successful(self) -> bool:
        """Check if command was successful"""
        return self.is_executed and self.success

    def get_error_code(self) -> int:
        """Get error code"""
        return self.error_code

    def set_error(self, error_code: int, message: str = "") -> None:
        """Set error information"""
        self.error_code = error_code
        self.error_message = message
        self.success = False

    def encode(self, stream) -> None:
        """Encode command to stream"""
        stream.write_v_int(self.command_type)
        stream.write_v_long(self.account_id)
        stream.write_v_int(self.timestamp)
        stream.write_boolean(self.is_executed)
        stream.write_boolean(self.success)
        stream.write_v_int(self.error_code)

    def decode(self, stream) -> None:
        """Decode command from stream"""
        self.command_type = stream.read_v_int()
        self.account_id = stream.read_v_long()
        self.timestamp = stream.read_v_int()
        self.is_executed = stream.read_boolean()
        self.success = stream.read_boolean()
        self.error_code = stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        status = "executed" if self.is_executed else "pending"
        return f"Command(type={self.command_type}, account={self.account_id}, {status})"
