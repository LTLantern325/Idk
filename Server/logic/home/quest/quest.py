"""
Python conversion of Supercell.Laser.Logic.Home.Quest.Quest.cs
Individual quest implementation
"""

from typing import TYPE_CHECKING
from ..helper.byte_stream_helper import ByteStreamHelper

if TYPE_CHECKING:
    from ...data.character_data import CharacterData

class Quest:
    """Individual quest class"""

    def __init__(self):
        """Initialize quest"""
        self.mission_type = 0  # 1=battles, 2=kills, 3=damage, 4=heal
        self.current_goal = 0
        self.quest_goal = 0
        self.game_mode_variation = -1  # -1 for any mode
        self.quest_seen = False
        self.character_id = 0  # 0 for any character
        self.reward = 0  # Token reward
        self.progress = 0

    def clone(self) -> 'Quest':
        """Create a copy of this quest"""
        new_quest = Quest()
        new_quest.mission_type = self.mission_type
        new_quest.current_goal = self.current_goal
        new_quest.quest_goal = self.quest_goal
        new_quest.game_mode_variation = self.game_mode_variation
        new_quest.quest_seen = self.quest_seen
        new_quest.character_id = self.character_id
        new_quest.reward = self.reward
        new_quest.progress = self.progress
        return new_quest

    def is_completed(self) -> bool:
        """Check if quest is completed"""
        return self.current_goal >= self.quest_goal

    def get_completion_percentage(self) -> float:
        """Get completion percentage"""
        if self.quest_goal == 0:
            return 0.0
        return min(100.0, (self.current_goal / self.quest_goal) * 100.0)

    def add_progress(self, amount: int) -> None:
        """Add progress to quest"""
        self.current_goal += amount
        self.progress = amount

    def reset_progress(self) -> None:
        """Reset quest progress"""
        self.current_goal = 0
        self.progress = 0

    def is_for_character(self, character_id: int) -> bool:
        """Check if quest is for specific character"""
        return self.character_id == 0 or self.character_id == character_id

    def is_for_game_mode(self, game_mode_variation: int) -> bool:
        """Check if quest is for specific game mode"""
        return self.game_mode_variation == -1 or self.game_mode_variation == game_mode_variation

    def matches_context(self, character_id: int, game_mode_variation: int) -> bool:
        """Check if quest matches battle context"""
        return (self.is_for_character(character_id) and 
                self.is_for_game_mode(game_mode_variation))

    def get_mission_type_name(self) -> str:
        """Get mission type name"""
        mission_names = {
            1: "Play battles",
            2: "Defeat enemies", 
            3: "Deal damage",
            4: "Heal teammates"
        }
        return mission_names.get(self.mission_type, "Unknown")

    def get_reward_tokens(self) -> int:
        """Get reward tokens"""
        return self.reward

    def set_reward_tokens(self, tokens: int) -> None:
        """Set reward tokens"""
        self.reward = max(0, tokens)

    def mark_as_seen(self) -> None:
        """Mark quest as seen by player"""
        self.quest_seen = True

    def is_seen(self) -> bool:
        """Check if quest has been seen"""
        return self.quest_seen

    def encode(self, encoder) -> None:
        """Encode quest to stream"""
        encoder.write_v_int(0)  # Unknown
        encoder.write_v_int(0)  # Unknown
        encoder.write_v_int(self.mission_type)  # Mission Type

        encoder.write_v_int(self.current_goal)  # Achieved Goal
        encoder.write_v_int(self.quest_goal)    # Quest Goal

        encoder.write_v_int(self.reward)  # Tokens Reward

        encoder.write_v_int(0)  # Unknown

        encoder.write_v_int(0)  # Current level
        encoder.write_v_int(0)  # Max level

        encoder.write_v_int(-1)  # Quest Timer

        encoder.write_boolean(False)  # Unknown
        encoder.write_boolean(self.quest_seen)  # Quest seen

        ByteStreamHelper.write_data_reference(encoder, self.character_id)

        encoder.write_v_int(self.game_mode_variation)  # Game mode variation
        encoder.write_v_int(self.progress)  # Progress

    def decode(self, decoder) -> None:
        """Decode quest from stream"""
        decoder.read_v_int()  # Unknown
        decoder.read_v_int()  # Unknown
        self.mission_type = decoder.read_v_int()

        self.current_goal = decoder.read_v_int()
        self.quest_goal = decoder.read_v_int()

        self.reward = decoder.read_v_int()

        decoder.read_v_int()  # Unknown
        decoder.read_v_int()  # Current level
        decoder.read_v_int()  # Max level
        decoder.read_v_int()  # Quest timer

        decoder.read_boolean()  # Unknown
        self.quest_seen = decoder.read_boolean()

        self.character_id = ByteStreamHelper.read_data_reference(decoder)

        self.game_mode_variation = decoder.read_v_int()
        self.progress = decoder.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        return (f"Quest({self.get_mission_type_name()}: "
                f"{self.current_goal}/{self.quest_goal}, "
                f"reward={self.reward})")
