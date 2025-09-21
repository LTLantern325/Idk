"""
Python conversion of Supercell.Laser.Logic.Command.Home.LogicSelectCharacterCommand.cs
Command for selecting character
"""

from ..command import Command

class LogicSelectCharacterCommand(Command):
    """Command for selecting character"""

    def __init__(self):
        """Initialize select character command"""
        super().__init__()
        self.character_global_id = 0

    def get_character_global_id(self) -> int:
        """Get character global ID"""
        return self.character_global_id

    def set_character_global_id(self, global_id: int) -> None:
        """Set character global ID"""
        self.character_global_id = global_id

    def execute(self, avatar: any) -> int:
        """Execute select character command"""
        avatar.selected_character = self.character_global_id
        return 0

    def encode(self, stream) -> None:
        """Encode command to stream"""
        super().encode(stream)
        stream.write_v_int(self.character_global_id)

    def decode(self, stream) -> None:
        """Decode command from stream"""
        super().decode(stream)
        self.character_global_id = stream.read_v_int()
