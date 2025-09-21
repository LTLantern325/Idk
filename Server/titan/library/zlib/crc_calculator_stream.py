"""
Python conversion of CRC calculator stream (simplified)
Stream wrapper that calculates CRC32 while reading/writing
"""

import io
from typing import Optional
from .crc32 import CRC32

class CrcCalculatorStream(io.IOBase):
    """Stream wrapper that calculates CRC32"""

    def __init__(self, stream: io.IOBase, leave_open: bool = False):
        """Initialize CRC calculator stream"""
        super().__init__()
        self._base_stream = stream
        self._leave_open = leave_open
        self._crc = CRC32()
        self._disposed = False
        self._total_bytes_slurped = 0

    @property
    def crc(self) -> int:
        """Get current CRC32 value"""
        return self._crc.crc32_result

    @property
    def total_bytes_slurped(self) -> int:
        """Get total bytes processed"""
        return self._total_bytes_slurped

    @property
    def readable(self) -> bool:
        """Check if readable"""
        return not self._disposed and self._base_stream.readable()

    @property
    def writable(self) -> bool:
        """Check if writable"""
        return not self._disposed and self._base_stream.writable()

    @property
    def seekable(self) -> bool:
        """Check if seekable"""
        return not self._disposed and self._base_stream.seekable()

    def read(self, size: int = -1) -> bytes:
        """Read data and update CRC"""
        if self._disposed:
            raise ValueError("Stream is disposed")

        data = self._base_stream.read(size)
        if data:
            self._crc.slurp_block(data, 0, len(data))
            self._total_bytes_slurped += len(data)

        return data

    def write(self, data: bytes) -> int:
        """Write data and update CRC"""
        if self._disposed:
            raise ValueError("Stream is disposed")

        result = self._base_stream.write(data)
        if data:
            self._crc.slurp_block(data, 0, len(data))
            self._total_bytes_slurped += len(data)

        return result

    def flush(self) -> None:
        """Flush stream"""
        if not self._disposed:
            self._base_stream.flush()

    def seek(self, offset: int, whence: int = io.SEEK_SET) -> int:
        """Seek in stream"""
        if self._disposed:
            raise ValueError("Stream is disposed")

        return self._base_stream.seek(offset, whence)

    def tell(self) -> int:
        """Get current position"""
        if self._disposed:
            raise ValueError("Stream is disposed")

        return self._base_stream.tell()

    def close(self) -> None:
        """Close stream"""
        if not self._disposed:
            try:
                if not self._leave_open:
                    self._base_stream.close()
            finally:
                self._disposed = True

    def reset_crc(self) -> None:
        """Reset CRC calculator"""
        self._crc.reset()
        self._total_bytes_slurped = 0

    def get_crc(self) -> int:
        """Get final CRC32 value"""
        return self.crc
