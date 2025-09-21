"""
Python conversion of Supercell.Laser.Logic.Message.Home.OutOfSyncMessage.cs
Out of sync message for handling client-server desynchronization
"""

from ..game_message import GameMessage

class OutOfSyncMessage(GameMessage):
    """Out of sync message for handling client-server desynchronization"""

    def __init__(self):
        """Initialize out of sync message"""
        super().__init__()
        self.client_tick = 0
        self.server_tick = 0
        self.client_checksum = 0
        self.server_checksum = 0
        self.reconnect_required = False

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24104  # Out of sync

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 9

    def get_client_tick(self) -> int:
        """Get client tick"""
        return self.client_tick

    def set_client_tick(self, tick: int) -> None:
        """Set client tick"""
        self.client_tick = tick

    def get_server_tick(self) -> int:
        """Get server tick"""
        return self.server_tick

    def set_server_tick(self, tick: int) -> None:
        """Set server tick"""
        self.server_tick = tick

    def get_tick_difference(self) -> int:
        """Get tick difference between client and server"""
        return abs(self.client_tick - self.server_tick)

    def is_reconnect_required(self) -> bool:
        """Check if reconnect is required"""
        return self.reconnect_required

    def set_reconnect_required(self, required: bool) -> None:
        """Set reconnect required flag"""
        self.reconnect_required = required

    def is_checksum_mismatch(self) -> bool:
        """Check if checksums mismatch"""
        return self.client_checksum != self.server_checksum

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.client_tick)
        self.stream.write_v_int(self.server_tick)
        self.stream.write_v_int(self.client_checksum)
        self.stream.write_v_int(self.server_checksum)
        self.stream.write_boolean(self.reconnect_required)

    def decode(self) -> None:
        """Decode message from stream"""
        self.client_tick = self.stream.read_v_int()
        self.server_tick = self.stream.read_v_int()
        self.client_checksum = self.stream.read_v_int()
        self.server_checksum = self.stream.read_v_int()
        self.reconnect_required = self.stream.read_boolean()

    def __str__(self) -> str:
        """String representation"""
        reconnect_info = " (reconnect required)" if self.reconnect_required else ""
        return (f"OutOfSyncMessage(client_tick={self.client_tick}, "
                f"server_tick={self.server_tick}{reconnect_info})")
