"""
Python conversion of Supercell.Laser.Logic.Data.GameModeVariationData.cs
Game mode variation data for different game modes
"""

from .data_tables import LogicData

class GameModeVariationData(LogicData):
    """Game mode variation data class"""

    def __init__(self):
        """Initialize game mode variation data"""
        super().__init__()
        self.name = ""
        self.variation = 0
        self.disabled = False
        self.tid = ""  # Text ID for localization

        # UI and display properties
        self.chat_suggestion_item_name = ""
        self.game_mode_room_icon_name = ""
        self.game_mode_icon_name = ""

        # Audio properties
        self.score_sfx = ""
        self.opponent_score_sfx = ""

        # Text properties
        self.score_text = ""
        self.score_text_end = ""
        self.intro_text = ""
        self.intro_desc_text = ""
        self.intro_desc_text2 = ""

        # Notification properties
        self.start_notification = ""
        self.end_notification = ""

        # Menu ordering
        self.friendly_menu_order = 0

    def get_name(self) -> str:
        """Get game mode name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set game mode name"""
        self.name = name

    def get_variation(self) -> int:
        """Get variation number"""
        return self.variation

    def set_variation(self, variation: int) -> None:
        """Set variation number"""
        self.variation = variation

    def is_disabled(self) -> bool:
        """Check if game mode is disabled"""
        return self.disabled

    def set_disabled(self, disabled: bool) -> None:
        """Set disabled status"""
        self.disabled = disabled

    def get_text_id(self) -> str:
        """Get text ID for localization"""
        return self.tid

    def set_text_id(self, tid: str) -> None:
        """Set text ID"""
        self.tid = tid

    def get_chat_suggestion_item_name(self) -> str:
        """Get chat suggestion item name"""
        return self.chat_suggestion_item_name

    def set_chat_suggestion_item_name(self, name: str) -> None:
        """Set chat suggestion item name"""
        self.chat_suggestion_item_name = name

    def get_room_icon_name(self) -> str:
        """Get room icon name"""
        return self.game_mode_room_icon_name

    def set_room_icon_name(self, icon_name: str) -> None:
        """Set room icon name"""
        self.game_mode_room_icon_name = icon_name

    def get_mode_icon_name(self) -> str:
        """Get mode icon name"""
        return self.game_mode_icon_name

    def set_mode_icon_name(self, icon_name: str) -> None:
        """Set mode icon name"""
        self.game_mode_icon_name = icon_name

    def get_score_sfx(self) -> str:
        """Get score sound effect"""
        return self.score_sfx

    def set_score_sfx(self, sfx: str) -> None:
        """Set score sound effect"""
        self.score_sfx = sfx

    def get_opponent_score_sfx(self) -> str:
        """Get opponent score sound effect"""
        return self.opponent_score_sfx

    def set_opponent_score_sfx(self, sfx: str) -> None:
        """Set opponent score sound effect"""
        self.opponent_score_sfx = sfx

    def get_score_text(self) -> str:
        """Get score text"""
        return self.score_text

    def set_score_text(self, text: str) -> None:
        """Set score text"""
        self.score_text = text

    def get_score_text_end(self) -> str:
        """Get score end text"""
        return self.score_text_end

    def set_score_text_end(self, text: str) -> None:
        """Set score end text"""
        self.score_text_end = text

    def get_intro_text(self) -> str:
        """Get intro text"""
        return self.intro_text

    def set_intro_text(self, text: str) -> None:
        """Set intro text"""
        self.intro_text = text

    def get_intro_desc_text(self) -> str:
        """Get intro description text"""
        return self.intro_desc_text

    def set_intro_desc_text(self, text: str) -> None:
        """Set intro description text"""
        self.intro_desc_text = text

    def get_intro_desc_text2(self) -> str:
        """Get second intro description text"""
        return self.intro_desc_text2

    def set_intro_desc_text2(self, text: str) -> None:
        """Set second intro description text"""
        self.intro_desc_text2 = text

    def get_start_notification(self) -> str:
        """Get start notification text"""
        return self.start_notification

    def set_start_notification(self, notification: str) -> None:
        """Set start notification text"""
        self.start_notification = notification

    def get_end_notification(self) -> str:
        """Get end notification text"""
        return self.end_notification

    def set_end_notification(self, notification: str) -> None:
        """Set end notification text"""
        self.end_notification = notification

    def get_friendly_menu_order(self) -> int:
        """Get friendly menu order"""
        return self.friendly_menu_order

    def set_friendly_menu_order(self, order: int) -> None:
        """Set friendly menu order"""
        self.friendly_menu_order = order

    def is_available(self) -> bool:
        """Check if game mode is available"""
        return not self.disabled and self.name != ""

    def has_custom_scoring(self) -> bool:
        """Check if game mode has custom scoring"""
        return self.score_text != "" or self.score_text_end != ""

    def has_intro_text(self) -> bool:
        """Check if game mode has intro text"""
        return self.intro_text != ""

    def has_sound_effects(self) -> bool:
        """Check if game mode has sound effects"""
        return self.score_sfx != "" or self.opponent_score_sfx != ""

    def __str__(self) -> str:
        """String representation"""
        status = "disabled" if self.disabled else "enabled"
        return f"GameModeVariationData('{self.name}', variation={self.variation}, {status})"
