"""
Python conversion of Supercell.Laser.Logic.Battle.Objects.Item.cs
Item class for battle items and collectibles
"""

from typing import Dict, Optional
from enum import IntEnum
from .game_object import GameObject

class ItemType(IntEnum):
    """Item types"""
    COIN = 1
    GEM = 2
    POWER_CUBE = 3
    HEALING_ITEM = 4
    AMMO = 5
    SHIELD = 6
    SPEED_BOOST = 7
    DAMAGE_BOOST = 8

class ItemRarity(IntEnum):
    """Item rarities"""
    COMMON = 1
    RARE = 2
    EPIC = 3
    MYTHIC = 4
    LEGENDARY = 5

class Item(GameObject):
    """Item class for battle items and collectibles"""

    def __init__(self):
        """Initialize item"""
        super().__init__()
        self.item_data_id = 0
        self.item_type = ItemType.COIN
        self.rarity = ItemRarity.COMMON
        self.amount = 1
        self.value = 10

        # Collection properties
        self.can_be_collected = True
        self.auto_collect_radius = 50.0
        self.collection_delay = 0.0
        self.expires = False
        self.expire_time = 0.0
        self.remaining_expire_time = 0.0

        # Power-up properties
        self.is_power_up = False
        self.power_up_duration = 0.0
        self.power_up_strength = 1.0

        # Visual properties
        self.bounce_height = 10.0
        self.bounce_speed = 2.0
        self.bounce_offset = 0.0
        self.glow_intensity = 1.0

        # Collection effects
        self.collected_by_id = 0
        self.collection_time = 0.0

    def get_item_data_id(self) -> int:
        """Get item data ID"""
        return self.item_data_id

    def set_item_data_id(self, data_id: int) -> None:
        """Set item data ID"""
        self.item_data_id = data_id

    def get_item_type(self) -> ItemType:
        """Get item type"""
        return self.item_type

    def set_item_type(self, item_type: ItemType) -> None:
        """Set item type"""
        self.item_type = item_type
        self._update_item_properties()

    def get_rarity(self) -> ItemRarity:
        """Get item rarity"""
        return self.rarity

    def set_rarity(self, rarity: ItemRarity) -> None:
        """Set item rarity"""
        self.rarity = rarity
        self._update_rarity_properties()

    def get_amount(self) -> int:
        """Get item amount"""
        return self.amount

    def set_amount(self, amount: int) -> None:
        """Set item amount"""
        self.amount = max(1, amount)

    def get_value(self) -> int:
        """Get item value"""
        return self.value

    def set_value(self, value: int) -> None:
        """Set item value"""
        self.value = max(0, value)

    def can_collect(self) -> bool:
        """Check if item can be collected"""
        return (self.can_be_collected and 
                self.is_object_active() and
                self.collection_delay <= 0 and
                (not self.expires or self.remaining_expire_time > 0))

    def is_in_collection_range(self, collector_x: float, collector_y: float) -> bool:
        """Check if collector is in range"""
        distance = self.distance_to_position(collector_x, collector_y)
        return distance <= self.auto_collect_radius

    def collect(self, collector_id: int, current_time: float = 0.0) -> bool:
        """Collect item"""
        if not self.can_collect():
            return False

        self.collected_by_id = collector_id
        self.collection_time = current_time
        self.can_be_collected = False
        self.destroy()

        return True

    def is_power_up_item(self) -> bool:
        """Check if this is a power-up item"""
        return self.is_power_up

    def set_is_power_up(self, is_power_up: bool) -> None:
        """Set power-up status"""
        self.is_power_up = is_power_up

    def get_power_up_duration(self) -> float:
        """Get power-up duration"""
        return self.power_up_duration

    def set_power_up_duration(self, duration: float) -> None:
        """Set power-up duration"""
        self.power_up_duration = max(0.0, duration)

    def get_power_up_strength(self) -> float:
        """Get power-up strength"""
        return self.power_up_strength

    def set_power_up_strength(self, strength: float) -> None:
        """Set power-up strength"""
        self.power_up_strength = max(0.0, strength)

    def set_expire_time(self, expire_time: float) -> None:
        """Set item expire time"""
        self.expires = True
        self.expire_time = expire_time
        self.remaining_expire_time = expire_time

    def is_expired(self) -> bool:
        """Check if item has expired"""
        return self.expires and self.remaining_expire_time <= 0

    def get_remaining_expire_time(self) -> float:
        """Get remaining expire time"""
        return self.remaining_expire_time

    def _update_item_properties(self) -> None:
        """Update item properties based on type"""
        if self.item_type == ItemType.COIN:
            self.value = 10 * self.amount
            self.collision_radius = 15.0
        elif self.item_type == ItemType.GEM:
            self.value = 50 * self.amount
            self.collision_radius = 20.0
        elif self.item_type == ItemType.POWER_CUBE:
            self.value = 100 * self.amount
            self.collision_radius = 25.0
            self.is_power_up = True
            self.power_up_duration = 30.0
            self.power_up_strength = 0.15 * self.amount  # 15% per cube
        elif self.item_type == ItemType.HEALING_ITEM:
            self.value = 200 * self.amount  # Healing amount
            self.collision_radius = 20.0
        elif self.item_type == ItemType.AMMO:
            self.value = 1 * self.amount  # Ammo count
            self.collision_radius = 18.0
        elif self.item_type == ItemType.SHIELD:
            self.value = 500 * self.amount  # Shield amount
            self.collision_radius = 22.0
            self.is_power_up = True
            self.power_up_duration = 15.0
        elif self.item_type == ItemType.SPEED_BOOST:
            self.collision_radius = 20.0
            self.is_power_up = True
            self.power_up_duration = 10.0
            self.power_up_strength = 0.3  # 30% speed boost
        elif self.item_type == ItemType.DAMAGE_BOOST:
            self.collision_radius = 20.0
            self.is_power_up = True
            self.power_up_duration = 8.0
            self.power_up_strength = 0.25  # 25% damage boost

    def _update_rarity_properties(self) -> None:
        """Update properties based on rarity"""
        rarity_multipliers = {
            ItemRarity.COMMON: 1.0,
            ItemRarity.RARE: 1.5,
            ItemRarity.EPIC: 2.0,
            ItemRarity.MYTHIC: 3.0,
            ItemRarity.LEGENDARY: 5.0
        }

        multiplier = rarity_multipliers.get(self.rarity, 1.0)
        self.value = int(self.value * multiplier)
        self.glow_intensity = 0.5 + (int(self.rarity) * 0.2)

    def get_collection_effect_data(self) -> Dict[str, any]:
        """Get data for collection effects"""
        effect_data = {
            'type': int(self.item_type),
            'amount': self.amount,
            'value': self.value,
            'rarity': int(self.rarity)
        }

        if self.is_power_up:
            effect_data.update({
                'duration': self.power_up_duration,
                'strength': self.power_up_strength
            })

        return effect_data

    def update(self, delta_time: float) -> None:
        """Update item"""
        super().update(delta_time)

        if not self.is_object_active():
            return

        # Update collection delay
        if self.collection_delay > 0:
            self.collection_delay -= delta_time

        # Update expire time
        if self.expires and self.remaining_expire_time > 0:
            self.remaining_expire_time -= delta_time
            if self.remaining_expire_time <= 0:
                self.destroy()
                return

        # Update bounce animation
        self.bounce_offset += self.bounce_speed * delta_time
        bounce_y = (self.bounce_height * 0.5) + (self.bounce_height * 0.5 * 
                   __import__('math').sin(self.bounce_offset))

        # Visual position is offset by bounce
        self.visual_y = self.y + bounce_y

    def get_type_name(self) -> str:
        """Get item type name"""
        type_names = {
            ItemType.COIN: "Coin",
            ItemType.GEM: "Gem",
            ItemType.POWER_CUBE: "Power Cube",
            ItemType.HEALING_ITEM: "Health Pack",
            ItemType.AMMO: "Ammo",
            ItemType.SHIELD: "Shield",
            ItemType.SPEED_BOOST: "Speed Boost",
            ItemType.DAMAGE_BOOST: "Damage Boost"
        }
        return type_names.get(self.item_type, "Unknown Item")

    def get_rarity_name(self) -> str:
        """Get rarity name"""
        rarity_names = {
            ItemRarity.COMMON: "Common",
            ItemRarity.RARE: "Rare",
            ItemRarity.EPIC: "Epic",
            ItemRarity.MYTHIC: "Mythic",
            ItemRarity.LEGENDARY: "Legendary"
        }
        return rarity_names.get(self.rarity, "Unknown")

    def encode(self, stream) -> None:
        """Encode item to stream"""
        super().encode(stream)
        stream.write_v_int(self.item_data_id)
        stream.write_v_int(int(self.item_type))
        stream.write_v_int(int(self.rarity))
        stream.write_v_int(self.amount)
        stream.write_v_int(self.value)
        stream.write_boolean(self.can_be_collected)
        stream.write_boolean(self.is_power_up)
        stream.write_float(self.remaining_expire_time)

    def decode(self, stream) -> None:
        """Decode item from stream"""
        super().decode(stream)
        self.item_data_id = stream.read_v_int()
        self.item_type = ItemType(stream.read_v_int())
        self.rarity = ItemRarity(stream.read_v_int())
        self.amount = stream.read_v_int()
        self.value = stream.read_v_int()
        self.can_be_collected = stream.read_boolean()
        self.is_power_up = stream.read_boolean()
        self.remaining_expire_time = stream.read_float()
        self._update_item_properties()

    def __str__(self) -> str:
        """String representation"""
        return f"Item({self.get_type_name()} x{self.amount}, {self.get_rarity_name()})"
