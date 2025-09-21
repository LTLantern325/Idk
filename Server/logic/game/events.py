"""
Python conversion of Supercell.Laser.Server.Logic.Game.Events.cs
Event management system
"""

import json
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import random

from logic.data.data_tables import DataTables
from logic.data.data_type import DataType
from logic.data.location_data import LocationData
from logic.home.items.event_data import EventData
from titan.json.logic_json import LogicJSONParser, LogicJSONObject, LogicJSONArray

class Events:
    """Static class for managing events"""

    REFRESH_MINUTES: int = 3

    _refresh_timer: Optional[threading.Timer] = None
    _config_slots: List['EventSlotConfig'] = []
    _slots: Dict[int, EventData] = {}

    @classmethod
    def init(cls) -> None:
        """Initialize events system"""
        cls._load_settings()
        cls._slots = {}

        # Start refresh timer
        cls._refresh_timer = threading.Timer(
            cls.REFRESH_MINUTES * 60, 
            cls._refresh_timer_elapsed
        )
        cls._refresh_timer.start()

        # Generate initial events
        cls._generate_events()

    @classmethod
    def _generate_events(cls) -> None:
        """Generate events for all slots"""
        for config_slot in cls._config_slots:
            event = cls._generate_event(
                config_slot.allowed_modes, 
                config_slot.slot, 
                config_slot.location
            )
            if event:
                cls._slots[config_slot.slot] = event

    @classmethod
    def _refresh_timer_elapsed(cls) -> None:
        """Called when refresh timer expires"""
        cls._generate_events()

        # Restart timer
        cls._refresh_timer = threading.Timer(
            cls.REFRESH_MINUTES * 60, 
            cls._refresh_timer_elapsed
        )
        cls._refresh_timer.start()

    @classmethod
    def _generate_event(cls, game_modes: List[str], slot: int, preset_location: int) -> Optional[EventData]:
        """Generate a single event"""
        # If preset location is specified
        if preset_location != 0:
            location = DataTables.get(DataType.LOCATION).get_data_with_id(preset_location)
            if location:
                event = EventData()
                event.end_time = datetime.now() + timedelta(minutes=cls.REFRESH_MINUTES)
                event.location_id = location.get_global_id()
                event.slot = slot
                return event

        # Random location selection
        location_table = DataTables.get(DataType.LOCATION)
        count = location_table.count
        rand = random.Random()

        # First try: find enabled location with matching game mode
        tries = 0
        while tries < 1000:
            location = location_table.get_data_with_id(rand.randint(0, count - 1))
            if location and not location.disabled and location.game_mode_variation in game_modes:
                event = EventData()
                event.end_time = datetime.now() + timedelta(minutes=cls.REFRESH_MINUTES)
                event.location_id = location.get_global_id()
                event.slot = slot
                return event
            tries += 1

        # Second try: find any location with matching game mode (ignore disabled status)
        tries = 0
        while tries < 1000:
            location = location_table.get_data_with_id(rand.randint(0, count - 1))
            if location and location.game_mode_variation in game_modes:
                event = EventData()
                event.end_time = datetime.now() + timedelta(minutes=cls.REFRESH_MINUTES)
                event.location_id = location.get_global_id()
                event.slot = slot
                return event
            tries += 1

        return None

    @classmethod
    def _load_settings(cls) -> None:
        """Load settings from gameplay.json"""
        try:
            with open("gameplay.json", 'r', encoding='utf-8') as f:
                data = json.load(f)

            slots_data = data.get("slots", [])
            cls._config_slots = []

            for slot_data in slots_data:
                config = EventSlotConfig()
                config.slot = slot_data.get("slot", 0)
                config.allowed_modes = slot_data.get("game_modes", [])
                config.location = slot_data.get("location", 0)
                cls._config_slots.append(config)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading gameplay.json: {e}")
            cls._config_slots = []

    @classmethod
    def get_event(cls, slot: int) -> Optional[EventData]:
        """Get event by slot"""
        return cls._slots.get(slot)

    @classmethod
    def has_slot(cls, slot: int) -> bool:
        """Check if slot has event"""
        return slot in cls._slots

    @classmethod
    def get_events(cls) -> List[EventData]:
        """Get all events"""
        return list(cls._slots.values())

class EventSlotConfig:
    """Configuration for event slot"""

    def __init__(self):
        self.slot: int = 0
        self.allowed_modes: List[str] = []
        self.location: int = 0
