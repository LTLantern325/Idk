"""
Python conversion of Supercell.Laser.Logic.Club.AllianceMember.cs
Alliance member class for club member data
"""

class AllianceMemberRole:
    """Alliance member roles"""
    MEMBER = 1
    ELDER = 2
    CO_LEADER = 3
    LEADER = 4

class AllianceMember:
    """Alliance member class for club member data"""

    def __init__(self):
        """Initialize alliance member"""
        self.account_id = 0
        self.name = ""
        self.role = AllianceMemberRole.MEMBER
        self.experience_level = 1
        self.trophies = 0
        self.donations_sent = 0
        self.donations_received = 0

        # Activity tracking
        self.last_seen = 0  # Seconds since last seen
        self.season_score = 0

        # Alliance info
        self.alliance_id = 0
        self.join_date = 0

        # Profile
        self.profile_icon_id = 0
        self.name_color_id = 0

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

    def get_role(self) -> int:
        """Get member role"""
        return self.role

    def set_role(self, role: int) -> None:
        """Set member role"""
        self.role = max(1, min(4, role))

    def get_experience_level(self) -> int:
        """Get experience level"""
        return self.experience_level

    def set_experience_level(self, level: int) -> None:
        """Set experience level"""
        self.experience_level = max(1, level)

    def get_trophies(self) -> int:
        """Get member trophies"""
        return self.trophies

    def set_trophies(self, trophies: int) -> None:
        """Set member trophies"""
        self.trophies = max(0, trophies)

    def get_donations_sent(self) -> int:
        """Get donations sent"""
        return self.donations_sent

    def add_donation_sent(self, amount: int) -> None:
        """Add to donations sent"""
        self.donations_sent += amount

    def get_donations_received(self) -> int:
        """Get donations received"""
        return self.donations_received

    def add_donation_received(self, amount: int) -> None:
        """Add to donations received"""
        self.donations_received += amount

    def get_last_seen(self) -> int:
        """Get last seen time"""
        return self.last_seen

    def set_last_seen(self, last_seen: int) -> None:
        """Set last seen time"""
        self.last_seen = max(0, last_seen)

    def is_online(self) -> bool:
        """Check if member is online"""
        return self.last_seen == 0

    def is_recently_active(self, threshold: int = 3600) -> bool:
        """Check if member was recently active"""
        return self.last_seen <= threshold  # Within threshold seconds

    def is_member(self) -> bool:
        """Check if role is member"""
        return self.role == AllianceMemberRole.MEMBER

    def is_elder(self) -> bool:
        """Check if role is elder"""
        return self.role == AllianceMemberRole.ELDER

    def is_co_leader(self) -> bool:
        """Check if role is co-leader"""
        return self.role == AllianceMemberRole.CO_LEADER

    def is_leader(self) -> bool:
        """Check if role is leader"""
        return self.role == AllianceMemberRole.LEADER

    def has_kick_permission(self) -> bool:
        """Check if can kick members"""
        return self.role >= AllianceMemberRole.CO_LEADER

    def has_invite_permission(self) -> bool:
        """Check if can invite members"""
        return self.role >= AllianceMemberRole.ELDER

    def has_promote_permission(self) -> bool:
        """Check if can promote members"""
        return self.role >= AllianceMemberRole.CO_LEADER

    def can_promote_to_role(self, target_role: int) -> bool:
        """Check if can promote to specific role"""
        return self.role > target_role and self.has_promote_permission()

    def get_role_name(self) -> str:
        """Get role name"""
        role_names = {
            AllianceMemberRole.MEMBER: "Member",
            AllianceMemberRole.ELDER: "Elder",
            AllianceMemberRole.CO_LEADER: "Co-Leader",
            AllianceMemberRole.LEADER: "Leader"
        }
        return role_names.get(self.role, "Unknown")

    def get_donation_ratio(self) -> float:
        """Get donation sent/received ratio"""
        if self.donations_received == 0:
            return float('inf') if self.donations_sent > 0 else 0.0
        return self.donations_sent / self.donations_received

    def get_activity_status(self) -> str:
        """Get activity status string"""
        if self.is_online():
            return "Online"
        elif self.last_seen < 3600:  # Less than 1 hour
            return f"{self.last_seen // 60} minutes ago"
        elif self.last_seen < 86400:  # Less than 1 day
            return f"{self.last_seen // 3600} hours ago"
        elif self.last_seen < 604800:  # Less than 7 days
            return f"{self.last_seen // 86400} days ago"
        else:
            return "Long time ago"

    def reset_season_stats(self) -> None:
        """Reset season statistics"""
        self.season_score = 0
        self.donations_sent = 0
        self.donations_received = 0

    def encode(self, stream) -> None:
        """Encode alliance member to stream"""
        stream.write_v_long(self.account_id)
        stream.write_string(self.name)
        stream.write_v_int(self.role)
        stream.write_v_int(self.experience_level)
        stream.write_v_int(self.trophies)
        stream.write_v_int(self.donations_sent)
        stream.write_v_int(self.donations_received)
        stream.write_v_int(self.last_seen)
        stream.write_v_int(self.season_score)
        stream.write_v_int(self.profile_icon_id)
        stream.write_v_int(self.name_color_id)

    def decode(self, stream) -> None:
        """Decode alliance member from stream"""
        self.account_id = stream.read_v_long()
        self.name = stream.read_string()
        self.role = stream.read_v_int()
        self.experience_level = stream.read_v_int()
        self.trophies = stream.read_v_int()
        self.donations_sent = stream.read_v_int()
        self.donations_received = stream.read_v_int()
        self.last_seen = stream.read_v_int()
        self.season_score = stream.read_v_int()
        self.profile_icon_id = stream.read_v_int()
        self.name_color_id = stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        return f"AllianceMember('{self.name}', {self.get_role_name()}, {self.trophies} trophies)"
