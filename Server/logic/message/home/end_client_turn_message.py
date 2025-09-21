"""
Python conversion of Supercell.Laser.Logic.Message.Home.EndClientTurnMessage.cs
End client turn message for turn-based operations
"""

from typing import List, TYPE_CHECKING
from ..game_message import GameMessage

if TYPE_CHECKING:
    from ...command.command import Command

class EndClientTurnMessage(GameMessage):
    """End client turn message for turn-based operations"""

    def __init__(self):
        """Initialize end client turn message"""
        super().__init__()
        self.tick = 0
        self.checksum = 0
        self.commands = []  # List[Command]

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14102

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_tick(self) -> int:
        """Get tick number"""
        return self.tick

    def set_tick(self, tick: int) -> None:
        """Set tick number"""
        self.tick = tick

    def get_checksum(self) -> int:
        """Get checksum"""
        return self.checksum

    def set_checksum(self, checksum: int) -> None:
        """Set checksum"""
        self.checksum = checksum

    def get_commands(self) -> List['Command']:
        """Get commands list"""
        return self.commands.copy()

    def add_command(self, command: 'Command') -> None:
        """Add command to list"""
        self.commands.append(command)

    def get_command_count(self) -> int:
        """Get number of commands"""
        return len(self.commands)

    def clear_commands(self) -> None:
        """Clear all commands"""
        self.commands.clear()

    def decode(self) -> None:
        """Decode message from stream"""
        # Read boolean flag
        self.stream.read_boolean()

        # Read tick and checksum
        self.tick = self.stream.read_v_int()
        self.checksum = self.stream.read_v_int()

        # Read commands count
        count = self.stream.read_v_int()

        # Read commands
        for i in range(count):
            # In original: CommandManager.DecodeCommand(Stream)
            # For now, create mock command
            command_type = self.stream.read_v_int()
            command_data = self.stream.read_v_int()

            mock_command = MockCommand(command_type, command_data)
            self.commands.append(mock_command)

    def encode(self) -> None:
        """Encode message to stream"""
        # Write boolean flag
        self.stream.write_boolean(True)

        # Write tick and checksum
        self.stream.write_v_int(self.tick)
        self.stream.write_v_int(self.checksum)

        # Write commands count
        self.stream.write_v_int(len(self.commands))

        # Write commands (simplified)
        for command in self.commands:
            if hasattr(command, 'command_type'):
                self.stream.write_v_int(command.command_type)
                self.stream.write_v_int(getattr(command, 'command_data', 0))

    def __str__(self) -> str:
        """String representation"""
        return (f"EndClientTurnMessage(tick={self.tick}, "
                f"checksum={self.checksum}, commands={len(self.commands)})")

class MockCommand:
    """Mock command for demonstration"""

    def __init__(self, command_type: int, command_data: int):
        self.command_type = command_type
        self.command_data = command_data
