"""
Python conversion of Supercell.Laser.Logic.Message.Club.AllianceDataMessage.cs
Alliance data message for sending alliance information
"""

from typing import TYPE_CHECKING
from ..game_message import GameMessage

if TYPE_CHECKING:
    from ...club.alliance import Alliance

class AllianceDataMessage(GameMessage):
    """Alliance data message for sending alliance information"""

    def __init__(self):
        """Initialize alliance data message"""
        super().__init__()
        self.alliance = None  # Alliance object
        self.is_my_alliance = False

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24301

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 11

    def get_alliance(self) -> 'Alliance':
        """Get alliance data"""
        return self.alliance

    def set_alliance(self, alliance: 'Alliance') -> None:
        """Set alliance data"""
        self.alliance = alliance

    def is_my_alliance(self) -> bool:
        """Check if this is player's alliance"""
        return self.is_my_alliance

    def set_my_alliance(self, is_mine: bool) -> None:
        """Set if this is player's alliance"""
        self.is_my_alliance = is_mine

    def has_alliance_data(self) -> bool:
        """Check if has alliance data"""
        return self.alliance is not None

    def encode(self) -> None:
        """Encode message to stream"""
        # Original C# code: Stream.WriteBoolean(false);
        self.stream.write_boolean(False)

        if self.alliance:
            # Alliance.Encode(Stream);
            self.alliance.encode(self.stream)
        else:
            # Write empty alliance data
            self.stream.write_v_int(0)

    def decode(self) -> None:
        """Decode message from stream"""
        # Read boolean flag
        has_data = self.stream.read_boolean()

        if has_data:
            # In real implementation, would decode Alliance
            # For now, just mark as having data
            pass

    def __str__(self) -> str:
        """String representation"""
        alliance_status = "with alliance" if self.has_alliance_data() else "no alliance"
        my_status = " (mine)" if self.is_my_alliance else ""
        return f"AllianceDataMessage({alliance_status}{my_status})"
