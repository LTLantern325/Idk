"""
Python conversion of Supercell.Laser.Logic.Team.TeamEntry.cs
Team entry for team management
"""

from typing import List
from .team_member import TeamMember

class TeamEntry:
    """Team entry containing team information"""

    def __init__(self):
        """Initialize team entry"""
        self.team_id = 0
        self.team_name = ""
        self.members: List[TeamMember] = []
        self.max_members = 3
        self.game_mode = 0
        self.map_id = 0
        self.is_public = True
        self.created_time = 0
        self.team_type = 0  # 0 = ranked, 1 = friendly

    def get_team_id(self) -> int:
        """Get team ID"""
        return self.team_id

    def set_team_id(self, team_id: int) -> None:
        """Set team ID"""
        self.team_id = team_id

    def get_team_name(self) -> str:
        """Get team name"""
        return self.team_name

    def set_team_name(self, name: str) -> None:
        """Set team name"""
        self.team_name = name

    def get_members(self) -> List[TeamMember]:
        """Get team members"""
        return self.members.copy()

    def add_member(self, member: TeamMember) -> bool:
        """Add member to team"""
        if len(self.members) >= self.max_members:
            return False

        member.set_team_slot(len(self.members))
        self.members.append(member)
        return True

    def remove_member(self, account_id: int) -> bool:
        """Remove member from team"""
        for i, member in enumerate(self.members):
            if member.account_id == account_id:
                self.members.pop(i)
                # Reassign slots
                for j, remaining_member in enumerate(self.members):
                    remaining_member.set_team_slot(j)
                return True
        return False

    def get_member_count(self) -> int:
        """Get number of members"""
        return len(self.members)

    def is_full(self) -> bool:
        """Check if team is full"""
        return len(self.members) >= self.max_members

    def get_leader(self) -> TeamMember:
        """Get team leader"""
        for member in self.members:
            if member.is_leader:
                return member
        return None

    def set_leader(self, account_id: int) -> bool:
        """Set team leader"""
        # Remove leader status from current leader
        for member in self.members:
            member.set_leader(False)

        # Set new leader
        for member in self.members:
            if member.account_id == account_id:
                member.set_leader(True)
                return True
        return False

    def get_member_by_id(self, account_id: int) -> TeamMember:
        """Get member by account ID"""
        for member in self.members:
            if member.account_id == account_id:
                return member
        return None

    def all_members_ready(self) -> bool:
        """Check if all members are ready"""
        return all(member.is_ready for member in self.members)

    def can_start_battle(self) -> bool:
        """Check if team can start battle"""
        return (len(self.members) > 0 and 
                self.all_members_ready() and
                all(member.has_character_selected() for member in self.members))

    def get_average_trophies(self) -> int:
        """Get average trophies of team"""
        if not self.members:
            return 0
        return sum(member.trophies for member in self.members) // len(self.members)

    def set_game_mode(self, game_mode: int) -> None:
        """Set game mode"""
        self.game_mode = game_mode

    def get_game_mode(self) -> int:
        """Get game mode"""
        return self.game_mode

    def set_map_id(self, map_id: int) -> None:
        """Set map ID"""
        self.map_id = map_id

    def get_map_id(self) -> int:
        """Get map ID"""
        return self.map_id

    def is_public_team(self) -> bool:
        """Check if team is public"""
        return self.is_public

    def set_public(self, public: bool) -> None:
        """Set team public status"""
        self.is_public = public

    def encode(self, stream) -> None:
        """Encode team entry to stream"""
        stream.write_v_long(self.team_id)
        stream.write_string(self.team_name)

        stream.write_v_int(len(self.members))
        for member in self.members:
            member.encode(stream)

        stream.write_v_int(self.max_members)
        stream.write_v_int(self.game_mode)
        stream.write_v_int(self.map_id)
        stream.write_boolean(self.is_public)
        stream.write_v_int(self.team_type)

    def __str__(self) -> str:
        """String representation"""
        return (f"TeamEntry(id={self.team_id}, name='{self.team_name}', "
                f"members={len(self.members)}/{self.max_members})")
