"""
Python conversion of Supercell.Laser.Logic.Command.Home.LogicPurchaseOfferCommand.cs
Command for purchasing offers
"""

from ..command import Command

class LogicPurchaseOfferCommand(Command):
    """Command for purchasing offers"""

    def __init__(self):
        """Initialize purchase offer command"""
        super().__init__()
        self.offer_global_id = 0
        self.offer_index = 0
        self.cost_gems = 0
        self.cost_gold = 0

    def get_offer_global_id(self) -> int:
        """Get offer global ID"""
        return self.offer_global_id

    def set_offer_global_id(self, global_id: int) -> None:
        """Set offer global ID"""
        self.offer_global_id = global_id

    def execute(self, avatar: any) -> int:
        """Execute purchase offer command"""
        # Check if player has enough currency
        if self.cost_gems > 0 and avatar.diamonds < self.cost_gems:
            return -1
        if self.cost_gold > 0 and avatar.gold < self.cost_gold:
            return -1

        # Deduct cost
        avatar.diamonds -= self.cost_gems
        avatar.gold -= self.cost_gold

        return 0

    def encode(self, stream) -> None:
        """Encode command to stream"""
        super().encode(stream)
        stream.write_v_int(self.offer_global_id)
        stream.write_v_int(self.offer_index)

    def decode(self, stream) -> None:
        """Decode command from stream"""
        super().decode(stream)
        self.offer_global_id = stream.read_v_int()
        self.offer_index = stream.read_v_int()
