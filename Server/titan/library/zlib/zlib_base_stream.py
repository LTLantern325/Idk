"""
Python conversion of ZLib base stream (simplified)
Base stream implementation for ZLib operations
"""

import io
import zlib
from typing import Optional
from .compression_level import CompressionLevel
from .compression_mode import CompressionMode
from .flush_type import FlushType
from .zlib_stream_flavor import ZlibStreamFlavor

class ZLibBaseStream:
    """Base stream for ZLib operations"""

    class StreamMode:
        """Stream mode enumeration"""
        READER = 0
        WRITER = 1

    def __init__(self, stream: io.IOBase, mode: CompressionMode, level: CompressionLevel,
                 flavor: ZlibStreamFlavor, leave_open: bool):
        """Initialize base stream"""
        self.m_stream = stream
        self.m_leave_open = leave_open
        self.m_buffer_size = 8192
        self.m_working_buffer: Optional[bytearray] = None
        self.m_flavor = flavor
        self.m_flush_mode = FlushType.NONE

        # Determine stream mode
        if mode == CompressionMode.COMPRESS:
            self.m_stream_mode = ZLibBaseStream.StreamMode.WRITER
            zlib_level = min(9, max(0, int(level)))
            if flavor == ZlibStreamFlavor.GZIP:
                self.m_compressor = zlib.compressobj(zlib_level, zlib.DEFLATED, 16 + 15)
            elif flavor == ZlibStreamFlavor.DEFLATE:
                self.m_compressor = zlib.compressobj(zlib_level, zlib.DEFLATED, -15)
            else:  # ZLIB
                self.m_compressor = zlib.compressobj(zlib_level, zlib.DEFLATED, 15)
            self.m_decompressor = None
        else:
            self.m_stream_mode = ZLibBaseStream.StreamMode.READER
            self.m_compressor = None
            if flavor == ZlibStreamFlavor.GZIP:
                self.m_decompressor = zlib.decompressobj(16 + 15)
            elif flavor == ZlibStreamFlavor.DEFLATE:
                self.m_decompressor = zlib.decompressobj(-15)
            else:  # ZLIB
                self.m_decompressor = zlib.decompressobj(15)

    def read(self, buffer: bytearray, offset: int, count: int) -> int:
        """Read from stream"""
        if self.m_stream_mode != ZLibBaseStream.StreamMode.READER:
            raise io.UnsupportedOperation("Stream not readable")

        if not self.m_decompressor:
            return 0

        # Read compressed data
        compressed_data = self.m_stream.read(count)
        if not compressed_data:
            return 0

        try:
            # Decompress
            decompressed = self.m_decompressor.decompress(compressed_data)
            bytes_to_copy = min(len(decompressed), count)

            # Copy to buffer
            buffer[offset:offset + bytes_to_copy] = decompressed[:bytes_to_copy]
            return bytes_to_copy
        except Exception:
            return 0

    def write(self, buffer: bytes, offset: int, count: int) -> None:
        """Write to stream"""
        if self.m_stream_mode != ZLibBaseStream.StreamMode.WRITER:
            raise io.UnsupportedOperation("Stream not writable")

        if not self.m_compressor:
            return

        try:
            # Get data to compress
            data = buffer[offset:offset + count]

            # Compress
            compressed = self.m_compressor.compress(data)

            # Write to underlying stream
            if compressed:
                self.m_stream.write(compressed)
        except Exception:
            pass

    def flush(self) -> None:
        """Flush stream"""
        if self.m_stream_mode == ZLibBaseStream.StreamMode.WRITER and self.m_compressor:
            if self.m_flush_mode == FlushType.SYNC:
                compressed = self.m_compressor.flush(zlib.Z_SYNC_FLUSH)
            else:
                compressed = self.m_compressor.flush(zlib.Z_NO_FLUSH)

            if compressed:
                self.m_stream.write(compressed)

        self.m_stream.flush()

    def close(self) -> None:
        """Close stream"""
        if self.m_stream_mode == ZLibBaseStream.StreamMode.WRITER and self.m_compressor:
            # Finalize compression
            final_data = self.m_compressor.flush()
            if final_data:
                self.m_stream.write(final_data)

        if not self.m_leave_open:
            self.m_stream.close()

    # Static utility methods
    @staticmethod
    def compress_string(text: str, compressor) -> None:
        """Compress string using compressor"""
        data = text.encode('utf-8')
        ZLibBaseStream.compress_buffer(data, compressor)

    @staticmethod
    def compress_buffer(data: bytes, compressor) -> None:
        """Compress buffer using compressor"""
        compressor.write(data, 0, len(data))
        compressor.close()

    @staticmethod
    def uncompress_string(compressed: bytes, decompressor) -> str:
        """Decompress to string using decompressor"""
        buffer = bytearray(len(compressed) * 4)  # Estimate
        bytes_read = decompressor.read(buffer, 0, len(buffer))
        return bytes(buffer[:bytes_read]).decode('utf-8')

    @staticmethod
    def uncompress_buffer(compressed: bytes, decompressor) -> bytes:
        """Decompress buffer using decompressor"""
        buffer = bytearray(len(compressed) * 4)  # Estimate
        bytes_read = decompressor.read(buffer, 0, len(buffer))
        return bytes(buffer[:bytes_read])
