"""
Python conversion of Supercell.Laser.Logic.Battle.Structures.BattlePlayer.cs
Battle player class for player data in battle
"""

from typing import Dict, List, Optional
from ..objects.character import Character

class BattlePlayerState:
    """Battle player states"""
    ALIVE = 0
    DEAD = 1
    SPECTATING = 2
    DISCONNECTED = 3

class BattlePlayer:
    """Battle player class for player data in battle"""

    def __init__(self):
        """Initialize battle player"""
        self.player_id = 0
        self.account_id = 0
        self.name = ""
        self.level = 1
        self.trophies = 0
        self.state = BattlePlayerState.ALIVE

        # Team information
        self.team_id = 0
        self.team_slot = 0

        # Character information
        self.character: Optional[Character] = None
        self.character_data_id = 0
        self.character_level = 1
        self.character_trophies = 0

        # Equipment
        self.equipped_skin_id = 0
        self.equipped_star_power_id = 0
        self.equipped_gadget_id = 0
        self.equipped_gear_ids = []

        # Battle statistics
        self.kills = 0
        self.deaths = 0
        self.assists = 0
        self.damage_dealt = 0
        self.damage_taken = 0
        self.healing_done = 0
        self.time_alive = 0.0
        self.distance_moved = 0.0

        # Power-ups collected
        self.power_cubes_collected = 0
        self.current_power_level = 0

        # Battle events
        self.first_blood = False
        self.mvp = False
        self.star_player = False

        # Connection
        self.is_connected = True
        self.ping = 0
        self.disconnect_time = 0.0

    def get_player_id(self) -> int:
        """Get player ID"""
        return self.player_id

    def set_player_id(self, player_id: int) -> None:
        """Set player ID"""
        self.player_id = player_id

    def get_account_id(self) -> int:
        """Get account ID"""
        return self.account_id

    def set_account_id(self, account_id: int) -> None:
        """Set account ID"""
        self.account_id = account_id

    def get_name(self) -> str:
        """Get player name"""
        return self.name

    def set_name(self, name: str) -> None:
        """Set player name"""
        self.name = name

    def get_level(self) -> int:
        """Get player level"""
        return self.level

    def set_level(self, level: int) -> None:
        """Set player level"""
        self.level = max(1, level)

    def get_trophies(self) -> int:
        """Get player trophies"""
        return self.trophies

    def set_trophies(self, trophies: int) -> None:
        """Set player trophies"""
        self.trophies = max(0, trophies)

    def get_state(self) -> int:
        """Get player state"""
        return self.state

    def set_state(self, state: int) -> None:
        """Set player state"""
        self.state = state

    def is_alive(self) -> bool:
        """Check if player is alive"""
        return self.state == BattlePlayerState.ALIVE

    def is_dead(self) -> bool:
        """Check if player is dead"""
        return self.state == BattlePlayerState.DEAD

    def is_spectating(self) -> bool:
        """Check if player is spectating"""
        return self.state == BattlePlayerState.SPECTATING

    def is_connected(self) -> bool:
        """Check if player is connected"""
        return self.is_connected and self.state != BattlePlayerState.DISCONNECTED

    def get_team_id(self) -> int:
        """Get team ID"""
        return self.team_id

    def set_team_id(self, team_id: int) -> None:
        """Set team ID"""
        self.team_id = team_id

    def get_team_slot(self) -> int:
        """Get team slot"""
        return self.team_slot

    def set_team_slot(self, slot: int) -> None:
        """Set team slot"""
        self.team_slot = slot

    def get_character(self) -> Optional[Character]:
        """Get character object"""
        return self.character

    def set_character(self, character: Character) -> None:
        """Set character object"""
        self.character = character
        if character:
            self.character_data_id = character.character_data_id
            self.character_level = character.level

    def get_character_data_id(self) -> int:
        """Get character data ID"""
        return self.character_data_id

    def set_character_data_id(self, data_id: int) -> None:
        """Set character data ID"""
        self.character_data_id = data_id

    def get_character_level(self) -> int:
        """Get character level"""
        return self.character_level

    def set_character_level(self, level: int) -> None:
        """Set character level"""
        self.character_level = max(1, min(11, level))

    def add_kill(self, victim_id: int) -> None:
        """Add kill"""
        self.kills += 1

        # Check for first blood
        if self.kills == 1 and not self.first_blood:
            self.first_blood = True

    def add_death(self, killer_id: int) -> None:
        """Add death"""
        self.deaths += 1
        self.state = BattlePlayerState.DEAD

    def add_assist(self, victim_id: int) -> None:
        """Add assist"""
        self.assists += 1

    def add_damage_dealt(self, amount: int) -> None:
        """Add damage dealt"""
        self.damage_dealt += amount

    def add_damage_taken(self, amount: int) -> None:
        """Add damage taken"""
        self.damage_taken += amount

    def add_healing_done(self, amount: int) -> None:
        """Add healing done"""
        self.healing_done += amount

    def collect_power_cube(self) -> None:
        """Collect power cube"""
        self.power_cubes_collected += 1
        self.current_power_level += 1

    def get_kill_death_ratio(self) -> float:
        """Get kill/death ratio"""
        return self.kills / max(1, self.deaths)

    def get_damage_efficiency(self) -> float:
        """Get damage efficiency (dealt / taken)"""
        return self.damage_dealt / max(1, self.damage_taken)

    def get_score(self) -> int:
        """Get battle score"""
        score = 0
        score += self.kills * 100
        score += self.assists * 25
        score += self.damage_dealt // 10
        score += self.healing_done // 5
        score -= self.deaths * 50

        if self.first_blood:
            score += 50
        if self.mvp:
            score += 200
        if self.star_player:
            score += 100

        return max(0, score)

    def respawn(self, spawn_x: float, spawn_y: float) -> None:
        """Respawn player"""
        self.state = BattlePlayerState.ALIVE
        if self.character:
            self.character.respawn(spawn_x, spawn_y)

    def disconnect(self, current_time: float) -> None:
        """Handle player disconnect"""
        self.is_connected = False
        self.state = BattlePlayerState.DISCONNECTED
        self.disconnect_time = current_time

    def reconnect(self) -> None:
        """Handle player reconnect"""
        self.is_connected = True
        if self.state == BattlePlayerState.DISCONNECTED:
            self.state = BattlePlayerState.ALIVE
        self.disconnect_time = 0.0

    def update(self, delta_time: float) -> None:
        """Update battle player"""
        if self.is_alive():
            self.time_alive += delta_time

        # Update character if present
        if self.character:
            self.character.update(delta_time)

            # Sync character stats
            self.kills = self.character.kills
            self.damage_dealt = self.character.damage_dealt

    def get_battle_summary(self) -> Dict[str, any]:
        """Get battle summary data"""
        return {
            'player_id': self.player_id,
            'name': self.name,
            'character_id': self.character_data_id,
            'kills': self.kills,
            'deaths': self.deaths,
            'assists': self.assists,
            'damage_dealt': self.damage_dealt,
            'damage_taken': self.damage_taken,
            'healing_done': self.healing_done,
            'power_cubes': self.power_cubes_collected,
            'score': self.get_score(),
            'kda': self.get_kill_death_ratio(),
            'first_blood': self.first_blood,
            'mvp': self.mvp,
            'star_player': self.star_player
        }

    def encode(self, stream) -> None:
        """Encode battle player to stream"""
        stream.write_v_int(self.player_id)
        stream.write_v_long(self.account_id)
        stream.write_string(self.name)
        stream.write_v_int(self.level)
        stream.write_v_int(self.trophies)
        stream.write_v_int(self.state)
        stream.write_v_int(self.team_id)
        stream.write_v_int(self.character_data_id)
        stream.write_v_int(self.character_level)
        stream.write_v_int(self.kills)
        stream.write_v_int(self.deaths)
        stream.write_v_int(self.damage_dealt)
        stream.write_v_int(self.power_cubes_collected)
        stream.write_boolean(self.is_connected)

    def decode(self, stream) -> None:
        """Decode battle player from stream"""
        self.player_id = stream.read_v_int()
        self.account_id = stream.read_v_long()
        self.name = stream.read_string()
        self.level = stream.read_v_int()
        self.trophies = stream.read_v_int()
        self.state = stream.read_v_int()
        self.team_id = stream.read_v_int()
        self.character_data_id = stream.read_v_int()
        self.character_level = stream.read_v_int()
        self.kills = stream.read_v_int()
        self.deaths = stream.read_v_int()
        self.damage_dealt = stream.read_v_int()
        self.power_cubes_collected = stream.read_v_int()
        self.is_connected = stream.read_boolean()

    def __str__(self) -> str:
        """String representation"""
        return f"BattlePlayer({self.name}, K:{self.kills} D:{self.deaths} A:{self.assists})"
