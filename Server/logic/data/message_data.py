"""
Python conversion of Supercell.Laser.Logic.Data.MessageData.cs
Message data class for chat messages and emotes
"""

from .data_tables import LogicData

class MessageData(LogicData):
    """Message data class for chat messages and emotes"""

    def __init__(self):
        """Initialize message data"""
        super().__init__()
        self.name = ""
        self.tid = ""  # Text ID for localization
        self.bubble_override_tid = ""
        self.disabled = False
        self.message_type = 0
        self.file_name = ""
        self.export_name = ""
        self.quick_emoji_type = 0
        self.sort_priority = 0
        self.age_gated = False

    def get_name(self) -> str:
        """Get message name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set message name"""
        self.name = name

    def get_text_id(self) -> str:
        """Get text ID for localization"""
        return self.tid

    def set_text_id(self, tid: str) -> None:
        """Set text ID"""
        self.tid = tid

    def get_bubble_override_tid(self) -> str:
        """Get bubble override text ID"""
        return self.bubble_override_tid

    def set_bubble_override_tid(self, tid: str) -> None:
        """Set bubble override text ID"""
        self.bubble_override_tid = tid

    def is_disabled(self) -> bool:
        """Check if message is disabled"""
        return self.disabled

    def set_disabled(self, disabled: bool) -> None:
        """Set disabled status"""
        self.disabled = disabled

    def get_message_type(self) -> int:
        """Get message type"""
        return self.message_type

    def set_message_type(self, message_type: int) -> None:
        """Set message type"""
        self.message_type = message_type

    def get_file_name(self) -> str:
        """Get file name"""
        return self.file_name

    def set_file_name(self, file_name: str) -> None:
        """Set file name"""
        self.file_name = file_name

    def get_export_name(self) -> str:
        """Get export name"""
        return self.export_name

    def set_export_name(self, export_name: str) -> None:
        """Set export name"""
        self.export_name = export_name

    def get_quick_emoji_type(self) -> int:
        """Get quick emoji type"""
        return self.quick_emoji_type

    def set_quick_emoji_type(self, emoji_type: int) -> None:
        """Set quick emoji type"""
        self.quick_emoji_type = emoji_type

    def get_sort_priority(self) -> int:
        """Get sort priority"""
        return self.sort_priority

    def set_sort_priority(self, priority: int) -> None:
        """Set sort priority"""
        self.sort_priority = priority

    def is_age_gated(self) -> bool:
        """Check if message is age gated"""
        return self.age_gated

    def set_age_gated(self, age_gated: bool) -> None:
        """Set age gated status"""
        self.age_gated = age_gated

    def has_visual_representation(self) -> bool:
        """Check if message has visual representation"""
        return self.file_name != "" and self.export_name != ""

    def has_bubble_override(self) -> bool:
        """Check if message has bubble override"""
        return self.bubble_override_tid != ""

    def is_quick_emoji(self) -> bool:
        """Check if message is a quick emoji"""
        return self.quick_emoji_type > 0

    def is_available(self) -> bool:
        """Check if message is available for use"""
        return not self.disabled and self.name != ""

    def is_suitable_for_age(self, user_age: int) -> bool:
        """Check if message is suitable for user age"""
        if not self.age_gated:
            return True
        return user_age >= 13  # Typical age gate threshold

    def __str__(self) -> str:
        """String representation"""
        status = "disabled" if self.disabled else "enabled"
        age_gate = ", age-gated" if self.age_gated else ""
        return f"MessageData('{self.name}', type={self.message_type}, {status}{age_gate})"
