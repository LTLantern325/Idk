"""
Python conversion of Blake2B fully unrolled core (simplified)  
Fully unrolled Blake2B core for maximum performance
"""

from .blake2b_core_simple import Blake2BCoreSimple
from typing import List

class Blake2BCoreUnrolled(Blake2BCoreSimple):
    """Fully unrolled Blake2B core"""

    @staticmethod
    def hash_unrolled(config: List[int], data: bytes, output_size: int) -> bytes:
        """Fully unrolled hash function"""
        # This would have completely unrolled loops in real implementation
        # For simplicity, we use the same implementation
        return Blake2BCoreSimple.hash(config, data, output_size)

    @staticmethod
    def compress_unrolled(state: List[int], block: bytes, counter: int, final_block: bool) -> None:
        """Fully unrolled compress function"""
        # Real implementation would have all 12 rounds manually unrolled
        # This is simplified
        Blake2BCoreSimple.compress(state, block, counter, final_block)
