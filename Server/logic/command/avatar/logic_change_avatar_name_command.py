"""
Python conversion of Supercell.Laser.Logic.Command.Avatar.LogicChangeAvatarNameCommand.cs
Command for changing avatar name
"""

from ..command import Command, CommandType

class LogicChangeAvatarNameCommand(Command):
    """Command for changing avatar name"""

    def __init__(self):
        """Initialize change avatar name command"""
        super().__init__()
        self.command_type = CommandType.AVATAR_CHANGE_NAME
        self.new_name = ""
        self.name_change_state = 0
        self.cost_diamonds = 50

    def get_new_name(self) -> str:
        """Get new name"""
        return self.new_name

    def set_new_name(self, name: str) -> None:
        """Set new name"""
        self.new_name = name[:20]  # Limit name length

    def get_name_change_state(self) -> int:
        """Get name change state"""
        return self.name_change_state

    def set_name_change_state(self, state: int) -> None:
        """Set name change state"""
        self.name_change_state = state

    def get_cost_diamonds(self) -> int:
        """Get diamond cost"""
        return self.cost_diamonds

    def can_execute(self, avatar: any) -> bool:
        """Check if command can be executed"""
        if not super().can_execute(avatar):
            return False

        # Check if name is valid
        if not self.new_name or len(self.new_name.strip()) < 3:
            return False

        # Check if player has enough diamonds (if not first name change)
        if self.name_change_state > 0 and avatar.diamonds < self.cost_diamonds:
            return False

        return True

    def execute(self, avatar: any) -> int:
        """Execute name change command"""
        if not self.can_execute(avatar):
            return -1

        old_name = avatar.name

        # Change name
        avatar.name = self.new_name.strip()

        # Deduct diamonds if not first name change
        if self.name_change_state > 0:
            avatar.diamonds -= self.cost_diamonds

        # Increment name change count
        self.name_change_state += 1
        avatar.name_change_count = self.name_change_state

        return 0

    def encode(self, stream) -> None:
        """Encode command to stream"""
        super().encode(stream)
        stream.write_string(self.new_name)
        stream.write_v_int(self.name_change_state)
        stream.write_v_int(self.cost_diamonds)

    def decode(self, stream) -> None:
        """Decode command from stream"""
        super().decode(stream)
        self.new_name = stream.read_string()
        self.name_change_state = stream.read_v_int()
        self.cost_diamonds = stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        return f"ChangeNameCommand(new_name='{self.new_name}', cost={self.cost_diamonds})"
