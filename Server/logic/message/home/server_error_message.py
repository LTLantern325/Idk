"""
Python conversion of Supercell.Laser.Logic.Message.Home.ServerErrorMessage.cs
Server error message for reporting server errors
"""

from ..game_message import GameMessage

class ServerErrorMessage(GameMessage):
    """Server error message for reporting server errors"""

    def __init__(self):
        """Initialize server error message"""
        super().__init__()
        self.error_code = 0
        self.error_message = ""
        self.error_details = ""

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24715  # Server error

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_error_code(self) -> int:
        """Get error code"""
        return self.error_code

    def set_error_code(self, code: int) -> None:
        """Set error code"""
        self.error_code = code

    def get_error_message(self) -> str:
        """Get error message"""
        return self.error_message

    def set_error_message(self, message: str) -> None:
        """Set error message"""
        self.error_message = message

    def get_error_details(self) -> str:
        """Get error details"""
        return self.error_details

    def set_error_details(self, details: str) -> None:
        """Set error details"""
        self.error_details = details

    def has_details(self) -> bool:
        """Check if has error details"""
        return self.error_details != ""

    def get_error_name(self) -> str:
        """Get human-readable error name"""
        errors = {
            0: "Unknown Error",
            1: "Internal Server Error",
            2: "Database Error",
            3: "Network Error",
            4: "Authentication Error",
            5: "Permission Denied",
            6: "Resource Not Found",
            7: "Rate Limited",
            8: "Service Unavailable"
        }
        return errors.get(self.error_code, f"Error {self.error_code}")

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.error_code)
        self.stream.write_string(self.error_message)
        self.stream.write_string(self.error_details)

    def decode(self) -> None:
        """Decode message from stream"""
        self.error_code = self.stream.read_v_int()
        self.error_message = self.stream.read_string()
        self.error_details = self.stream.read_string()

    def __str__(self) -> str:
        """String representation"""
        return f"ServerErrorMessage({self.get_error_name()}: '{self.error_message}')"
