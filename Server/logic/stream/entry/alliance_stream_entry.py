"""
Python conversion of Supercell.Laser.Logic.Stream.Entry.AllianceStreamEntry.cs
Alliance stream entry for chat and events
"""

from enum import IntEnum
from datetime import datetime, timezone
from typing import Optional

class StreamEntryType(IntEnum):
    """Stream entry types"""
    CHAT_MESSAGE = 1
    MEMBER_JOINED = 2
    MEMBER_LEFT = 3
    MEMBER_KICKED = 4
    MEMBER_PROMOTED = 5
    MEMBER_DEMOTED = 6
    ALLIANCE_SETTINGS_CHANGED = 7
    DONATION_REQUEST = 8
    DONATION_RECEIVED = 9

class AllianceStreamEntry:
    """Alliance stream entry"""

    def __init__(self):
        """Initialize stream entry"""
        self.entry_type = StreamEntryType.CHAT_MESSAGE
        self.sender_id = 0
        self.sender_name = ""
        self.target_id = 0
        self.target_name = ""
        self.message = ""
        self.extra_data = 0
        self.timestamp = datetime.now(timezone.utc)

    def set_type(self, entry_type: StreamEntryType) -> None:
        """Set entry type"""
        self.entry_type = entry_type

    def get_type(self) -> StreamEntryType:
        """Get entry type"""
        return self.entry_type

    def set_sender_id(self, sender_id: int) -> None:
        """Set sender ID"""
        self.sender_id = sender_id

    def get_sender_id(self) -> int:
        """Get sender ID"""
        return self.sender_id

    def set_sender_name(self, name: str) -> None:
        """Set sender name"""
        self.sender_name = name

    def get_sender_name(self) -> str:
        """Get sender name"""
        return self.sender_name

    def set_target_id(self, target_id: int) -> None:
        """Set target ID"""
        self.target_id = target_id

    def get_target_id(self) -> int:
        """Get target ID"""
        return self.target_id

    def set_target_name(self, name: str) -> None:
        """Set target name"""
        self.target_name = name

    def get_target_name(self) -> str:
        """Get target name"""
        return self.target_name

    def set_message(self, message: str) -> None:
        """Set message"""
        self.message = message

    def get_message(self) -> str:
        """Get message"""
        return self.message

    def set_extra_data(self, data: int) -> None:
        """Set extra data"""
        self.extra_data = data

    def get_extra_data(self) -> int:
        """Get extra data"""
        return self.extra_data

    def set_timestamp(self, timestamp: datetime) -> None:
        """Set timestamp"""
        self.timestamp = timestamp

    def get_timestamp(self) -> datetime:
        """Get timestamp"""
        return self.timestamp

    def is_chat_message(self) -> bool:
        """Check if entry is chat message"""
        return self.entry_type == StreamEntryType.CHAT_MESSAGE

    def is_system_message(self) -> bool:
        """Check if entry is system message"""
        return self.entry_type != StreamEntryType.CHAT_MESSAGE

    def get_age_in_seconds(self) -> int:
        """Get age in seconds"""
        now = datetime.now(timezone.utc)
        return int((now - self.timestamp).total_seconds())

    def get_age_in_minutes(self) -> int:
        """Get age in minutes"""
        return self.get_age_in_seconds() // 60

    def get_age_in_hours(self) -> int:
        """Get age in hours"""
        return self.get_age_in_minutes() // 60

    def encode(self, stream) -> None:
        """Encode stream entry"""
        stream.write_v_int(self.entry_type)
        stream.write_v_long(self.sender_id)
        stream.write_string(self.sender_name)

        # Entry-specific data
        if self.entry_type == StreamEntryType.CHAT_MESSAGE:
            stream.write_string(self.message)
        else:
            # System message
            stream.write_v_long(self.target_id)
            stream.write_string(self.target_name)
            stream.write_v_int(self.extra_data)

        # Timestamp (seconds since epoch)
        timestamp_seconds = int(self.timestamp.timestamp())
        stream.write_v_int(timestamp_seconds)

    def decode(self, stream) -> None:
        """Decode stream entry"""
        self.entry_type = StreamEntryType(stream.read_v_int())
        self.sender_id = stream.read_v_long()
        self.sender_name = stream.read_string()

        # Entry-specific data
        if self.entry_type == StreamEntryType.CHAT_MESSAGE:
            self.message = stream.read_string()
        else:
            # System message
            self.target_id = stream.read_v_long()
            self.target_name = stream.read_string()
            self.extra_data = stream.read_v_int()

        # Timestamp
        timestamp_seconds = stream.read_v_int()
        self.timestamp = datetime.fromtimestamp(timestamp_seconds, tz=timezone.utc)

    def __str__(self) -> str:
        """String representation"""
        if self.is_chat_message():
            return f"ChatMessage(from='{self.sender_name}', message='{self.message}')"
        else:
            return f"SystemMessage(type={self.entry_type.name}, sender='{self.sender_name}')"
