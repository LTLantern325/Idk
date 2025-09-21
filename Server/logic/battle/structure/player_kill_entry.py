"""
Python conversion of Supercell.Laser.Logic.Battle.Structures.PlayerKillEntry.cs
Player kill entry for tracking kills in battle
"""

from typing import Optional

class KillType:
    """Kill types"""
    NORMAL = 0
    HEADSHOT = 1
    MELEE = 2
    EXPLOSION = 3
    ENVIRONMENTAL = 4
    SUPER = 5

class PlayerKillEntry:
    """Player kill entry for tracking kills in battle"""

    def __init__(self):
        """Initialize kill entry"""
        self.killer_id = 0
        self.victim_id = 0
        self.kill_type = KillType.NORMAL
        self.timestamp = 0.0
        self.position_x = 0.0
        self.position_y = 0.0

        # Kill details
        self.weapon_id = 0
        self.damage_dealt = 0
        self.distance = 0.0
        self.is_revenge = False
        self.is_first_blood = False
        self.kill_streak = 0

        # Assist information
        self.assist_players = []  # List of player IDs who assisted
        self.assist_damage = {}   # Dict[player_id, damage_dealt]

        # Special conditions
        self.was_headshot = False
        self.was_environmental = False
        self.used_super = False
        self.used_gadget = False

    def get_killer_id(self) -> int:
        """Get killer player ID"""
        return self.killer_id

    def set_killer_id(self, killer_id: int) -> None:
        """Set killer player ID"""
        self.killer_id = killer_id

    def get_victim_id(self) -> int:
        """Get victim player ID"""
        return self.victim_id

    def set_victim_id(self, victim_id: int) -> None:
        """Set victim player ID"""
        self.victim_id = victim_id

    def get_kill_type(self) -> int:
        """Get kill type"""
        return self.kill_type

    def set_kill_type(self, kill_type: int) -> None:
        """Set kill type"""
        self.kill_type = kill_type

    def get_timestamp(self) -> float:
        """Get kill timestamp"""
        return self.timestamp

    def set_timestamp(self, timestamp: float) -> None:
        """Set kill timestamp"""
        self.timestamp = timestamp

    def get_position(self) -> tuple:
        """Get kill position"""
        return (self.position_x, self.position_y)

    def set_position(self, x: float, y: float) -> None:
        """Set kill position"""
        self.position_x = x
        self.position_y = y

    def get_weapon_id(self) -> int:
        """Get weapon ID used for kill"""
        return self.weapon_id

    def set_weapon_id(self, weapon_id: int) -> None:
        """Set weapon ID"""
        self.weapon_id = weapon_id

    def get_damage_dealt(self) -> int:
        """Get damage dealt for kill"""
        return self.damage_dealt

    def set_damage_dealt(self, damage: int) -> None:
        """Set damage dealt"""
        self.damage_dealt = damage

    def get_distance(self) -> float:
        """Get kill distance"""
        return self.distance

    def set_distance(self, distance: float) -> None:
        """Set kill distance"""
        self.distance = distance

    def set_revenge_kill(self, is_revenge: bool) -> None:
        """Set revenge kill status"""
        self.is_revenge = is_revenge

    def is_revenge_kill(self) -> bool:
        """Check if this was a revenge kill"""
        return self.is_revenge

    def set_first_blood(self, is_first_blood: bool) -> None:
        """Set first blood status"""
        self.is_first_blood = is_first_blood

    def is_first_blood_kill(self) -> bool:
        """Check if this was first blood"""
        return self.is_first_blood

    def get_kill_streak(self) -> int:
        """Get killer's kill streak"""
        return self.kill_streak

    def set_kill_streak(self, streak: int) -> None:
        """Set kill streak"""
        self.kill_streak = max(0, streak)

    def add_assist(self, player_id: int, damage: int) -> None:
        """Add assist to kill"""
        if player_id != self.killer_id and player_id != self.victim_id:
            if player_id not in self.assist_players:
                self.assist_players.append(player_id)
            self.assist_damage[player_id] = damage

    def get_assist_players(self) -> list:
        """Get list of assist player IDs"""
        return self.assist_players.copy()

    def get_assist_count(self) -> int:
        """Get number of assists"""
        return len(self.assist_players)

    def get_assist_damage(self, player_id: int) -> int:
        """Get assist damage by player"""
        return self.assist_damage.get(player_id, 0)

    def get_total_assist_damage(self) -> int:
        """Get total assist damage"""
        return sum(self.assist_damage.values())

    def set_headshot(self, was_headshot: bool) -> None:
        """Set headshot status"""
        self.was_headshot = was_headshot
        if was_headshot:
            self.kill_type = KillType.HEADSHOT

    def is_headshot_kill(self) -> bool:
        """Check if kill was headshot"""
        return self.was_headshot

    def set_environmental(self, was_environmental: bool) -> None:
        """Set environmental kill status"""
        self.was_environmental = was_environmental
        if was_environmental:
            self.kill_type = KillType.ENVIRONMENTAL

    def is_environmental_kill(self) -> bool:
        """Check if kill was environmental"""
        return self.was_environmental

    def set_used_super(self, used_super: bool) -> None:
        """Set super ability usage"""
        self.used_super = used_super
        if used_super:
            self.kill_type = KillType.SUPER

    def was_super_kill(self) -> bool:
        """Check if super was used for kill"""
        return self.used_super

    def set_used_gadget(self, used_gadget: bool) -> None:
        """Set gadget usage"""
        self.used_gadget = used_gadget

    def was_gadget_kill(self) -> bool:
        """Check if gadget was used for kill"""
        return self.used_gadget

    def is_long_range_kill(self, min_distance: float = 500.0) -> bool:
        """Check if kill was long range"""
        return self.distance >= min_distance

    def is_close_range_kill(self, max_distance: float = 100.0) -> bool:
        """Check if kill was close range"""
        return self.distance <= max_distance

    def get_kill_score(self) -> int:
        """Calculate score for this kill"""
        base_score = 100

        # Bonus for special kills
        if self.is_first_blood:
            base_score += 50
        if self.is_headshot_kill():
            base_score += 25
        if self.is_revenge_kill():
            base_score += 20
        if self.is_long_range_kill():
            base_score += 15
        if self.was_super_kill():
            base_score += 30

        # Kill streak bonus
        streak_bonus = min(self.kill_streak * 10, 100)
        base_score += streak_bonus

        return base_score

    def get_kill_type_name(self) -> str:
        """Get kill type name"""
        type_names = {
            KillType.NORMAL: "Normal",
            KillType.HEADSHOT: "Headshot",
            KillType.MELEE: "Melee",
            KillType.EXPLOSION: "Explosion",
            KillType.ENVIRONMENTAL: "Environmental",
            KillType.SUPER: "Super"
        }
        return type_names.get(self.kill_type, "Unknown")

    def get_kill_description(self) -> str:
        """Get detailed kill description"""
        desc = f"{self.get_kill_type_name()} kill"

        modifiers = []
        if self.is_first_blood:
            modifiers.append("First Blood")
        if self.is_revenge_kill():
            modifiers.append("Revenge")
        if self.is_long_range_kill():
            modifiers.append("Long Range")
        if self.was_gadget_kill():
            modifiers.append("Gadget")

        if modifiers:
            desc += f" ({', '.join(modifiers)})"

        if self.kill_streak > 1:
            desc += f" - {self.kill_streak} Kill Streak"

        return desc

    def encode(self, stream) -> None:
        """Encode kill entry to stream"""
        stream.write_v_int(self.killer_id)
        stream.write_v_int(self.victim_id)
        stream.write_v_int(self.kill_type)
        stream.write_float(self.timestamp)
        stream.write_float(self.position_x)
        stream.write_float(self.position_y)
        stream.write_v_int(self.weapon_id)
        stream.write_v_int(self.damage_dealt)
        stream.write_float(self.distance)
        stream.write_boolean(self.is_revenge)
        stream.write_boolean(self.is_first_blood)
        stream.write_v_int(self.kill_streak)

        # Write assists
        stream.write_v_int(len(self.assist_players))
        for player_id in self.assist_players:
            stream.write_v_int(player_id)
            stream.write_v_int(self.assist_damage.get(player_id, 0))

    def decode(self, stream) -> None:
        """Decode kill entry from stream"""
        self.killer_id = stream.read_v_int()
        self.victim_id = stream.read_v_int()
        self.kill_type = stream.read_v_int()
        self.timestamp = stream.read_float()
        self.position_x = stream.read_float()
        self.position_y = stream.read_float()
        self.weapon_id = stream.read_v_int()
        self.damage_dealt = stream.read_v_int()
        self.distance = stream.read_float()
        self.is_revenge = stream.read_boolean()
        self.is_first_blood = stream.read_boolean()
        self.kill_streak = stream.read_v_int()

        # Read assists
        assist_count = stream.read_v_int()
        self.assist_players.clear()
        self.assist_damage.clear()

        for i in range(assist_count):
            player_id = stream.read_v_int()
            damage = stream.read_v_int()
            self.assist_players.append(player_id)
            self.assist_damage[player_id] = damage

    def __str__(self) -> str:
        """String representation"""
        return f"KillEntry(Killer:{self.killer_id} -> Victim:{self.victim_id}, {self.get_kill_description()})"
