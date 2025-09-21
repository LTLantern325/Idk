"""
Python conversion of Supercell.Laser.Logic.Message.Home.NotificationMessage.cs
Notification message for in-game notifications
"""

from ..game_message import GameMessage

class NotificationMessage(GameMessage):
    """Notification message for in-game notifications"""

    def __init__(self):
        """Initialize notification message"""
        super().__init__()
        self.notification_id = 0
        self.notification_type = 0  # 0=info, 1=warning, 2=error, 3=success
        self.title = ""
        self.message_text = ""
        self.button_text = ""
        self.auto_dismiss_seconds = 0
        self.priority = 0  # 0=low, 1=normal, 2=high, 3=urgent

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24715  # Notification message

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_notification_id(self) -> int:
        """Get notification ID"""
        return self.notification_id

    def set_notification_id(self, notification_id: int) -> None:
        """Set notification ID"""
        self.notification_id = notification_id

    def get_notification_type(self) -> int:
        """Get notification type"""
        return self.notification_type

    def set_notification_type(self, notification_type: int) -> None:
        """Set notification type"""
        self.notification_type = notification_type

    def is_info_notification(self) -> bool:
        """Check if info notification"""
        return self.notification_type == 0

    def is_warning_notification(self) -> bool:
        """Check if warning notification"""
        return self.notification_type == 1

    def is_error_notification(self) -> bool:
        """Check if error notification"""
        return self.notification_type == 2

    def is_success_notification(self) -> bool:
        """Check if success notification"""
        return self.notification_type == 3

    def get_type_name(self) -> str:
        """Get human-readable type name"""
        types = {0: "Info", 1: "Warning", 2: "Error", 3: "Success"}
        return types.get(self.notification_type, "Unknown")

    def has_auto_dismiss(self) -> bool:
        """Check if notification auto-dismisses"""
        return self.auto_dismiss_seconds > 0

    def get_priority_name(self) -> str:
        """Get human-readable priority name"""
        priorities = {0: "Low", 1: "Normal", 2: "High", 3: "Urgent"}
        return priorities.get(self.priority, "Unknown")

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.notification_id)
        self.stream.write_v_int(self.notification_type)
        self.stream.write_string(self.title)
        self.stream.write_string(self.message_text)
        self.stream.write_string(self.button_text)
        self.stream.write_v_int(self.auto_dismiss_seconds)
        self.stream.write_v_int(self.priority)

    def decode(self) -> None:
        """Decode message from stream"""
        self.notification_id = self.stream.read_v_int()
        self.notification_type = self.stream.read_v_int()
        self.title = self.stream.read_string()
        self.message_text = self.stream.read_string()
        self.button_text = self.stream.read_string()
        self.auto_dismiss_seconds = self.stream.read_v_int()
        self.priority = self.stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        return (f"NotificationMessage({self.get_type_name()}, "
                f"'{self.title}', priority={self.get_priority_name()})")
