"""
Python conversion of Supercell.Laser.Server.Logic.Game.Matchmaking.cs
Matchmaking system for game battles
"""

import threading
import time
import random
from typing import Dict, List, Optional, Tuple
from collections import deque
from dataclasses import dataclass

from logic.battle.battle_mode import BattleMode
from logic.battle.structures.battle_player import BattlePlayer
from logic.data.character_data import CharacterData
from logic.data.data_tables import DataTables
from logic.home.items.event_data import EventData
from logic.listener.logic_server_listener import LogicServerListener
from logic.message.battle.start_loading_message import StartLoadingMessage
from logic.message.battle.match_making_status_message import MatchMakingStatusMessage
from logic.message.battle.match_making_cancelled_message import MatchMakingCancelledMessage
from logic.message.home.authentication_failed_message import AuthenticationFailedMessage
from logic.team.team_entry import TeamEntry
from logic.team.team_member import TeamMember
from logic.util.game_mode_util import GameModeUtil
from logic.util.game_play_util import GamePlayUtil
from networking.connection import Connection
from networking.udp_gateway import UDPGateway
from networking.session.sessions import Sessions
from .events import Events
from .battles import Battles
from .teams import Teams

class Matchmaking:
    """Static class for managing matchmaking"""

    _slots: Dict[int, 'MatchmakingSlot'] = {}
    _update_thread: Optional[threading.Thread] = None
    _running: bool = False

    @classmethod
    def init(cls) -> None:
        """Initialize matchmaking system"""
        cls._slots = {}

        # Create slots for each event
        for event in Events.get_events():
            mode = GameModeUtil.get_game_mode_variation(event.location.game_mode_variation)
            player_count = GamePlayUtil.get_player_count_with_game_mode_variation(mode)
            cls._slots[event.slot] = MatchmakingSlot(event, player_count)

        cls._running = True
        cls._update_thread = threading.Thread(target=cls._update, daemon=True)
        cls._update_thread.start()

    @classmethod
    def _update(cls) -> None:
        """Update all matchmaking slots"""
        while cls._running:
            try:
                for slot in cls._slots.values():
                    slot.update()
                time.sleep(0.25)  # 250ms
            except Exception as e:
                print(f"Error in matchmaking update: {e}")
                time.sleep(0.25)

    @classmethod
    def request_matchmake(cls, connection: Connection, slot: int, team: int = -1) -> None:
        """Request matchmaking for connection"""
        if slot not in cls._slots:
            return

        connection.matchmake_slot = slot
        entry = MatchmakingEntry(connection)
        entry.player_team_id = team
        connection.matchmaking_entry = entry
        cls._slots[slot].add(entry)

    @classmethod
    def cancel_matchmake(cls, connection: Connection) -> None:
        """Cancel matchmaking for connection"""
        slot = connection.matchmake_slot
        if slot in cls._slots:
            connection.matchmake_slot = -1
            cls._slots[slot].remove(connection.matchmaking_entry)

            # Handle team cancellation
            if connection.matchmaking_entry.player_team_id > 0:
                team = Teams.get(connection.matchmaking_entry.player_team_id)
                if team:
                    for member in team.members:
                        member.is_ready = False
                        session = Sessions.get_session(member.account_id)
                        if session:
                            session.connection.matchmaking_entry.player_team_id = -1
                            cls.cancel_matchmake(session.connection)
                            cancelled_msg = MatchMakingCancelledMessage()
                            session.connection.send(cancelled_msg)
                    team.team_updated()

class MatchmakingSlot:
    """Matchmaking slot for specific event/game mode"""

    SEARCH_TIMEOUT = 3600
    BOT_BRAWLERS = [0, 1, 2, 3, 5, 6, 9, 10, 11, 12, 13, 14, 15, 16, 18, 23, 24, 27, 32, 38, 39, 40, 41, 42, 43, 45, 46, 48, 50, 54, 62]

    def __init__(self, event_data: EventData, players_required: int):
        self.players_required = players_required
        self.event_data = event_data
        self.queue: List[MatchmakingEntry] = []
        self.request_queue: deque = deque()
        self.remove_queue: deque = deque()
        self.seconds_left = self.SEARCH_TIMEOUT
        self.turns = 0

        # Special case for solo showdown
        if GameModeUtil.get_game_mode_variation(event_data.location.game_mode_variation) == 30:
            self.players_required = 1

    def update(self) -> None:
        """Update matchmaking slot"""
        try:
            if Sessions.maintenance:
                return

            # Remove disconnected players
            for entry in self.queue[:]:
                if not entry.connection.is_open:
                    self.remove(entry)

            # Process remove queue
            while self.remove_queue:
                entry = self.remove_queue.popleft()
                if entry in self.queue:
                    self.queue.remove(entry)

            # Process request queue
            while self.request_queue:
                entry = self.request_queue.popleft()
                # Check for duplicates
                existing = next((e for e in self.queue if e.connection == entry.connection), None)
                if not existing:
                    self.queue.append(entry)

            # Start games when enough players
            while len(self.queue) >= self.players_required:
                players = self.queue[:self.players_required]
                self.start_game(players)
                self.queue = self.queue[self.players_required:]

            # Handle timeout
            if self.queue and len(self.queue) < self.players_required and self.seconds_left <= 0:
                self.seconds_left = self.SEARCH_TIMEOUT
                self.start_game(self.queue[:])
                self.queue = []

            # Update timer
            if self.queue:
                self.turns += 1
                if self.turns >= 4:
                    self.turns = 0
                    self.seconds_left -= 1
            else:
                self.turns = 0
                self.seconds_left = self.SEARCH_TIMEOUT

            # Send status updates
            if self.queue:
                status_msg = MatchMakingStatusMessage()
                status_msg.seconds = self.seconds_left
                status_msg.found = len(self.queue)
                status_msg.max = self.players_required
                status_msg.show_tips = True

                for entry in self.queue:
                    entry.connection.send(status_msg)

        except Exception as e:
            print(f"Error in matchmaking slot update: {e}")

    def start_game(self, entries: List['MatchmakingEntry']) -> None:
        """Start game with given entries"""
        try:
            battle = BattleMode(self.event_data.location_id)
            battle.id = Battles.add(battle)

            rand = random.Random()

            # Handle different game modes
            if battle.get_game_mode_variation() == 7:  # Boss Fight
                self._setup_boss_fight(battle, entries, rand)
            elif GameModeUtil.has_two_teams(battle.get_game_mode_variation()):
                self._setup_team_battle(battle, entries, rand)
            else:
                self._setup_solo_battle(battle, entries, rand)

            # Start battle
            battle.add_game_objects()
            battle.start()

        except Exception as e:
            print(f"Error starting game: {e}")

    def _setup_boss_fight(self, battle: BattleMode, entries: List['MatchmakingEntry'], rand: random.Random) -> None:
        """Setup boss fight battle"""
        for i, entry in enumerate(entries):
            socket = UDPGateway.create_socket()
            socket.tcp_connection = entry.connection
            socket.battle = battle
            entry.connection.udp_session_id = socket.session_id

            player = BattlePlayer.create(entry.connection.home, entry.connection.avatar, i, 0)
            player.team_id = entry.player_team_id
            player.hero_power_level = 21
            entry.player = player
            battle.add_player(player, entry.connection.udp_session_id)

        # Add boss
        boss = BattlePlayer.create_story_mode_dummy("首领", battle.get_players_count_with_game_mode_variation(), 1, 32, 310, 254)
        battle.add_player(boss, -1)
        boss.bot = 2
        boss.hero_power_level = 391

    def _setup_team_battle(self, battle: BattleMode, entries: List['MatchmakingEntry'], rand: random.Random) -> None:
        """Setup team-based battle"""
        # Sort entries by teams
        sorted_entries = []
        team_entries = {}

        # Group team players
        for entry in entries[:]:
            if entry.player_team_id > 0:
                if entry.player_team_id not in team_entries:
                    team_entries[entry.player_team_id] = []
                team_entries[entry.player_team_id].append(entry)
                entries.remove(entry)

        # Add team players
        team_index = 0
        for team_id, team_players in team_entries.items():
            for entry in team_players:
                sorted_entries.append(entry)
                entry.preferred_team = team_index
            team_index = 1 - team_index  # Alternate between 0 and 1

        # Add solo players
        sorted_entries.extend(entries)

        # Create battle players
        for i, entry in enumerate(sorted_entries):
            socket = UDPGateway.create_socket()
            socket.tcp_connection = entry.connection
            socket.battle = battle
            entry.connection.udp_session_id = socket.session_id

            team_idx = i % 2
            if entry.preferred_team != -1:
                team_idx = entry.preferred_team

            # Balance teams
            if battle.get_team_players_count(team_idx) >= 3:
                team_idx = 1 - team_idx

            player = BattlePlayer.create(entry.connection.home, entry.connection.avatar, i, team_idx)
            player.team_id = entry.player_team_id
            entry.player = player
            battle.add_player(player, entry.connection.udp_session_id)

        # Add bots to fill teams
        self._add_team_bots(battle, sorted_entries, rand)

        # Send loading messages
        self._send_loading_messages(battle, sorted_entries)

    def _setup_solo_battle(self, battle: BattleMode, entries: List['MatchmakingEntry'], rand: random.Random) -> None:
        """Setup solo battle (like showdown)"""
        for i, entry in enumerate(entries):
            socket = UDPGateway.create_socket()
            socket.tcp_connection = entry.connection
            socket.battle = battle
            entry.connection.udp_session_id = socket.session_id

            player = BattlePlayer.create(entry.connection.home, entry.connection.avatar, i, i)
            player.team_id = entry.player_team_id
            entry.player = player
            battle.add_player(player, entry.connection.udp_session_id)

        # Add bots
        for i in range(len(entries), battle.get_players_count_with_game_mode_variation()):
            bot_character = 16000000 + self.BOT_BRAWLERS[rand.randint(0, len(self.BOT_BRAWLERS) - 1)]
            character_data = DataTables.get(16).get_data_by_global_id(bot_character)
            bot = BattlePlayer.create_bot_info(character_data.item_name.upper(), i, i, bot_character)
            battle.add_player(bot, -1)

        # Send loading messages
        self._send_loading_messages(battle, entries)

    def _add_team_bots(self, battle: BattleMode, entries: List['MatchmakingEntry'], rand: random.Random) -> None:
        """Add bots to balance teams"""
        team1_bots = []
        team2_bots = []

        for i in range(len(entries), battle.get_players_count_with_game_mode_variation()):
            team_idx = i % 2
            if battle.get_team_players_count(team_idx) >= 3:
                team_idx = 1 - team_idx

            # Find valid bot character
            valid_bot = False
            bot_character = -1
            while not valid_bot:
                bot_character = 16000000 + self.BOT_BRAWLERS[rand.randint(0, len(self.BOT_BRAWLERS) - 1)]
                if team_idx == 0:
                    valid_bot = bot_character not in team1_bots
                    if valid_bot:
                        team1_bots.append(bot_character)
                else:
                    valid_bot = bot_character not in team2_bots
                    if valid_bot:
                        team2_bots.append(bot_character)

            character_data = DataTables.get(16).get_data_by_global_id(bot_character)
            bot_name = f"机器人{i - len(entries) + 1}号"
            bot = BattlePlayer.create_bot_info(bot_name, i, team_idx, bot_character)
            battle.add_player(bot, -1)

    def _send_loading_messages(self, battle: BattleMode, entries: List['MatchmakingEntry']) -> None:
        """Send loading messages to all players"""
        for entry in entries:
            loading_msg = StartLoadingMessage()
            loading_msg.location_id = battle.location.get_global_id()
            loading_msg.team_index = entry.player.team_index
            loading_msg.own_index = entry.player.player_index
            loading_msg.game_mode = battle.get_game_mode_variation()

            entry.connection.avatar.udp_session_id = entry.connection.udp_session_id
            loading_msg.players.extend(battle.get_players())
            entry.connection.send(loading_msg)
            battle.dummy = loading_msg

    def add(self, entry: 'MatchmakingEntry') -> None:
        """Add entry to matchmaking"""
        self.request_queue.append(entry)

    def remove(self, entry: 'MatchmakingEntry') -> None:
        """Remove entry from matchmaking"""
        self.remove_queue.append(entry)

@dataclass
class MatchmakingEntry:
    """Entry in matchmaking queue"""

    def __init__(self, connection: Connection):
        self.connection = connection
        self.player: Optional[BattlePlayer] = None
        self.player_team_id: int = -1
        self.preferred_team: int = -1
