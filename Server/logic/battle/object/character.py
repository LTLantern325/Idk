"""
Python conversion of Supercell.Laser.Logic.Battle.Objects.Character.cs
Character class for battle characters/brawlers
"""

from typing import Dict, List, Optional
from enum import IntEnum
from .game_object import GameObject

class CharacterState(IntEnum):
    """Character states"""
    IDLE = 0
    MOVING = 1
    ATTACKING = 2
    USING_SUPER = 3
    STUNNED = 4
    DEAD = 5

class Character(GameObject):
    """Character class for battle characters/brawlers"""

    def __init__(self):
        """Initialize character"""
        super().__init__()
        self.character_data_id = 0
        self.level = 1
        self.state = CharacterState.IDLE

        # Stats
        self.max_health = 1000
        self.current_health = 1000
        self.damage = 100
        self.movement_speed = 200.0
        self.attack_range = 300.0
        self.attack_speed = 1.0  # attacks per second

        # Timers
        self.last_attack_time = 0.0
        self.attack_cooldown = 1.0  # seconds between attacks
        self.respawn_time = 0.0
        self.stun_remaining = 0.0

        # Super ability
        self.super_charge = 0
        self.super_charge_max = 1000
        self.has_super_ready = False

        # Equipment
        self.equipped_skin_id = 0
        self.equipped_gadget_id = 0
        self.equipped_star_power_id = 0
        self.equipped_gear_ids = []

        # Battle stats
        self.kills = 0
        self.assists = 0
        self.damage_dealt = 0
        self.damage_taken = 0
        self.healing_done = 0

        # Movement
        self.target_x = 0.0
        self.target_y = 0.0
        self.is_moving_to_target = False
        self.movement_direction_x = 0.0
        self.movement_direction_y = 0.0

    def get_character_data_id(self) -> int:
        """Get character data ID"""
        return self.character_data_id

    def set_character_data_id(self, data_id: int) -> None:
        """Set character data ID"""
        self.character_data_id = data_id

    def get_level(self) -> int:
        """Get character level"""
        return self.level

    def set_level(self, level: int) -> None:
        """Set character level"""
        self.level = max(1, min(11, level))
        self._update_stats_for_level()

    def _update_stats_for_level(self) -> None:
        """Update stats based on level"""
        level_multiplier = 1.0 + (self.level - 1) * 0.1
        base_health = 1000
        base_damage = 100

        self.max_health = int(base_health * level_multiplier)
        self.damage = int(base_damage * level_multiplier)

        # Heal to full if leveling up
        if self.current_health == self.max_health // level_multiplier:
            self.current_health = self.max_health

    def get_health_percentage(self) -> float:
        """Get health as percentage"""
        return (self.current_health / self.max_health) * 100.0 if self.max_health > 0 else 0.0

    def take_damage(self, amount: int, attacker_id: int = 0) -> bool:
        """Take damage and return true if killed"""
        if self.state == CharacterState.DEAD:
            return False

        old_health = self.current_health
        self.current_health = max(0, self.current_health - amount)
        actual_damage = old_health - self.current_health
        self.damage_taken += actual_damage

        # Add super charge from taking damage
        self.add_super_charge(actual_damage // 2)

        if self.current_health <= 0:
            self.die(attacker_id)
            return True

        return False

    def heal(self, amount: int) -> int:
        """Heal character and return actual amount healed"""
        if self.state == CharacterState.DEAD:
            return 0

        old_health = self.current_health
        self.current_health = min(self.max_health, self.current_health + amount)
        actual_healing = self.current_health - old_health
        self.healing_done += actual_healing

        return actual_healing

    def die(self, killer_id: int = 0) -> None:
        """Kill character"""
        self.state = CharacterState.DEAD
        self.current_health = 0
        self.respawn_time = 3.0  # 3 second respawn
        self.super_charge = 0
        self.has_super_ready = False

    def respawn(self, spawn_x: float, spawn_y: float) -> None:
        """Respawn character"""
        self.state = CharacterState.IDLE
        self.current_health = self.max_health
        self.x = spawn_x
        self.y = spawn_y
        self.respawn_time = 0.0
        self.super_charge = 0
        self.has_super_ready = False

    def can_attack(self, current_time: float) -> bool:
        """Check if can attack"""
        return (self.state != CharacterState.DEAD and 
                self.state != CharacterState.STUNNED and
                current_time - self.last_attack_time >= self.attack_cooldown)

    def attack(self, target_x: float, target_y: float, current_time: float) -> bool:
        """Perform attack"""
        if not self.can_attack(current_time):
            return False

        # Calculate distance to target
        dx = target_x - self.x
        dy = target_y - self.y
        distance = (dx * dx + dy * dy) ** 0.5

        if distance > self.attack_range:
            return False  # Out of range

        self.state = CharacterState.ATTACKING
        self.last_attack_time = current_time
        self.damage_dealt += self.damage

        # Add super charge from attacking
        self.add_super_charge(self.damage // 4)

        return True

    def can_use_super(self) -> bool:
        """Check if can use super"""
        return (self.has_super_ready and 
                self.state != CharacterState.DEAD and
                self.state != CharacterState.STUNNED)

    def use_super(self, target_x: float, target_y: float) -> bool:
        """Use super ability"""
        if not self.can_use_super():
            return False

        self.state = CharacterState.USING_SUPER
        self.super_charge = 0
        self.has_super_ready = False

        return True

    def add_super_charge(self, amount: int) -> None:
        """Add super charge"""
        if self.state == CharacterState.DEAD:
            return

        self.super_charge = min(self.super_charge_max, self.super_charge + amount)
        if self.super_charge >= self.super_charge_max:
            self.has_super_ready = True

    def get_super_charge_percentage(self) -> float:
        """Get super charge as percentage"""
        return (self.super_charge / self.super_charge_max) * 100.0

    def move_to(self, target_x: float, target_y: float) -> None:
        """Start moving to target position"""
        self.target_x = target_x
        self.target_y = target_y
        self.is_moving_to_target = True

        # Calculate movement direction
        dx = target_x - self.x
        dy = target_y - self.y
        distance = (dx * dx + dy * dy) ** 0.5

        if distance > 0:
            self.movement_direction_x = dx / distance
            self.movement_direction_y = dy / distance
            self.state = CharacterState.MOVING

    def stop_movement(self) -> None:
        """Stop movement"""
        self.is_moving_to_target = False
        self.movement_direction_x = 0.0
        self.movement_direction_y = 0.0
        if self.state == CharacterState.MOVING:
            self.state = CharacterState.IDLE

    def stun(self, duration: float) -> None:
        """Stun character"""
        if self.state != CharacterState.DEAD:
            self.state = CharacterState.STUNNED
            self.stun_remaining = duration
            self.stop_movement()

    def is_alive(self) -> bool:
        """Check if character is alive"""
        return self.state != CharacterState.DEAD

    def is_stunned(self) -> bool:
        """Check if character is stunned"""
        return self.state == CharacterState.STUNNED

    def update(self, delta_time: float) -> None:
        """Update character"""
        super().update(delta_time)

        # Update stun
        if self.is_stunned():
            self.stun_remaining -= delta_time
            if self.stun_remaining <= 0:
                self.state = CharacterState.IDLE

        # Update respawn
        if self.state == CharacterState.DEAD and self.respawn_time > 0:
            self.respawn_time -= delta_time

        # Update movement
        if self.is_moving_to_target and self.state == CharacterState.MOVING:
            move_distance = self.movement_speed * delta_time

            # Calculate distance to target
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance_to_target = (dx * dx + dy * dy) ** 0.5

            if distance_to_target <= move_distance:
                # Reached target
                self.x = self.target_x
                self.y = self.target_y
                self.stop_movement()
            else:
                # Move towards target
                self.x += self.movement_direction_x * move_distance
                self.y += self.movement_direction_y * move_distance

    def get_kill_death_ratio(self) -> float:
        """Get kill/death ratio"""
        deaths = 1  # Avoid division by zero
        return self.kills / deaths

    def encode(self, stream) -> None:
        """Encode character to stream"""
        super().encode(stream)
        stream.write_v_int(self.character_data_id)
        stream.write_v_int(self.level)
        stream.write_v_int(int(self.state))
        stream.write_v_int(self.current_health)
        stream.write_v_int(self.super_charge)
        stream.write_boolean(self.has_super_ready)
        stream.write_v_int(self.kills)
        stream.write_v_int(self.damage_dealt)

    def decode(self, stream) -> None:
        """Decode character from stream"""
        super().decode(stream)
        self.character_data_id = stream.read_v_int()
        self.level = stream.read_v_int()
        self.state = CharacterState(stream.read_v_int())
        self.current_health = stream.read_v_int()
        self.super_charge = stream.read_v_int()
        self.has_super_ready = stream.read_boolean()
        self.kills = stream.read_v_int()
        self.damage_dealt = stream.read_v_int()
        self._update_stats_for_level()

    def __str__(self) -> str:
        """String representation"""
        return f"Character(id={self.character_data_id}, level={self.level}, health={self.current_health}/{self.max_health})"
