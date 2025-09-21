"""
Python conversion of Supercell.Laser.Server.Message.MessageManager.cs (simplified)
Message manager for handling client messages
"""

from datetime import datetime, timedelta
from typing import Dict, Optional
import time

from networking.connection import Connection
from logic.home.home_mode import HomeMode
from logic.message.game_message import GameMessage
from logic.message.account.client_hello_message import ClientHelloMessage
from logic.message.account.auth.authentication_message import AuthenticationMessage
from logic.message.account.auth.authentication_ok_message import AuthenticationOkMessage
from logic.message.account.auth.authentication_failed_message import AuthenticationFailedMessage
from logic.message.account.server_hello_message import ServerHelloMessage
from logic.message.home.own_home_data_message import OwnHomeDataMessage
from logic.message.account.client_info_message import ClientInfoMessage
from logic.message.security.udp_connection_info_message import UdpConnectionInfoMessage
from logic.message.account.keep_alive_server_message import KeepAliveServerMessage
from logic.message.battle.matchmake_request_message import MatchmakeRequestMessage
from logic.message.battle.cancel_matchmaking_message import CancelMatchmakingMessage
from logic.message.battle.match_making_cancelled_message import MatchMakingCancelledMessage
from logic.message.home.go_home_message import GoHomeMessage
from logic.message.home.change_avatar_name_message import ChangeAvatarNameMessage
from logic.message.home.available_server_command_message import AvailableServerCommandMessage
from logic.command.avatar.logic_change_avatar_name_command import LogicChangeAvatarNameCommand
from database.accounts import Accounts
from database.alliances import Alliances
from database.cache.account_cache import AccountCache
from logic.game.events import Events
from logic.game.matchmaking import Matchmaking
from logic.game.battles import Battles
from logic.game.teams import Teams
from networking.session.sessions import Sessions
from settings.configuration import Configuration
from utils.helpers import Helpers
from logger import Logger

class MessageManager:
    """Message manager for handling client messages"""

    def __init__(self, connection: Connection):
        """Initialize message manager"""
        self.connection = connection
        self.home_mode: Optional[HomeMode] = None
        self.last_keep_alive = datetime.utcnow()

    def is_alive(self) -> bool:
        """Check if connection is alive based on keep alive"""
        return (datetime.utcnow() - self.last_keep_alive).total_seconds() < 15

    def receive_message(self, message: GameMessage) -> None:
        """Handle incoming message"""
        try:
            message_type = message.get_message_type()

            # Update keep alive for certain messages
            if message_type != 10100:  # Not ClientHello
                # Could send lobby info here if needed
                pass

            # Route message to appropriate handler
            if message_type == 10100:
                self._client_hello_received(message)
            elif message_type == 10101:
                self._login_received(message)
            elif message_type == 10107 or message_type == 10177:
                self._client_info_received(message)
            elif message_type == 10108:
                self._keep_alive_received()
            elif message_type == 10212:
                self._change_name_received(message)
            elif message_type == 14456:
                self._go_home_received(message)
            elif message_type == 18977:
                self._matchmake_request_received(message)
            elif message_type == 14106:
                self._cancel_matchmaking_received(message)
            # Add more message handlers as needed
            else:
                Logger.print_log(f"MessageManager::ReceiveMessage - no case for {message.__class__.__name__} ({message_type})")

        except Exception as e:
            Logger.error(f"Error handling message {message.__class__.__name__}: {e}")

    def _client_hello_received(self, message: ClientHelloMessage) -> None:
        """Handle ClientHello message"""
        try:
            self.connection.messaging.disable_crypto = False

            if Sessions.maintenance:
                self.connection.send(AuthenticationFailedMessage(error_code=10))
                return

            if message.major_version < 53:
                self.connection.send(AuthenticationFailedMessage(
                    error_code=8,
                    update_url="https://pd.qq.com/s/3az5imfyn"
                ))
                return

            self.connection.messaging.seed = message.client_seed
            self.connection.nonce = Helpers.random_string(32)

            hello = ServerHelloMessage()
            hello.set_server_hello_token(self.connection.messaging.session_token)
            hello.nonce = self.connection.nonce
            self.connection.send(hello)

        except Exception as e:
            Logger.error(f"Error in client hello: {e}")

    def _login_received(self, message: AuthenticationMessage) -> None:
        """Handle authentication/login message"""
        try:
            if message.client_major < 53:
                self.connection.send(AuthenticationFailedMessage(
                    error_code=8,
                    update_url="https://pd.qq.com/s/3az5imfyn"
                ))
                return

            if Sessions.maintenance:
                self.connection.send(AuthenticationFailedMessage(
                    error_code=10,
                    date_time=datetime.parse("2023-02-14 13:30:00")
                ))
                return

            # Load or create account
            account = None
            if message.account_id == 0:
                account = Accounts.create()
                AccountCache.save_all()
            else:
                account = Accounts.load(message.account_id)

            if not account:
                self.connection.send(AuthenticationFailedMessage(
                    error_code=1,
                    message="未找到账号。"
                ))
                return

            account.avatar.refresh()

            Logger.print_log(f"{account.avatar.name}({account.account_id})已登录。")

            if account.avatar.banned:
                self.connection.send(AuthenticationFailedMessage(error_code=11))
                return

            # Send login success
            login_ok = AuthenticationOkMessage()
            login_ok.account_id = account.account_id
            login_ok.pass_token = account.pass_token
            login_ok.server_environment = "dev"
            self.connection.send(login_ok)

            # Initialize home mode
            from logic.home.home_mode import HomeMode
            from .home_game_listener import HomeGameListener

            self.home_mode = HomeMode.load_home_state(
                HomeGameListener(self.connection),
                account.home,
                account.avatar,
                Events.get_events()
            )

            # Send home data
            ohd = OwnHomeDataMessage()
            ohd.home = self.home_mode.home
            ohd.avatar = self.home_mode.avatar
            self.connection.send(ohd)

            # Create session
            Sessions.create(self.home_mode, self.connection)

        except Exception as e:
            Logger.error(f"Error in login: {e}")

    def _client_info_received(self, message: ClientInfoMessage) -> None:
        """Handle client info message"""
        try:
            info = UdpConnectionInfoMessage()
            info.session_id = self.connection.udp_session_id
            info.server_address = Configuration.instance.udp_host
            info.server_port = Configuration.instance.udp_port
            self.connection.send(info)
        except Exception as e:
            Logger.error(f"Error in client info: {e}")

    def _keep_alive_received(self) -> None:
        """Handle keep alive message"""
        self.last_keep_alive = datetime.utcnow()
        # Could send KeepAliveServerMessage if needed

    def _change_name_received(self, message: ChangeAvatarNameMessage) -> None:
        """Handle name change request"""
        try:
            if not self.home_mode:
                return

            command = LogicChangeAvatarNameCommand()
            command.name = message.name
            command.change_name_cost = 0
            command.execute(self.home_mode)

            server_command = AvailableServerCommandMessage()
            server_command.command = command
            self.connection.send(server_command)

        except Exception as e:
            Logger.error(f"Error changing name: {e}")

    def _go_home_received(self, message: GoHomeMessage) -> None:
        """Handle go home request"""
        try:
            if self.connection.home and self.connection.avatar:
                ohd = OwnHomeDataMessage()
                ohd.home = self.connection.home
                ohd.avatar = self.connection.avatar
                self.connection.send(ohd)
        except Exception as e:
            Logger.error(f"Error going home: {e}")

    def _matchmake_request_received(self, message: MatchmakeRequestMessage) -> None:
        """Handle matchmaking request"""
        try:
            slot = message.event_slot

            if not Events.has_slot(slot):
                slot = 1

            Matchmaking.request_matchmake(self.connection, slot)

        except Exception as e:
            Logger.error(f"Error in matchmaking request: {e}")

    def _cancel_matchmaking_received(self, message: CancelMatchmakingMessage) -> None:
        """Handle cancel matchmaking"""
        try:
            Matchmaking.cancel_matchmake(self.connection)
            self.connection.send(MatchMakingCancelledMessage())
        except Exception as e:
            Logger.error(f"Error canceling matchmaking: {e}")

    # Add more message handlers as needed...

    def _handle_team_messages(self, message_type: int, message: GameMessage) -> None:
        """Handle team-related messages"""
        # Implement team message handling
        pass

    def _handle_alliance_messages(self, message_type: int, message: GameMessage) -> None:
        """Handle alliance-related messages"""
        # Implement alliance message handling
        pass

    def _handle_friend_messages(self, message_type: int, message: GameMessage) -> None:
        """Handle friend-related messages"""
        # Implement friend message handling
        pass
