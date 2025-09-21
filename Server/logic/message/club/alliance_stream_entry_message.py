"""
Python conversion of Supercell.Laser.Logic.Message.Club.AllianceStreamEntryMessage.cs
Alliance stream entry message for alliance stream entries
"""

from typing import TYPE_CHECKING
from ..game_message import GameMessage

if TYPE_CHECKING:
    from ...club.alliance_stream_entry import AllianceStreamEntry

class AllianceStreamEntryMessage(GameMessage):
    """Alliance stream entry message for alliance stream entries"""

    def __init__(self):
        """Initialize alliance stream entry message"""
        super().__init__()
        self.stream_entry = None  # AllianceStreamEntry object

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24311  # Alliance stream entry

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 11

    def get_stream_entry(self) -> 'AllianceStreamEntry':
        """Get stream entry"""
        return self.stream_entry

    def set_stream_entry(self, entry: 'AllianceStreamEntry') -> None:
        """Set stream entry"""
        self.stream_entry = entry

    def has_stream_entry(self) -> bool:
        """Check if has stream entry"""
        return self.stream_entry is not None

    def encode(self) -> None:
        """Encode message to stream"""
        if self.stream_entry:
            self.stream_entry.encode(self.stream)
        else:
            # Write empty stream entry data
            self.stream.write_v_int(0)

    def decode(self) -> None:
        """Decode message from stream"""
        # In real implementation, would decode AllianceStreamEntry
        # For now, just mark as having data
        entry_data = self.stream.read_v_int()
        if entry_data > 0:
            # Skip stream entry data (simplified)
            pass

    def __str__(self) -> str:
        """String representation"""
        entry_status = "with entry" if self.has_stream_entry() else "no entry"
        return f"AllianceStreamEntryMessage({entry_status})"
