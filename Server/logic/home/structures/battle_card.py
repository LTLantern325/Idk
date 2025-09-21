"""
Python conversion of Supercell.Laser.Logic.Home.Structures.BattleCard.cs
Battle card for player cosmetics in battles
"""

from ..helper.byte_stream_helper import ByteStreamHelper

class BattleCard:
    """Battle card containing player cosmetics for battles"""

    def __init__(self):
        """Initialize battle card"""
        self.thumbnail1 = 0  # First thumbnail/profile icon
        self.thumbnail2 = 0  # Second thumbnail/profile icon  
        self.emote = 0       # Selected emote
        self.title = 0       # Player title

    def get_thumbnail1(self) -> int:
        """Get first thumbnail ID"""
        return self.thumbnail1

    def set_thumbnail1(self, thumbnail_id: int) -> None:
        """Set first thumbnail ID"""
        self.thumbnail1 = thumbnail_id

    def get_thumbnail2(self) -> int:
        """Get second thumbnail ID"""
        return self.thumbnail2

    def set_thumbnail2(self, thumbnail_id: int) -> None:
        """Set second thumbnail ID"""
        self.thumbnail2 = thumbnail_id

    def get_emote(self) -> int:
        """Get emote ID"""
        return self.emote

    def set_emote(self, emote_id: int) -> None:
        """Set emote ID"""
        self.emote = emote_id

    def get_title(self) -> int:
        """Get title ID"""
        return self.title

    def set_title(self, title_id: int) -> None:
        """Set title ID"""
        self.title = title_id

    def has_thumbnail1(self) -> bool:
        """Check if has first thumbnail"""
        return self.thumbnail1 != 0

    def has_thumbnail2(self) -> bool:
        """Check if has second thumbnail"""
        return self.thumbnail2 != 0

    def has_emote(self) -> bool:
        """Check if has emote"""
        return self.emote != 0

    def has_title(self) -> bool:
        """Check if has title"""
        return self.title != 0

    def is_default_card(self) -> bool:
        """Check if using default battle card"""
        return (self.thumbnail1 == 0 and self.thumbnail2 == 0 and 
                self.emote == 0 and self.title == 0)

    def reset_to_default(self) -> None:
        """Reset battle card to default state"""
        self.thumbnail1 = 0
        self.thumbnail2 = 0
        self.emote = 0
        self.title = 0

    def copy_from(self, other: 'BattleCard') -> None:
        """Copy settings from another battle card"""
        self.thumbnail1 = other.thumbnail1
        self.thumbnail2 = other.thumbnail2
        self.emote = other.emote
        self.title = other.title

    def set_cosmetics(self, thumbnail1: int = 0, thumbnail2: int = 0, 
                     emote: int = 0, title: int = 0) -> None:
        """Set all cosmetics at once"""
        self.thumbnail1 = thumbnail1
        self.thumbnail2 = thumbnail2
        self.emote = emote
        self.title = title

    def encode(self, stream) -> None:
        """Encode battle card to stream"""
        # Write null reference first
        ByteStreamHelper.write_data_reference(stream, None)

        # Write cosmetic data references
        ByteStreamHelper.write_data_reference(stream, self.thumbnail1)
        ByteStreamHelper.write_data_reference(stream, self.thumbnail2)
        ByteStreamHelper.write_data_reference(stream, self.emote)
        ByteStreamHelper.write_data_reference(stream, self.title)

        # Write boolean flags indicating if each cosmetic is default (0)
        stream.write_boolean(self.thumbnail1 == 0)
        stream.write_boolean(self.thumbnail2 == 0)
        stream.write_boolean(self.emote == 0)
        stream.write_boolean(self.title == 0)

    def decode(self, stream) -> None:
        """Decode battle card from stream"""
        # Read null reference
        ByteStreamHelper.read_data_reference(stream)

        # Read cosmetic data references
        self.thumbnail1 = ByteStreamHelper.read_data_reference(stream)
        self.thumbnail2 = ByteStreamHelper.read_data_reference(stream)
        self.emote = ByteStreamHelper.read_data_reference(stream)
        self.title = ByteStreamHelper.read_data_reference(stream)

        # Read boolean flags
        stream.read_boolean()  # thumbnail1 is default
        stream.read_boolean()  # thumbnail2 is default
        stream.read_boolean()  # emote is default
        stream.read_boolean()  # title is default

    def __str__(self) -> str:
        """String representation"""
        return (f"BattleCard(thumb1={self.thumbnail1}, thumb2={self.thumbnail2}, "
                f"emote={self.emote}, title={self.title})")
