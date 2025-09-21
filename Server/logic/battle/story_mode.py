"""
Python conversion of Supercell.Laser.Logic.Battle.StoryMode.cs
Story mode for single player campaigns
"""

from typing import List, Dict, Optional

class StoryChapter:
    """Story mode chapter"""

    def __init__(self, chapter_id: int, name: str):
        """Initialize story chapter"""
        self.chapter_id = chapter_id
        self.name = name
        self.levels = []  # List of story levels
        self.is_unlocked = False
        self.stars_earned = 0
        self.max_stars = 0

    def add_level(self, level_id: int, name: str, difficulty: int) -> None:
        """Add level to chapter"""
        level_data = {
            'level_id': level_id,
            'name': name,
            'difficulty': difficulty,
            'completed': False,
            'stars': 0
        }
        self.levels.append(level_data)
        self.max_stars += 3  # Max 3 stars per level

    def complete_level(self, level_id: int, stars: int) -> bool:
        """Complete a level with star rating"""
        for level in self.levels:
            if level['level_id'] == level_id:
                level['completed'] = True
                old_stars = level['stars']
                level['stars'] = max(old_stars, stars)
                self.stars_earned += (stars - old_stars)
                return True
        return False

    def is_chapter_completed(self) -> bool:
        """Check if all levels in chapter are completed"""
        return all(level['completed'] for level in self.levels)

    def get_completion_percentage(self) -> float:
        """Get completion percentage"""
        if not self.levels:
            return 0.0
        completed = sum(1 for level in self.levels if level['completed'])
        return (completed / len(self.levels)) * 100.0

class StoryMode:
    """Story mode management"""

    def __init__(self):
        """Initialize story mode"""
        self.chapters = {}  # Dict[int, StoryChapter]
        self.current_chapter = 0
        self.total_stars = 0
        self.experience_gained = 0

        # Initialize default chapters
        self._initialize_chapters()

    def _initialize_chapters(self) -> None:
        """Initialize default story chapters"""
        # Chapter 1: Training Grounds
        chapter1 = StoryChapter(1, "Training Grounds")
        chapter1.add_level(101, "First Steps", 1)
        chapter1.add_level(102, "Power Up", 1)
        chapter1.add_level(103, "Team Work", 2)
        chapter1.is_unlocked = True
        self.chapters[1] = chapter1

        # Chapter 2: Forest Adventures
        chapter2 = StoryChapter(2, "Forest Adventures")
        chapter2.add_level(201, "Into the Woods", 2)
        chapter2.add_level(202, "Hidden Treasures", 3)
        chapter2.add_level(203, "Boss Fight", 4)
        self.chapters[2] = chapter2

        # Chapter 3: Desert Trials
        chapter3 = StoryChapter(3, "Desert Trials")
        chapter3.add_level(301, "Sandstorm", 3)
        chapter3.add_level(302, "Oasis Defense", 4)
        chapter3.add_level(303, "Pyramid Escape", 5)
        self.chapters[3] = chapter3

    def get_chapter(self, chapter_id: int) -> Optional[StoryChapter]:
        """Get chapter by ID"""
        return self.chapters.get(chapter_id)

    def unlock_chapter(self, chapter_id: int) -> bool:
        """Unlock a chapter"""
        chapter = self.chapters.get(chapter_id)
        if chapter:
            chapter.is_unlocked = True
            return True
        return False

    def complete_level(self, chapter_id: int, level_id: int, stars: int) -> bool:
        """Complete a story level"""
        chapter = self.chapters.get(chapter_id)
        if chapter and chapter.is_unlocked:
            success = chapter.complete_level(level_id, stars)
            if success:
                self.total_stars += stars
                self.experience_gained += stars * 10  # 10 XP per star

                # Auto-unlock next chapter if current is completed
                if chapter.is_chapter_completed():
                    next_chapter_id = chapter_id + 1
                    if next_chapter_id in self.chapters:
                        self.unlock_chapter(next_chapter_id)

                return True
        return False

    def get_available_chapters(self) -> List[StoryChapter]:
        """Get list of unlocked chapters"""
        return [chapter for chapter in self.chapters.values() if chapter.is_unlocked]

    def get_total_completion(self) -> float:
        """Get total completion percentage across all chapters"""
        if not self.chapters:
            return 0.0

        total_levels = 0
        completed_levels = 0

        for chapter in self.chapters.values():
            total_levels += len(chapter.levels)
            completed_levels += sum(1 for level in chapter.levels if level['completed'])

        return (completed_levels / total_levels) * 100.0 if total_levels > 0 else 0.0

    def get_rewards_earned(self) -> Dict[str, int]:
        """Get total rewards earned from story mode"""
        return {
            'stars': self.total_stars,
            'experience': self.experience_gained,
            'coins': self.total_stars * 5,  # 5 coins per star
            'tokens': self.total_stars * 2  # 2 tokens per star
        }

    def can_replay_level(self, chapter_id: int, level_id: int) -> bool:
        """Check if level can be replayed for better score"""
        chapter = self.chapters.get(chapter_id)
        if not chapter:
            return False

        for level in chapter.levels:
            if level['level_id'] == level_id:
                return level['completed'] and level['stars'] < 3
        return False

    def encode(self, stream) -> None:
        """Encode story mode progress to stream"""
        stream.write_v_int(len(self.chapters))
        for chapter_id, chapter in self.chapters.items():
            stream.write_v_int(chapter_id)
            stream.write_boolean(chapter.is_unlocked)
            stream.write_v_int(chapter.stars_earned)

            stream.write_v_int(len(chapter.levels))
            for level in chapter.levels:
                stream.write_v_int(level['level_id'])
                stream.write_boolean(level['completed'])
                stream.write_v_int(level['stars'])

        stream.write_v_int(self.total_stars)
        stream.write_v_int(self.experience_gained)

    def decode(self, stream) -> None:
        """Decode story mode progress from stream"""
        chapter_count = stream.read_v_int()
        for i in range(chapter_count):
            chapter_id = stream.read_v_int()
            is_unlocked = stream.read_boolean()
            stars_earned = stream.read_v_int()

            if chapter_id in self.chapters:
                chapter = self.chapters[chapter_id]
                chapter.is_unlocked = is_unlocked
                chapter.stars_earned = stars_earned

            level_count = stream.read_v_int()
            for j in range(level_count):
                level_id = stream.read_v_int()
                completed = stream.read_boolean()
                stars = stream.read_v_int()

                # Update level progress if chapter exists
                if chapter_id in self.chapters:
                    chapter = self.chapters[chapter_id]
                    for level in chapter.levels:
                        if level['level_id'] == level_id:
                            level['completed'] = completed
                            level['stars'] = stars
                            break

        self.total_stars = stream.read_v_int()
        self.experience_gained = stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        return f"StoryMode(chapters={len(self.chapters)}, stars={self.total_stars})"
