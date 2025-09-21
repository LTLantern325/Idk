"""
Python conversion of Supercell.Laser.Logic.Message.Home.PlayerMapsMessage.cs
Player maps message for sending player's custom maps
"""

from typing import List, Dict, Any
from ..game_message import GameMessage

class PlayerMapsMessage(GameMessage):
    """Player maps message for sending player's custom maps"""

    def __init__(self):
        """Initialize player maps message"""
        super().__init__()
        self.player_id = 0
        self.maps = []  # List of map dictionaries

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24463

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def add_map(self, map_id: int, name: str, data: str, game_mode: int) -> None:
        """Add map to the list"""
        map_info = {
            'id': map_id,
            'name': name,
            'data': data,
            'game_mode': game_mode
        }
        self.maps.append(map_info)

    def get_map_count(self) -> int:
        """Get number of maps"""
        return len(self.maps)

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_long(self.player_id)
        self.stream.write_v_int(len(self.maps))

        for map_info in self.maps:
            self.stream.write_v_int(map_info['id'])
            self.stream.write_string(map_info['name'])
            self.stream.write_string(map_info['data'])
            self.stream.write_v_int(map_info['game_mode'])

    def decode(self) -> None:
        """Decode message from stream"""
        self.player_id = self.stream.read_v_long()
        count = self.stream.read_v_int()

        self.maps.clear()
        for i in range(count):
            map_id = self.stream.read_v_int()
            name = self.stream.read_string()
            data = self.stream.read_string()
            game_mode = self.stream.read_v_int()
            self.add_map(map_id, name, data, game_mode)

    def __str__(self) -> str:
        """String representation"""
        return f"PlayerMapsMessage(player_id={self.player_id}, maps={len(self.maps)})"
