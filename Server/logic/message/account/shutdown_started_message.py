"""
Python conversion of Supercell.Laser.Logic.Message.Account.ShutdownStartedMessage.cs
Shutdown started message for server shutdown notification
"""

from ..game_message import GameMessage

class ShutdownStartedMessage(GameMessage):
    """Shutdown started message for server shutdown notification"""

    def __init__(self):
        """Initialize shutdown started message"""
        super().__init__()
        self.seconds_until_shutdown = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 20161  # Placeholder message type

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 1

    def get_seconds_until_shutdown(self) -> int:
        """Get seconds until server shutdown"""
        return self.seconds_until_shutdown

    def set_seconds_until_shutdown(self, seconds: int) -> None:
        """Set seconds until server shutdown"""
        self.seconds_until_shutdown = max(0, seconds)

    def get_minutes_until_shutdown(self) -> float:
        """Get minutes until shutdown"""
        return self.seconds_until_shutdown / 60.0

    def is_immediate_shutdown(self) -> bool:
        """Check if shutdown is immediate"""
        return self.seconds_until_shutdown == 0

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.seconds_until_shutdown)

    def decode(self) -> None:
        """Decode message from stream"""
        self.seconds_until_shutdown = self.stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        if self.is_immediate_shutdown():
            return "ShutdownStartedMessage(immediate)"
        else:
            return f"ShutdownStartedMessage({self.seconds_until_shutdown}s)"
