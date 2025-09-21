"""
Python conversion of Supercell.Laser.Logic.Friends.Friend.cs
Friend class for friend system
"""

class FriendState:
    """Friend states"""
    NONE = 0
    PENDING = 1
    ACCEPTED = 2
    BLOCKED = 3

class Friend:
    """Friend class for friend system"""

    def __init__(self):
        """Initialize friend"""
        self.account_id = 0
        self.name = ""
        self.state = FriendState.NONE
        self.level = 1
        self.trophies = 0
        self.profile_icon = 0
        self.name_color = 0

        # Activity
        self.is_online = False
        self.last_seen = 0  # Seconds since last seen

        # Friend relationship
        self.added_time = 0
        self.interaction_count = 0
        self.last_interaction = 0

        # Profile info
        self.status_message = ""
        self.favourite_brawler = 0
        self.club_name = ""
        self.club_id = 0

    def get_account_id(self) -> int:
        """Get account ID"""
        return self.account_id

    def set_account_id(self, account_id: int) -> None:
        """Set account ID"""
        self.account_id = account_id

    def get_name(self) -> str:
        """Get friend name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set friend name"""
        self.name = name

    def get_state(self) -> int:
        """Get friend state"""
        return self.state

    def set_state(self, state: int) -> None:
        """Set friend state"""
        self.state = state

    def get_level(self) -> int:
        """Get friend level"""
        return self.level

    def set_level(self, level: int) -> None:
        """Set friend level"""
        self.level = max(1, level)

    def get_trophies(self) -> int:
        """Get friend trophies"""
        return self.trophies

    def set_trophies(self, trophies: int) -> None:
        """Set friend trophies"""
        self.trophies = max(0, trophies)

    def is_friend_online(self) -> bool:
        """Check if friend is online"""
        return self.is_online

    def set_online_status(self, online: bool) -> None:
        """Set online status"""
        self.is_online = online
        if not online:
            self.last_seen = 0  # Will be set to current time externally

    def get_last_seen(self) -> int:
        """Get last seen time"""
        return self.last_seen

    def set_last_seen(self, last_seen: int) -> None:
        """Set last seen time"""
        self.last_seen = last_seen

    def is_pending(self) -> bool:
        """Check if friend request is pending"""
        return self.state == FriendState.PENDING

    def is_accepted(self) -> bool:
        """Check if friend is accepted"""
        return self.state == FriendState.ACCEPTED

    def is_blocked(self) -> bool:
        """Check if friend is blocked"""
        return self.state == FriendState.BLOCKED

    def accept_friend_request(self) -> None:
        """Accept friend request"""
        if self.state == FriendState.PENDING:
            self.state = FriendState.ACCEPTED

    def block_friend(self) -> None:
        """Block friend"""
        self.state = FriendState.BLOCKED

    def unblock_friend(self) -> None:
        """Unblock friend"""
        if self.state == FriendState.BLOCKED:
            self.state = FriendState.NONE

    def add_interaction(self) -> None:
        """Add interaction (message, battle, etc.)"""
        self.interaction_count += 1
        # last_interaction would be set externally to current time

    def get_status_message(self) -> str:
        """Get status message"""
        return self.status_message

    def set_status_message(self, message: str) -> None:
        """Set status message"""
        self.status_message = message[:100]  # Limit length

    def get_activity_status(self) -> str:
        """Get activity status string"""
        if self.is_online:
            return "Online"
        elif self.last_seen == 0:
            return "Unknown"
        elif self.last_seen < 3600:  # Less than 1 hour
            return f"{self.last_seen // 60} minutes ago"
        elif self.last_seen < 86400:  # Less than 1 day
            return f"{self.last_seen // 3600} hours ago"
        elif self.last_seen < 604800:  # Less than 7 days
            return f"{self.last_seen // 86400} days ago"
        else:
            return "Long time ago"

    def get_state_name(self) -> str:
        """Get friend state name"""
        state_names = {
            FriendState.NONE: "None",
            FriendState.PENDING: "Pending",
            FriendState.ACCEPTED: "Accepted",
            FriendState.BLOCKED: "Blocked"
        }
        return state_names.get(self.state, "Unknown")

    def encode(self, stream) -> None:
        """Encode friend to stream"""
        stream.write_v_long(self.account_id)
        stream.write_string(self.name)
        stream.write_v_int(self.state)
        stream.write_v_int(self.level)
        stream.write_v_int(self.trophies)
        stream.write_v_int(self.profile_icon)
        stream.write_v_int(self.name_color)
        stream.write_boolean(self.is_online)
        stream.write_v_int(self.last_seen)
        stream.write_string(self.status_message)
        stream.write_v_int(self.favourite_brawler)
        stream.write_string(self.club_name)

    def decode(self, stream) -> None:
        """Decode friend from stream"""
        self.account_id = stream.read_v_long()
        self.name = stream.read_string()
        self.state = stream.read_v_int()
        self.level = stream.read_v_int()
        self.trophies = stream.read_v_int()
        self.profile_icon = stream.read_v_int()
        self.name_color = stream.read_v_int()
        self.is_online = stream.read_boolean()
        self.last_seen = stream.read_v_int()
        self.status_message = stream.read_string()
        self.favourite_brawler = stream.read_v_int()
        self.club_name = stream.read_string()

    def __str__(self) -> str:
        """String representation"""
        status = "Online" if self.is_online else self.get_activity_status()
        return f"Friend('{self.name}', {self.get_state_name()}, {self.trophies} trophies, {status})"
