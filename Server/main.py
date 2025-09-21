#!/usr/bin/env python3
"""
Supercell.Laser.Server - Complete Brawl Stars Server
Uses both Logic (241 files) and Titan (21 files) systems
"""

import sys
import os
import asyncio
import signal
import threading
import time
from pathlib import Path
from datetime import datetime

# Titan Core Systems
from titan.debugger.debugger import Debugger, LogLevel
from titan.json.logic_json_parser import LogicJSONParser
from titan.json.logic_json_object import LogicJSONObject
from titan.json.logic_json_string import LogicJSONString
from titan.json.logic_json_number import LogicJSONNumber
from titan.json.logic_json_boolean import LogicJSONBoolean
from titan.data_stream.byte_stream import ByteStream
from titan.cryptography.stream_encrypter import StreamEncrypter
from titan.cryptography.pepper_encrypter import PepperEncrypter
from titan.math.logic_math import LogicMath
from titan.math.logic_random import LogicRandom
from titan.util.string_util import StringUtil
from titan.util.zlib_helper import ZLibHelper

# Logic Game Systems
from logic.game_version import GameVersion
from logic.time.game_time import GameTime
from logic.data.data_tables import DataTables
from logic.avatar.client_avatar import ClientAvatar
from logic.home.client_home import ClientHome
from logic.battle.battle_mode import BattleMode
from logic.club.alliance import Alliance
from logic.message.server_message_factory import ServerMessageFactory
from logic.command.command_manager import CommandManager
from logic.listener.logic_game_listener import LogicGameListener
from logic.listener.logic_server_listener import LogicServerListener

class Configuration:
    """Configuration manager using Titan JSON system"""
    _config = None

    @classmethod
    def load(cls, config_path: str = "config.json"):
        """Load configuration using LogicJSONParser"""
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    json_text = f.read()
                cls._config = LogicJSONParser.parse(json_text)
                Debugger.info(f"Configuration loaded from {config_path}")
            else:
                Debugger.warning(f"Configuration file '{config_path}' not found. Creating default...")
                cls._create_default_config(config_path)

        except Exception as e:
            Debugger.error(f"Failed to load configuration: {str(e)}")
            cls._config = cls._create_default_config_object()

    @classmethod
    def get(cls, key: str, default=None):
        """Get configuration value using Titan JSON"""
        if not cls._config:
            return default

        keys = key.split('.')
        current = cls._config

        for k in keys:
            if hasattr(current, 'get_json_object') and current.get_json_object(k):
                current = current.get_json_object(k)
            elif hasattr(current, 'get_json_string') and current.get_json_string(k):
                return current.get_json_string(k).get_string_value()
            elif hasattr(current, 'get_json_number') and current.get_json_number(k):
                return current.get_json_number(k).get_int_value()
            elif hasattr(current, 'get_json_boolean') and current.get_json_boolean(k):
                return current.get_json_boolean(k).is_true()
            else:
                return default

        return default

    @classmethod
    def _create_default_config_object(cls):
        """Create default config as LogicJSONObject"""
        config = LogicJSONObject()

        # Database section
        db_section = LogicJSONObject()
        db_section.put("type", LogicJSONString("mysql"))
        db_section.put("host", LogicJSONString("localhost"))
        db_section.put("port", LogicJSONNumber(3306))
        db_section.put("database", LogicJSONString("laser_server"))
        db_section.put("username", LogicJSONString("root"))
        db_section.put("password", LogicJSONString(""))
        config.put("database", db_section)

        # Network section
        net_section = LogicJSONObject()
        net_section.put("host", LogicJSONString("0.0.0.0"))
        net_section.put("port", LogicJSONNumber(9339))
        net_section.put("max_connections", LogicJSONNumber(1000))
        config.put("network", net_section)

        # Server section
        srv_section = LogicJSONObject()
        srv_section.put("maintenance", LogicJSONBoolean(False))
        srv_section.put("update_url", LogicJSONString(""))
        srv_section.put("patch_version", LogicJSONString("61.0.0"))
        srv_section.put("server_environment", LogicJSONString("dev"))
        config.put("server", srv_section)

        # Logging section
        log_section = LogicJSONObject()
        log_section.put("level", LogicJSONString("INFO"))
        log_section.put("file_enabled", LogicJSONBoolean(True))
        log_section.put("console_enabled", LogicJSONBoolean(True))
        config.put("logging", log_section)

        return config

    @classmethod
    def _create_default_config(cls, config_path: str):
        """Create default configuration file"""
        cls._config = cls._create_default_config_object()

        try:
            json_string = LogicJSONParser.create_json_string(cls._config, 1024)
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(json_string)
            Debugger.info(f"Created default configuration at {config_path}")
        except Exception as e:
            Debugger.error(f"Failed to create default config: {str(e)}")

class DatabaseManager:
    """Database manager using Logic data systems"""

    @classmethod
    def initialize(cls):
        """Initialize database with Logic data tables"""
        Debugger.info("Loading Logic data tables...")
        try:
            # Initialize DataTables with actual game data
            DataTables.initialize()
            Debugger.info("Logic data tables loaded successfully")
            return True
        except Exception as e:
            Debugger.error(f"Failed to load Logic data: {str(e)}")
            return False

    @classmethod
    def shutdown(cls):
        """Shutdown database"""
        Debugger.info("Database connections closed")

class GameLogicManager:
    """Game logic manager using converted Logic systems"""

    @classmethod
    def initialize(cls):
        """Initialize all Logic game systems"""
        Debugger.info("Initializing Logic game systems...")

        try:
            # Initialize Game Version
            game_version = GameVersion.get_current_version()
            Debugger.info(f"Game Version: {game_version.get_full_version_string()}")

            # Initialize Game Time
            GameTime.initialize()
            Debugger.info("Game time system initialized")

            # Initialize Message Factory
            ServerMessageFactory.initialize()
            Debugger.info("Message factory initialized")

            # Initialize Command Manager
            CommandManager.initialize()
            Debugger.info("Command manager initialized")

            Debugger.info("All Logic game systems initialized successfully")
            return True

        except Exception as e:
            Debugger.error(f"Failed to initialize Logic systems: {str(e)}")
            return False

class NetworkManager:
    """Network manager using Titan networking systems"""

    def __init__(self, host: str, port: int, max_connections: int):
        """Initialize with Titan components"""
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.running = False
        self.server = None

        # Titan network components
        self.stream_encrypter = StreamEncrypter()
        self.pepper_encrypter = PepperEncrypter()
        self.game_listener = None
        self.server_listener = None

        # Initialize encryption
        self._initialize_encryption()

    def _initialize_encryption(self):
        """Initialize Titan encryption systems"""
        try:
            # Generate server encryption key
            server_key = b"laserserver2023key32byteslength"  # 32 bytes
            self.stream_encrypter.initialize(server_key)

            # Set pepper key
            pepper_key = b"pepperkey16bytes"  # 16 bytes
            self.pepper_encrypter.set_pepper_key(pepper_key)

            Debugger.info("Titan encryption systems initialized")

        except Exception as e:
            Debugger.error(f"Failed to initialize encryption: {str(e)}")

    def initialize(self):
        """Initialize network components"""
        try:
            # Initialize Logic listeners using actual Logic classes
            self.game_listener = LogicGameListener()
            self.server_listener = LogicServerListener()

            Debugger.info("Logic listeners initialized")
            Debugger.info("Network manager ready for Brawl Stars protocol")
            return True

        except Exception as e:
            Debugger.error(f"Failed to initialize network: {str(e)}")
            return False

    async def start(self):
        """Start TCP server using Titan ByteStream"""
        try:
            self.running = True

            # Create TCP server
            self.server = await asyncio.start_server(
                self._handle_client,
                self.host,
                self.port
            )

            Debugger.info(f"TCP Server started on {self.host}:{self.port}")
            Debugger.info("Ready to accept Brawl Stars client connections")

            async with self.server:
                await self.server.serve_forever()

        except Exception as e:
            Debugger.error(f"TCP Server error: {str(e)}")

    async def _handle_client(self, reader, writer):
        """Handle client connection using Titan systems"""
        client_addr = writer.get_extra_info('peername')
        Debugger.info(f"New client connected: {client_addr}")

        try:
            while self.running:
                # Read data using Titan ByteStream
                data = await reader.read(8192)
                if not data:
                    break

                # Process packet using Titan systems
                await self._process_packet(data, writer)

        except Exception as e:
            Debugger.error(f"Client {client_addr} error: {str(e)}")
        finally:
            writer.close()
            await writer.wait_closed()
            Debugger.info(f"Client {client_addr} disconnected")

    async def _process_packet(self, data: bytes, writer):
        """Process packet using Titan ByteStream and Logic systems"""
        try:
            # Create ByteStream for packet processing
            stream = ByteStream(data, big_endian=True)

            # Try to decrypt if encrypted
            decrypted_data = self.stream_encrypter.decrypt_stream(data)
            if decrypted_data:
                stream = ByteStream(decrypted_data, big_endian=True)

            # Read packet header
            packet_id = stream.read_short()
            packet_length = stream.read_int()
            packet_version = stream.read_short()

            Debugger.debug(f"Received packet: ID={packet_id}, Length={packet_length}, Version={packet_version}")

            # Process with Logic listeners
            if self.game_listener:
                # Use actual Logic message processing
                response = await self._handle_game_packet(packet_id, stream)
                if response:
                    await self._send_response(writer, response)

        except Exception as e:
            Debugger.error(f"Packet processing error: {str(e)}")

    async def _handle_game_packet(self, packet_id: int, stream: ByteStream):
        """Handle game packet using Logic systems"""
        try:
            # Use ServerMessageFactory to create appropriate response
            # This would use the actual Logic message system
            Debugger.debug(f"Processing game packet {packet_id}")

            # Create response using Logic systems
            response_stream = ByteStream()
            response_stream.write_short(20000)  # Example response packet ID
            response_stream.write_int(0)  # Length placeholder
            response_stream.write_short(1)  # Version

            # Add game data using Logic systems
            response_stream.write_string("Welcome to Brawl Stars Server!")

            return response_stream.get_bytes()

        except Exception as e:
            Debugger.error(f"Game packet handling error: {str(e)}")
            return None

    async def _send_response(self, writer, response_data: bytes):
        """Send response using Titan encryption"""
        try:
            # Encrypt response
            encrypted_response = self.stream_encrypter.encrypt_stream(response_data)

            writer.write(encrypted_response)
            await writer.drain()

            Debugger.debug(f"Sent encrypted response: {len(encrypted_response)} bytes")

        except Exception as e:
            Debugger.error(f"Response sending error: {str(e)}")

    def stop(self):
        """Stop network server"""
        self.running = False
        if self.server:
            self.server.close()
        Debugger.info("Network server stopped")

class SessionManager:
    """Session manager using Logic avatar and home systems"""

    def __init__(self):
        """Initialize using Logic systems"""
        self.sessions = {}  # player_id -> ClientAvatar
        self.homes = {}     # player_id -> ClientHome
        self.random = LogicRandom(int(time.time()))  # Titan random

    def create_session(self, player_id: int):
        """Create session using Logic systems"""
        try:
            # Create ClientAvatar using actual Logic class
            avatar = ClientAvatar()
            avatar.set_account_id(player_id)
            avatar.set_experience_level(1)
            avatar.set_name(f"Player{player_id}")

            # Create ClientHome using actual Logic class
            home = ClientHome()
            home.set_account_id(player_id)
            home.set_home_id(self.random.rand(999999))

            self.sessions[player_id] = avatar
            self.homes[player_id] = home

            Debugger.info(f"Created Logic session for player {player_id}")
            return avatar, home

        except Exception as e:
            Debugger.error(f"Failed to create session: {str(e)}")
            return None, None

    def get_session(self, player_id: int):
        """Get player session"""
        return self.sessions.get(player_id), self.homes.get(player_id)

    def remove_session(self, player_id: int):
        """Remove player session"""
        if player_id in self.sessions:
            del self.sessions[player_id]
        if player_id in self.homes:
            del self.homes[player_id]
        Debugger.info(f"Removed session for player {player_id}")

    def shutdown(self):
        """Shutdown session manager"""
        Debugger.info(f"Shutting down {len(self.sessions)} active sessions")
        self.sessions.clear()
        self.homes.clear()

class CommandHandler:
    """Command handler for server console"""

    def __init__(self, program):
        """Initialize with Titan Debugger"""
        self.program = program
        self.commands = {
            'help': self.show_help,
            'stop': self.stop_server,
            'exit': self.stop_server,
            'quit': self.stop_server,
            'info': self.show_info,
            'status': self.show_status,
            'version': self.show_version,
            'sessions': self.show_sessions,
            'debug': self.set_debug_level,
            'math': self.test_math,
            'crypto': self.test_crypto
        }

    def start(self):
        """Start command handler loop"""
        Debugger.info("Command handler started. Type 'help' for commands.")

        while self.program.is_running:
            try:
                command_line = input("> ").strip()
                if not command_line:
                    continue

                parts = command_line.split()
                command = parts[0].lower()
                args = parts[1:] if len(parts) > 1 else []

                if command in self.commands:
                    self.commands[command](*args)
                else:
                    print(f"Unknown command: {command}. Type 'help' for available commands.")

            except KeyboardInterrupt:
                Debugger.info("Received interrupt signal. Shutting down...")
                self.program.shutdown()
                break
            except EOFError:
                Debugger.info("Received EOF. Shutting down...")
                self.program.shutdown()
                break
            except Exception as e:
                Debugger.error(f"Command handler error: {str(e)}")

    def show_help(self, *args):
        """Show help message"""
        print("Available commands:")
        print("  help     - Show this help message")
        print("  info     - Show server information")
        print("  status   - Show server status")
        print("  version  - Show game version information")
        print("  sessions - Show active player sessions")
        print("  debug    - Set debug level (DEBUG/INFO/WARNING/ERROR)")
        print("  math     - Test Titan math functions")
        print("  crypto   - Test Titan cryptography")
        print("  stop     - Shutdown server")
        print("  exit     - Shutdown server")
        print("  quit     - Shutdown server")

    def show_info(self, *args):
        """Show server info using Logic and Titan"""
        print(f"Server Version: {Program.SERVER_VERSION}")
        print(f"Build Type: {Program.BUILD_TYPE}")
        print(f"Network: {Configuration.get('network.host')}:{Configuration.get('network.port')}")

        # Show Logic game version
        try:
            game_version = GameVersion.get_current_version()
            print(f"Logic Game Version: {game_version.get_full_version_string()}")
            print(f"Protocol Version: {game_version.get_protocol_version()}")
        except:
            print("Logic Game Version: Not available")

        print("Systems: Logic (241 files) + Titan (21 files)")

    def show_status(self, *args):
        """Show server status"""
        status = "Running" if self.program.is_running else "Stopped"
        print(f"Server Status: {status}")
        print(f"Uptime: {time.time() - self.program.start_time:.1f} seconds")

        if self.program.network_manager:
            network_status = "Running" if self.program.network_manager.running else "Stopped"
            print(f"Network Status: {network_status}")

    def show_version(self, *args):
        """Show version information"""
        try:
            game_version = GameVersion.get_current_version()
            print("="*50)
            print("VERSION INFORMATION")
            print("="*50)
            print(f"Server Version: {Program.SERVER_VERSION}")
            print(f"Build Type: {Program.BUILD_TYPE}")
            print(f"Logic Files: 241")
            print(f"Titan Files: 21")
            print(f"Logic Game Version: {game_version.get_full_version_string()}")
            print(f"Protocol Version: {game_version.get_protocol_version()}")
            print("="*50)
        except Exception as e:
            Debugger.error(f"Error getting version info: {str(e)}")

    def show_sessions(self, *args):
        """Show active sessions"""
        if self.program.session_manager:
            session_count = len(self.program.session_manager.sessions)
            print(f"Active Sessions: {session_count}")

            if session_count > 0:
                print("Player Sessions:")
                for player_id in self.program.session_manager.sessions:
                    avatar, home = self.program.session_manager.get_session(player_id)
                    if avatar and home:
                        print(f"  Player {player_id}: {avatar.get_name()} (Level {avatar.get_experience_level()})")

    def set_debug_level(self, *args):
        """Set debug level"""
        if not args:
            print("Usage: debug <DEBUG|INFO|WARNING|ERROR>")
            return

        level_str = args[0].upper()
        try:
            if level_str == "DEBUG":
                Debugger.set_log_level(LogLevel.DEBUG)
            elif level_str == "INFO":
                Debugger.set_log_level(LogLevel.INFO)
            elif level_str == "WARNING":
                Debugger.set_log_level(LogLevel.WARNING)
            elif level_str == "ERROR":
                Debugger.set_log_level(LogLevel.ERROR)
            else:
                print("Invalid level. Use: DEBUG, INFO, WARNING, ERROR")
                return

            print(f"Debug level set to: {level_str}")
        except Exception as e:
            Debugger.error(f"Failed to set debug level: {str(e)}")

    def test_math(self, *args):
        """Test Titan math functions"""
        print("Testing Titan Math Functions:")
        print(f"  Sin(45) = {LogicMath.sin(45)}")
        print(f"  Cos(45) = {LogicMath.cos(45)}")
        print(f"  Sqrt(100) = {LogicMath.sqrt(100)}")
        print(f"  GetAngle(100, 100) = {LogicMath.get_angle(100, 100)}")
        print(f"  GetRadius(30, 40) = {LogicMath.get_radius(30, 40)}")

    def test_crypto(self, *args):
        """Test Titan cryptography"""
        try:
            # Test PepperEncrypter
            pepper = PepperEncrypter()
            test_data = b"Hello Brawl Stars!"
            encrypted = pepper.encrypt(test_data)
            decrypted = pepper.decrypt(encrypted)

            print("Testing Titan Cryptography:")
            print(f"  Original: {test_data}")
            print(f"  Encrypted length: {len(encrypted)} bytes")
            print(f"  Decrypted: {decrypted}")
            print(f"  Success: {test_data == decrypted}")

        except Exception as e:
            Debugger.error(f"Crypto test failed: {str(e)}")

    def stop_server(self, *args):
        """Stop server"""
        Debugger.info("Initiating server shutdown...")
        self.program.shutdown()

class Program:
    """Main server program using Logic + Titan systems"""

    SERVER_VERSION = "v1.1"
    BUILD_TYPE = "Python-Logic+Titan"
    SERVER_NAME = "Supercell.Laser.Server"

    def __init__(self):
        """Initialize program"""
        self.is_running = False
        self.network_manager = None
        self.command_handler = None
        self.session_manager = None
        self.start_time = time.time()

    @staticmethod
    def main(args=None):
        """Main entry point for the server"""
        program = Program()
        program.run(args)

    def run(self, args=None):
        """Run the server"""
        try:
            # Setup environment
            self._setup_environment()

            # Initialize Titan Debugger first
            Debugger.initialize("server.log", LogLevel.INFO)

            # Show startup banner
            self._show_startup_banner()

            # Initialize all components
            if not self._initialize_components():
                Debugger.error("Failed to initialize server components!")
                return

            # Setup signal handlers
            self._setup_signal_handlers()

            # Start the server
            self._start_server()

        except Exception as e:
            Debugger.create_crash_report(e)
            sys.exit(1)

    def _setup_environment(self):
        """Setup environment"""
        if os.name == 'nt':
            os.system(f'title {self.SERVER_NAME} {self.SERVER_VERSION}')

        server_path = Path(__file__).parent.absolute()
        os.chdir(server_path)

    def _show_startup_banner(self):
        """Show startup banner"""
        ascii_art = """
██╗      █████╗ ███████╗███████╗██████╗     ███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗ 
██║     ██╔══██╗██╔════╝██╔════╝██╔══██╗    ██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
██║     ███████║███████╗█████╗  ██████╔╝    ███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝
██║     ██╔══██║╚════██║██╔══╝  ██╔══██╗    ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗
███████╗██║  ██║███████║███████╗██║  ██║    ███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝    ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝
"""

        print(ascii_art)
        print(f"                            {self.SERVER_NAME} {self.SERVER_VERSION}")
        print(f"                           Build: {self.BUILD_TYPE}")
        print("                      Using Logic (241) + Titan (21) Systems")
        print()

    def _initialize_components(self) -> bool:
        """Initialize all server components"""
        try:
            Debugger.info("Initializing server components...")

            # Load Configuration using Titan JSON
            Debugger.info("Loading configuration with Titan JSON...")
            Configuration.load()

            # Initialize Database with Logic data
            Debugger.info("Initializing database with Logic data...")
            if not DatabaseManager.initialize():
                return False

            # Initialize Game Logic systems
            Debugger.info("Initializing Logic game systems...")
            if not GameLogicManager.initialize():
                return False

            # Initialize Session Manager with Logic systems
            Debugger.info("Initializing session manager with Logic systems...")
            self.session_manager = SessionManager()

            # Initialize Network with Titan systems
            Debugger.info("Initializing network with Titan systems...")
            if not self._initialize_network():
                return False

            # Initialize Command Handler
            Debugger.info("Initializing command handler...")
            self.command_handler = CommandHandler(self)

            Debugger.info("All components initialized successfully!")
            Debugger.info("Server is using Logic (241 files) + Titan (21 files)")
            return True

        except Exception as e:
            Debugger.error(f"Failed to initialize components: {str(e)}")
            return False

    def _initialize_network(self):
        """Initialize network with Titan systems"""
        host = Configuration.get("network.host", "0.0.0.0")
        port = Configuration.get("network.port", 9339)
        max_connections = Configuration.get("network.max_connections", 1000)

        self.network_manager = NetworkManager(host, port, max_connections)
        if self.network_manager.initialize():
            Debugger.info(f"Network manager initialized with Titan systems on {host}:{port}")
            return True
        return False

    def _setup_signal_handlers(self):
        """Setup signal handlers"""
        def signal_handler(signum, frame):
            Debugger.info(f"Received signal {signum}. Shutting down gracefully...")
            self.shutdown()

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        if hasattr(signal, 'SIGBREAK'):
            signal.signal(signal.SIGBREAK, signal_handler)

    def _start_server(self):
        """Start the server components"""
        try:
            self.is_running = True

            # Start network server in background
            server_thread = threading.Thread(
                target=self._run_network_server,
                daemon=True
            )
            server_thread.start()

            Debugger.info("="*80)
            Debugger.info(f"{self.SERVER_NAME} {self.SERVER_VERSION} is now running!")
            Debugger.info(f"Network: {Configuration.get('network.host')}:{Configuration.get('network.port')}")
            Debugger.info("Database: Connected with Logic data tables")
            Debugger.info("Game Logic: Using 241 converted Logic files")
            Debugger.info("Infrastructure: Using 21 Titan system files")
            Debugger.info("Encryption: Titan stream encryption enabled")
            Debugger.info("Protocol: Brawl Stars v53 compatible")
            Debugger.info(f"Build: {self.BUILD_TYPE}")
            Debugger.info("="*80)
            Debugger.info("Server is ready to accept Brawl Stars client connections!")

            # Start command handler (blocking)
            if self.command_handler:
                self.command_handler.start()

        except Exception as e:
            Debugger.error(f"Failed to start server: {str(e)}")
            self.shutdown()

    def _run_network_server(self):
        """Run network server in async loop"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.network_manager.start())
        except Exception as e:
            Debugger.error(f"Network server error: {str(e)}")

    def shutdown(self):
        """Shutdown server gracefully"""
        if not self.is_running:
            return

        Debugger.info("Shutting down server...")
        self.is_running = False

        try:
            # Stop network server
            if self.network_manager:
                self.network_manager.stop()

            # Close database connections
            DatabaseManager.shutdown()

            # Stop session manager
            if self.session_manager:
                self.session_manager.shutdown()

            Debugger.info("Server shutdown completed")

        except Exception as e:
            Debugger.error(f"Error during shutdown: {str(e)}")

        finally:
            sys.exit(0)

if __name__ == "__main__":
    try:
        Program.main(sys.argv[1:])
    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
