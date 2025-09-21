"""
Python conversion of Supercell.Laser.Logic.Command.Home.LogicQuestsSeenCommand.cs
Command for marking quests as seen
"""

from ..command import Command
from typing import List

class LogicQuestsSeenCommand(Command):
    """Command for marking quests as seen"""

    def __init__(self):
        """Initialize quests seen command"""
        super().__init__()
        self.quest_ids = []  # List of quest IDs to mark as seen

    def add_quest_id(self, quest_id: int) -> None:
        """Add quest ID to mark as seen"""
        if quest_id not in self.quest_ids:
            self.quest_ids.append(quest_id)

    def get_quest_ids(self) -> List[int]:
        """Get quest IDs"""
        return self.quest_ids.copy()

    def set_quest_ids(self, quest_ids: List[int]) -> None:
        """Set quest IDs"""
        self.quest_ids = quest_ids.copy()

    def execute(self, avatar: any) -> int:
        """Execute quests seen command"""
        # Mark quests as seen
        if not hasattr(avatar, 'seen_quests'):
            avatar.seen_quests = set()

        for quest_id in self.quest_ids:
            avatar.seen_quests.add(quest_id)

        # Update quest notifications
        if hasattr(avatar, 'quest_notifications'):
            for quest_id in self.quest_ids:
                if quest_id in avatar.quest_notifications:
                    avatar.quest_notifications[quest_id]['seen'] = True

        # Update daily/weekly quest tracking
        if not hasattr(avatar, 'quest_tracking'):
            avatar.quest_tracking = {
                'daily_seen': [],
                'weekly_seen': [],
                'special_seen': []
            }

        for quest_id in self.quest_ids:
            # Determine quest type based on ID range (simplified)
            if quest_id < 1000:  # Daily quests
                if quest_id not in avatar.quest_tracking['daily_seen']:
                    avatar.quest_tracking['daily_seen'].append(quest_id)
            elif quest_id < 2000:  # Weekly quests
                if quest_id not in avatar.quest_tracking['weekly_seen']:
                    avatar.quest_tracking['weekly_seen'].append(quest_id)
            else:  # Special quests
                if quest_id not in avatar.quest_tracking['special_seen']:
                    avatar.quest_tracking['special_seen'].append(quest_id)

        return 0

    def encode(self, stream) -> None:
        """Encode command to stream"""
        super().encode(stream)
        stream.write_v_int(len(self.quest_ids))
        for quest_id in self.quest_ids:
            stream.write_v_int(quest_id)

    def decode(self, stream) -> None:
        """Decode command from stream"""
        super().decode(stream)
        quest_count = stream.read_v_int()
        self.quest_ids.clear()
        for i in range(quest_count):
            quest_id = stream.read_v_int()
            self.quest_ids.append(quest_id)

    def __str__(self) -> str:
        """String representation"""
        return f"QuestsSeenCommand({len(self.quest_ids)} quests: {self.quest_ids})"
