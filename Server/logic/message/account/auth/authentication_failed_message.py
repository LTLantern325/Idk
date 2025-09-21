"""
Python conversion of Supercell.Laser.Logic.Message.Account.Auth.AuthenticationFailedMessage.cs
Authentication failed message for login failures
"""

from ...game_message import GameMessage

class AuthenticationFailedMessage(GameMessage):
    """Authentication failed message for login failures"""

    def __init__(self):
        """Initialize authentication failed message"""
        super().__init__()
        self.error_code = 0
        self.error_message = ""
        self.redirect_url = ""

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 20103  # Authentication failed response

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 1

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

    def get_redirect_url(self) -> str:
        """Get redirect URL"""
        return self.redirect_url

    def set_redirect_url(self, url: str) -> None:
        """Set redirect URL"""
        self.redirect_url = url

    def has_redirect(self) -> bool:
        """Check if has redirect URL"""
        return self.redirect_url != ""

    def get_error_name(self) -> str:
        """Get human-readable error name"""
        errors = {
            0: "Unknown Error",
            1: "Invalid Credentials",
            2: "Account Banned",
            3: "Server Maintenance",
            4: "Version Mismatch",
            5: "Account Locked",
            6: "Facebook Login Failed",
            7: "Game Center Login Failed",
            8: "Too Many Attempts"
        }
        return errors.get(self.error_code, f"Error {self.error_code}")

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.error_code)
        self.stream.write_string(self.error_message)
        self.stream.write_string(self.redirect_url)

    def decode(self) -> None:
        """Decode message from stream"""
        self.error_code = self.stream.read_v_int()
        self.error_message = self.stream.read_string()
        self.redirect_url = self.stream.read_string()

    def __str__(self) -> str:
        """String representation"""
        redirect_info = " (with redirect)" if self.has_redirect() else ""
        return f"AuthenticationFailedMessage({self.get_error_name()}{redirect_info})"
