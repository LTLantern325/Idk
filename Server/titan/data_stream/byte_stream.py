"""
Python conversion of Supercell.Laser.Titan.DataStream.ByteStream.cs
Byte-level data stream operations for network protocols
"""

import struct
from typing import Union

class ByteStream:
    """Byte stream for network protocol serialization"""

    def __init__(self, data: bytes = None, big_endian: bool = True):
        """Initialize byte stream"""
        self.data = bytearray(data) if data else bytearray()
        self.offset = 0
        self.big_endian = big_endian
        self.endian_prefix = '>' if big_endian else '<'

    def write_byte(self, value: int) -> None:
        """Write single byte"""
        self.data.append(value & 0xFF)

    def read_byte(self) -> int:
        """Read single byte"""
        if self.offset >= len(self.data):
            return 0
        value = self.data[self.offset]
        self.offset += 1
        return value

    def write_boolean(self, value: bool) -> None:
        """Write boolean"""
        self.write_byte(1 if value else 0)

    def read_boolean(self) -> bool:
        """Read boolean"""
        return self.read_byte() != 0

    def write_short(self, value: int) -> None:
        """Write 16-bit short"""
        self.data.extend(struct.pack(f'{self.endian_prefix}h', value))

    def read_short(self) -> int:
        """Read 16-bit short"""
        if self.offset + 2 > len(self.data):
            return 0
        value = struct.unpack(f'{self.endian_prefix}h', self.data[self.offset:self.offset+2])[0]
        self.offset += 2
        return value

    def write_int(self, value: int) -> None:
        """Write 32-bit integer"""
        self.data.extend(struct.pack(f'{self.endian_prefix}i', value))

    def read_int(self) -> int:
        """Read 32-bit integer"""
        if self.offset + 4 > len(self.data):
            return 0
        value = struct.unpack(f'{self.endian_prefix}i', self.data[self.offset:self.offset+4])[0]
        self.offset += 4
        return value

    def write_long(self, value: int) -> None:
        """Write 64-bit long"""
        self.data.extend(struct.pack(f'{self.endian_prefix}q', value))

    def read_long(self) -> int:
        """Read 64-bit long"""
        if self.offset + 8 > len(self.data):
            return 0
        value = struct.unpack(f'{self.endian_prefix}q', self.data[self.offset:self.offset+8])[0]
        self.offset += 8
        return value

    def write_v_int(self, value: int) -> None:
        """Write variable-length integer"""
        value = value & 0xFFFFFFFF  # Ensure 32-bit

        while value >= 0x80:
            self.write_byte((value & 0x7F) | 0x80)
            value >>= 7

        self.write_byte(value & 0x7F)

    def read_v_int(self) -> int:
        """Read variable-length integer"""
        result = 0
        shift = 0

        while shift < 32:
            byte_val = self.read_byte()
            result |= (byte_val & 0x7F) << shift

            if (byte_val & 0x80) == 0:
                break

            shift += 7

        return result

    def write_string(self, value: str) -> None:
        """Write string with length prefix"""
        if value is None:
            self.write_v_int(0)
        else:
            encoded = value.encode('utf-8')
            self.write_v_int(len(encoded))
            self.data.extend(encoded)

    def read_string(self) -> str:
        """Read string with length prefix"""
        length = self.read_v_int()
        if length <= 0:
            return ""

        if self.offset + length > len(self.data):
            return ""

        data = self.data[self.offset:self.offset + length]
        self.offset += length

        try:
            return data.decode('utf-8')
        except UnicodeDecodeError:
            return ""

    def write_bytes(self, data: bytes) -> None:
        """Write byte array with length prefix"""
        if data is None:
            self.write_v_int(0)
        else:
            self.write_v_int(len(data))
            self.data.extend(data)

    def read_bytes(self) -> bytes:
        """Read byte array with length prefix"""
        length = self.read_v_int()
        if length <= 0:
            return b""

        if self.offset + length > len(self.data):
            return b""

        data = self.data[self.offset:self.offset + length]
        self.offset += length
        return bytes(data)

    def get_remaining_bytes(self) -> int:
        """Get number of remaining bytes"""
        return max(0, len(self.data) - self.offset)

    def get_capacity(self) -> int:
        """Get total capacity"""
        return len(self.data)

    def reset_offset(self) -> None:
        """Reset read offset"""
        self.offset = 0

    def set_offset(self, offset: int) -> None:
        """Set read offset"""
        self.offset = max(0, min(offset, len(self.data)))

    def get_bytes(self) -> bytes:
        """Get all bytes"""
        return bytes(self.data)

    def clear(self) -> None:
        """Clear stream"""
        self.data.clear()
        self.offset = 0
