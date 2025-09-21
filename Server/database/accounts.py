"""
Python conversion of Supercell.Laser.Server.Database.Accounts.cs
Database operations for user accounts
"""

import json
import mysql.connector
from mysql.connector import Error
from typing import List, Optional
import random
import string
from datetime import datetime

from logic.home.structures import Hero
from database.cache.account_cache import AccountCache
from database.models.account import Account
from settings.configuration import Configuration
from utils.helpers import Helpers

class Accounts:
    """Static class for account database operations"""

    _avatar_id_counter: int = 0
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
        Accounts._connection_string = json.dumps(connection_config)

        # Initialize JSON serialization settings
        # Python's json module handles null/None values differently than C#

        # Initialize account cache
        AccountCache.init()

        # Get the maximum avatar ID from database
        Accounts._avatar_id_counter = Accounts.get_max_avatar_id()

    @staticmethod
    def get_max_avatar_id() -> int:
        """Get the maximum avatar ID from database"""
        try:
            config = json.loads(Accounts._connection_string)
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            cursor.execute("SELECT COALESCE(MAX(Id), 0) FROM accounts")
            result = cursor.fetchone()

            cursor.close()
            connection.close()

            return int(result[0]) if result else 0
        except Error as e:
            print(f"Database error in get_max_avatar_id: {e}")
            return 0

    @staticmethod
    def create() -> Account:
        """Create a new account"""
        account = Account()
        Accounts._avatar_id_counter += 1
        account.account_id = Accounts._avatar_id_counter
        account.pass_token = Helpers.random_string(40)

        # Set up avatar
        account.avatar.account_id = account.account_id
        account.avatar.pass_token = account.pass_token

        # Set up home
        account.home.home_id = account.account_id

        # Add default hero (Shelly - ID 16000000)
        hero = Hero(16000000)
        account.avatar.heroes.append(hero)

        # Serialize account to JSON
        json_data = json.dumps(account.to_dict(), ensure_ascii=False, separators=(',', ':'))

        try:
            # Save to database
            config = json.loads(Accounts._connection_string)
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            query = "INSERT INTO accounts (`Id`, `Trophies`, `Data`) VALUES (%s, %s, %s)"
            cursor.execute(query, (account.account_id, account.avatar.trophies, json_data))

            cursor.close()
            connection.close()

            # Cache the account
            AccountCache.cache(account)

            return account

        except Error as e:
            print(f"Database error in create: {e}")
            return None

    @staticmethod
    def save(account: Account) -> None:
        """Save account to database"""
        if not account:
            return

        json_data = json.dumps(account.to_dict(), ensure_ascii=False, separators=(',', ':'))

        try:
            config = json.loads(Accounts._connection_string)
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            query = "UPDATE accounts SET `Trophies`=%s, `Data`=%s WHERE Id = %s"
            cursor.execute(query, (account.avatar.trophies, json_data, account.account_id))

            cursor.close()
            connection.close()

        except Error as e:
            print(f"Database error in save: {e}")

    @staticmethod
    def load(account_id: int) -> Optional[Account]:
        """Load account from database"""
        # Check cache first
        if AccountCache.is_account_cached(account_id):
            return AccountCache.get_account(account_id)

        try:
            config = json.loads(Accounts._connection_string)
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM accounts WHERE Id = %s", (account_id,))
            result = cursor.fetchone()

            if result:
                # Assuming the Data column is at index 2 (Id, Trophies, Data)
                account_data = json.loads(result[2])
                account = Account.from_dict(account_data)

                # Cache the account
                AccountCache.cache(account)

                cursor.close()
                connection.close()
                return account

            cursor.close()
            connection.close()
            return None

        except Error as e:
            print(f"Database error in load: {e}")
            return None

    @staticmethod
    def get_ranking_list() -> List[Account]:
        """Get global ranking list"""
        account_list = []

        try:
            config = json.loads(Accounts._connection_string)
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            # Original C# had ORDER BY Trophies DESC commented out
            cursor.execute("SELECT * FROM accounts LIMIT 200")
            results = cursor.fetchall()

            for result in results:
                try:
                    account_data = json.loads(result[2])  # Data column
                    account = Account.from_dict(account_data)
                    account_list.append(account)
                except json.JSONDecodeError:
                    continue

            cursor.close()
            connection.close()

        except Error as e:
            print(f"Database error in get_ranking_list: {e}")

        return account_list

    @staticmethod
    def get_brawler_ranking_list(hero_data_id: int) -> List[Account]:
        """Get brawler-specific ranking list"""
        account_list = []

        try:
            config = json.loads(Accounts._connection_string)
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM accounts WHERE Trophies >= 1000")
            results = cursor.fetchall()

            for result in results:
                try:
                    account_data = json.loads(result[2])  # Data column
                    account = Account.from_dict(account_data)

                    # Check if account has the specified hero
                    if account.avatar.has_hero(hero_data_id):
                        account_list.append(account)

                except json.JSONDecodeError:
                    continue

            cursor.close()
            connection.close()

            # Sort by brawler trophies (descending)
            account_list.sort(
                key=lambda a: a.avatar.get_hero(hero_data_id).trophies if a.avatar.get_hero(hero_data_id) else 0,
                reverse=True
            )

        except Error as e:
            print(f"Database error in get_brawler_ranking_list: {e}")

        return account_list
