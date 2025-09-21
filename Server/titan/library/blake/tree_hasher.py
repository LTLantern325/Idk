"""
Python conversion of tree hasher (simplified)
Generic tree hasher interface
"""

from abc import ABC, abstractmethod
from typing import List, Optional

class TreeHasher(ABC):
    """Base class for tree hashers"""

    def __init__(self):
        """Initialize tree hasher"""
        self.leaf_size = 0
        self.fan_out = 1
        self.max_height = 1
        self.inner_hash_size = 0

    @abstractmethod
    def initialize(self) -> None:
        """Initialize hasher"""
        pass

    @abstractmethod
    def update(self, data: bytes) -> None:
        """Update with data"""
        pass

    @abstractmethod
    def finish(self) -> bytes:
        """Finish and get hash"""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset hasher"""
        pass

    def compute_hash(self, data: bytes) -> bytes:
        """Compute hash of data"""
        self.reset()
        self.initialize()
        self.update(data)
        return self.finish()

class Blake2BTreeHasher(TreeHasher):
    """Blake2B tree hasher implementation"""

    def __init__(self, hash_size: int = 64, key: Optional[bytes] = None):
        """Initialize Blake2B tree hasher"""
        super().__init__()
        self.hash_size = hash_size
        self.key = key
        self.current_data = bytearray()
        self.initialized = False

    def initialize(self) -> None:
        """Initialize hasher"""
        self.current_data = bytearray()
        self.initialized = True

    def update(self, data: bytes) -> None:
        """Update with data"""
        if not self.initialized:
            self.initialize()
        self.current_data.extend(data)

    def finish(self) -> bytes:
        """Finish and get hash"""
        if not self.initialized:
            self.initialize()

        # Simplified tree hashing (sequential in this case)
        from .blake2b_hasher import Blake2BHasher
        hasher = Blake2BHasher(self.hash_size, self.key)
        hasher.update(bytes(self.current_data))
        return hasher.finish()

    def reset(self) -> None:
        """Reset hasher"""
        self.current_data = bytearray()
        self.initialized = False
