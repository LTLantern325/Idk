"""
Python conversion of Supercell.Laser.Titan.Library.ZLib.ZLibStream.cs (simplified)
ZLib stream wrapper for compression/decompression
"""

import io
import zlib
from typing import Optional
from .compression_level import CompressionLevel
from .compression_mode import CompressionMode
from .flush_type import FlushType
from .zlib_exception import ZLibException

class ZLibStream(io.IOBase):
    """ZLib stream for compression/decompression"""

    def __init__(self, stream: io.IOBase, mode: CompressionMode, 
                 level: CompressionLevel = CompressionLevel.DEFAULT, leave_open: bool = False):
        """Initialize ZLib stream"""
        super().__init__()
        self._base_stream = stream
        self._mode = mode
        self._level = level
        self._leave_open = leave_open
        self._disposed = False

        # Initialize compressor/decompressor
        if mode == CompressionMode.COMPRESS:
            zlib_level = min(9, max(0, int(level)))
            self._compressor = zlib.compressobj(zlib_level)
            self._decompressor = None
        else:
            self._compressor = None
            self._decompressor = zlib.decompressobj()

        # Buffer and statistics
        self._buffer_size = 8192
        self._total_in = 0
        self._total_out = 0
        self._flush_mode = FlushType.NONE

    @property
    def flush_mode(self) -> FlushType:
        """Get flush mode"""
        return self._flush_mode

    @flush_mode.setter
    def flush_mode(self, value: FlushType) -> None:
        """Set flush mode"""
        if self._disposed:
            raise ValueError("Stream is disposed")
        self._flush_mode = value

    @property
    def buffer_size(self) -> int:
        """Get buffer size"""
        return self._buffer_size

    @buffer_size.setter  
    def buffer_size(self, value: int) -> None:
        """Set buffer size"""
        if self._disposed:
            raise ValueError("Stream is disposed")
        if value < 1024:
            raise ValueError("Buffer size too small")
        self._buffer_size = value

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
        """Check if stream is readable"""
        return not self._disposed and self._mode == CompressionMode.DECOMPRESS

    @property
    def writable(self) -> bool:
        """Check if stream is writable"""
        return not self._disposed and self._mode == CompressionMode.COMPRESS

    @property
    def seekable(self) -> bool:
        """Check if stream is seekable (always False)"""
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
        if size == -1:
            compressed_data = self._base_stream.read()
        else:
            compressed_data = self._base_stream.read(size)

        if not compressed_data:
            return b''

        try:
            # Decompress data
            decompressed = self._decompressor.decompress(compressed_data)
            self._total_in += len(compressed_data)
            self._total_out += len(decompressed)
            return decompressed
        except Exception as e:
            raise ZLibException(f"Decompression error: {e}")

    def write(self, data: bytes) -> int:
        """Write data to be compressed"""
        if self._disposed:
            raise ValueError("Stream is disposed")

        if self._mode != CompressionMode.COMPRESS:
            raise io.UnsupportedOperation("Stream not writable")

        if not self._compressor:
            return 0

        try:
            # Compress data
            compressed = self._compressor.compress(data)
            bytes_written = self._base_stream.write(compressed)

            self._total_in += len(data)
            self._total_out += len(compressed)

            return len(data)
        except Exception as e:
            raise ZLibException(f"Compression error: {e}")

    def flush(self) -> None:
        """Flush stream"""
        if self._disposed:
            raise ValueError("Stream is disposed")

        if self._mode == CompressionMode.COMPRESS and self._compressor:
            # Flush compressor
            if self._flush_mode == FlushType.SYNC:
                compressed = self._compressor.flush(zlib.Z_SYNC_FLUSH)
            else:
                compressed = self._compressor.flush(zlib.Z_NO_FLUSH)

            if compressed:
                self._base_stream.write(compressed)
                self._total_out += len(compressed)

        self._base_stream.flush()

    def close(self) -> None:
        """Close stream"""
        if not self._disposed:
            try:
                if self._mode == CompressionMode.COMPRESS and self._compressor:
                    # Finalize compression
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

    # Static utility methods
    @staticmethod
    def compress_string(text: str) -> bytes:
        """Compress string to bytes"""
        data = text.encode('utf-8')
        return ZLibStream.compress_buffer(data, CompressionLevel.BEST_COMPRESSION)

    @staticmethod
    def compress_buffer(data: bytes, level: CompressionLevel) -> bytes:
        """Compress buffer"""
        zlib_level = min(9, max(0, int(level)))
        return zlib.compress(data, zlib_level)

    @staticmethod
    def uncompress_string(compressed: bytes) -> str:
        """Decompress bytes to string"""
        data = ZLibStream.uncompress_buffer(compressed)
        return data.decode('utf-8')

    @staticmethod
    def uncompress_buffer(compressed: bytes) -> bytes:
        """Decompress buffer"""
        return zlib.decompress(compressed)
