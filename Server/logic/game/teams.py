"""
Python conversion of Supercell.Laser.Server.Logic.Game.Teams.cs
Team management system
"""

import random
from typing import Dict, List, Optional
from dataclasses import dataclass

from logic.battle.battle_mode import BattleMode
from logic.battle.structures.battle_player import BattlePlayer
from logic.battle.structures.battle_player_map import BattlePlayerMap
from logic.command.home.logic_add_notification_command import LogicAddNotificationCommand
from logic.data.character_data import CharacterData
from logic.data.data_tables import DataTables
from logic.data.data_type import DataType
from logic.message.battle.start_loading_message import StartLoadingMessage
from logic.message.home.available_server_command_message import AvailableServerCommandMessage
from logic.message.team.team_game_starting_message import TeamGameStartingMessage
from logic.notification.floater_text_notification import FloaterTextNotification
from logic.team.team_entry import TeamEntry
from logic.team.team_member import TeamMember
from logic.util.game_mode_util import GameModeUtil
from networking.connection import Connection
from networking.session.sessions import Sessions
from networking.udp_gateway import UDPGateway
from .battles import Battles
from .matchmaking import Matchmaking, MatchmakingSlot

class Teams:
    """Static class for managing teams"""

    _entries: Dict[int, TeamEntry] = {}
    _team_id_counter: int = 0

    @classmethod
    def init(cls) -> None:
        """Initialize teams system"""
        cls._entries = {}
        cls._team_id_counter = 0

    @classmethod
    def get_count(cls) -> int:
        """Get team count"""
        return len(cls._entries)

    @classmethod
    def create(cls) -> TeamEntry:
        """Create new team"""
        entry = TeamEntry()
        cls._team_id_counter += 1
        entry.id = cls._team_id_counter
        cls._entries[entry.id] = entry
        return entry

    @classmethod
    def remove(cls, team_id: int) -> None:
        """Remove team by ID"""
        cls._entries.pop(team_id, None)

    @classmethod
    def get(cls, team_id: int) -> Optional[TeamEntry]:
        """Get team by ID"""
        return cls._entries.get(team_id)

    @classmethod
    def start_game(cls, team: TeamEntry) -> None:
        """Start game for team"""
        try:
            if team.type == 0:  # Matchmaking
                cls._start_matchmaking_game(team)
            elif team.type == 1:  # Friendly battle
                cls._start_friendly_game(team)
        except Exception as e:
            print(f"Error starting team game: {e}")

    @classmethod
    def _start_matchmaking_game(cls, team: TeamEntry) -> None:
        """Start matchmaking game for team"""
        for member in team.members:
            connection = Sessions.get_session(member.account_id).connection
            if connection:
                starting_msg = TeamGameStartingMessage()
                starting_msg.location_id = team.location_id
                connection.send(starting_msg)

                Matchmaking.request_matchmake(connection, team.event_slot, team.id)
                member.is_ready = False

    @classmethod
    def _start_friendly_game(cls, team: TeamEntry) -> None:
        """Start friendly game for team"""
        # Check if game mode is supported
        supported_modes = ["GemGrab", "Bounty", "Heist"]
        location_data = DataTables.get(DataType.LOCATION).get_data_by_global_id(team.location_id)

        if location_data.game_mode_variation not in supported_modes:
            # Send notification that game mode is not available
            notification_cmd = LogicAddNotificationCommand()
            notification_cmd.notification = FloaterTextNotification("该游戏模式暂不可用")

            server_cmd_msg = AvailableServerCommandMessage()
            server_cmd_msg.command = notification_cmd

            for member in team.members:
                session = Sessions.get_session(member.account_id)
                if session:
                    session.connection.send(server_cmd_msg)
            return

        # Create battle
        battle = BattleMode(team.location_id)
        battle.id = Battles.add(battle)

        if team.battle_player_map:
            battle.set_player_map(team.battle_player_map)

        battle.set_event_modifiers(team.custom_modifiers)

        # Create entries for team members
        entries = []
        for member in team.members:
            session = Sessions.get_session(member.account_id)
            if session:
                entry = MatchmakingEntry(session.connection)
                entry.preferred_team = member.team_index
                entries.append(entry)
                member.is_ready = False

        # Add players to battle
        for i, entry in enumerate(entries):
            socket = UDPGateway.create_socket()
            socket.tcp_connection = entry.connection
            socket.battle = battle
            entry.connection.udp_session_id = socket.session_id

            team_index = entry.preferred_team
            player = BattlePlayer.create(entry.connection.home, entry.connection.avatar, i, team_index)
            player.team_id = entry.player_team_id
            entry.player = player
            battle.add_player(player, entry.connection.udp_session_id)

        # Add bots to fill teams
        cls._add_friendly_bots(battle, team, entries)

        # Send loading messages
        for i, entry in enumerate(entries):
            loading_msg = StartLoadingMessage()
            loading_msg.location_id = battle.location.get_global_id()
            loading_msg.team_index = entry.player.team_index
            loading_msg.own_index = entry.player.player_index
            loading_msg.game_mode = battle.get_game_mode_variation()

            if battle.battle_player_map:
                loading_msg.set_player_map(battle.battle_player_map)

            loading_msg.modifiers = battle.event_modifiers

            entry.connection.avatar.udp_session_id = entry.connection.udp_session_id
            loading_msg.players.extend(battle.get_players())
            entry.connection.send(loading_msg)
            battle.dummy = loading_msg

        battle.add_game_objects()
        battle.start()

    @classmethod
    def _add_friendly_bots(cls, battle: BattleMode, team: TeamEntry, entries: List) -> None:
        """Add bots to friendly battle"""
        team1_bots = []
        team2_bots = []

        # Add bots for team 0
        for i in range(battle.get_team_players_count(0), battle.get_players_count_with_game_mode_variation() // 2):
            if i in team.disabled_bots:
                continue

            # Find valid bot character
            valid_bot = False
            bot_character = -1
            while not valid_bot:
                bot_character = 16000000 + random.choice(MatchmakingSlot.BOT_BRAWLERS)
                valid_bot = bot_character not in team1_bots

            team1_bots.append(bot_character)
            character_data = DataTables.get(16).get_data_by_global_id(bot_character)
            bot = BattlePlayer.create_bot_info(str(i - len(entries) + 1), battle.get_players_count(), 0, bot_character)
            battle.add_player(bot, -1)

        # Add bots for team 1
        start_idx = battle.get_players_count_with_game_mode_variation() // 2 + battle.get_team_players_count(1)
        for i in range(start_idx, battle.get_players_count_with_game_mode_variation()):
            if i in team.disabled_bots:
                continue

            # Find valid bot character
            valid_bot = False
            bot_character = -1
            while not valid_bot:
                bot_character = 16000000 + random.choice(MatchmakingSlot.BOT_BRAWLERS)
                valid_bot = bot_character not in team2_bots

            team2_bots.append(bot_character)
            character_data = DataTables.get(16).get_data_by_global_id(bot_character)
            bot = BattlePlayer.create_bot_info(str(i - len(entries) + 1), battle.get_players_count(), 1, bot_character)
            battle.add_player(bot, -1)

# Import at the end to avoid circular imports
from .matchmaking import MatchmakingEntry
