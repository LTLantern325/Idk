"""
Python conversion of Supercell.Laser.Logic.Message.Club.JoinableAllianceListMessage.cs
Joinable alliance list message for sending list of joinable alliances
"""

from typing import List, Dict, Any
from ..game_message import GameMessage

class JoinableAllianceListMessage(GameMessage):
    """Joinable alliance list message for sending list of joinable alliances"""

    def __init__(self):
        """Initialize joinable alliance list message"""
        super().__init__()
        self.alliances = []  # List of alliance data

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24303

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 11

    def add_alliance(self, alliance_id: int, name: str, member_count: int, required_trophies: int) -> None:
        """Add alliance to the list"""
        alliance_data = {
            'id': alliance_id,
            'name': name,
            'member_count': member_count,
            'required_trophies': required_trophies,
            'badge_id': 0,
            'join_type': 0
        }
        self.alliances.append(alliance_data)

    def get_alliance_count(self) -> int:
        """Get number of alliances"""
        return len(self.alliances)

    def clear_alliances(self) -> None:
        """Clear all alliances"""
        self.alliances.clear()

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(len(self.alliances))

        for alliance in self.alliances:
            self.stream.write_v_long(alliance['id'])
            self.stream.write_string(alliance['name'])
            self.stream.write_v_int(alliance['member_count'])
            self.stream.write_v_int(alliance['required_trophies'])
            self.stream.write_v_int(alliance.get('badge_id', 0))
            self.stream.write_v_int(alliance.get('join_type', 0))

    def decode(self) -> None:
        """Decode message from stream"""
        count = self.stream.read_v_int()

        self.alliances.clear()
        for i in range(count):
            alliance_id = self.stream.read_v_long()
            name = self.stream.read_string()
            member_count = self.stream.read_v_int()
            required_trophies = self.stream.read_v_int()
            badge_id = self.stream.read_v_int()
            join_type = self.stream.read_v_int()

            alliance_data = {
                'id': alliance_id,
                'name': name,
                'member_count': member_count,
                'required_trophies': required_trophies,
                'badge_id': badge_id,
                'join_type': join_type
            }
            self.alliances.append(alliance_data)

    def __str__(self) -> str:
        """String representation"""
        return f"JoinableAllianceListMessage({len(self.alliances)} alliances)"
