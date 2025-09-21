"""
Python conversion of Supercell.Laser.Logic.Data.ChallengeData.cs
Challenge data class for special events and challenges
"""

from typing import List
from .data_tables import LogicData

class ChallengeData(LogicData):
    """Challenge data class for special events and challenges"""

    def __init__(self):
        """Initialize challenge data"""
        super().__init__()
        self.name = ""
        self.challenge_id = 0
        self.file_name = ""

        # Localization arrays
        self.locale = []  # string[]
        self.logo_asset = []  # string[]

        # Visual assets
        self.event_asset = ""
        self.banner_swf = ""
        self.event_banner = ""
        self.header_frame = ""

        # Reward items
        self.reward_item = ""
        self.reward_unlocked_item = ""

        # Text IDs for localization
        self.tid = ""
        self.stage_tid = ""
        self.reward_tid = ""
        self.completed_tid = ""
        self.reward_popup_tid = ""
        self.battle_end_header_tid = ""
        self.battle_end_win_label_tid = ""
        self.battle_end_win_tid = ""

        # Notifications
        self.start_notification = ""
        self.reminder_notification = ""

        # Teaser content
        self.teaser_title_tid = ""
        self.teaser_info_tid = ""

    def get_name(self) -> str:
        """Get challenge name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set challenge name"""
        self.name = name

    def get_challenge_id(self) -> int:
        """Get challenge ID"""
        return self.challenge_id

    def set_challenge_id(self, challenge_id: int) -> None:
        """Set challenge ID"""
        self.challenge_id = challenge_id

    def get_file_name(self) -> str:
        """Get file name"""
        return self.file_name

    def set_file_name(self, file_name: str) -> None:
        """Set file name"""
        self.file_name = file_name

    def get_locales(self) -> List[str]:
        """Get supported locales"""
        return self.locale.copy()

    def add_locale(self, locale: str) -> None:
        """Add supported locale"""
        if locale not in self.locale:
            self.locale.append(locale)

    def get_logo_assets(self) -> List[str]:
        """Get logo assets"""
        return self.logo_asset.copy()

    def add_logo_asset(self, asset: str) -> None:
        """Add logo asset"""
        if asset not in self.logo_asset:
            self.logo_asset.append(asset)

    def get_event_asset(self) -> str:
        """Get event asset"""
        return self.event_asset

    def set_event_asset(self, asset: str) -> None:
        """Set event asset"""
        self.event_asset = asset

    def get_reward_item(self) -> str:
        """Get reward item"""
        return self.reward_item

    def set_reward_item(self, item: str) -> None:
        """Set reward item"""
        self.reward_item = item

    def get_reward_unlocked_item(self) -> str:
        """Get reward unlocked item"""
        return self.reward_unlocked_item

    def set_reward_unlocked_item(self, item: str) -> None:
        """Set reward unlocked item"""
        self.reward_unlocked_item = item

    def get_text_id(self) -> str:
        """Get main text ID"""
        return self.tid

    def set_text_id(self, tid: str) -> None:
        """Set main text ID"""
        self.tid = tid

    def get_start_notification(self) -> str:
        """Get start notification"""
        return self.start_notification

    def set_start_notification(self, notification: str) -> None:
        """Set start notification"""
        self.start_notification = notification

    def get_reminder_notification(self) -> str:
        """Get reminder notification"""
        return self.reminder_notification

    def set_reminder_notification(self, notification: str) -> None:
        """Set reminder notification"""
        self.reminder_notification = notification

    def has_reward(self) -> bool:
        """Check if challenge has reward"""
        return self.reward_item != ""

    def has_unlocked_reward(self) -> bool:
        """Check if challenge has unlocked reward"""
        return self.reward_unlocked_item != ""

    def has_visual_assets(self) -> bool:
        """Check if challenge has visual assets"""
        return (self.event_asset != "" or self.banner_swf != "" or 
                self.event_banner != "" or len(self.logo_asset) > 0)

    def has_notifications(self) -> bool:
        """Check if challenge has notifications"""
        return self.start_notification != "" or self.reminder_notification != ""

    def has_teaser_content(self) -> bool:
        """Check if challenge has teaser content"""
        return self.teaser_title_tid != "" or self.teaser_info_tid != ""

    def supports_locale(self, locale: str) -> bool:
        """Check if challenge supports specific locale"""
        return locale in self.locale

    def get_locale_count(self) -> int:
        """Get number of supported locales"""
        return len(self.locale)

    def get_asset_count(self) -> int:
        """Get number of logo assets"""
        return len(self.logo_asset)

    def has_battle_end_content(self) -> bool:
        """Check if challenge has battle end content"""
        return (self.battle_end_header_tid != "" or 
                self.battle_end_win_label_tid != "" or 
                self.battle_end_win_tid != "")

    def get_all_text_ids(self) -> List[str]:
        """Get all text IDs used by this challenge"""
        text_ids = []
        for tid in [self.tid, self.stage_tid, self.reward_tid, self.completed_tid,
                   self.reward_popup_tid, self.battle_end_header_tid,
                   self.battle_end_win_label_tid, self.battle_end_win_tid,
                   self.teaser_title_tid, self.teaser_info_tid]:
            if tid:
                text_ids.append(tid)
        return text_ids

    def __str__(self) -> str:
        """String representation"""
        return (f"ChallengeData('{self.name}', id={self.challenge_id}, "
                f"locales={len(self.locale)}, has_reward={self.has_reward()})")
