"""
Python conversion of Supercell.Laser.Logic.Team.TeamInviteEntry.cs
Team invite entry for team invitations
"""

class TeamInviteEntry:
    """Team invite entry for managing team invitations"""

    def __init__(self):
        """Initialize team invite entry"""
        self.inviter_id = 0  # Account ID of the inviter
        self.id = 0          # Invitation ID  
        self.name = ""       # Inviter name
        self.slot = 0        # Team slot position

    def get_inviter_id(self) -> int:
        """Get inviter account ID"""
        return self.inviter_id

    def set_inviter_id(self, inviter_id: int) -> None:
        """Set inviter account ID"""
        self.inviter_id = inviter_id

    def get_id(self) -> int:
        """Get invitation ID"""
        return self.id

    def set_id(self, invite_id: int) -> None:
        """Set invitation ID"""
        self.id = invite_id

    def get_name(self) -> str:
        """Get inviter name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set inviter name"""
        self.name = name

    def get_slot(self) -> int:
        """Get team slot"""
        return self.slot

    def set_slot(self, slot: int) -> None:
        """Set team slot"""
        self.slot = slot

    def is_valid(self) -> bool:
        """Check if invitation is valid"""
        return self.inviter_id > 0 and self.name != ""

    def encode(self, stream) -> None:
        """Encode team invite entry to stream"""
        stream.write_long(self.inviter_id)
        stream.write_long(self.id)
        stream.write_string(self.name)
        stream.write_v_int(1)  # Unknown constant
        stream.write_v_int(self.slot)

    def decode(self, stream) -> None:
        """Decode team invite entry from stream"""
        self.inviter_id = stream.read_long()
        self.id = stream.read_long()
        self.name = stream.read_string()
        stream.read_v_int()  # Unknown constant
        self.slot = stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        return f"TeamInviteEntry(inviter='{self.name}', slot={self.slot})"
