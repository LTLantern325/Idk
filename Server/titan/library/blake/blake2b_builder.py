"""
Python conversion of Supercell.Laser.Titan.Library.Blake.Blake2BBuilder.cs
Blake2B configuration builder
"""

from typing import Optional
from .blake2b_config import Blake2BConfig
from .blake2b_tree_config import Blake2BTreeConfig

class Blake2BBuilder:
    """Static Blake2B builder class"""

    # Sequential tree configuration
    _SEQUENTIAL_TREE_CONFIG = None

    @classmethod
    def get_sequential_tree_config(cls) -> Blake2BTreeConfig:
        """Get sequential tree configuration"""
        if cls._SEQUENTIAL_TREE_CONFIG is None:
            cls._SEQUENTIAL_TREE_CONFIG = Blake2BTreeConfig()
            cls._SEQUENTIAL_TREE_CONFIG.intermediate_hash_size = 0
            cls._SEQUENTIAL_TREE_CONFIG.leaf_size = 0
            cls._SEQUENTIAL_TREE_CONFIG.fan_out = 1
            cls._SEQUENTIAL_TREE_CONFIG.max_height = 1
        return cls._SEQUENTIAL_TREE_CONFIG

    @staticmethod
    def config_b(config: Blake2BConfig, tree_config: Optional[Blake2BTreeConfig] = None) -> list:
        """Build Blake2B configuration"""
        is_sequential = tree_config is None
        if is_sequential:
            tree_config = Blake2BBuilder.get_sequential_tree_config()

        # Initialize raw config array (8 64-bit values)
        raw_config = [0] * 8

        # Set output size
        raw_config[0] |= config.output_size

        # Set key length if key exists
        if config.key is not None:
            raw_config[0] |= len(config.key) << 8

        # Set tree parameters
        raw_config[0] |= tree_config.fan_out << 16
        raw_config[0] |= tree_config.max_height << 24
        raw_config[0] |= tree_config.leaf_size << 32
        raw_config[2] |= tree_config.intermediate_hash_size << 8

        # Set salt if exists
        if config.salt is not None and len(config.salt) >= 16:
            raw_config[4] = Blake2BBuilder._bytes_to_uint64(config.salt, 0)
            raw_config[5] = Blake2BBuilder._bytes_to_uint64(config.salt, 8)

        # Set personalization if exists
        if config.personalization is not None and len(config.personalization) >= 16:
            raw_config[6] = Blake2BBuilder._bytes_to_uint64(config.personalization, 0)
            raw_config[7] = Blake2BBuilder._bytes_to_uint64(config.personalization, 8)

        return raw_config

    @staticmethod
    def config_b_set_node(raw_config: list, depth: int, node_offset: int) -> None:
        """Set node configuration"""
        raw_config[1] = node_offset
        raw_config[2] = (raw_config[2] & ~0xFF) | depth

    @staticmethod
    def _bytes_to_uint64(data: bytes, offset: int) -> int:
        """Convert bytes to uint64 (little endian)"""
        if offset + 8 > len(data):
            return 0

        result = 0
        for i in range(8):
            result |= data[offset + i] << (i * 8)
        return result
