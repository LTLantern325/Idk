"""
Python conversion of Supercell.Laser.Logic.Message.Account.Auth.AuthenticationOkMessage.cs
Authentication OK message for successful login
"""

from ...game_message import GameMessage

class AuthenticationOkMessage(GameMessage):
    """Authentication OK message for successful login"""

    def __init__(self):
        """Initialize authentication OK message"""
        super().__init__()
        self.account_id = 0
        self.home_id = 0
        self.pass_token = ""
        self.facebook_id = ""
        self.gamecenter_id = ""
        self.server_major_version = 0
        self.server_minor_version = 0
        self.server_build_version = 0
        self.content_url = ""
        self.session_count = 0
        self.play_time_seconds = 0
        self.days_since_started_playing = 0
        self.facebook_app_id = ""
        self.server_environment = ""
        self.login_count = 0
        self.country_code = ""

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 20104  # Authentication OK response

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 1

    def get_account_id(self) -> int:
        """Get account ID"""
        return self.account_id

    def set_account_id(self, account_id: int) -> None:
        """Set account ID"""
        self.account_id = account_id

    def get_home_id(self) -> int:
        """Get home ID"""
        return self.home_id

    def set_home_id(self, home_id: int) -> None:
        """Set home ID"""
        self.home_id = home_id

    def get_server_version(self) -> str:
        """Get server version string"""
        return f"{self.server_major_version}.{self.server_minor_version}.{self.server_build_version}"

    def is_facebook_connected(self) -> bool:
        """Check if Facebook is connected"""
        return self.facebook_id != ""

    def is_gamecenter_connected(self) -> bool:
        """Check if Game Center is connected"""
        return self.gamecenter_id != ""

    def get_play_time_hours(self) -> float:
        """Get play time in hours"""
        return self.play_time_seconds / 3600.0

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_long(self.account_id)
        self.stream.write_v_long(self.home_id)
        self.stream.write_string(self.pass_token)
        self.stream.write_string(self.facebook_id)
        self.stream.write_string(self.gamecenter_id)
        self.stream.write_v_int(self.server_major_version)
        self.stream.write_v_int(self.server_minor_version)
        self.stream.write_v_int(self.server_build_version)
        self.stream.write_string(self.content_url)
        self.stream.write_v_int(self.session_count)
        self.stream.write_v_int(self.play_time_seconds)
        self.stream.write_v_int(self.days_since_started_playing)
        self.stream.write_string(self.facebook_app_id)
        self.stream.write_string(self.server_environment)
        self.stream.write_v_int(self.login_count)
        self.stream.write_string(self.country_code)

    def decode(self) -> None:
        """Decode message from stream"""
        self.account_id = self.stream.read_v_long()
        self.home_id = self.stream.read_v_long()
        self.pass_token = self.stream.read_string()
        self.facebook_id = self.stream.read_string()
        self.gamecenter_id = self.stream.read_string()
        self.server_major_version = self.stream.read_v_int()
        self.server_minor_version = self.stream.read_v_int()
        self.server_build_version = self.stream.read_v_int()
        self.content_url = self.stream.read_string()
        self.session_count = self.stream.read_v_int()
        self.play_time_seconds = self.stream.read_v_int()
        self.days_since_started_playing = self.stream.read_v_int()
        self.facebook_app_id = self.stream.read_string()
        self.server_environment = self.stream.read_string()
        self.login_count = self.stream.read_v_int()
        self.country_code = self.stream.read_string()

    def __str__(self) -> str:
        """String representation"""
        return (f"AuthenticationOkMessage(account_id={self.account_id}, "
                f"home_id={self.home_id}, version={self.get_server_version()})")
