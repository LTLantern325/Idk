"""
Python conversion of Supercell.Laser.Logic.Message.Team.Stream.TeamStreamMessage.cs
Team stream message for team stream data
"""

from typing import List, Any
from ...game_message import GameMessage

class TeamStreamMessage(GameMessage):
    """Team stream message for team stream data"""

    def __init__(self):
        """Initialize team stream message"""
        super().__init__()
        self.stream_entries = []  # List of stream entries
        self.team_id = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24368  # Team stream

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_team_id(self) -> int:
        """Get team ID"""
        return self.team_id

    def set_team_id(self, team_id: int) -> None:
        """Set team ID"""
        self.team_id = team_id

    def add_stream_entry(self, entry: Any) -> None:
        """Add stream entry"""
        self.stream_entries.append(entry)

    def get_stream_entries(self) -> List[Any]:
        """Get stream entries"""
        return self.stream_entries.copy()

    def get_entry_count(self) -> int:
        """Get number of entries"""
        return len(self.stream_entries)

    def clear_entries(self) -> None:
        """Clear all entries"""
        self.stream_entries.clear()

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_long(self.team_id)
        self.stream.write_v_int(len(self.stream_entries))

        for entry in self.stream_entries:
            if hasattr(entry, 'encode'):
                entry.encode(self.stream)
            else:
                # Write simplified entry data
                self.stream.write_v_int(0)  # Empty entry

    def decode(self) -> None:
        """Decode message from stream"""
        self.team_id = self.stream.read_v_long()
        entry_count = self.stream.read_v_int()

        self.stream_entries.clear()
        for i in range(entry_count):
            # Skip entry data for now (simplified)
            self.stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        return f"TeamStreamMessage(team_id={self.team_id}, entries={len(self.stream_entries)})"
