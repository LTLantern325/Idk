"""
Python conversion of Supercell.Laser.Logic.Command.Home.LogicSelectEmoteCommand.cs
Command for selecting emote
"""

from ..command import Command

class LogicSelectEmoteCommand(Command):
    """Command for selecting emote"""

    def __init__(self):
        """Initialize select emote command"""
        super().__init__()
        self.emote_global_id = 0
        self.slot_index = 0  # Emote slot (0-3 typically)
        self.character_global_id = 0  # Character to equip emote on

    def get_emote_global_id(self) -> int:
        """Get emote global ID"""
        return self.emote_global_id

    def set_emote_global_id(self, global_id: int) -> None:
        """Set emote global ID"""
        self.emote_global_id = global_id

    def get_slot_index(self) -> int:
        """Get emote slot index"""
        return self.slot_index

    def set_slot_index(self, slot_index: int) -> None:
        """Set emote slot index"""
        self.slot_index = max(0, min(3, slot_index))  # Limit to 4 slots

    def get_character_global_id(self) -> int:
        """Get character global ID"""
        return self.character_global_id

    def set_character_global_id(self, global_id: int) -> None:
        """Set character global ID"""
        self.character_global_id = global_id

    def execute(self, avatar: any) -> int:
        """Execute select emote command"""
        # Check if emote is owned
        if not hasattr(avatar, 'unlocked_emotes'):
            avatar.unlocked_emotes = []

        if self.emote_global_id != 0 and self.emote_global_id not in avatar.unlocked_emotes:
            return -1  # Emote not owned

        # Initialize selected emotes structure
        if not hasattr(avatar, 'selected_emotes'):
            avatar.selected_emotes = {}

        # Character-specific emotes
        if self.character_global_id != 0:
            if self.character_global_id not in avatar.selected_emotes:
                avatar.selected_emotes[self.character_global_id] = [0, 0, 0, 0]  # 4 emote slots

            # Set emote for specific slot
            if self.slot_index < len(avatar.selected_emotes[self.character_global_id]):
                avatar.selected_emotes[self.character_global_id][self.slot_index] = self.emote_global_id
        else:
            # Global emote selection
            if 'global' not in avatar.selected_emotes:
                avatar.selected_emotes['global'] = [0, 0, 0, 0]

            if self.slot_index < len(avatar.selected_emotes['global']):
                avatar.selected_emotes['global'][self.slot_index] = self.emote_global_id

        return 0

    def encode(self, stream) -> None:
        """Encode command to stream"""
        super().encode(stream)
        stream.write_v_int(self.emote_global_id)
        stream.write_v_int(self.slot_index)
        stream.write_v_int(self.character_global_id)

    def decode(self, stream) -> None:
        """Decode command from stream"""
        super().decode(stream)
        self.emote_global_id = stream.read_v_int()
        self.slot_index = stream.read_v_int()
        self.character_global_id = stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        if self.character_global_id != 0:
            return f"SelectEmoteCommand(emote={self.emote_global_id}, slot={self.slot_index}, character={self.character_global_id})"
        else:
            return f"SelectEmoteCommand(emote={self.emote_global_id}, slot={self.slot_index}, global)"
