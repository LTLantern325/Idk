"""
Python conversion of Supercell.Laser.Logic.Home.Quest.Quests.cs
Quest management system
"""

import random
from typing import List, TYPE_CHECKING
from .quest import Quest

if TYPE_CHECKING:
    from ...avatar.client_avatar import ClientAvatar
    from ..client_home import ClientHome

class Quests:
    """Quest management system"""

    # Game modes allowed for quests
    ALLOWED_MODES = [0, 3, 6]  # Gem Grab, Bounty, Showdown

    # Goal tables for different quest types
    GOAL_TABLE = [40000, 50000, 60000, 80000, 100000]

    def __init__(self):
        """Initialize quests"""
        self.quest_list: List[Quest] = []

    def add_random_quests(self, unlocked_heroes: List['ClientAvatar'], count: int) -> None:
        """Add random quests based on unlocked heroes"""
        if not unlocked_heroes:
            return

        character_ids = [hero.character_id for hero in unlocked_heroes]

        for _ in range(count):
            quest = Quest()

            # Random mission type (1-4)
            quest.mission_type = random.randint(1, 4)

            # 80% chance for character-specific quest
            for_character = random.randint(1, 120) > 40

            if for_character and character_ids:
                quest.character_id = random.choice(character_ids)
                quest.game_mode_variation = -1  # Any mode
            else:
                quest.game_mode_variation = random.choice(self.ALLOWED_MODES)
                quest.character_id = 0  # Any character

            # Set goals and rewards based on mission type
            if quest.mission_type == 1:  # Play battles
                quest.quest_goal = random.randint(6, 12)
                quest.reward = 500 if quest.quest_goal >= 10 else 250

            elif quest.mission_type == 2:  # Defeat enemies
                quest.quest_goal = random.randint(12, 30)
                quest.reward = 500 if quest.quest_goal >= 20 else 250

            elif quest.mission_type in [3, 4]:  # Damage or heal
                quest.quest_goal = random.choice(self.GOAL_TABLE)
                quest.reward = 500 if quest.quest_goal >= 80000 else 250

            self.quest_list.append(quest)

    def update_quests_progress(self, game_mode_variation: int, character_id: int, 
                             kills: int, damage: int, heals: int, 
                             home: 'ClientHome') -> List[Quest]:
        """Update quest progress and return progressive updates"""
        completed = []
        progressive = []

        for quest in self.quest_list.copy():
            # Check if quest matches battle context
            if not quest.matches_context(character_id, game_mode_variation):
                continue

            progress_quest = quest.clone()
            progress_made = False

            # Update based on mission type
            if quest.mission_type == 1:  # Play battles
                progress_quest.progress = 1
                quest.add_progress(1)
                progress_made = True

            elif quest.mission_type == 2:  # Defeat enemies
                if kills > 0:
                    progress_quest.progress = kills
                    quest.add_progress(kills)
                    progress_made = True

            elif quest.mission_type == 3:  # Deal damage
                if damage > 0:
                    progress_quest.progress = damage
                    quest.add_progress(damage)
                    progress_made = True

            elif quest.mission_type == 4:  # Heal teammates
                if heals > 0:
                    # Cap progress at remaining amount needed
                    remaining = quest.quest_goal - quest.current_goal
                    actual_progress = min(heals, remaining)

                    progress_quest.progress = actual_progress
                    quest.add_progress(actual_progress)
                    progress_made = True

            if progress_made:
                progressive.append(progress_quest)

                # Check if quest completed
                if quest.is_completed():
                    completed.append(quest)

        # Remove completed quests and give rewards
        for quest in completed:
            self.quest_list.remove(quest)
            if hasattr(home, 'token_reward'):
                home.token_reward += quest.reward
            if hasattr(home, 'brawl_pass_tokens'):
                home.brawl_pass_tokens += quest.reward

        return progressive

    def get_quest_count(self) -> int:
        """Get total quest count"""
        return len(self.quest_list)

    def get_completed_quest_count(self) -> int:
        """Get completed quest count"""
        return sum(1 for quest in self.quest_list if quest.is_completed())

    def get_active_quest_count(self) -> int:
        """Get active (incomplete) quest count"""
        return sum(1 for quest in self.quest_list if not quest.is_completed())

    def clear_completed_quests(self) -> List[Quest]:
        """Remove and return completed quests"""
        completed = [q for q in self.quest_list if q.is_completed()]
        self.quest_list = [q for q in self.quest_list if not q.is_completed()]
        return completed

    def get_quests_for_character(self, character_id: int) -> List[Quest]:
        """Get quests for specific character"""
        return [q for q in self.quest_list if q.is_for_character(character_id)]

    def get_quests_for_mode(self, game_mode_variation: int) -> List[Quest]:
        """Get quests for specific game mode"""
        return [q for q in self.quest_list if q.is_for_game_mode(game_mode_variation)]

    def mark_all_as_seen(self) -> None:
        """Mark all quests as seen"""
        for quest in self.quest_list:
            quest.mark_as_seen()

    def get_total_reward_tokens(self) -> int:
        """Get total tokens from all quests"""
        return sum(quest.reward for quest in self.quest_list)

    def has_character_specific_quests(self) -> bool:
        """Check if any quests are character-specific"""
        return any(quest.character_id != 0 for quest in self.quest_list)

    def has_mode_specific_quests(self) -> bool:
        """Check if any quests are mode-specific"""
        return any(quest.game_mode_variation != -1 for quest in self.quest_list)

    def encode(self, encoder) -> None:
        """Encode quests to stream"""
        encoder.write_v_int(len(self.quest_list))
        for quest in self.quest_list:
            quest.encode(encoder)

    def decode(self, decoder) -> None:
        """Decode quests from stream"""
        quest_count = decoder.read_v_int()
        self.quest_list = []

        for _ in range(quest_count):
            quest = Quest()
            quest.decode(decoder)
            self.quest_list.append(quest)

    def __str__(self) -> str:
        """String representation"""
        completed = self.get_completed_quest_count()
        total = self.get_quest_count()
        return f"Quests({completed}/{total} completed)"
