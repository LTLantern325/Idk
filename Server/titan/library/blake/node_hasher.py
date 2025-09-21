"""
Python conversion of generic node hasher
Base node hasher interface
"""

from abc import ABC, abstractmethod
from typing import Optional

class NodeHasher(ABC):
    """Base class for node hashers"""

    def __init__(self):
        """Initialize node hasher"""
        self.node_depth = 0
        self.node_offset = 0
        self.is_last_node = False

    @abstractmethod
    def initialize(self, depth: int, offset: int) -> None:
        """Initialize node at depth and offset"""
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

    def set_last_node(self, is_last: bool) -> None:
        """Set if this is the last node"""
        self.is_last_node = is_last

class SimpleNodeHasher(NodeHasher):
    """Simple implementation of node hasher"""

    def __init__(self, hash_size: int = 64):
        """Initialize simple node hasher"""
        super().__init__()
        self.hash_size = hash_size
        self.data = bytearray()
        self.initialized = False

    def initialize(self, depth: int, offset: int) -> None:
        """Initialize node"""
        self.node_depth = depth
        self.node_offset = offset
        self.data = bytearray()
        self.initialized = True

    def update(self, data: bytes) -> None:
        """Update with data"""
        if not self.initialized:
            self.initialize(0, 0)
        self.data.extend(data)

    def finish(self) -> bytes:
        """Finish and get hash"""
        if not self.initialized:
            self.initialize(0, 0)

        # Simple hash using Blake2B
        import hashlib
        hasher = hashlib.blake2b(digest_size=self.hash_size)
        hasher.update(bytes(self.data))
        return hasher.digest()

    def reset(self) -> None:
        """Reset hasher"""
        self.data = bytearray()
        self.initialized = False
