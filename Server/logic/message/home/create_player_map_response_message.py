"""
Python conversion of Supercell.Laser.Logic.Message.Home.CreatePlayerMapResponseMessage.cs
Create player map response message for map creation responses
"""

from ..game_message import GameMessage

class CreatePlayerMapResponseMessage(GameMessage):
    """Create player map response message for map creation responses"""

    def __init__(self):
        """Initialize create player map response message"""
        super().__init__()
        self.success = False
        self.error_code = 0
        self.map_id = 0
        self.error_message = ""

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24460  # Create map response

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def is_success(self) -> bool:
        """Check if map creation was successful"""
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

    def get_map_id(self) -> int:
        """Get created map ID"""
        return self.map_id

    def set_map_id(self, map_id: int) -> None:
        """Set created map ID"""
        self.map_id = map_id

    def get_error_message(self) -> str:
        """Get error message"""
        return self.error_message

    def set_error_message(self, message: str) -> None:
        """Set error message"""
        self.error_message = message

    def get_error_name(self) -> str:
        """Get human-readable error name"""
        errors = {
            0: "No Error",
            1: "Invalid Map Name",
            2: "Invalid Map Data", 
            3: "Map Too Large",
            4: "Map Too Small",
            5: "Inappropriate Content",
            6: "Map Limit Reached"
        }
        return errors.get(self.error_code, f"Error {self.error_code}")

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_boolean(self.success)
        self.stream.write_v_int(self.error_code)
        self.stream.write_v_int(self.map_id)
        self.stream.write_string(self.error_message)

    def decode(self) -> None:
        """Decode message from stream"""
        self.success = self.stream.read_boolean()
        self.error_code = self.stream.read_v_int()
        self.map_id = self.stream.read_v_int()
        self.error_message = self.stream.read_string()

    def __str__(self) -> str:
        """String representation"""
        if self.success:
            return f"CreatePlayerMapResponseMessage(success, map_id={self.map_id})"
        else:
            return f"CreatePlayerMapResponseMessage(failed, {self.get_error_name()})"
