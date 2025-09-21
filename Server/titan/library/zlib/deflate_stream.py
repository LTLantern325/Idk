"""
Python conversion of Deflate stream (simplified)
Raw deflate compression/decompression stream
"""

import io
import zlib
from typing import Optional
from .compression_level import CompressionLevel
from .compression_mode import CompressionMode
from .zlib_exception import ZLibException

class DeflateStream(io.IOBase):
    """Deflate stream for raw deflate compression/decompression"""

    def __init__(self, stream: io.IOBase, mode: CompressionMode,
                 level: CompressionLevel = CompressionLevel.DEFAULT, leave_open: bool = False):
        """Initialize Deflate stream"""
        super().__init__()
        self._base_stream = stream
        self._mode = mode
        self._level = level
        self._leave_open = leave_open
        self._disposed = False

        # Initialize raw deflate compressor/decompressor
        if mode == CompressionMode.COMPRESS:
            zlib_level = min(9, max(0, int(level)))
            self._compressor = zlib.compressobj(zlib_level, zlib.DEFLATED, -15)  # Raw deflate
            self._decompressor = None
        else:
            self._compressor = None
            self._decompressor = zlib.decompressobj(-15)  # Raw deflate

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

        if not self._decompressor:
            return b''

        # Read compressed data from base stream
        compressed_data = self._base_stream.read(size if size > 0 else 8192)
        if not compressed_data:
            return b''

        try:
            decompressed = self._decompressor.decompress(compressed_data)
            self._total_in += len(compressed_data)
            self._total_out += len(decompressed)
            return decompressed
        except Exception as e:
            raise ZLibException(f"Deflate decompression error: {e}")

    def write(self, data: bytes) -> int:
        """Write data to be compressed"""
        if self._disposed:
            raise ValueError("Stream is disposed")

        if self._mode != CompressionMode.COMPRESS:
            raise io.UnsupportedOperation("Stream not writable")

        if not self._compressor:
            return 0

        try:
            compressed = self._compressor.compress(data)
            if compressed:
                self._base_stream.write(compressed)
                self._total_out += len(compressed)

            self._total_in += len(data)
            return len(data)
        except Exception as e:
            raise ZLibException(f"Deflate compression error: {e}")

    def flush(self) -> None:
        """Flush stream"""
        if not self._disposed and self._mode == CompressionMode.COMPRESS and self._compressor:
            compressed = self._compressor.flush(zlib.Z_SYNC_FLUSH)
            if compressed:
                self._base_stream.write(compressed)
                self._total_out += len(compressed)

            self._base_stream.flush()

    def close(self) -> None:
        """Close stream"""
        if not self._disposed:
            try:
                if self._mode == CompressionMode.COMPRESS and self._compressor:
                    final_data = self._compressor.flush()
                    if final_data:
                        self._base_stream.write(final_data)
                        self._total_out += len(final_data)

                if not self._leave_open:
                    self._base_stream.close()
            finally:
                self._disposed = True
                self._compressor = None
                self._decompressor = None

    @staticmethod
    def compress_buffer(data: bytes, level: CompressionLevel) -> bytes:
        """Compress buffer using raw deflate"""
        zlib_level = min(9, max(0, int(level)))
        compressor = zlib.compressobj(zlib_level, zlib.DEFLATED, -15)
        compressed = compressor.compress(data) + compressor.flush()
        return compressed

    @staticmethod
    def uncompress_buffer(compressed: bytes) -> bytes:
        """Decompress raw deflate buffer"""
        decompressor = zlib.decompressobj(-15)
        return decompressor.decompress(compressed)
