"""
Python conversion of Supercell.Laser.Logic.Command.Home.LogicGiveDeliveryItemsCommand.cs
Command for giving delivery items to player
"""

from ..command import Command
from typing import List, Dict

class LogicGiveDeliveryItemsCommand(Command):
    """Command for giving delivery items to player"""

    def __init__(self):
        """Initialize give delivery items command"""
        super().__init__()
        self.delivery_items = []  # List of delivery item data
        self.source = "admin"  # Source of delivery
        self.message = ""  # Optional message

    def add_delivery_item(self, item_type: int, item_id: int, amount: int) -> None:
        """Add delivery item"""
        self.delivery_items.append({
            'type': item_type,  # 0=coins, 1=gems, 2=tokens, 3=character, 4=skin, etc.
            'id': item_id,
            'amount': amount
        })

    def get_delivery_items(self) -> List[Dict]:
        """Get delivery items list"""
        return self.delivery_items.copy()

    def set_source(self, source: str) -> None:
        """Set delivery source"""
        self.source = source

    def set_message(self, message: str) -> None:
        """Set delivery message"""
        self.message = message

    def execute(self, avatar: any) -> int:
        """Execute give delivery items command"""
        if not self.delivery_items:
            return -1  # No items to deliver

        # Apply each delivery item
        for item in self.delivery_items:
            item_type = item['type']
            item_id = item['id']
            amount = item['amount']

            if item_type == 0:  # Coins
                avatar.gold += amount
            elif item_type == 1:  # Gems
                avatar.diamonds += amount
            elif item_type == 2:  # Tokens
                if not hasattr(avatar, 'tokens'):
                    avatar.tokens = 0
                avatar.tokens += amount
            elif item_type == 3:  # Character
                if not hasattr(avatar, 'unlocked_characters'):
                    avatar.unlocked_characters = []
                if item_id not in avatar.unlocked_characters:
                    avatar.unlocked_characters.append(item_id)
            elif item_type == 4:  # Skin
                if not hasattr(avatar, 'unlocked_skins'):
                    avatar.unlocked_skins = []
                if item_id not in avatar.unlocked_skins:
                    avatar.unlocked_skins.append(item_id)
            elif item_type == 5:  # Power points
                if not hasattr(avatar, 'power_points'):
                    avatar.power_points = {}
                character_id = item_id
                if character_id not in avatar.power_points:
                    avatar.power_points[character_id] = 0
                avatar.power_points[character_id] += amount

        # Add to delivery history
        if not hasattr(avatar, 'delivery_history'):
            avatar.delivery_history = []

        avatar.delivery_history.append({
            'items': self.delivery_items.copy(),
            'source': self.source,
            'message': self.message,
            'timestamp': self.timestamp
        })

        return 0

    def encode(self, stream) -> None:
        """Encode command to stream"""
        super().encode(stream)
        stream.write_string(self.source)
        stream.write_string(self.message)

        # Write delivery items
        stream.write_v_int(len(self.delivery_items))
        for item in self.delivery_items:
            stream.write_v_int(item['type'])
            stream.write_v_int(item['id'])
            stream.write_v_int(item['amount'])

    def decode(self, stream) -> None:
        """Decode command from stream"""
        super().decode(stream)
        self.source = stream.read_string()
        self.message = stream.read_string()

        # Read delivery items
        item_count = stream.read_v_int()
        self.delivery_items.clear()
        for i in range(item_count):
            item_type = stream.read_v_int()
            item_id = stream.read_v_int()
            amount = stream.read_v_int()
            self.delivery_items.append({
                'type': item_type,
                'id': item_id,
                'amount': amount
            })

    def __str__(self) -> str:
        """String representation"""
        return f"GiveDeliveryItemsCommand({len(self.delivery_items)} items from {self.source})"
