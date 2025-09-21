"""
Python conversion of Supercell.Laser.Logic.Message.Account.Auth.AuthenticationMessage.cs
Authentication message for user login
"""

from ...game_message import GameMessage

class AuthenticationMessage(GameMessage):
    """Authentication message for user login"""

    def __init__(self):
        """Initialize authentication message"""
        super().__init__()
        self.account_id = 0
        self.pass_token = ""
        self.client_major_version = 0
        self.client_minor_version = 0
        self.client_build_version = 0
        self.resource_sha = ""
        self.device_udid = ""
        self.mac_address = ""
        self.device_model = ""
        self.locale_key = ""
        self.language = ""
        self.advertising_gaid = ""
        self.os_version = ""
        self.is_android = False
        self.android_id = ""
        self.facebook_app_id = ""
        self.facebook_id = ""
        self.force_save_to_server = False
        self.client_seed = 0
        self.public_key_version = 1

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 10101

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 1

    def get_account_id(self) -> int:
        """Get account ID"""
        return self.account_id

    def set_account_id(self, account_id: int) -> None:
        """Set account ID"""
        self.account_id = account_id

    def get_pass_token(self) -> str:
        """Get password token"""
        return self.pass_token

    def set_pass_token(self, token: str) -> None:
        """Set password token"""
        self.pass_token = token

    def get_client_version(self) -> str:
        """Get full client version string"""
        return f"{self.client_major_version}.{self.client_minor_version}.{self.client_build_version}"

    def is_facebook_login(self) -> bool:
        """Check if using Facebook login"""
        return self.facebook_id != ""

    def is_guest_login(self) -> bool:
        """Check if guest login"""
        return self.account_id == 0 and self.pass_token == ""

    def has_device_info(self) -> bool:
        """Check if has device information"""
        return self.device_model != "" and self.os_version != ""

    def encode(self) -> None:
        """Encode message to stream"""
        # Simplified encoding - the real version has many more fields
        self.stream.write_v_long(self.account_id)
        self.stream.write_string(self.pass_token)
        self.stream.write_v_int(self.client_major_version)
        self.stream.write_v_int(self.client_minor_version) 
        self.stream.write_v_int(self.client_build_version)
        self.stream.write_string(self.resource_sha)
        self.stream.write_string(self.device_udid)
        self.stream.write_string(self.mac_address)
        self.stream.write_string(self.device_model)
        self.stream.write_string(self.locale_key)
        self.stream.write_string(self.language)
        self.stream.write_string(self.advertising_gaid)
        self.stream.write_string(self.os_version)
        self.stream.write_boolean(self.is_android)
        self.stream.write_string(self.android_id)
        self.stream.write_string(self.facebook_app_id)
        self.stream.write_string(self.facebook_id)
        self.stream.write_boolean(self.force_save_to_server)
        self.stream.write_v_int(self.client_seed)
        self.stream.write_v_int(self.public_key_version)

    def decode(self) -> None:
        """Decode message from stream"""
        # Simplified decoding - the real version has many more fields
        self.account_id = self.stream.read_v_long()
        self.pass_token = self.stream.read_string()
        self.client_major_version = self.stream.read_v_int()
        self.client_minor_version = self.stream.read_v_int()
        self.client_build_version = self.stream.read_v_int()
        self.resource_sha = self.stream.read_string()
        self.device_udid = self.stream.read_string()
        self.mac_address = self.stream.read_string()
        self.device_model = self.stream.read_string()
        self.locale_key = self.stream.read_string()
        self.language = self.stream.read_string()
        self.advertising_gaid = self.stream.read_string()
        self.os_version = self.stream.read_string()
        self.is_android = self.stream.read_boolean()
        self.android_id = self.stream.read_string()
        self.facebook_app_id = self.stream.read_string()
        self.facebook_id = self.stream.read_string()
        self.force_save_to_server = self.stream.read_boolean()
        self.client_seed = self.stream.read_v_int()
        self.public_key_version = self.stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        login_type = "facebook" if self.is_facebook_login() else ("guest" if self.is_guest_login() else "account")
        return (f"AuthenticationMessage(id={self.account_id}, type={login_type}, "
                f"version={self.get_client_version()})")
