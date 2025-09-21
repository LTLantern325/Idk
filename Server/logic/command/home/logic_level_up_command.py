"""
Python conversion of Supercell.Laser.Logic.Command.Home.LogicLevelUpCommand.cs
Command for leveling up character
"""

from ..command import Command

class LogicLevelUpCommand(Command):
    """Command for leveling up character"""

    def __init__(self):
        """Initialize level up command"""
        super().__init__()
        self.character_global_id = 0
        self.new_level = 1
        self.power_points_cost = 0
        self.gold_cost = 0

    def get_character_global_id(self) -> int:
        """Get character global ID"""
        return self.character_global_id

    def set_character_global_id(self, global_id: int) -> None:
        """Set character global ID"""
        self.character_global_id = global_id

    def execute(self, avatar: any) -> int:
        """Execute level up command"""
        # Implementation would level up character
        return 0

    def encode(self, stream) -> None:
        """Encode command to stream"""
        super().encode(stream)
        stream.write_v_int(self.character_global_id)
        stream.write_v_int(self.new_level)

    def decode(self, stream) -> None:
        """Decode command from stream"""
        super().decode(stream)
        self.character_global_id = stream.read_v_int()
        self.new_level = stream.read_v_int()
