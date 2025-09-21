"""
Python conversion of Supercell.Laser.Logic.Message.MessageFactory.cs
Message factory for creating messages by type ID
"""

from typing import Dict, Type, Optional
from .game_message import GameMessage

# Import specific message classes (would be actual imports in real implementation)
class MessageFactory:
    """Factory for creating game messages by type ID"""

    # Singleton instance
    instance: Optional['MessageFactory'] = None

    def __init__(self):
        """Initialize message factory"""
        # Message type definitions - maps message type ID to class
        # Note: In actual implementation, these would be real message classes
        self.definitions: Dict[int, str] = {
            # Account messages
            10100: "ClientHelloMessage",
            10101: "AuthenticationMessage", 
            10107: "ClientCapabilitiesMessage",
            10108: "KeepAliveMessage",
            10110: "AnalyticEventMessage",

            # Player messages
            10177: "ClientInfoMessage",
            10212: "ChangeAvatarNameMessage",

            # Friend messages
            10501: "AcceptFriendMessage",
            10502: "AddFriendMessage",
            10504: "AskForFriendListMessage",
            10506: "RemoveFriendMessage",

            # Input messages
            10555: "ClientInputMessage",

            # Map editor messages
            12100: "CreatePlayerMapMessage",
            12101: "DeletePlayerMapMessage",
            12102: "GetPlayerMapsMessage", 
            12103: "UpdatePlayerMapMessage",
            12108: "GoHomeFromMapEditorMessage",
            12110: "TeamSetPlayerMapMessage",

            # Home messages
            14456: "GoHomeMessage",
            14102: "EndClientTurnMessage",
            14104: "StartSpectateMessage",
            14106: "CancelMatchmakingMessage",
            14107: "StopSpectateMessage",
            14109: "GoHomeFromOfflinePractiseMessage",
            14118: "SinglePlayerMatchRequestMessage",
            14166: "ChronosEventSeenMessage",

            # Matchmaking
            18977: "MatchmakeRequestMessage",

            # Player profile
            15081: "GetPlayerProfileMessage",

            # Alliance messages
            14301: "CreateAllianceMessage",
            14302: "AskForAllianceDataMessage",
            14303: "AskForJoinableAllianceListMessage",
            14305: "JoinAllianceMessage",
            14307: "KickAllianceMemberMessage",
            14308: "LeaveAllianceMessage",
            14315: "ChatToAllianceStreamMessage",
            14316: "ChangeAllianceSettingsMessage",

            # Team messages
            12541: "TeamCreateMessage",
            14353: "TeamLeaveMessage",
            14354: "TeamChangeMemberSettingsMessage",
            14355: "TeamSetMemberReadyMessage",
            14357: "TeamToggleMemberSideMessage",
            14049: "TeamChatMessage",
            14361: "TeamMemberStatusMessage",
            14362: "TeamSetEventMessage",
            14363: "TeamSetLocationMessage",
            14365: "TeamInviteMessage",
            14366: "PlayerStatusMessage",
            14369: "TeamPremadeChatMessage",
            14373: "TeamBotSlotDisableMessage",
            14479: "TeamInvitationResponseMessage",
            14881: "TeamRequestJoinMessage",

            # Leaderboard
            14403: "GetLeaderboardMessage",

            # Avatar name check
            14600: "AvatarNameCheckRequestMessage"
        }

    @classmethod
    def get_instance(cls) -> 'MessageFactory':
        """Get singleton instance"""
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def create_message_by_type(self, message_type: int) -> Optional[GameMessage]:
        """Create message instance by type ID"""
        if message_type not in self.definitions:
            return None

        # In actual implementation, this would use real class imports
        # For now, return a mock message for demonstration
        message_class_name = self.definitions[message_type]

        # This is a simplified mock - in real implementation would create actual instances
        return MockGameMessage(message_type, message_class_name)

    def get_message_name(self, message_type: int) -> Optional[str]:
        """Get message class name by type ID"""
        return self.definitions.get(message_type)

    def get_all_message_types(self) -> list[int]:
        """Get all registered message type IDs"""
        return list(self.definitions.keys())

    def get_message_count(self) -> int:
        """Get number of registered message types"""
        return len(self.definitions)

    def is_message_type_registered(self, message_type: int) -> bool:
        """Check if message type is registered"""
        return message_type in self.definitions

    def get_messages_by_category(self) -> Dict[str, list[int]]:
        """Get messages grouped by category based on type ID ranges"""
        categories = {
            "Account": [],
            "Player": [], 
            "Friends": [],
            "Input": [],
            "MapEditor": [],
            "Home": [],
            "Matchmaking": [],
            "Profile": [],
            "Alliance": [],
            "Team": [],
            "Leaderboard": [],
            "Other": []
        }

        for msg_type in self.definitions.keys():
            if 10100 <= msg_type <= 10199:
                categories["Account"].append(msg_type)
            elif 10200 <= msg_type <= 10299:
                categories["Player"].append(msg_type)
            elif 10500 <= msg_type <= 10599:
                categories["Friends"].append(msg_type)
            elif 10550 <= msg_type <= 10599:
                categories["Input"].append(msg_type)
            elif 12100 <= msg_type <= 12199:
                categories["MapEditor"].append(msg_type)
            elif 14100 <= msg_type <= 14199:
                categories["Home"].append(msg_type)
            elif 18900 <= msg_type <= 18999:
                categories["Matchmaking"].append(msg_type)
            elif 15000 <= msg_type <= 15099:
                categories["Profile"].append(msg_type)
            elif 14300 <= msg_type <= 14399:
                if msg_type <= 14320:
                    categories["Alliance"].append(msg_type)
                else:
                    categories["Team"].append(msg_type)
            elif 14400 <= msg_type <= 14499:
                if msg_type <= 14410:
                    categories["Leaderboard"].append(msg_type)
                else:
                    categories["Team"].append(msg_type)
            else:
                categories["Other"].append(msg_type)

        # Remove empty categories
        return {k: v for k, v in categories.items() if v}

class MockGameMessage(GameMessage):
    """Mock game message for demonstration"""

    def __init__(self, message_type: int, class_name: str):
        super().__init__()
        self._message_type = message_type
        self._class_name = class_name

    def get_message_type(self) -> int:
        return self._message_type

    def get_service_node_type(self) -> int:
        return 1  # Default service node

    def __str__(self) -> str:
        return f"MockGameMessage({self._class_name}, type={self._message_type})"
