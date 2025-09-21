"""
Python conversion of Supercell.Laser.Logic.Command.Home.LogicGatchaCommand.cs
Command for gatcha/box opening
"""

from ..command import Command

class LogicGatchaCommand(Command):
    """Command for gatcha/box opening"""

    def __init__(self):
        """Initialize gatcha command"""
        super().__init__()
        self.box_type = 0
        self.box_count = 1
        self.use_gems = False
        self.cost = 0

    def get_box_type(self) -> int:
        """Get box type"""
        return self.box_type

    def set_box_type(self, box_type: int) -> None:
        """Set box type"""
        self.box_type = box_type

    def get_box_count(self) -> int:
        """Get number of boxes to open"""
        return self.box_count

    def set_box_count(self, count: int) -> None:
        """Set box count"""
        self.box_count = max(1, count)

    def execute(self, avatar: any) -> int:
        """Execute gatcha command"""
        # Check cost
        if self.use_gems:
            if avatar.diamonds < self.cost:
                return -1
            avatar.diamonds -= self.cost
        else:
            # Use tokens or other currency
            pass

        # Open boxes (implementation would handle rewards)
        return 0

    def encode(self, stream) -> None:
        """Encode command to stream"""
        super().encode(stream)
        stream.write_v_int(self.box_type)
        stream.write_v_int(self.box_count)
        stream.write_boolean(self.use_gems)
        stream.write_v_int(self.cost)

    def decode(self, stream) -> None:
        """Decode command from stream"""
        super().decode(stream)
        self.box_type = stream.read_v_int()
        self.box_count = stream.read_v_int()
        self.use_gems = stream.read_boolean()
        self.cost = stream.read_v_int()
