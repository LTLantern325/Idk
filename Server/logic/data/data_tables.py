"""
Python conversion of Supercell.Laser.Logic.Data.DataTables.cs
Data tables manager for game data
"""

from typing import Dict, List, Optional, Any
from enum import IntEnum

class DataType(IntEnum):
    """Data type enumeration"""
    ACCESSORY = 1
    ALLIANCE_BADGE = 2
    ALLIANCE_ROLE = 3
    AREA_EFFECT = 4
    BOSS = 5
    CAMPAIGN = 6
    CARD = 7
    CHALLENGE = 8
    CHARACTER = 16
    EMOTE = 17
    GAME_MODE_VARIATION = 18
    GEAR = 19
    GLOBAL = 20
    ITEM = 21
    LOCALE = 22
    LOCATION = 23
    LOCATION_THEME = 24
    MAP_BLOCK = 25
    MAP = 26
    MESSAGE = 27
    MILESTONE = 28
    NAME_COLOR = 29
    PIN = 30
    PLAYER_THUMBNAIL = 31
    PROJECTILE = 32
    REGION = 33
    RESOURCE = 34
    SKILL = 35
    SKIN_CONF = 36
    SKIN = 37
    SKIN_RARITY = 38
    THEME = 39
    TILE = 40

class LogicData:
    """Base logic data class"""

    def __init__(self):
        """Initialize logic data"""
        self.name = ""
        self.instance_id = 0
        self.global_id = 0

    def get_name(self) -> str:
        """Get data name"""
        return self.name

    def get_instance_id(self) -> int:
        """Get instance ID"""
        return self.instance_id

    def get_global_id(self) -> int:
        """Get global ID"""
        return self.global_id

    def set_instance_id(self, instance_id: int) -> None:
        """Set instance ID"""
        self.instance_id = instance_id

    def set_global_id(self, global_id: int) -> None:
        """Set global ID"""
        self.global_id = global_id

class LogicDataTable:
    """Logic data table for specific data type"""

    def __init__(self, data_type: DataType):
        """Initialize data table"""
        self.data_type = data_type
        self.datas: List[LogicData] = []
        self.data_map: Dict[int, LogicData] = {}

    def add_data(self, data: LogicData) -> None:
        """Add data to table"""
        self.datas.append(data)
        self.data_map[data.get_instance_id()] = data

    def get_data(self, index: int) -> Optional[LogicData]:
        """Get data by index"""
        if 0 <= index < len(self.datas):
            return self.datas[index]
        return None

    def get_data_with_id(self, instance_id: int) -> Optional[LogicData]:
        """Get data by instance ID"""
        return self.data_map.get(instance_id)

    def get_datas(self) -> List[LogicData]:
        """Get all data"""
        return self.datas

    def get_data_count(self) -> int:
        """Get data count"""
        return len(self.datas)

    def get_data_type(self) -> DataType:
        """Get data type"""
        return self.data_type

class DataTables:
    """Static data tables manager"""

    _tables: Dict[DataType, LogicDataTable] = {}
    _initialized = False

    @classmethod
    def initialize(cls) -> None:
        """Initialize all data tables"""
        if cls._initialized:
            return

        # Initialize all data types
        for data_type in DataType:
            cls._tables[data_type] = LogicDataTable(data_type)

        cls._load_game_data()
        cls._initialized = True

    @classmethod
    def _load_game_data(cls) -> None:
        """Load game data (placeholder implementation)"""
        # This would load actual game data from files
        # For now, create some dummy data

        # Character data (simplified)
        character_table = cls._tables[DataType.CHARACTER]
        for i in range(50):  # Create 50 dummy characters
            character = LogicData()
            character.name = f"Character_{i}"
            character.set_instance_id(i)
            character.set_global_id(16000000 + i)
            character_table.add_data(character)

    @classmethod
    def get(cls, data_type: DataType) -> LogicDataTable:
        """Get data table by type"""
        if not cls._initialized:
            cls.initialize()
        return cls._tables.get(data_type, LogicDataTable(data_type))

    @classmethod
    def get_table(cls, table_index: int) -> LogicDataTable:
        """Get data table by index"""
        # Convert index to DataType (simplified mapping)
        data_type = DataType(table_index) if table_index in DataType._value2member_map_ else DataType.CHARACTER
        return cls.get(data_type)
