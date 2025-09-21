"""
Python conversion of Supercell.Laser.Logic.Team.TeamMember.cs
Team member representation
"""

from typing import TYPE_CHECKING
from ..helper.byte_stream_helper import ByteStreamHelper

if TYPE_CHECKING:
    from ..avatar.client_avatar import ClientAvatar

class TeamMember:
    """Team member class"""

    def __init__(self):
        """Initialize team member"""
        self.account_id = 0
        self.name = ""
        self.is_leader = False
        self.is_ready = False
        self.character_id = 0
        self.skin_id = 0
        self.trophies = 0
        self.team_slot = 0
        self._avatar = None

    def get_account_id(self) -> int:
        """Get account ID"""
        return self.account_id

    def set_account_id(self, account_id: int) -> None:
        """Set account ID"""
        self.account_id = account_id

    def get_name(self) -> str:
        """Get member name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set member name"""
        self.name = name

    def is_team_leader(self) -> bool:
        """Check if member is team leader"""
        return self.is_leader

    def set_leader(self, leader: bool) -> None:
        """Set leader status"""
        self.is_leader = leader

    def is_member_ready(self) -> bool:
        """Check if member is ready"""
        return self.is_ready

    def set_ready(self, ready: bool) -> None:
        """Set ready status"""
        self.is_ready = ready

    def get_character_id(self) -> int:
        """Get selected character ID"""
        return self.character_id

    def set_character_id(self, character_id: int) -> None:
        """Set selected character ID"""
        self.character_id = character_id

    def get_skin_id(self) -> int:
        """Get selected skin ID"""
        return self.skin_id

    def set_skin_id(self, skin_id: int) -> None:
        """Set selected skin ID"""
        self.skin_id = skin_id

    def get_trophies(self) -> int:
        """Get member trophies"""
        return self.trophies

    def set_trophies(self, trophies: int) -> None:
        """Set member trophies"""
        self.trophies = trophies

    def get_team_slot(self) -> int:
        """Get team slot position"""
        return self.team_slot

    def set_team_slot(self, slot: int) -> None:
        """Set team slot position"""
        self.team_slot = slot

    def set_avatar(self, avatar: 'ClientAvatar') -> None:
        """Set member avatar"""
        self._avatar = avatar
        if avatar:
            self.account_id = avatar.account_id
            self.name = avatar.name
            self.trophies = avatar.trophies

    def get_avatar(self) -> 'ClientAvatar':
        """Get member avatar"""
        return self._avatar

    def can_start_battle(self) -> bool:
        """Check if member can start battle"""
        return self.is_leader and self.is_ready

    def has_character_selected(self) -> bool:
        """Check if member has character selected"""
        return self.character_id > 0

    def encode(self, stream) -> None:
        """Encode team member to stream"""
        stream.write_v_long(self.account_id)
        stream.write_string(self.name)
        stream.write_boolean(self.is_leader)
        stream.write_boolean(self.is_ready)

        ByteStreamHelper.write_data_reference(stream, self.character_id)
        ByteStreamHelper.write_data_reference(stream, self.skin_id)

        stream.write_v_int(self.trophies)
        stream.write_v_int(self.team_slot)

    def decode(self, stream) -> None:
        """Decode team member from stream"""
        self.account_id = stream.read_v_long()
        self.name = stream.read_string()
        self.is_leader = stream.read_boolean()
        self.is_ready = stream.read_boolean()

        self.character_id = ByteStreamHelper.read_data_reference(stream)
        self.skin_id = ByteStreamHelper.read_data_reference(stream)

        self.trophies = stream.read_v_int()
        self.team_slot = stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        role = "Leader" if self.is_leader else "Member"
        status = "Ready" if self.is_ready else "Not Ready"
        return f"TeamMember('{self.name}', {role}, {status})"
