"""
Python conversion of Supercell.Laser.Logic.Message.Home.AvailableServerCommandMessage.cs
Available server command message for server command availability
"""

from typing import List
from ..game_message import GameMessage

class AvailableServerCommandMessage(GameMessage):
    """Available server command message for server command availability"""

    def __init__(self):
        """Initialize available server command message"""
        super().__init__()
        self.available_commands = []  # List of available command IDs

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24111  # Placeholder message type

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_available_commands(self) -> List[int]:
        """Get list of available commands"""
        return self.available_commands.copy()

    def add_available_command(self, command_id: int) -> None:
        """Add available command"""
        if command_id not in self.available_commands:
            self.available_commands.append(command_id)

    def remove_available_command(self, command_id: int) -> None:
        """Remove available command"""
        if command_id in self.available_commands:
            self.available_commands.remove(command_id)

    def is_command_available(self, command_id: int) -> bool:
        """Check if command is available"""
        return command_id in self.available_commands

    def get_command_count(self) -> int:
        """Get number of available commands"""
        return len(self.available_commands)

    def clear_commands(self) -> None:
        """Clear all commands"""
        self.available_commands.clear()

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(len(self.available_commands))
        for command_id in self.available_commands:
            self.stream.write_v_int(command_id)

    def decode(self) -> None:
        """Decode message from stream"""
        count = self.stream.read_v_int()
        self.available_commands.clear()
        for i in range(count):
            command_id = self.stream.read_v_int()
            self.available_commands.append(command_id)

    def __str__(self) -> str:
        """String representation"""
        return f"AvailableServerCommandMessage(commands={len(self.available_commands)})"
