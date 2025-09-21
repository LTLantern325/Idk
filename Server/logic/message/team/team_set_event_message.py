"""
Python conversion of Supercell.Laser.Logic.Message.Team.TeamSetEventMessage.cs
Team set event message for setting team event
"""

from ..game_message import GameMessage

class TeamSetEventMessage(GameMessage):
    """Team set event message for setting team event"""

    def __init__(self):
        """Initialize team set event message"""
        super().__init__()
        self.event_id = 0
        self.event_data = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14361

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_event_id(self) -> int:
        """Get event ID"""
        return self.event_id

    def set_event_id(self, event_id: int) -> None:
        """Set event ID"""
        self.event_id = event_id

    def get_event_data(self) -> int:
        """Get event data"""
        return self.event_data

    def set_event_data(self, data: int) -> None:
        """Set event data"""
        self.event_data = data

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.event_id)
        self.stream.write_v_int(self.event_data)

    def decode(self) -> None:
        """Decode message from stream"""
        self.event_id = self.stream.read_v_int()
        self.event_data = self.stream.read_v_int()

    def is_valid_event(self) -> bool:
        """Check if event is valid"""
        return self.event_id > 0

    def __str__(self) -> str:
        """String representation"""
        return f"TeamSetEventMessage(event_id={self.event_id}, data={self.event_data})"
