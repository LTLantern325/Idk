"""
Python conversion of Blake2B base functionality (simplified)
Base class for Blake2B implementations
"""

from abc import ABC, abstractmethod
from typing import Optional

class Blake2BBase(ABC):
    """Base class for Blake2B implementations"""

    def __init__(self):
        """Initialize Blake2B base"""
        self.digest_size = 64
        self.key_size = 0
        self.initialized = False

    @abstractmethod
    def initialize(self, config) -> None:
        """Initialize with configuration"""
        pass

    @abstractmethod
    def update(self, data: bytes, offset: int, count: int) -> None:
        """Update with data"""
        pass

    @abstractmethod
    def final(self, output: bytearray, offset: int) -> None:
        """Finalize hash"""
        pass

    def hash_core(self, data: bytes, offset: int, count: int) -> None:
        """Hash core implementation"""
        self.update(data, offset, count)

    def hash_final(self) -> bytes:
        """Get final hash"""
        output = bytearray(self.digest_size)
        self.final(output, 0)
        return bytes(output)

    def compute_hash(self, data: bytes) -> bytes:
        """Compute hash of data"""
        if not self.initialized:
            raise RuntimeError("Hasher not initialized")

        self.update(data, 0, len(data))
        return self.hash_final()

class Hasher(ABC):
    """Generic hasher interface"""

    @abstractmethod
    def update(self, data: bytes) -> None:
        """Update hash with data"""
        pass

    @abstractmethod
    def finish(self) -> bytes:
        """Get final hash"""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset hasher"""
        pass
