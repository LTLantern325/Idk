"""
Python conversion of Supercell.Laser.Server.Settings.Fingerprint.cs
Fingerprint loading for game client validation
"""

import json
from typing import Optional

from titan.json.logic_json import LogicJSONParser, LogicJSONObject
from logger import Logger

class Fingerprint:
    """Static class for fingerprint management"""

    sha: Optional[str] = None
    version: Optional[str] = None

    @classmethod
    def load(cls) -> None:
        """Load fingerprint from JSON file"""
        try:
            with open("Assets/fingerprint.json", 'r', encoding='utf-8') as f:
                json_data = f.read()

            json_object = LogicJSONParser.parse_object(json_data)
            cls.sha = json_object.get_json_string("sha").get_string_value()
            cls.version = json_object.get_json_string("version").get_string_value()

            Logger.print_log(f"Loaded fingerprint.json v{cls.version}")

        except FileNotFoundError:
            Logger.error("fingerprint.json not found in Assets/ folder")
            cls.sha = ""
            cls.version = "unknown"
        except Exception as e:
            Logger.error(f"Error loading fingerprint.json: {e}")
            cls.sha = ""
            cls.version = "unknown"

    @classmethod
    def get_sha(cls) -> str:
        """Get fingerprint SHA"""
        return cls.sha or ""

    @classmethod
    def get_version(cls) -> str:
        """Get fingerprint version"""
        return cls.version or "unknown"

    @classmethod
    def is_loaded(cls) -> bool:
        """Check if fingerprint is loaded"""
        return cls.sha is not None and cls.version is not None
