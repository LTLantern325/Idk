"""
Python conversion of Supercell.Laser.Logic.Message.Battle.StartSpectateMessage.cs
Start spectate message for spectating battles
"""

from ..game_message import GameMessage

class StartSpectateMessage(GameMessage):
    """Start spectate message for spectating battles"""

    def __init__(self):
        """Initialize start spectate message"""
        super().__init__()
        self.target_player_id = 0
        self.battle_id = 0
        self.spectate_type = 0  # 0=player, 1=random battle, 2=club battle

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 14104

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_target_player_id(self) -> int:
        """Get target player ID to spectate"""
        return self.target_player_id

    def set_target_player_id(self, player_id: int) -> None:
        """Set target player ID to spectate"""
        self.target_player_id = player_id

    def get_battle_id(self) -> int:
        """Get battle ID to spectate"""
        return self.battle_id

    def set_battle_id(self, battle_id: int) -> None:
        """Set battle ID to spectate"""
        self.battle_id = battle_id

    def get_spectate_type(self) -> int:
        """Get spectate type"""
        return self.spectate_type

    def set_spectate_type(self, spec_type: int) -> None:
        """Set spectate type"""
        self.spectate_type = spec_type

    def is_player_spectate(self) -> bool:
        """Check if spectating specific player"""
        return self.spectate_type == 0

    def is_random_battle_spectate(self) -> bool:
        """Check if spectating random battle"""
        return self.spectate_type == 1

    def is_club_battle_spectate(self) -> bool:
        """Check if spectating club battle"""
        return self.spectate_type == 2

    def get_spectate_type_name(self) -> str:
        """Get human-readable spectate type"""
        if self.spectate_type == 0:
            return "Player"
        elif self.spectate_type == 1:
            return "Random Battle"
        elif self.spectate_type == 2:
            return "Club Battle"
        else:
            return "Unknown"

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_long(self.target_player_id)
        self.stream.write_v_long(self.battle_id)
        self.stream.write_v_int(self.spectate_type)

    def decode(self) -> None:
        """Decode message from stream"""
        self.target_player_id = self.stream.read_v_long()
        self.battle_id = self.stream.read_v_long()
        self.spectate_type = self.stream.read_v_int()

    def is_valid(self) -> bool:
        """Check if message is valid"""
        if self.is_player_spectate():
            return self.target_player_id > 0
        else:
            return self.battle_id > 0

    def __str__(self) -> str:
        """String representation"""
        if self.is_player_spectate():
            return f"StartSpectateMessage(player_id={self.target_player_id})"
        else:
            return f"StartSpectateMessage(battle_id={self.battle_id}, type={self.get_spectate_type_name()})"
