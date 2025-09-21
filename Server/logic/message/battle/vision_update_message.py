"""
Python conversion of Supercell.Laser.Logic.Message.Battle.VisionUpdateMessage.cs
Vision update message for battle vision updates
"""

from typing import List
from ..game_message import GameMessage

class VisionUpdateMessage(GameMessage):
    """Vision update message for battle vision updates"""

    def __init__(self):
        """Initialize vision update message"""
        super().__init__()
        self.tick = 0
        self.vision_updates = []  # List of vision update data
        self.fog_of_war_enabled = False

    def get_message_type(self) -> int:
        """Get message type ID"""
        return 24109  # Placeholder message type

    def get_service_node_type(self) -> int:
        """Get service node type"""
        return 27

    def get_tick(self) -> int:
        """Get tick number"""
        return self.tick

    def set_tick(self, tick: int) -> None:
        """Set tick number"""
        self.tick = tick

    def add_vision_update(self, x: int, y: int, radius: int, visible: bool) -> None:
        """Add vision update"""
        update = {
            'x': x,
            'y': y,
            'radius': radius,
            'visible': visible
        }
        self.vision_updates.append(update)

    def get_vision_updates(self) -> List[dict]:
        """Get vision updates"""
        return self.vision_updates.copy()

    def clear_vision_updates(self) -> None:
        """Clear all vision updates"""
        self.vision_updates.clear()

    def get_update_count(self) -> int:
        """Get number of vision updates"""
        return len(self.vision_updates)

    def is_fog_of_war_enabled(self) -> bool:
        """Check if fog of war is enabled"""
        return self.fog_of_war_enabled

    def set_fog_of_war_enabled(self, enabled: bool) -> None:
        """Set fog of war enabled status"""
        self.fog_of_war_enabled = enabled

    def encode(self) -> None:
        """Encode message to stream"""
        self.stream.write_v_int(self.tick)
        self.stream.write_boolean(self.fog_of_war_enabled)

        # Write vision updates count
        self.stream.write_v_int(len(self.vision_updates))

        # Write vision updates
        for update in self.vision_updates:
            self.stream.write_v_int(update['x'])
            self.stream.write_v_int(update['y'])
            self.stream.write_v_int(update['radius'])
            self.stream.write_boolean(update['visible'])

    def decode(self) -> None:
        """Decode message from stream"""
        self.tick = self.stream.read_v_int()
        self.fog_of_war_enabled = self.stream.read_boolean()

        # Read vision updates count
        count = self.stream.read_v_int()

        # Read vision updates
        self.vision_updates.clear()
        for i in range(count):
            x = self.stream.read_v_int()
            y = self.stream.read_v_int()
            radius = self.stream.read_v_int()
            visible = self.stream.read_boolean()

            self.add_vision_update(x, y, radius, visible)

    def __str__(self) -> str:
        """String representation"""
        fog_status = "enabled" if self.fog_of_war_enabled else "disabled"
        return (f"VisionUpdateMessage(tick={self.tick}, "
                f"updates={len(self.vision_updates)}, fog={fog_status})")
