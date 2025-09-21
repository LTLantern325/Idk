"""
Python conversion of Supercell.Laser.Logic.Message.Account.DisconnectedMessage.cs
Disconnected message for client disconnection
"""

from ..game_message import GameMessage

class DisconnectedMessage(GameMessage):
    """Disconnected message for client disconnection"""

    def __init__(self):
        """Initialize disconnected message"""
        super().__init__()
        self.reason_code = 0
        self.reason_message = ""

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 25892  # Placeholder message type

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 1

    def get_reason_code(self) -> int:
        """Get disconnection reason code"""
        return self.reason_code

    def set_reason_code(self, code: int) -> None:
        """Set disconnection reason code"""
        self.reason_code = code

    def get_reason_message(self) -> str:
        """Get disconnection reason message"""
        return self.reason_message

    def set_reason_message(self, message: str) -> None:
        """Set disconnection reason message"""
        self.reason_message = message

    def get_reason_name(self) -> str:
        """Get human-readable reason name"""
        reasons = {
            0: "Unknown",
            1: "Connection Lost",
            2: "Server Shutdown",
            3: "Kicked",
            4: "Maintenance",
            5: "Client Error"
        }
        return reasons.get(self.reason_code, f"Code {self.reason_code}")

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.reason_code)
        self.stream.write_string(self.reason_message)

    def decode(self) -> None:
        """Decode message from stream"""
        self.reason_code = self.stream.read_v_int()
        self.reason_message = self.stream.read_string()

    def __str__(self) -> str:
        """String representation"""
        return f"DisconnectedMessage({self.get_reason_name()})"
