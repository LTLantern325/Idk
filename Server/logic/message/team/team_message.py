"""
Python conversion of Supercell.Laser.Logic.Message.Team.TeamMessage.cs
Team message for sending team information
"""

from typing import List, Dict, Any, TYPE_CHECKING
from ..game_message import GameMessage

if TYPE_CHECKING:
    from ...team.team_member import TeamMember

class TeamMessage(GameMessage):
    """Team message for sending team information"""

    def __init__(self):
        """Initialize team message"""
        super().__init__()
        self.team_id = 0
        self.team_type = 0
        self.game_mode = 0
        self.map_id = 0
        self.members = []  # List of TeamMember objects
        self.max_members = 3
        self.is_full = False

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24350  # Team data

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_team_id(self) -> int:
        """Get team ID"""
        return self.team_id

    def set_team_id(self, team_id: int) -> None:
        """Set team ID"""
        self.team_id = team_id

    def get_member_count(self) -> int:
        """Get current member count"""
        return len(self.members)

    def add_member(self, member: 'TeamMember') -> None:
        """Add member to team"""
        if len(self.members) < self.max_members:
            self.members.append(member)
            self.is_full = len(self.members) >= self.max_members

    def remove_member(self, member_id: int) -> bool:
        """Remove member from team"""
        for i, member in enumerate(self.members):
            if hasattr(member, 'player_id') and member.player_id == member_id:
                self.members.pop(i)
                self.is_full = False
                return True
        return False

    def is_team_full(self) -> bool:
        """Check if team is full"""
        return self.is_full

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_long(self.team_id)
        self.stream.write_v_int(self.team_type)
        self.stream.write_v_int(self.game_mode)
        self.stream.write_v_int(self.map_id)

        # Write members
        self.stream.write_v_int(len(self.members))
        for member in self.members:
            if hasattr(member, 'encode'):
                member.encode(self.stream)
            else:
                # Write simplified member data
                self.stream.write_v_long(getattr(member, 'player_id', 0))
                self.stream.write_string(getattr(member, 'name', ''))
                self.stream.write_v_int(getattr(member, 'character_id', 0))

        self.stream.write_v_int(self.max_members)
        self.stream.write_boolean(self.is_full)

    def decode(self) -> None:
        """Decode message from stream"""
        self.team_id = self.stream.read_v_long()
        self.team_type = self.stream.read_v_int()
        self.game_mode = self.stream.read_v_int()
        self.map_id = self.stream.read_v_int()

        # Read members (simplified)
        member_count = self.stream.read_v_int()
        self.members.clear()
        for i in range(member_count):
            # Skip member data for now
            self.stream.read_v_long()  # player_id
            self.stream.read_string()   # name
            self.stream.read_v_int()    # character_id

        self.max_members = self.stream.read_v_int()
        self.is_full = self.stream.read_boolean()

    def __str__(self) -> str:
        """String representation"""
        return f"TeamMessage(team_id={self.team_id}, members={len(self.members)}/{self.max_members})"
