"""
Python conversion of Supercell.Laser.Logic.Notification.BaseNotification.cs
Base notification class for all game notifications
"""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from enum import IntEnum

class NotificationType(IntEnum):
    """Notification type enumeration"""
    FLOATER_TEXT = 1
    FREE_TEXT = 2
    REWARD_RECEIVED = 3
    LEVEL_UP = 4
    ACHIEVEMENT = 5

class BaseNotification(ABC):
    """Base class for all notifications"""

    def __init__(self, notification_type: NotificationType):
        """Initialize base notification"""
        self.notification_type = notification_type
        self.timestamp = datetime.now(timezone.utc)
        self.is_read = False
        self.is_dismissed = False
        self.priority = 1  # 1 = low, 2 = medium, 3 = high
        self.duration = 3000  # Duration in milliseconds
        self.auto_dismiss = True

    def get_notification_type(self) -> NotificationType:
        """Get notification type"""
        return self.notification_type

    def mark_as_read(self) -> None:
        """Mark notification as read"""
        self.is_read = True

    def dismiss(self) -> None:
        """Dismiss notification"""
        self.is_dismissed = True
        self.is_read = True

    def get_age_in_seconds(self) -> int:
        """Get notification age in seconds"""
        now = datetime.now(timezone.utc)
        return int((now - self.timestamp).total_seconds())

    def is_expired(self, max_age_seconds: int = 86400) -> bool:
        """Check if notification is expired (default 24 hours)"""
        return self.get_age_in_seconds() > max_age_seconds

    @abstractmethod
    def get_title(self) -> str:
        """Get notification title"""
        pass

    @abstractmethod
    def get_message(self) -> str:
        """Get notification message"""
        pass

    @abstractmethod
    def encode(self, stream) -> None:
        """Encode notification to stream"""
        pass

    def encode_base(self, stream) -> None:
        """Encode base notification data"""
        stream.write_v_int(int(self.notification_type))
        stream.write_v_long(int(self.timestamp.timestamp()))
        stream.write_boolean(self.is_read)
        stream.write_boolean(self.is_dismissed)
        stream.write_v_int(self.priority)
        stream.write_v_int(self.duration)
        stream.write_boolean(self.auto_dismiss)
