"""
Python conversion of Supercell.Laser.Server Resources.cs
Resource initialization for the Supercell Laser Server
"""

from logic.data import DataTables
from logic.listener import LogicServerListener
from database import Accounts, Alliances
from logic import Logic
from logic.game import Events, Sessions, Leaderboards, Battles, Matchmaking, Teams
from message import Processor
from networking import Connections, UDPGateway, TCPGateway
from networking.session import Session
from settings import Configuration

class Resources:
    """Static class for initializing server resources"""

    @staticmethod
    def init_database():
        """
        Initializes the databases
        """
        config = Configuration.instance
        Accounts.init(config.database_username, config.database_password)
        Alliances.init(config.database_username, config.database_password)

    @staticmethod
    def init_logic():
        """
        Initializes the logic part of server
        """
        # Note: Fingerprint.Load() is commented out in original C# code
        # Fingerprint.load()

        DataTables.load()
        Events.init()
        Sessions.init()
        Leaderboards.init()
        Battles.init()
        Matchmaking.init()
        Teams.init()

    @staticmethod
    def init_network():
        """
        Initializes the network part of server
        """
        Processor.init()
        Connections.init()

        # Set up server listener
        LogicServerListener.instance = ServerListener()

        # Initialize gateways
        config = Configuration.instance
        UDPGateway.init("0.0.0.0", config.udp_port)
        TCPGateway.init("0.0.0.0", 9339)

class ServerListener:
    """Server listener implementation"""

    def __init__(self):
        """Initialize server listener"""
        self.active = False
        self.connections = []

    def start(self):
        """Start listening for connections"""
        self.active = True
        print("Server listener started")

    def stop(self):
        """Stop listening for connections"""
        self.active = False
        print("Server listener stopped")

    def handle_connection(self, connection):
        """Handle incoming connection"""
        self.connections.append(connection)
        print(f"New connection established: {connection}")

    def remove_connection(self, connection):
        """Remove connection"""
        if connection in self.connections:
            self.connections.remove(connection)
            print(f"Connection removed: {connection}")
