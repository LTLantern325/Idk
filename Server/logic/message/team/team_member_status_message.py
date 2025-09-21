"""
Python conversion of Supercell.Laser.Logic.Message.Team.TeamMemberStatusMessage.cs
Team member status message for team member status updates
"""

from ..game_message import GameMessage

class TeamMemberStatusMessage(GameMessage):
    """Team member status message for team member status updates"""

    def __init__(self):
        """Initialize team member status message"""
        super().__init__()
        self.player_id = 0
        self.status = 0  # 0=not_ready, 1=ready, 2=in_battle
        self.character_id = 0

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24359  # Team member status

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_player_id(self) -> int:
        """Get player ID"""
        return self.player_id

    def set_player_id(self, player_id: int) -> None:
        """Set player ID"""
        self.player_id = player_id

    def get_status(self) -> int:
        """Get member status"""
        return self.status

    def set_status(self, status: int) -> None:
        """Set member status"""
        self.status = status

    def is_ready(self) -> bool:
        """Check if member is ready"""
        return self.status == 1

    def is_in_battle(self) -> bool:
        """Check if member is in battle"""
        return self.status == 2

    def get_status_name(self) -> str:
        """Get human-readable status name"""
        statuses = {0: "Not Ready", 1: "Ready", 2: "In Battle"}
        return statuses.get(self.status, "Unknown")

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_long(self.player_id)
        self.stream.write_v_int(self.status)
        self.stream.write_v_int(self.character_id)

    def decode(self) -> None:
        """Decode message from stream"""
        self.player_id = self.stream.read_v_long()
        self.status = self.stream.read_v_int()
        self.character_id = self.stream.read_v_int()

    def __str__(self) -> str:
        """String representation"""
        return f"TeamMemberStatusMessage(player_id={self.player_id}, {self.get_status_name()})"
