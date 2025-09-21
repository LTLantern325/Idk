"""
Python conversion of Supercell.Laser.Logic.Command.CommandManager.cs
Command manager for handling game commands
"""

from typing import Dict, List, Optional, Type
from .command import Command
from .avatar.logic_change_avatar_name_command import LogicChangeAvatarNameCommand
from .avatar.logic_diamonds_added_command import LogicDiamondsAddedCommand

class CommandManager:
    """Command manager for handling game commands"""

    def __init__(self):
        """Initialize command manager"""
        self.command_types: Dict[int, Type[Command]] = {}
        self.pending_commands: List[Command] = []
        self.executed_commands: List[Command] = []
        self.command_history: Dict[int, List[Command]] = {}  # account_id -> commands

        # Statistics
        self.commands_executed = 0
        self.commands_failed = 0

        self._register_default_commands()

    def _register_default_commands(self) -> None:
        """Register default command types"""
        from .command import CommandType
        self.command_types = {
            CommandType.AVATAR_CHANGE_NAME: LogicChangeAvatarNameCommand,
            CommandType.DIAMONDS_ADDED: LogicDiamondsAddedCommand
        }

    def register_command_type(self, command_type: int, command_class: Type[Command]) -> None:
        """Register command type"""
        self.command_types[command_type] = command_class

    def create_command(self, command_type: int, account_id: int = 0) -> Optional[Command]:
        """Create command instance"""
        if command_type not in self.command_types:
            return None

        command_class = self.command_types[command_type]
        command = command_class()
        command.set_command_type(command_type)
        command.set_account_id(account_id)

        return command

    def queue_command(self, command: Command) -> bool:
        """Queue command for execution"""
        if not command:
            return False

        self.pending_commands.append(command)
        return True

    def execute_command(self, command: Command, avatar: any) -> bool:
        """Execute single command"""
        if not command or not command.can_execute(avatar):
            return False

        try:
            error_code = command.execute(avatar)

            if error_code == 0:
                command.success = True
                self.commands_executed += 1
            else:
                command.set_error(error_code)
                self.commands_failed += 1

            command.is_executed = True

            # Add to history
            account_id = command.get_account_id()
            if account_id not in self.command_history:
                self.command_history[account_id] = []
            self.command_history[account_id].append(command)

            # Move to executed list
            if command in self.pending_commands:
                self.pending_commands.remove(command)
            self.executed_commands.append(command)

            return command.success

        except Exception as e:
            command.set_error(-1, str(e))
            command.is_executed = True
            self.commands_failed += 1
            return False

    def execute_pending_commands(self, avatar: any) -> int:
        """Execute all pending commands"""
        executed_count = 0
        commands_to_execute = self.pending_commands.copy()

        for command in commands_to_execute:
            if self.execute_command(command, avatar):
                executed_count += 1

        return executed_count

    def get_pending_command_count(self) -> int:
        """Get number of pending commands"""
        return len(self.pending_commands)

    def get_executed_command_count(self) -> int:
        """Get number of executed commands"""
        return len(self.executed_commands)

    def get_command_history(self, account_id: int) -> List[Command]:
        """Get command history for account"""
        return self.command_history.get(account_id, [])

    def get_last_command(self, account_id: int) -> Optional[Command]:
        """Get last command for account"""
        history = self.get_command_history(account_id)
        return history[-1] if history else None

    def get_failed_commands(self) -> List[Command]:
        """Get all failed commands"""
        return [cmd for cmd in self.executed_commands if not cmd.success]

    def clear_executed_commands(self) -> None:
        """Clear executed command history"""
        self.executed_commands.clear()

    def clear_command_history(self, account_id: int) -> None:
        """Clear command history for account"""
        if account_id in self.command_history:
            del self.command_history[account_id]

    def get_statistics(self) -> Dict[str, int]:
        """Get command statistics"""
        return {
            'pending_commands': len(self.pending_commands),
            'executed_commands': len(self.executed_commands),
            'commands_executed': self.commands_executed,
            'commands_failed': self.commands_failed,
            'success_rate': (self.commands_executed / max(1, self.commands_executed + self.commands_failed)) * 100
        }

    def encode(self, stream) -> None:
        """Encode command manager state"""
        # Encode pending commands
        stream.write_v_int(len(self.pending_commands))
        for command in self.pending_commands:
            command.encode(stream)

        # Encode statistics
        stream.write_v_int(self.commands_executed)
        stream.write_v_int(self.commands_failed)

    def decode(self, stream) -> None:
        """Decode command manager state"""
        # Decode pending commands
        pending_count = stream.read_v_int()
        self.pending_commands.clear()

        for i in range(pending_count):
            # Create command based on type
            command_type = stream.read_v_int()
            command = self.create_command(command_type)

            if command:
                # Decode the rest of the command
                stream_pos = stream.position
                stream.position = stream_pos - 4  # Go back to re-read type
                command.decode(stream)
                self.pending_commands.append(command)

        # Decode statistics
        self.commands_executed = stream.read_v_int()
        self.commands_failed = stream.read_v_int()
