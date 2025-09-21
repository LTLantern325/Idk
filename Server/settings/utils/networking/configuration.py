"""
Python conversion for Configuration settings
Basic configuration class for server settings
"""

import json
from typing import Optional

class Configuration:
    """Configuration class for server settings"""

    instance: Optional['Configuration'] = None

    def __init__(self):
        """Initialize configuration"""
        self.database_username: str = ""
        self.database_password: str = ""
        self.database_name: str = ""
        self.udp_port: int = 9339
        self.tcp_port: int = 9339
        self.server_host: str = "0.0.0.0"

    @classmethod
    def load_from_file(cls, filename: str) -> 'Configuration':
        """Load configuration from JSON file"""
        config = cls()

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            config.database_username = data.get("database_username", "")
            config.database_password = data.get("database_password", "")  
            config.database_name = data.get("database_name", "")
            config.udp_port = data.get("udp_port", 9339)
            config.tcp_port = data.get("tcp_port", 9339)
            config.server_host = data.get("server_host", "0.0.0.0")

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load configuration from {filename}: {e}")
            print("Using default configuration values")

        return config

    def save_to_file(self, filename: str) -> None:
        """Save configuration to JSON file"""
        data = {
            "database_username": self.database_username,
            "database_password": self.database_password,
            "database_name": self.database_name,
            "udp_port": self.udp_port,
            "tcp_port": self.tcp_port,
            "server_host": self.server_host
        }

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving configuration to {filename}: {e}")
