"""
Python conversion of Supercell.Laser.Server.Networking.Security.PepperKey.cs
Pepper encryption key management
"""

import secrets
from typing import Optional

class PepperKey:
    """Static class for Pepper encryption key management"""

    _private_key: Optional[bytes] = None
    _public_key: Optional[bytes] = None
    _initialized: bool = False

    # Default server keys (same as in Messaging.cs)
    DEFAULT_PRIVATE_KEY = bytes([
        158, 217, 110, 5, 87, 249, 222, 234, 204, 121, 177, 228, 
        59, 79, 93, 217, 25, 33, 113, 185, 119, 171, 205, 246, 
        11, 185, 185, 22, 140, 152, 107, 20
    ])

    @classmethod
    def init(cls) -> None:
        """Initialize pepper keys"""
        if not cls._initialized:
            cls._private_key = cls.DEFAULT_PRIVATE_KEY
            cls._public_key = cls._generate_public_key(cls._private_key)
            cls._initialized = True

    @classmethod
    def _generate_public_key(cls, private_key: bytes) -> bytes:
        """Generate public key from private key"""
        # In real implementation, this would use proper crypto
        # For now, return a placeholder
        return secrets.token_bytes(32)

    @classmethod
    def get_private_key(cls) -> bytes:
        """Get private key"""
        if not cls._initialized:
            cls.init()
        return cls._private_key

    @classmethod
    def get_public_key(cls) -> bytes:
        """Get public key"""
        if not cls._initialized:
            cls.init()
        return cls._public_key

    @classmethod
    def generate_new_keys(cls) -> None:
        """Generate new random keys"""
        cls._private_key = secrets.token_bytes(32)
        cls._public_key = cls._generate_public_key(cls._private_key)
        cls._initialized = True

    @classmethod
    def set_keys(cls, private_key: bytes, public_key: bytes = None) -> None:
        """Set custom keys"""
        cls._private_key = private_key
        if public_key:
            cls._public_key = public_key
        else:
            cls._public_key = cls._generate_public_key(private_key)
        cls._initialized = True
