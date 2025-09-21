"""
Python conversion of ZLib internal constants
Internal constants used by ZLib algorithms
"""

class InternalConstants:
    """Internal ZLib constants"""

    # Maximum window size
    MAX_WSIZE = 32768

    # Window size mask
    WMASK = MAX_WSIZE - 1

    # Hash bits
    HASH_BITS = 15
    HASH_SIZE = 1 << HASH_BITS
    HASH_MASK = HASH_SIZE - 1

    # Match length constants
    MIN_MATCH = 3
    MAX_MATCH = 258

    # Lookahead constants  
    MIN_LOOKAHEAD = MAX_MATCH + MIN_MATCH + 1

    # Compression method constants
    Z_DEFLATED = 8

    # Memory levels
    DEF_MEM_LEVEL = 8

    # String lengths
    LENGTH_CODES = 29
    LITERALS = 256
    L_CODES = LITERALS + 1 + LENGTH_CODES
    D_CODES = 30
    BL_CODES = 19
    HEAP_SIZE = 2 * L_CODES + 1
    MAX_BITS = 15

    # Bit length codes
    BIT_LENGTH_ORDER = [16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15]

    # Configuration table
    CONFIG_TABLE = [
        # good, lazy, nice, chain
        (0, 0, 0, 0),      # store only
        (4, 4, 8, 4),      # max speed, no lazy matches
        (4, 5, 16, 8),     # 
        (4, 6, 32, 32),    # 
        (4, 4, 16, 16),    # lazy matches
        (8, 16, 32, 32),   # 
        (8, 16, 128, 128), # 
        (8, 32, 128, 256), # 
        (32, 128, 258, 1024), # max compression
        (32, 258, 258, 4096)  # max compression
    ]
