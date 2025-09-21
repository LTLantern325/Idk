"""
Python conversion of Supercell.Laser.Logic.Club.Alliance.cs
Alliance class for club/alliance management
"""

from typing import Dict, List, Optional
from .alliance_member import AllianceMember
from .alliance_header import AllianceHeader

class Alliance:
    """Alliance class for club/alliance management"""

    def __init__(self):
        """Initialize alliance"""
        self.alliance_id = 0
        self.name = ""
        self.description = ""
        self.type = 1  # Open = 1, Invite Only = 2, Closed = 3
        self.badge_id = 0
        self.required_trophies = 0
        self.required_score = 0

        # Member management
        self.members: Dict[int, AllianceMember] = {}
        self.member_count = 0
        self.max_members = 100

        # Statistics
        self.trophies = 0
        self.experience = 0
        self.experience_level = 1
        self.wins = 0

        # Settings
        self.region = "GLOBAL"
        self.language = "EN"
        self.is_family_friendly = True

        # Activity
        self.creation_date = 0
        self.last_activity = 0

        # War/events
        self.war_trophies = 0
        self.war_wins = 0
        self.war_losses = 0

    def get_alliance_id(self) -> int:
        """Get alliance ID"""
        return self.alliance_id

    def set_alliance_id(self, alliance_id: int) -> None:
        """Set alliance ID"""
        self.alliance_id = alliance_id

    def get_name(self) -> str:
        """Get alliance name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set alliance name"""
        self.name = name[:50]  # Limit name length

    def get_description(self) -> str:
        """Get alliance description"""
        return self.description

    def set_description(self, description: str) -> None:
        """Set alliance description"""
        self.description = description[:500]  # Limit description length

    def get_type(self) -> int:
        """Get alliance type"""
        return self.type

    def set_type(self, alliance_type: int) -> None:
        """Set alliance type"""
        self.type = max(1, min(3, alliance_type))

    def get_badge_id(self) -> int:
        """Get alliance badge ID"""
        return self.badge_id

    def set_badge_id(self, badge_id: int) -> None:
        """Set alliance badge ID"""
        self.badge_id = badge_id

    def get_required_trophies(self) -> int:
        """Get required trophies to join"""
        return self.required_trophies

    def set_required_trophies(self, trophies: int) -> None:
        """Set required trophies"""
        self.required_trophies = max(0, trophies)

    def add_member(self, member: AllianceMember) -> bool:
        """Add member to alliance"""
        if self.member_count >= self.max_members:
            return False

        if member.account_id in self.members:
            return False  # Already in alliance

        self.members[member.account_id] = member
        member.alliance_id = self.alliance_id
        self.member_count += 1

        # Update alliance statistics
        self.trophies += member.trophies
        self.experience += member.experience_level * 10

        return True

    def remove_member(self, account_id: int) -> bool:
        """Remove member from alliance"""
        if account_id not in self.members:
            return False

        member = self.members[account_id]

        # Update alliance statistics
        self.trophies -= member.trophies
        self.experience -= member.experience_level * 10

        del self.members[account_id]
        self.member_count -= 1

        return True

    def get_member(self, account_id: int) -> Optional[AllianceMember]:
        """Get member by account ID"""
        return self.members.get(account_id)

    def get_all_members(self) -> List[AllianceMember]:
        """Get all members"""
        return list(self.members.values())

    def get_members_by_role(self, role: int) -> List[AllianceMember]:
        """Get members by role"""
        return [member for member in self.members.values() if member.role == role]

    def get_leaders(self) -> List[AllianceMember]:
        """Get all leaders"""
        return self.get_members_by_role(4)  # Leader role = 4

    def get_co_leaders(self) -> List[AllianceMember]:
        """Get all co-leaders"""
        return self.get_members_by_role(3)  # Co-leader role = 3

    def get_elders(self) -> List[AllianceMember]:
        """Get all elders"""
        return self.get_members_by_role(2)  # Elder role = 2

    def get_members_only(self) -> List[AllianceMember]:
        """Get regular members"""
        return self.get_members_by_role(1)  # Member role = 1

    def can_join(self, player_trophies: int) -> bool:
        """Check if player can join alliance"""
        if self.member_count >= self.max_members:
            return False

        if player_trophies < self.required_trophies:
            return False

        if self.type == 3:  # Closed
            return False

        return True

    def is_open(self) -> bool:
        """Check if alliance is open"""
        return self.type == 1

    def is_invite_only(self) -> bool:
        """Check if alliance is invite only"""
        return self.type == 2

    def is_closed(self) -> bool:
        """Check if alliance is closed"""
        return self.type == 3

    def get_average_trophies(self) -> int:
        """Get average member trophies"""
        if self.member_count == 0:
            return 0
        return self.trophies // self.member_count

    def get_total_donations(self) -> int:
        """Get total donations by all members"""
        return sum(member.donations_sent for member in self.members.values())

    def get_total_donations_received(self) -> int:
        """Get total donations received by all members"""
        return sum(member.donations_received for member in self.members.values())

    def get_activity_score(self) -> int:
        """Get alliance activity score"""
        score = 0
        for member in self.members.values():
            if member.is_online():
                score += 10
            elif member.last_seen < 86400:  # Less than 24 hours
                score += 5
            elif member.last_seen < 604800:  # Less than 7 days
                score += 1
        return score

    def promote_member(self, account_id: int, promoter_id: int) -> bool:
        """Promote member"""
        member = self.get_member(account_id)
        promoter = self.get_member(promoter_id)

        if not member or not promoter:
            return False

        # Check permissions
        if promoter.role <= member.role:
            return False  # Can't promote someone of equal or higher rank

        if member.role >= 4:
            return False  # Already max rank

        member.role += 1
        return True

    def demote_member(self, account_id: int, demoter_id: int) -> bool:
        """Demote member"""
        member = self.get_member(account_id)
        demoter = self.get_member(demoter_id)

        if not member or not demoter:
            return False

        # Check permissions
        if demoter.role <= member.role:
            return False

        if member.role <= 1:
            return False  # Already min rank

        member.role -= 1
        return True

    def get_header(self) -> AllianceHeader:
        """Get alliance header"""
        header = AllianceHeader()
        header.alliance_id = self.alliance_id
        header.name = self.name
        header.badge_id = self.badge_id
        header.type = self.type
        header.member_count = self.member_count
        header.trophies = self.trophies
        header.required_trophies = self.required_trophies
        return header

    def encode(self, stream) -> None:
        """Encode alliance to stream"""
        stream.write_v_long(self.alliance_id)
        stream.write_string(self.name)
        stream.write_string(self.description)
        stream.write_v_int(self.type)
        stream.write_v_int(self.badge_id)
        stream.write_v_int(self.required_trophies)
        stream.write_v_int(self.trophies)
        stream.write_v_int(self.member_count)
        stream.write_v_int(self.experience_level)

        # Write members
        stream.write_v_int(len(self.members))
        for member in self.members.values():
            member.encode(stream)

    def decode(self, stream) -> None:
        """Decode alliance from stream"""
        self.alliance_id = stream.read_v_long()
        self.name = stream.read_string()
        self.description = stream.read_string()
        self.type = stream.read_v_int()
        self.badge_id = stream.read_v_int()
        self.required_trophies = stream.read_v_int()
        self.trophies = stream.read_v_int()
        self.member_count = stream.read_v_int()
        self.experience_level = stream.read_v_int()

        # Read members
        member_count = stream.read_v_int()
        self.members.clear()
        for i in range(member_count):
            member = AllianceMember()
            member.decode(stream)
            self.members[member.account_id] = member

    def __str__(self) -> str:
        """String representation"""
        return f"Alliance('{self.name}', {self.member_count}/{self.max_members} members, {self.trophies} trophies)"
