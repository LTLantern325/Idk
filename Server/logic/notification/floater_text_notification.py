"""
Python conversion of Supercell.Laser.Logic.Notification.FloaterTextNotification.cs
Floater text notification for in-game messages
"""

from .base_notification import BaseNotification, NotificationType

class FloaterTextNotification(BaseNotification):
    """Floater text notification for brief in-game messages"""

    def __init__(self, text: str = "", x: float = 0.0, y: float = 0.0):
        """Initialize floater text notification"""
        super().__init__(NotificationType.FLOATER_TEXT)
        self.text = text
        self.x_position = x
        self.y_position = y
        self.color = 0xFFFFFF  # White color by default
        self.font_size = 12
        self.animation_type = 0  # 0 = fade in/out, 1 = slide up, 2 = bounce
        self.fade_duration = 500
        self.display_duration = 2000

        # Floater text typically has short duration and auto-dismisses
        self.duration = self.display_duration
        self.auto_dismiss = True
        self.priority = 1  # Low priority

    def get_text(self) -> str:
        """Get floater text"""
        return self.text

    def set_text(self, text: str) -> None:
        """Set floater text"""
        self.text = text

    def get_position(self) -> tuple:
        """Get floater position"""
        return (self.x_position, self.y_position)

    def set_position(self, x: float, y: float) -> None:
        """Set floater position"""
        self.x_position = x
        self.y_position = y

    def get_title(self) -> str:
        """Get notification title"""
        return "Floater Text"

    def get_message(self) -> str:
        """Get notification message"""
        return self.text

    def encode(self, stream) -> None:
        """Encode floater text notification"""
        self.encode_base(stream)
        stream.write_string(self.text)
        stream.write_float(self.x_position)
        stream.write_float(self.y_position)
        stream.write_v_int(self.color)
        stream.write_v_int(self.font_size)
        stream.write_v_int(self.animation_type)
        stream.write_v_int(self.fade_duration)
        stream.write_v_int(self.display_duration)
