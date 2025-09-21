"""
Python conversion of Supercell.Laser.Logic.Team.TeamJoinRequest.cs
Team join request (placeholder implementation)
"""

class TeamJoinRequest:
    """Team join request class - basic placeholder"""

    def __init__(self):
        """Initialize team join request"""
        self.request_id = 0
        self.player_id = 0
        self.player_name = ""
        self.message = ""
        self.timestamp = 0

    def get_request_id(self) -> int:
        """Get request ID"""
        return self.request_id

    def set_request_id(self, request_id: int) -> None:
        """Set request ID"""
        self.request_id = request_id

    def get_player_id(self) -> int:
        """Get player ID"""
        return self.player_id

    def set_player_id(self, player_id: int) -> None:
        """Set player ID"""
        self.player_id = player_id

    def get_player_name(self) -> str:
        """Get player name"""
        return self.player_name

    def set_player_name(self, name: str) -> None:
        """Set player name"""
        self.player_name = name

    def get_message(self) -> str:
        """Get join request message"""
        return self.message

    def set_message(self, message: str) -> None:
        """Set join request message"""
        self.message = message

    def encode(self, stream) -> None:
        """Encode team join request to stream"""
        # Original C# implementation throws NotImplementedException
        # Providing basic implementation
        stream.write_v_long(self.request_id)
        stream.write_v_long(self.player_id)
        stream.write_string(self.player_name)
        stream.write_string(self.message)
        stream.write_v_int(self.timestamp)

    def decode(self, stream) -> None:
        """Decode team join request from stream"""
        self.request_id = stream.read_v_long()
        self.player_id = stream.read_v_long()
        self.player_name = stream.read_string()
        self.message = stream.read_string()
        self.timestamp = stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        return f"TeamJoinRequest(player='{self.player_name}', id={self.request_id})"
