"""
Python conversion of Supercell.Laser.Logic.Message.Club.MyAllianceMessage.cs
My alliance message for sending current alliance data
"""

from typing import TYPE_CHECKING
from ..game_message import GameMessage

if TYPE_CHECKING:
    from ...club.alliance import Alliance

class MyAllianceMessage(GameMessage):
    """My alliance message for sending current alliance data"""

    def __init__(self):
        """Initialize my alliance message"""
        super().__init__()
        self.alliance = None  # Alliance object
        self.is_in_alliance = False

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24399  # My alliance response

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 11

    def get_alliance(self) -> 'Alliance':
        """Get alliance data"""
        return self.alliance

    def set_alliance(self, alliance: 'Alliance') -> None:
        """Set alliance data"""
        self.alliance = alliance
        self.is_in_alliance = alliance is not None

    def is_player_in_alliance(self) -> bool:
        """Check if player is in alliance"""
        return self.is_in_alliance

    def has_alliance_data(self) -> bool:
        """Check if has alliance data"""
        return self.alliance is not None

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_boolean(self.is_in_alliance)

        if self.alliance and self.is_in_alliance:
            self.alliance.encode(self.stream)
        else:
            # Write empty alliance data
            self.stream.write_v_int(0)

    def decode(self) -> None:
        """Decode message from stream"""
        self.is_in_alliance = self.stream.read_boolean()

        if self.is_in_alliance:
            # In real implementation, would decode Alliance
            # For now, just mark as having data
            alliance_data = self.stream.read_v_int()
            if alliance_data > 0:
                # Skip alliance data (simplified)
                pass

    def __str__(self) -> str:
        """String representation"""
        if self.is_in_alliance:
            return "MyAllianceMessage(in alliance)"
        else:
            return "MyAllianceMessage(no alliance)"
