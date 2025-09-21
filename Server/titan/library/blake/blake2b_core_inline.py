"""
Python conversion of Blake2B inline core (simplified)
Inline optimized Blake2B core
"""

from .blake2b_core_simple import Blake2BCoreSimple
from typing import List

class Blake2BCoreInline(Blake2BCoreSimple):
    """Inline optimized Blake2B core"""

    @staticmethod
    def hash_inline(config: List[int], data: bytes, output_size: int) -> bytes:
        """Inline hash function with optimizations"""
        # This is essentially the same as simple for our purposes
        # Real implementation would have inline optimizations
        return Blake2BCoreSimple.hash(config, data, output_size)

    @staticmethod
    def compress_inline(state: List[int], block: bytes, counter: int, final_block: bool) -> None:
        """Inline compress function"""
        # Simplified inline compression
        # Real implementation would have manual loop unrolling
        Blake2BCoreSimple.compress(state, block, counter, final_block)
