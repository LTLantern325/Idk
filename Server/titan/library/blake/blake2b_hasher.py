"""
Python conversion of Supercell.Laser.Titan.Library.Blake.Blake2BHasher.cs (simplified)
Blake2B hashing implementation
"""

import hashlib
from typing import Optional

class Blake2BHasher:
    """Blake2B hasher implementation"""

    def __init__(self, hash_size: int = 64, key: Optional[bytes] = None):
        """Initialize Blake2B hasher"""
        self.hash_size = hash_size
        self.key = key
        self.hasher = hashlib.blake2b(digest_size=hash_size, key=key)

    def update(self, data: bytes) -> None:
        """Update hash with data"""
        self.hasher.update(data)

    def finish(self) -> bytes:
        """Finalize and return hash"""
        return self.hasher.digest()

    def finalize(self, output: bytearray) -> None:
        """Finalize hash into output buffer"""
        digest = self.hasher.digest()
        output[:len(digest)] = digest

    def reset(self) -> None:
        """Reset hasher state"""
        self.hasher = hashlib.blake2b(digest_size=self.hash_size, key=self.key)

    @staticmethod
    def compute_hash(data: bytes, hash_size: int = 64, key: Optional[bytes] = None) -> bytes:
        """Compute Blake2B hash of data"""
        hasher = Blake2BHasher(hash_size, key)
        hasher.update(data)
        return hasher.finish()

    def get_hash_size(self) -> int:
        """Get hash output size"""
        return self.hash_size

class Blake2BConfig:
    """Blake2B configuration"""

    def __init__(self):
        """Initialize config"""
        self.hash_size = 64
        self.key = None
        self.salt = None
        self.personalization = None

    def set_hash_size(self, size: int) -> None:
        """Set hash output size"""
        if 1 <= size <= 64:
            self.hash_size = size

    def set_key(self, key: bytes) -> None:
        """Set key for keyed hashing"""
        if len(key) <= 64:
            self.key = key

    def create_hasher(self) -> Blake2BHasher:
        """Create hasher with this config"""
        return Blake2BHasher(self.hash_size, self.key)
