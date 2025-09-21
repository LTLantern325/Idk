"""
Python conversion of Supercell.Laser.Logic.Message.Team.Stream.QuickChatStreamEntry.cs
Quick chat stream entry for team quick chat messages
"""

from typing import Optional

class QuickChatStreamEntry:
    """Quick chat stream entry for team quick chat messages"""

    def __init__(self):
        """Initialize quick chat stream entry"""
        self.player_id = 0
        self.player_name = ""
        self.quick_chat_id = 0
        self.timestamp = 0

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

    def get_quick_chat_id(self) -> int:
        """Get quick chat ID"""
        return self.quick_chat_id

    def set_quick_chat_id(self, chat_id: int) -> None:
        """Set quick chat ID"""
        self.quick_chat_id = chat_id

    def get_timestamp(self) -> int:
        """Get timestamp"""
        return self.timestamp

    def set_timestamp(self, timestamp: int) -> None:
        """Set timestamp"""
        self.timestamp = timestamp

    def encode(self, stream) -> None:
        """Encode entry to stream"""
        stream.write_v_long(self.player_id)
        stream.write_string(self.player_name)
        stream.write_v_int(self.quick_chat_id)
        stream.write_v_int(self.timestamp)

    def decode(self, stream) -> None:
        """Decode entry from stream"""
        self.player_id = stream.read_v_long()
        self.player_name = stream.read_string()
        self.quick_chat_id = stream.read_v_int()
        self.timestamp = stream.read_v_int()

    def is_valid_entry(self) -> bool:
        """Check if entry is valid"""
        return (self.player_id > 0 and 
                self.player_name != "" and 
                self.quick_chat_id > 0)

    def __str__(self) -> str:
        """String representation"""
        return f"QuickChatStreamEntry('{self.player_name}', chat_id={self.quick_chat_id})"
