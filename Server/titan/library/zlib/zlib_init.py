"""
ZLib compression library
"""

from .zlib_stream import ZLibStream
from .gzip_stream import GZipStream
from .deflate_stream import DeflateStream
from .compression_level import CompressionLevel
from .compression_mode import CompressionMode

__all__ = ['ZLibStream', 'GZipStream', 'DeflateStream', 'CompressionLevel', 'CompressionMode']
