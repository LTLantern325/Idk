"""
Python conversion of Blake2B tree configuration
Tree configuration for Blake2B hashing
"""

class Blake2BTreeConfig:
    """Blake2B tree configuration"""

    def __init__(self):
        """Initialize tree configuration"""
        self.intermediate_hash_size = 0
        self.leaf_size = 0
        self.fan_out = 1
        self.max_height = 1
        self.node_offset = 0
        self.node_depth = 0
        self.inner_hash_size = 0
        self.is_last_node = False

    def is_sequential(self) -> bool:
        """Check if configuration is for sequential hashing"""
        return (self.fan_out == 1 and 
                self.max_height == 1 and 
                self.leaf_size == 0 and
                self.intermediate_hash_size == 0)

    def clone(self) -> 'Blake2BTreeConfig':
        """Clone tree configuration"""
        config = Blake2BTreeConfig()
        config.intermediate_hash_size = self.intermediate_hash_size
        config.leaf_size = self.leaf_size
        config.fan_out = self.fan_out
        config.max_height = self.max_height
        config.node_offset = self.node_offset
        config.node_depth = self.node_depth
        config.inner_hash_size = self.inner_hash_size
        config.is_last_node = self.is_last_node
        return config
