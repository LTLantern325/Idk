"""
Python conversion of Blake2B node hasher (simplified)
Node hasher for Blake2B tree mode
"""

from typing import Optional
from .blake2b_config import Blake2BConfig
from .blake2b_tree_config import Blake2BTreeConfig
from .blake2b_hasher import Blake2BHasher

class Blake2BNodeHasher:
    """Blake2B node hasher for tree mode"""

    def __init__(self, config: Blake2BConfig, tree_config: Blake2BTreeConfig):
        """Initialize node hasher"""
        self.config = config
        self.tree_config = tree_config
        self.hasher = Blake2BHasher(config.output_size, config.key)
        self.initialized = False

    def initialize(self) -> None:
        """Initialize node hasher"""
        if not self.initialized:
            self.hasher.reset()
            self.initialized = True

    def update(self, data: bytes) -> None:
        """Update with data"""
        if not self.initialized:
            self.initialize()
        self.hasher.update(data)

    def finish(self) -> bytes:
        """Finish and get hash"""
        if not self.initialized:
            self.initialize()
        return self.hasher.finish()

    def reset(self) -> None:
        """Reset hasher"""
        self.initialized = False
        self.hasher.reset()

    def compute_hash(self, data: bytes) -> bytes:
        """Compute hash of data"""
        self.reset()
        self.update(data)
        return self.finish()
