"""
Python conversion of Supercell.Laser.Server.Settings.Configuration.cs
Server configuration management
"""

import json
from typing import Optional
from dataclasses import dataclass

@dataclass
class Configuration:
    """Server configuration class"""

    udp_host: str = "0.0.0.0"
    udp_port: int = 9339
    database_username: str = ""
    database_password: str = ""
    database_name: str = ""
    update_sha: str = ""
    content_url: str = ""
    fingerprint: str = ""

    # Singleton instance
    instance: Optional['Configuration'] = None

    @classmethod
    def load_from_file(cls, filename: str) -> 'Configuration':
        """Load configuration from JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            config = cls()
            config.udp_host = data.get("udp_host", "0.0.0.0")
            config.udp_port = data.get("udp_port", 9339)
            config.database_username = data.get("database_username", "")
            config.database_password = data.get("database_password", "")
            config.database_name = data.get("database_name", "")
            config.update_sha = data.get("update_sha", "")
            config.content_url = data.get("ContentUrl", "")
            config.fingerprint = data.get("Fingerprint", "")

            return config

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading configuration from {filename}: {e}")
            return cls()  # Return default configuration

    def save_to_file(self, filename: str) -> None:
        """Save configuration to JSON file"""
        data = {
            "udp_host": self.udp_host,
            "udp_port": self.udp_port,
            "database_username": self.database_username,
            "database_password": self.database_password,
            "database_name": self.database_name,
            "update_sha": self.update_sha,
            "ContentUrl": self.content_url,
            "Fingerprint": self.fingerprint
        }

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving configuration to {filename}: {e}")
