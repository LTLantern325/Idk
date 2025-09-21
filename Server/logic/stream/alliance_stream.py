"""
Python conversion of Supercell.Laser.Logic.Stream.AllianceStream.cs
Alliance stream for chat and events
"""

from typing import List, Optional
from datetime import datetime, timezone

class AllianceStream:
    """Alliance stream for messages and events"""

    def __init__(self):
        """Initialize alliance stream"""
        self.entries: List['AllianceStreamEntry'] = []
        self.max_entries = 100

    def add_entry(self, entry: 'AllianceStreamEntry') -> None:
        """Add entry to stream"""
        entry.set_timestamp(datetime.now(timezone.utc))
        self.entries.insert(0, entry)  # Add to beginning

        # Keep only max entries
        if len(self.entries) > self.max_entries:
            self.entries = self.entries[:self.max_entries]

    def send_chat_message(self, member: 'AllianceMember', message: str) -> 'AllianceStreamEntry':
        """Send chat message and return entry"""
        from .entry.alliance_stream_entry import AllianceStreamEntry, StreamEntryType

        entry = AllianceStreamEntry()
        entry.set_type(StreamEntryType.CHAT_MESSAGE)
        entry.set_sender_id(member.account_id)
        entry.set_sender_name(member.avatar.name if member.avatar else "Unknown")
        entry.set_message(message)

        self.add_entry(entry)
        return entry

    def add_join_event(self, member: 'AllianceMember') -> 'AllianceStreamEntry':
        """Add member join event"""
        from .entry.alliance_stream_entry import AllianceStreamEntry, StreamEntryType

        entry = AllianceStreamEntry()
        entry.set_type(StreamEntryType.MEMBER_JOINED)
        entry.set_sender_id(member.account_id)
        entry.set_sender_name(member.avatar.name if member.avatar else "Unknown")

        self.add_entry(entry)
        return entry

    def add_leave_event(self, member: 'AllianceMember') -> 'AllianceStreamEntry':
        """Add member leave event"""
        from .entry.alliance_stream_entry import AllianceStreamEntry, StreamEntryType

        entry = AllianceStreamEntry()
        entry.set_type(StreamEntryType.MEMBER_LEFT)
        entry.set_sender_id(member.account_id)
        entry.set_sender_name(member.avatar.name if member.avatar else "Unknown")

        self.add_entry(entry)
        return entry

    def add_promotion_event(self, promoted_member: 'AllianceMember', promoter: 'AllianceMember', 
                           new_role: int) -> 'AllianceStreamEntry':
        """Add member promotion event"""
        from .entry.alliance_stream_entry import AllianceStreamEntry, StreamEntryType

        entry = AllianceStreamEntry()
        entry.set_type(StreamEntryType.MEMBER_PROMOTED)
        entry.set_sender_id(promoter.account_id)
        entry.set_sender_name(promoter.avatar.name if promoter.avatar else "Unknown")
        entry.set_target_id(promoted_member.account_id)
        entry.set_target_name(promoted_member.avatar.name if promoted_member.avatar else "Unknown")
        entry.set_extra_data(new_role)

        self.add_entry(entry)
        return entry

    def add_kick_event(self, kicked_member: 'AllianceMember', kicker: 'AllianceMember') -> 'AllianceStreamEntry':
        """Add member kick event"""
        from .entry.alliance_stream_entry import AllianceStreamEntry, StreamEntryType

        entry = AllianceStreamEntry()
        entry.set_type(StreamEntryType.MEMBER_KICKED)
        entry.set_sender_id(kicker.account_id)
        entry.set_sender_name(kicker.avatar.name if kicker.avatar else "Unknown")
        entry.set_target_id(kicked_member.account_id)
        entry.set_target_name(kicked_member.avatar.name if kicked_member.avatar else "Unknown")

        self.add_entry(entry)
        return entry

    def get_entries(self, count: int = 50) -> List['AllianceStreamEntry']:
        """Get stream entries"""
        return self.entries[:count]

    def get_recent_entries(self, hours: int = 24) -> List['AllianceStreamEntry']:
        """Get recent entries within hours"""
        cutoff_time = datetime.now(timezone.utc) - datetime.timedelta(hours=hours)
        return [entry for entry in self.entries if entry.timestamp >= cutoff_time]

    def clear_old_entries(self, days: int = 7) -> None:
        """Clear entries older than specified days"""
        cutoff_time = datetime.now(timezone.utc) - datetime.timedelta(days=days)
        self.entries = [entry for entry in self.entries if entry.timestamp >= cutoff_time]

    def get_entry_count(self) -> int:
        """Get total entry count"""
        return len(self.entries)

    def get_chat_message_count(self) -> int:
        """Get chat message count"""
        from .entry.alliance_stream_entry import StreamEntryType
        return sum(1 for entry in self.entries if entry.entry_type == StreamEntryType.CHAT_MESSAGE)

    def encode(self, stream) -> None:
        """Encode alliance stream"""
        # Encode recent entries
        recent_entries = self.get_entries(20)  # Last 20 entries
        stream.write_v_int(len(recent_entries))

        for entry in recent_entries:
            entry.encode(stream)

    def decode(self, stream) -> None:
        """Decode alliance stream"""
        entry_count = stream.read_v_int()
        self.entries = []

        for _ in range(entry_count):
            from .entry.alliance_stream_entry import AllianceStreamEntry
            entry = AllianceStreamEntry()
            entry.decode(stream)
            self.entries.append(entry)
