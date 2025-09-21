"""
Python conversion of Supercell.Laser.Titan.Library.ZLib.ZLibCodec.cs (simplified)
ZLib codec for compression and decompression
"""

import zlib
from typing import Optional
from .compression_level import CompressionLevel
from .compression_mode import CompressionMode
from .compression_strategy import CompressionStrategy
from .flush_type import FlushType
from .zlib_exception import ZLibException

class ZLibCodec:
    """ZLib codec for compression/decompression"""

    def __init__(self, mode: Optional[CompressionMode] = None):
        """Initialize ZLib codec"""
        # Buffer properties
        self.input_buffer: Optional[bytes] = None
        self.next_in = 0
        self.available_bytes_in = 0
        self.total_bytes_in = 0

        self.output_buffer: Optional[bytearray] = None
        self.next_out = 0
        self.available_bytes_out = 0
        self.total_bytes_out = 0

        # Status and message
        self.message = ""

        # Configuration
        self.compress_level = CompressionLevel.DEFAULT
        self.window_bits = 15
        self.strategy = CompressionStrategy.DEFAULT

        # Internal state
        self._compressor = None
        self._decompressor = None
        self._adler32 = 1

        if mode is not None:
            if mode == CompressionMode.COMPRESS:
                if self.initialize_deflate() != 0:
                    raise ZLibException("Cannot initialize for deflate.")
            elif mode == CompressionMode.DECOMPRESS:
                if self.initialize_inflate() != 0:
                    raise ZLibException("Cannot initialize for inflate.")
            else:
                raise ZLibException("Invalid compression mode.")

    @property
    def adler32(self) -> int:
        """Get Adler32 checksum"""
        return self._adler32

    # Inflate (decompression) methods
    def initialize_inflate(self, window_bits: int = 15, expect_rfc1950_header: bool = True) -> int:
        """Initialize for inflation (decompression)"""
        try:
            self.window_bits = window_bits
            # Python zlib handles RFC1950 headers by default
            if expect_rfc1950_header:
                self._decompressor = zlib.decompressobj(window_bits)
            else:
                self._decompressor = zlib.decompressobj(-window_bits)  # Raw deflate
            return 0
        except Exception as e:
            self.message = str(e)
            return -1

    def inflate(self, flush: FlushType) -> int:
        """Perform inflation"""
        if self._decompressor is None:
            raise ZLibException("No inflate state!")

        if not self.input_buffer or self.available_bytes_in <= 0:
            return 0

        try:
            # Get input data
            input_data = self.input_buffer[self.next_in:self.next_in + self.available_bytes_in]

            # Decompress
            if flush == FlushType.FINISH:
                output_data = self._decompressor.decompress(input_data)
                if self._decompressor.unused_data:
                    remaining = len(self._decompressor.unused_data)
                else:
                    remaining = 0
            else:
                output_data = self._decompressor.decompress(input_data)
                remaining = 0

            # Update output
            if output_data and self.output_buffer:
                bytes_to_copy = min(len(output_data), self.available_bytes_out)
                self.output_buffer[self.next_out:self.next_out + bytes_to_copy] = output_data[:bytes_to_copy]
                self.next_out += bytes_to_copy
                self.available_bytes_out -= bytes_to_copy
                self.total_bytes_out += bytes_to_copy

            # Update input
            bytes_consumed = self.available_bytes_in - remaining
            self.next_in += bytes_consumed
            self.available_bytes_in = remaining
            self.total_bytes_in += bytes_consumed

            return 0 if remaining > 0 or len(output_data) > 0 else 1

        except Exception as e:
            self.message = str(e)
            return -1

    def end_inflate(self) -> int:
        """End inflation"""
        self._decompressor = None
        return 0

    def sync_inflate(self) -> int:
        """Sync inflate"""
        # Simplified implementation
        return 0

    # Deflate (compression) methods  
    def initialize_deflate(self, level: CompressionLevel = CompressionLevel.DEFAULT, 
                          bits: int = 15, want_rfc1950_header: bool = True) -> int:
        """Initialize for deflation (compression)"""
        try:
            self.compress_level = level
            self.window_bits = bits

            # Convert compression level
            zlib_level = min(9, max(0, int(level)))

            if want_rfc1950_header:
                self._compressor = zlib.compressobj(zlib_level, zlib.DEFLATED, bits)
            else:
                self._compressor = zlib.compressobj(zlib_level, zlib.DEFLATED, -bits)

            return 0
        except Exception as e:
            self.message = str(e)
            return -1

    def deflate(self, flush: FlushType) -> int:
        """Perform deflation"""
        if self._compressor is None:
            raise ZLibException("No deflate state!")

        if not self.input_buffer:
            return 0

        try:
            # Get input data
            if self.available_bytes_in > 0:
                input_data = self.input_buffer[self.next_in:self.next_in + self.available_bytes_in]
            else:
                input_data = b''

            # Compress
            if flush == FlushType.FINISH:
                output_data = self._compressor.compress(input_data) + self._compressor.flush()
            elif flush == FlushType.SYNC:
                output_data = self._compressor.compress(input_data) + self._compressor.flush(zlib.Z_SYNC_FLUSH)
            else:
                output_data = self._compressor.compress(input_data)

            # Update output
            if output_data and self.output_buffer:
                bytes_to_copy = min(len(output_data), self.available_bytes_out)
                self.output_buffer[self.next_out:self.next_out + bytes_to_copy] = output_data[:bytes_to_copy]
                self.next_out += bytes_to_copy
                self.available_bytes_out -= bytes_to_copy
                self.total_bytes_out += bytes_to_copy

            # Update input
            self.next_in += self.available_bytes_in
            self.total_bytes_in += self.available_bytes_in
            self.available_bytes_in = 0

            return 0

        except Exception as e:
            self.message = str(e)
            return -1

    def end_deflate(self) -> int:
        """End deflation"""
        self._compressor = None
        return 0

    def reset_deflate(self) -> None:
        """Reset deflate state"""
        if self._compressor:
            # Reinitialize compressor
            self.initialize_deflate(self.compress_level, self.window_bits, True)

    def set_deflate_params(self, level: CompressionLevel, strategy: CompressionStrategy) -> int:
        """Set deflate parameters"""
        self.compress_level = level
        self.strategy = strategy
        return 0

    def set_dictionary(self, dictionary: bytes) -> int:
        """Set compression dictionary"""
        # Simplified implementation
        return 0
