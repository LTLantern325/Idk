"""
Python conversion of Supercell.Laser.Server.Database.Alliances.cs
Database operations for alliances/clubs
"""

import json
import mysql.connector
from mysql.connector import Error
from typing import List, Optional
import random

from logic.club.alliance import Alliance
from database.cache.alliance_cache import AllianceCache
from settings.configuration import Configuration

class Alliances:
    """Static class for alliance database operations"""

    _alliance_id_counter: int = 0
    _connection_string: str = ""

    @staticmethod
    def init(user: str, password: str) -> None:
        """Initialize database connection and settings"""
        config = Configuration.instance

        # Build connection configuration
        connection_config = {
            'host': '127.0.0.1',
            'user': user,
            'password': password,
            'database': config.database_name,
            'charset': 'utf8mb4',
            'autocommit': True,
            'ssl_disabled': True
        }

        # Store connection string for later use
        Alliances._connection_string = json.dumps(connection_config)

        # Initialize JSON serialization settings
        # Python's json module handles null/None values differently than C#

        # Initialize alliance cache
        AllianceCache.init()

        # Get the maximum alliance ID from database
        Alliances._alliance_id_counter = Alliances.get_max_alliance_id()

    @staticmethod
    def get_max_alliance_id() -> int:
        """Get the maximum alliance ID from database"""
        try:
            config = json.loads(Alliances._connection_string)
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            cursor.execute("SELECT COALESCE(MAX(Id), 0) FROM alliances")
            result = cursor.fetchone()

            cursor.close()
            connection.close()

            return int(result[0]) if result else 0
        except Error as e:
            print(f"Database error in get_max_alliance_id: {e}")
            return 0

    @staticmethod
    def create(alliance: Alliance) -> None:
        """Create a new alliance"""
        if not alliance:
            return

        Alliances._alliance_id_counter += 1
        alliance.id = Alliances._alliance_id_counter

        # Serialize alliance to JSON
        json_data = json.dumps(alliance.to_dict(), ensure_ascii=False, separators=(',', ':'))

        try:
            config = json.loads(Alliances._connection_string)
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            query = "INSERT INTO alliances (`Id`, `Name`, `Trophies`, `Data`) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (alliance.id, alliance.name, alliance.trophies, json_data))

            cursor.close()
            connection.close()

            # Cache the alliance
            AllianceCache.cache(alliance)

        except Error as e:
            print(f"Database error in create: {e}")

    @staticmethod
    def save(alliance: Alliance) -> None:
        """Save alliance to database"""
        if not alliance:
            return

        json_data = json.dumps(alliance.to_dict(), ensure_ascii=False, separators=(',', ':'))

        try:
            config = json.loads(Alliances._connection_string)
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            query = "UPDATE alliances SET `Trophies`=%s, `Data`=%s WHERE Id = %s"
            cursor.execute(query, (alliance.trophies, json_data, alliance.id))

            cursor.close()
            connection.close()

        except Error as e:
            print(f"Database error in save: {e}")

    @staticmethod
    def load(alliance_id: int) -> Optional[Alliance]:
        """Load alliance from database"""
        # Check cache first
        if AllianceCache.is_alliance_cached(alliance_id):
            return AllianceCache.get_alliance(alliance_id)

        try:
            config = json.loads(Alliances._connection_string)
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM alliances WHERE Id = %s", (alliance_id,))
            result = cursor.fetchone()

            if result:
                # Assuming the Data column is at index 3 (Id, Name, Trophies, Data)
                alliance_data = json.loads(result[3])
                alliance = Alliance.from_dict(alliance_data)

                # Cache the alliance
                AllianceCache.cache(alliance)

                cursor.close()
                connection.close()
                return alliance

            cursor.close()
            connection.close()
            return None

        except Error as e:
            print(f"Database error in load: {e}")
            return None

    @staticmethod
    def get_ranking_list() -> List[Alliance]:
        """Get global alliance ranking list"""
        alliance_list = []

        try:
            config = json.loads(Alliances._connection_string)
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM alliances ORDER BY `Trophies` DESC LIMIT 200")
            results = cursor.fetchall()

            for result in results:
                try:
                    alliance_data = json.loads(result[3])  # Data column
                    alliance = Alliance.from_dict(alliance_data)
                    alliance_list.append(alliance)
                except json.JSONDecodeError:
                    continue

            cursor.close()
            connection.close()

        except Error as e:
            print(f"Database error in get_ranking_list: {e}")

        return alliance_list

    @staticmethod
    def get_random_alliances(max_count: int) -> List[Alliance]:
        """Get random alliances up to max_count"""
        count = min(max_count, Alliances._alliance_id_counter)
        alliance_list = []

        try:
            rand = random.Random()
            for i in range(count):
                # Generate random ID between 1 and alliance_id_counter
                random_id = rand.randint(1, Alliances._alliance_id_counter)
                alliance = Alliances.load(random_id)
                if alliance:
                    alliance_list.append(alliance)

        except Exception as e:
            print(f"Error in get_random_alliances: {e}")

        return alliance_list
