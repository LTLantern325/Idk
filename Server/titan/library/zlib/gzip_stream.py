"""
Python conversion of GZip stream (simplified)
GZip compression/decompression stream
"""

import io
import gzip
from typing import Optional
from .compression_level import CompressionLevel
from .compression_mode import CompressionMode
from .zlib_exception import ZLibException

class GZipStream(io.IOBase):
    """GZip stream for compression/decompression"""

    def __init__(self, stream: io.IOBase, mode: CompressionMode, 
                 level: CompressionLevel = CompressionLevel.DEFAULT, leave_open: bool = False):
        """Initialize GZip stream"""
        super().__init__()
        self._base_stream = stream
        self._mode = mode
        self._level = level
        self._leave_open = leave_open
        self._disposed = False

        # Initialize gzip compressor/decompressor
        if mode == CompressionMode.COMPRESS:
            compresslevel = min(9, max(1, int(level)))
            self._gzip_file = gzip.GzipFile(fileobj=stream, mode='wb', compresslevel=compresslevel)
        else:
            self._gzip_file = gzip.GzipFile(fileobj=stream, mode='rb')

        self._total_in = 0
        self._total_out = 0

    @property
    def total_in(self) -> int:
        """Get total bytes in"""
        return self._total_in

    @property
    def total_out(self) -> int:
        """Get total bytes out"""
        return self._total_out

    @property
    def readable(self) -> bool:
        """Check if readable"""
        return not self._disposed and self._mode == CompressionMode.DECOMPRESS

    @property
    def writable(self) -> bool:
        """Check if writable"""
        return not self._disposed and self._mode == CompressionMode.COMPRESS

    @property
    def seekable(self) -> bool:
        """Check if seekable"""
        return False

    def read(self, size: int = -1) -> bytes:
        """Read decompressed data"""
        if self._disposed:
            raise ValueError("Stream is disposed")

        if self._mode != CompressionMode.DECOMPRESS:
            raise io.UnsupportedOperation("Stream not readable")

        try:
            data = self._gzip_file.read(size)
            self._total_out += len(data) if data else 0
            return data if data else b''
        except Exception as e:
            raise ZLibException(f"GZip decompression error: {e}")

    def write(self, data: bytes) -> int:
        """Write data to be compressed"""
        if self._disposed:
            raise ValueError("Stream is disposed")

        if self._mode != CompressionMode.COMPRESS:
            raise io.UnsupportedOperation("Stream not writable")

        try:
            self._gzip_file.write(data)
            self._total_in += len(data)
            return len(data)
        except Exception as e:
            raise ZLibException(f"GZip compression error: {e}")

    def flush(self) -> None:
        """Flush stream"""
        if not self._disposed:
            self._gzip_file.flush()

    def close(self) -> None:
        """Close stream"""
        if not self._disposed:
            try:
                self._gzip_file.close()
                if not self._leave_open:
                    self._base_stream.close()
            finally:
                self._disposed = True

    # Static utility methods
    @staticmethod
    def compress_string(text: str) -> bytes:
        """Compress string to gzip bytes"""
        return gzip.compress(text.encode('utf-8'))

    @staticmethod
    def compress_buffer(data: bytes, level: CompressionLevel) -> bytes:
        """Compress buffer to gzip"""
        compresslevel = min(9, max(1, int(level)))
        return gzip.compress(data, compresslevel)

    @staticmethod
    def uncompress_string(compressed: bytes) -> str:
        """Decompress gzip bytes to string"""
        return gzip.decompress(compressed).decode('utf-8')

    @staticmethod
    def uncompress_buffer(compressed: bytes) -> bytes:
        """Decompress gzip buffer"""
        return gzip.decompress(compressed)
