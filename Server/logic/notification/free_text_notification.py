"""
Python conversion of Supercell.Laser.Logic.Notification.FreeTextNotification.cs
Free text notification for general messages
"""

from .base_notification import BaseNotification, NotificationType

class FreeTextNotification(BaseNotification):
    """Free text notification for general messages"""

    def __init__(self, title: str = "", message: str = ""):
        """Initialize free text notification"""
        super().__init__(NotificationType.FREE_TEXT)
        self.title_text = title
        self.message_text = message
        self.icon_id = 0
        self.action_type = 0  # 0 = none, 1 = dismiss, 2 = action button
        self.action_text = ""
        self.action_data = ""
        self.is_persistent = False
        self.show_timestamp = True

        # Free text typically has longer duration and may not auto-dismiss
        self.duration = 5000
        self.auto_dismiss = False
        self.priority = 2  # Medium priority

    def get_title_text(self) -> str:
        """Get title text"""
        return self.title_text

    def set_title_text(self, title: str) -> None:
        """Set title text"""
        self.title_text = title

    def get_message_text(self) -> str:
        """Get message text"""
        return self.message_text

    def set_message_text(self, message: str) -> None:
        """Set message text"""
        self.message_text = message

    def is_notification_persistent(self) -> bool:
        """Check if notification is persistent"""
        return self.is_persistent

    def set_persistent(self, persistent: bool) -> None:
        """Set persistent status"""
        self.is_persistent = persistent
        if persistent:
            self.auto_dismiss = False

    def has_action(self) -> bool:
        """Check if notification has action"""
        return self.action_type > 0 and self.action_text != ""

    def get_title(self) -> str:
        """Get notification title"""
        return self.title_text

    def get_message(self) -> str:
        """Get notification message"""
        return self.message_text

    def set_simple_message(self, title: str, message: str) -> None:
        """Set simple title and message"""
        self.title_text = title
        self.message_text = message

    def encode(self, stream) -> None:
        """Encode free text notification"""
        self.encode_base(stream)
        stream.write_string(self.title_text)
        stream.write_string(self.message_text)
        stream.write_v_int(self.icon_id)
        stream.write_v_int(self.action_type)
        stream.write_string(self.action_text)
        stream.write_string(self.action_data)
        stream.write_boolean(self.is_persistent)
        stream.write_boolean(self.show_timestamp)
