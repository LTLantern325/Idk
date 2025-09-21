"""
Python conversion of Supercell.Laser.Server.Handler.CmdHandler.cs
Command handler for server administration commands
"""

import sys
import threading
import inspect
from typing import List, Optional

from logic.avatar.client_avatar import ClientAvatar
from logic.battle.level.map_loader import MapLoader
from logic.data.data_tables import DataTables
from logic.data.data_type import DataType
from logic.data.character_data import CharacterData
from logic.data.helper.logic_long_code_generator import LogicLongCodeGenerator
from logic.home.client_home import ClientHome
from logic.listener.logic_server_listener import LogicServerListener
from logic.message.account.auth.authentication_failed_message import AuthenticationFailedMessage
from logic.message.account.auth.unlock_account_ok_message import UnlockAccountOkMessage
from logic.util.logic_util import LogicUtil
from database.accounts import Accounts
from database.alliances import Alliances
from database.cache.account_cache import AccountCache
from database.cache.alliance_cache import AllianceCache
from database.models.account import Account
from networking.session.sessions import Sessions
from logger import Logger

class CmdHandler:
    """Static class for handling server commands"""

    @staticmethod
    def start():
        """Start the command handler loop"""
        print("Command handler started. Type commands starting with '/' or 'help' for available commands.")

        while True:
            try:
                cmd = input("> ").strip()
                if not cmd:
                    continue

                if cmd.lower() == "help":
                    CmdHandler._print_help()
                    continue

                if not cmd.startswith("/"):
                    print("Commands must start with '/'")
                    continue

                CmdHandler.handle_cmd(cmd)

            except KeyboardInterrupt:
                print("\nShutting down command handler...")
                break
            except EOFError:
                print("\nEOF received, shutting down...")
                break
            except Exception as e:
                print(f"Error processing command: {e}")

    @staticmethod
    def _print_help():
        """Print available commands"""
        print("Available commands:")
        print("  /premium [TAG]           - Give premium status to account")
        print("  /ban [TAG]               - Ban account")
        print("  /unban [TAG]             - Unban account")
        print("  /changename [TAG] [NAME] - Change account name")
        print("  /getvalue [TAG] [FIELD]  - Get field value from account")
        print("  /changevalue [TAG] [FIELD] [VALUE] - Change field value")
        print("  /unlockall [TAG]         - Unlock all brawlers for account")
        print("  /removeall [TAG]         - Remove all brawlers from account")
        print("  /maintenance             - Start maintenance mode")
        print("  /m                       - Start maintenance mode (short)")
        print("  /login [TAG]             - Send login token (requires session)")
        print("  /changetheme [THEME_ID]  - Change theme (requires session)")
        print("  /ToID [TAG]              - Convert tag to ID")
        print("  help                     - Show this help message")

    @staticmethod
    def handle_cmd(cmd: str, own_account_id: int = -1):
        """Handle a command string"""
        if not cmd.startswith("/"):
            return

        cmd = cmd[1:]  # Remove leading '/'
        args = cmd.split()

        if len(args) < 1:
            return

        command = args[0].lower()

        try:
            if command == "premium":
                CmdHandler._execute_give_premium_to_account(args)
            elif command == "ban":
                CmdHandler._execute_ban_account(args)
            elif command == "toid":
                if len(args) >= 2:
                    account_id = LogicLongCodeGenerator.to_id(args[1])
                    print(f"ID: {account_id}")
                else:
                    print("Usage: /ToID [TAG]")
            elif command == "unban":
                CmdHandler._execute_unban_account(args)
            elif command == "changename":
                CmdHandler._execute_change_name_for_account(args)
            elif command == "getvalue":
                CmdHandler._execute_get_field_value(args)
            elif command == "changevalue":
                CmdHandler._execute_change_value_for_account(args)
            elif command == "unlockall":
                CmdHandler._execute_unlock_all_for_account(args)
            elif command == "removeall":
                CmdHandler._execute_remove_all_for_account(args)
            elif command == "maintenance" or command == "m":
                print("Starting maintenance...")
                CmdHandler._execute_shutdown()
                print("Maintenance started!")
            elif command == "md":
                # Map data debug command
                logic_datas = DataTables.get(DataType.MAP).get_datas()
                if logic_datas:
                    logic_data = logic_datas[0]
                    s = logic_data.get_csv_row().get_value_at(1)
                    o = logic_data.get_csv_row().get_array_size_at(1)
                    m = MapLoader.init_with_map_from_data_table(None, DataTables.get(19), "Tutorial")
                    print(f"Map data: {s}, size: {o}")
            elif command == "login":
                if own_account_id == -1:
                    print("Login command requires session context")
                    return
                if len(args) < 2:
                    print("Usage: /login [TAG]")
                    return

                account_id = LogicLongCodeGenerator.to_id(args[1])
                account = Accounts.load(account_id)
                if not account:
                    print("Fail: account not found!")
                    return

                if LogicServerListener.instance and LogicServerListener.instance.is_player_online(own_account_id):
                    game_listener = LogicServerListener.instance.get_game_listener(own_account_id)
                    if game_listener:
                        unlock_msg = UnlockAccountOkMessage()
                        unlock_msg.account_id = account.account_id
                        unlock_msg.pass_token = account.pass_token
                        game_listener.send_tcp_message(unlock_msg)
            elif command == "changetheme":
                if own_account_id == -1:
                    print("Change theme command requires session context")
                    return
                if len(args) < 2:
                    print("Usage: /changetheme [THEME_ID]")
                    return

                account = Accounts.load(own_account_id)
                if account:
                    try:
                        theme_id = int(args[1])
                        account.home.preferred_theme_id = theme_id
                        print(f"Theme changed to {theme_id}")
                    except ValueError:
                        print("Invalid theme ID")
                else:
                    print("Account not found")
            else:
                print(f"Unknown command: {command}")

        except Exception as e:
            print(f"Error executing command '{command}': {e}")

    @staticmethod
    def _execute_unlock_all_for_account(args: List[str]):
        """Unlock all brawlers for account"""
        if len(args) != 2:
            print("Usage: /unlockall [TAG]")
            return

        account_id = LogicLongCodeGenerator.to_id(args[1])
        account = Accounts.load(account_id)
        if not account:
            print("Fail: account not found!")
            return

        # Refresh avatar to unlock all
        account.avatar.refresh()

        AccountCache.save_all()
        Logger.print_log(f"Successfully unlocked all brawlers for account {account_id} ({args[1]})")

        # Kick player if online
        if Sessions.is_session_active(account_id):
            session = Sessions.get_session(account_id)
            if session and session.game_listener:
                auth_fail_msg = AuthenticationFailedMessage()
                auth_fail_msg.message = "6"
                session.game_listener.send_tcp_message(auth_fail_msg)
            Sessions.remove(account_id)

    @staticmethod
    def _execute_remove_all_for_account(args: List[str]):
        """Remove all brawlers from account"""
        if len(args) != 2:
            print("Usage: /removeall [TAG]")
            return

        account_id = LogicLongCodeGenerator.to_id(args[1])
        account = Accounts.load(account_id)
        if not account:
            print("Fail: account not found!")
            return

        # Remove all heroes starting from 16000001
        i = 1
        while True:
            hero_id = 16000000 + i
            if account.avatar.has_hero(hero_id):
                character = DataTables.get(16).get_data_with_id(i)
                if not character or not character.is_hero():
                    break
                account.avatar.remove_hero(character.get_global_id())
                i += 1
            else:
                break

        Logger.print_log(f"Successfully removed all brawlers for account {account_id} ({args[1]})")

        # Kick player if online
        if Sessions.is_session_active(account_id):
            session = Sessions.get_session(account_id)
            if session and session.game_listener:
                auth_fail_msg = AuthenticationFailedMessage()
                auth_fail_msg.message = "Your account updated!"
                session.game_listener.send_tcp_message(auth_fail_msg)
            Sessions.remove(account_id)

    @staticmethod
    def _execute_give_premium_to_account(args: List[str]):
        """Give premium status to account"""
        if len(args) != 2:
            print("Usage: /premium [TAG]")
            return

        account_id = LogicLongCodeGenerator.to_id(args[1])
        account = Accounts.load(account_id)
        if not account:
            print("Fail: account not found!")
            return

        account.avatar.is_premium = True

        # Kick player if online to refresh
        if Sessions.is_session_active(account_id):
            session = Sessions.get_session(account_id)
            if session and session.game_listener:
                auth_fail_msg = AuthenticationFailedMessage()
                auth_fail_msg.message = "Your account updated!"
                session.game_listener.send_tcp_message(auth_fail_msg)
            Sessions.remove(account_id)

    @staticmethod
    def _execute_unban_account(args: List[str]):
        """Unban account"""
        if len(args) != 2:
            print("Usage: /unban [TAG]")
            return

        account_id = LogicLongCodeGenerator.to_id(args[1])
        account = Accounts.load(account_id)
        if not account:
            print("Fail: account not found!")
            return

        account.avatar.banned = False

        # Kick player if online to refresh
        if Sessions.is_session_active(account_id):
            session = Sessions.get_session(account_id)
            if session and session.game_listener:
                auth_fail_msg = AuthenticationFailedMessage()
                auth_fail_msg.message = "Your account updated!"
                session.game_listener.send_tcp_message(auth_fail_msg)
            Sessions.remove(account_id)

    @staticmethod
    def _execute_ban_account(args: List[str]):
        """Ban account"""
        if len(args) != 2:
            print("Usage: /ban [TAG]")
            return

        account_id = LogicLongCodeGenerator.to_id(args[1])
        account = Accounts.load(account_id)
        if not account:
            print("Fail: account not found!")
            return

        account.avatar.banned = True
        account.avatar.reset_trophies()
        account.avatar.name = "Brawler"

        # Kick player if online
        if Sessions.is_session_active(account_id):
            session = Sessions.get_session(account_id)
            if session and session.game_listener:
                auth_fail_msg = AuthenticationFailedMessage()
                auth_fail_msg.message = "Your account updated!"
                session.game_listener.send_tcp_message(auth_fail_msg)
            Sessions.remove(account_id)

    @staticmethod
    def _execute_change_name_for_account(args: List[str]):
        """Change account name"""
        if len(args) != 3:
            print("Usage: /changename [TAG] [NewName]")
            return

        account_id = LogicLongCodeGenerator.to_id(args[1])
        account = Accounts.load(account_id)
        if not account:
            print("Fail: account not found!")
            return

        account.avatar.name = args[2]

        # Kick player if online to refresh
        if Sessions.is_session_active(account_id):
            session = Sessions.get_session(account_id)
            if session and session.game_listener:
                auth_fail_msg = AuthenticationFailedMessage()
                auth_fail_msg.message = "Your account updated!"
                session.game_listener.send_tcp_message(auth_fail_msg)
            Sessions.remove(account_id)

    @staticmethod
    def _execute_get_field_value(args: List[str]):
        """Get field value from account"""
        if len(args) != 3:
            print("Usage: /getvalue [TAG] [FieldName]")
            return

        account_id = LogicLongCodeGenerator.to_id(args[1])
        account = Accounts.load(account_id)
        if not account:
            print("Fail: account not found!")
            return

        field_name = args[2]

        try:
            if hasattr(account.avatar, field_name):
                value = getattr(account.avatar, field_name)
                print(f"ClientAvatar::{field_name} = {value}")
            else:
                print(f"Fail: ClientAvatar::{field_name} not found!")
        except Exception as e:
            print(f"Error getting field value: {e}")

    @staticmethod
    def _execute_change_value_for_account(args: List[str]):
        """Change field value for account"""
        if len(args) != 4:
            print("Usage: /changevalue [TAG] [FieldName] [Value]")
            return

        account_id = LogicLongCodeGenerator.to_id(args[1])
        account = Accounts.load(account_id)
        if not account:
            print("Fail: account not found!")
            return

        field_name = args[2]

        try:
            if hasattr(account.avatar, field_name):
                value = int(args[3])
                setattr(account.avatar, field_name, value)
                print(f"Successfully changed {field_name} to {value}")

                # Kick player if online to refresh
                if Sessions.is_session_active(account_id):
                    session = Sessions.get_session(account_id)
                    if session and session.game_listener:
                        auth_fail_msg = AuthenticationFailedMessage()
                        auth_fail_msg.message = "Your account updated!"
                        session.game_listener.send_tcp_message(auth_fail_msg)
                    Sessions.remove(account_id)
            else:
                print(f"Fail: ClientAvatar::{field_name} not found!")
        except ValueError:
            print("Invalid value - must be an integer")
        except Exception as e:
            print(f"Error changing field value: {e}")

    @staticmethod
    def _execute_shutdown():
        """Execute server shutdown"""
        Sessions.start_shutdown()
        AccountCache.save_all()
        AllianceCache.save_all()

        AccountCache._started = False
        AllianceCache._started = False
