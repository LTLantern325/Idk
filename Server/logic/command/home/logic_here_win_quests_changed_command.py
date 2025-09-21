"""
Python conversion of Supercell.Laser.Logic.Command.Home.LogicHeroWinQuestsChangedCommand.cs
Command for when hero win quests are changed
"""

from ..command import Command
from typing import List

class LogicHeroWinQuestsChangedCommand(Command):
    """Command for when hero win quests are changed"""

    def __init__(self):
        """Initialize hero win quests changed command"""
        super().__init__()
        self.hero_global_id = 0
        self.quest_changes = []  # List of quest change data

    def get_hero_global_id(self) -> int:
        """Get hero global ID"""
        return self.hero_global_id

    def set_hero_global_id(self, global_id: int) -> None:
        """Set hero global ID"""
        self.hero_global_id = global_id

    def add_quest_change(self, quest_id: int, change_type: int, old_value: int, new_value: int) -> None:
        """Add quest change"""
        self.quest_changes.append({
            'quest_id': quest_id,
            'change_type': change_type,  # 0=progress, 1=status, 2=target
            'old_value': old_value,
            'new_value': new_value
        })

    def get_quest_changes(self) -> List:
        """Get quest changes"""
        return self.quest_changes.copy()

    def execute(self, avatar: any) -> int:
        """Execute hero win quests changed command"""
        # Update hero quest data
        if not hasattr(avatar, 'hero_quests'):
            avatar.hero_quests = {}

        if self.hero_global_id not in avatar.hero_quests:
            avatar.hero_quests[self.hero_global_id] = {}

        hero_quests = avatar.hero_quests[self.hero_global_id]

        # Apply quest changes
        for change in self.quest_changes:
            quest_id = change['quest_id']
            change_type = change['change_type']
            new_value = change['new_value']

            if quest_id not in hero_quests:
                hero_quests[quest_id] = {
                    'progress': 0,
                    'status': 0,  # 0=active, 1=completed, 2=claimed
                    'target': 10
                }

            quest = hero_quests[quest_id]

            if change_type == 0:  # Progress change
                quest['progress'] = new_value
                # Check if quest is completed
                if quest['progress'] >= quest['target'] and quest['status'] == 0:
                    quest['status'] = 1  # Mark as completed
            elif change_type == 1:  # Status change
                quest['status'] = new_value
            elif change_type == 2:  # Target change
                quest['target'] = new_value

        # Add to quest change history
        if not hasattr(avatar, 'quest_change_history'):
            avatar.quest_change_history = []

        avatar.quest_change_history.append({
            'hero_id': self.hero_global_id,
            'changes': self.quest_changes.copy(),
            'timestamp': self.timestamp
        })

        return 0

    def encode(self, stream) -> None:
        """Encode command to stream"""
        super().encode(stream)
        stream.write_v_int(self.hero_global_id)

        # Write quest changes
        stream.write_v_int(len(self.quest_changes))
        for change in self.quest_changes:
            stream.write_v_int(change['quest_id'])
            stream.write_v_int(change['change_type'])
            stream.write_v_int(change['old_value'])
            stream.write_v_int(change['new_value'])

    def decode(self, stream) -> None:
        """Decode command from stream"""
        super().decode(stream)
        self.hero_global_id = stream.read_v_int()

        # Read quest changes
        change_count = stream.read_v_int()
        self.quest_changes.clear()
        for i in range(change_count):
            quest_id = stream.read_v_int()
            change_type = stream.read_v_int()
            old_value = stream.read_v_int()
            new_value = stream.read_v_int()
            self.quest_changes.append({
                'quest_id': quest_id,
                'change_type': change_type,
                'old_value': old_value,
                'new_value': new_value
            })

    def __str__(self) -> str:
        """String representation"""
        return f"HeroWinQuestsChangedCommand(hero_id={self.hero_global_id}, {len(self.quest_changes)} changes)"
