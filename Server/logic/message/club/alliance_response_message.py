"""
Python conversion of Supercell.Laser.Logic.Message.Club.AllianceResponseMessage.cs
Alliance response message for alliance operation responses
"""

from ..game_message import GameMessage

class AllianceResponseMessage(GameMessage):
    """Alliance response message for alliance operation responses"""

    def __init__(self):
        """Initialize alliance response message"""
        super().__init__()
        self.response_type = 0
        self.error_code = 0
        self.success = False
        self.alliance_id = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24310  # Placeholder message type

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 11

    def get_response_type(self) -> int:
        """Get response type"""
        return self.response_type

    def set_response_type(self, response_type: int) -> None:
        """Set response type"""
        self.response_type = response_type

    def is_success(self) -> bool:
        """Check if operation was successful"""
        return self.success

    def set_success(self, success: bool) -> None:
        """Set success status"""
        self.success = success

    def get_error_code(self) -> int:
        """Get error code"""
        return self.error_code

    def set_error_code(self, code: int) -> None:
        """Set error code"""
        self.error_code = code

    def get_response_name(self) -> str:
        """Get human-readable response name"""
        responses = {
            0: "Join",
            1: "Leave", 
            2: "Create",
            3: "Invite",
            4: "Kick"
        }
        return responses.get(self.response_type, f"Type {self.response_type}")

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.response_type)
        self.stream.write_boolean(self.success)
        self.stream.write_v_int(self.error_code)
        self.stream.write_v_long(self.alliance_id)

    def decode(self) -> None:
        """Decode message from stream"""
        self.response_type = self.stream.read_v_int()
        self.success = self.stream.read_boolean()
        self.error_code = self.stream.read_v_int()
        self.alliance_id = self.stream.read_v_long()

    def __str__(self) -> str:
        """String representation"""
        status = "success" if self.success else "failed"
        return f"AllianceResponseMessage({self.get_response_name()}, {status})"
