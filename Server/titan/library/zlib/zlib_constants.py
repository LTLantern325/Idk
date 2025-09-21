"""
Python conversion of ZLib constants
ZLib algorithm constants and return codes
"""

class ZLibConstants:
    """ZLib constants"""

    # Return codes
    Z_OK = 0
    Z_STREAM_END = 1
    Z_NEED_DICT = 2
    Z_ERRNO = -1
    Z_STREAM_ERROR = -2
    Z_DATA_ERROR = -3
    Z_MEM_ERROR = -4
    Z_BUF_ERROR = -5
    Z_VERSION_ERROR = -6

    # Compression levels
    Z_NO_COMPRESSION = 0
    Z_BEST_SPEED = 1
    Z_BEST_COMPRESSION = 9
    Z_DEFAULT_COMPRESSION = -1

    # Compression strategies
    Z_FILTERED = 1
    Z_HUFFMAN_ONLY = 2
    Z_RLE = 3
    Z_FIXED = 4
    Z_DEFAULT_STRATEGY = 0

    # Data types
    Z_BINARY = 0
    Z_TEXT = 1
    Z_ASCII = Z_TEXT
    Z_UNKNOWN = 2

    # Flush values
    Z_NO_FLUSH = 0
    Z_PARTIAL_FLUSH = 1
    Z_SYNC_FLUSH = 2
    Z_FULL_FLUSH = 3
    Z_FINISH = 4
    Z_BLOCK = 5
    Z_TREES = 6

    # Window bits
    WINDOW_BITS_MAX = 15
    WINDOW_BITS_DEFAULT = WINDOW_BITS_MAX

    # Memory levels
    MEM_LEVEL_MAX = 9
    MEM_LEVEL_DEFAULT = 8
    MEM_LEVEL_MIN = 1

    # Buffer sizes
    WORKING_BUFFER_SIZE_DEFAULT = 8192
    WORKING_BUFFER_SIZE_MIN = 1024

    @staticmethod
    def get_error_message(code: int) -> str:
        """Get error message for return code"""
        messages = {
            ZLibConstants.Z_OK: "OK",
            ZLibConstants.Z_STREAM_END: "Stream end",
            ZLibConstants.Z_NEED_DICT: "Need dictionary",
            ZLibConstants.Z_ERRNO: "File error",
            ZLibConstants.Z_STREAM_ERROR: "Stream error",
            ZLibConstants.Z_DATA_ERROR: "Data error",
            ZLibConstants.Z_MEM_ERROR: "Memory error",
            ZLibConstants.Z_BUF_ERROR: "Buffer error",
            ZLibConstants.Z_VERSION_ERROR: "Version error"
        }
        return messages.get(code, f"Unknown error ({code})")
