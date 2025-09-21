"""
Python conversion of Supercell.Laser.Logic.Command.Home.LogicSelectSkinCommand.cs
Command for selecting character skin
"""

from ..command import Command

class LogicSelectSkinCommand(Command):
    """Command for selecting character skin"""

    def __init__(self):
        """Initialize select skin command"""
        super().__init__()
        self.skin_global_id = 0
        self.character_global_id = 0

    def get_skin_global_id(self) -> int:
        """Get skin global ID"""
        return self.skin_global_id

    def set_skin_global_id(self, global_id: int) -> None:
        """Set skin global ID"""
        self.skin_global_id = global_id

    def get_character_global_id(self) -> int:
        """Get character global ID"""
        return self.character_global_id

    def set_character_global_id(self, global_id: int) -> None:
        """Set character global ID"""
        self.character_global_id = global_id

    def execute(self, avatar: any) -> int:
        """Execute select skin command"""
        # Set selected skin for character
        if hasattr(avatar, 'selected_skins'):
            avatar.selected_skins[self.character_global_id] = self.skin_global_id
        return 0

    def encode(self, stream) -> None:
        """Encode command to stream"""
        super().encode(stream)
        stream.write_v_int(self.skin_global_id)
        stream.write_v_int(self.character_global_id)

    def decode(self, stream) -> None:
        """Decode command from stream"""
        super().decode(stream)
        self.skin_global_id = stream.read_v_int()
        self.character_global_id = stream.read_v_int()
