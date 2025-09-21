"""
Python conversion of Supercell.Laser.Logic.Command.Home.LogicSelectStarPowerCommand.cs
Command for selecting star power
"""

from ..command import Command

class LogicSelectStarPowerCommand(Command):
    """Command for selecting star power"""

    def __init__(self):
        """Initialize select star power command"""
        super().__init__()
        self.star_power_global_id = 0
        self.character_global_id = 0

    def get_star_power_global_id(self) -> int:
        """Get star power global ID"""
        return self.star_power_global_id

    def set_star_power_global_id(self, global_id: int) -> None:
        """Set star power global ID"""
        self.star_power_global_id = global_id

    def get_character_global_id(self) -> int:
        """Get character global ID"""
        return self.character_global_id

    def set_character_global_id(self, global_id: int) -> None:
        """Set character global ID"""
        self.character_global_id = global_id

    def execute(self, avatar: any) -> int:
        """Execute select star power command"""
        # Check if character is owned
        if not hasattr(avatar, 'unlocked_characters'):
            avatar.unlocked_characters = []

        if self.character_global_id not in avatar.unlocked_characters:
            return -1  # Character not owned

        # Check if star power is owned
        if self.star_power_global_id != 0:
            if not hasattr(avatar, 'unlocked_star_powers'):
                avatar.unlocked_star_powers = []

            if self.star_power_global_id not in avatar.unlocked_star_powers:
                return -2  # Star power not owned

        # Initialize selected star powers
        if not hasattr(avatar, 'selected_star_powers'):
            avatar.selected_star_powers = {}

        # Set selected star power for character
        avatar.selected_star_powers[self.character_global_id] = self.star_power_global_id

        return 0

    def encode(self, stream) -> None:
        """Encode command to stream"""
        super().encode(stream)
        stream.write_v_int(self.star_power_global_id)
        stream.write_v_int(self.character_global_id)

    def decode(self, stream) -> None:
        """Decode command from stream"""
        super().decode(stream)
        self.star_power_global_id = stream.read_v_int()
        self.character_global_id = stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        return f"SelectStarPowerCommand(star_power={self.star_power_global_id}, character={self.character_global_id})"
