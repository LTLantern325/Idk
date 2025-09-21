"""
Python conversion of Supercell.Laser.Logic.Command.Home.LogicSelectGearCommand.cs
Command for selecting gear
"""

from ..command import Command

class LogicSelectGearCommand(Command):
    """Command for selecting gear"""

    def __init__(self):
        """Initialize select gear command"""
        super().__init__()
        self.gear_global_id = 0
        self.character_global_id = 0
        self.gear_slot = 0  # 0=first gear slot, 1=second gear slot

    def get_gear_global_id(self) -> int:
        """Get gear global ID"""
        return self.gear_global_id

    def set_gear_global_id(self, global_id: int) -> None:
        """Set gear global ID"""
        self.gear_global_id = global_id

    def get_character_global_id(self) -> int:
        """Get character global ID"""
        return self.character_global_id

    def set_character_global_id(self, global_id: int) -> None:
        """Set character global ID"""
        self.character_global_id = global_id

    def get_gear_slot(self) -> int:
        """Get gear slot"""
        return self.gear_slot

    def set_gear_slot(self, slot: int) -> None:
        """Set gear slot"""
        self.gear_slot = max(0, min(1, slot))  # Limit to 2 gear slots

    def execute(self, avatar: any) -> int:
        """Execute select gear command"""
        # Check if character is owned
        if not hasattr(avatar, 'unlocked_characters'):
            avatar.unlocked_characters = []

        if self.character_global_id not in avatar.unlocked_characters:
            return -1  # Character not owned

        # Check if gear is owned
        if self.gear_global_id != 0:
            if not hasattr(avatar, 'unlocked_gears'):
                avatar.unlocked_gears = []

            if self.gear_global_id not in avatar.unlocked_gears:
                return -2  # Gear not owned

        # Initialize selected gears structure
        if not hasattr(avatar, 'selected_gears'):
            avatar.selected_gears = {}

        if self.character_global_id not in avatar.selected_gears:
            avatar.selected_gears[self.character_global_id] = [0, 0]  # 2 gear slots

        # Set gear for specific slot
        character_gears = avatar.selected_gears[self.character_global_id]
        if self.gear_slot < len(character_gears):
            character_gears[self.gear_slot] = self.gear_global_id

        return 0

    def encode(self, stream) -> None:
        """Encode command to stream"""
        super().encode(stream)
        stream.write_v_int(self.gear_global_id)
        stream.write_v_int(self.character_global_id)
        stream.write_v_int(self.gear_slot)

    def decode(self, stream) -> None:
        """Decode command from stream"""
        super().decode(stream)
        self.gear_global_id = stream.read_v_int()
        self.character_global_id = stream.read_v_int()
        self.gear_slot = stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        return f"SelectGearCommand(gear={self.gear_global_id}, character={self.character_global_id}, slot={self.gear_slot})"
