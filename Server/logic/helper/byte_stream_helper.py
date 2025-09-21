"""
Python conversion of Supercell.Laser.Logic.Helper.ByteStreamHelper.cs
Helper class for byte stream operations
"""

import struct
from typing import List, Optional

class ByteStreamHelper:
    """Helper class for byte stream operations"""

    @staticmethod
    def write_int(stream, value: int) -> None:
        """Write 32-bit integer to stream"""
        stream.write(struct.pack('>i', value))

    @staticmethod
    def read_int(stream) -> int:
        """Read 32-bit integer from stream"""
        data = stream.read(4)
        if len(data) < 4:
            return 0
        return struct.unpack('>i', data)[0]

    @staticmethod
    def write_long(stream, value: int) -> None:
        """Write 64-bit long to stream"""
        stream.write(struct.pack('>q', value))

    @staticmethod
    def read_long(stream) -> int:
        """Read 64-bit long from stream"""
        data = stream.read(8)
        if len(data) < 8:
            return 0
        return struct.unpack('>q', data)[0]

    @staticmethod
    def write_short(stream, value: int) -> None:
        """Write 16-bit short to stream"""
        stream.write(struct.pack('>h', value))

    @staticmethod
    def read_short(stream) -> int:
        """Read 16-bit short from stream"""
        data = stream.read(2)
        if len(data) < 2:
            return 0
        return struct.unpack('>h', data)[0]

    @staticmethod
    def write_byte(stream, value: int) -> None:
        """Write single byte to stream"""
        stream.write(struct.pack('B', value & 0xFF))

    @staticmethod
    def read_byte(stream) -> int:
        """Read single byte from stream"""
        data = stream.read(1)
        if len(data) < 1:
            return 0
        return struct.unpack('B', data)[0]

    @staticmethod
    def write_boolean(stream, value: bool) -> None:
        """Write boolean to stream"""
        ByteStreamHelper.write_byte(stream, 1 if value else 0)

    @staticmethod
    def read_boolean(stream) -> bool:
        """Read boolean from stream"""
        return ByteStreamHelper.read_byte(stream) != 0

    @staticmethod
    def write_string(stream, value: str) -> None:
        """Write string to stream with length prefix"""
        if value is None:
            ByteStreamHelper.write_v_int(stream, 0)
        else:
            encoded = value.encode('utf-8')
            ByteStreamHelper.write_v_int(stream, len(encoded))
            stream.write(encoded)

    @staticmethod
    def read_string(stream) -> str:
        """Read string from stream"""
        length = ByteStreamHelper.read_v_int(stream)
        if length <= 0:
            return ""

        data = stream.read(length)
        if len(data) < length:
            return ""

        try:
            return data.decode('utf-8')
        except UnicodeDecodeError:
            return ""

    @staticmethod
    def write_v_int(stream, value: int) -> None:
        """Write variable-length integer to stream"""
        value = value & 0xFFFFFFFF  # Ensure 32-bit

        while value >= 0x80:
            stream.write(struct.pack('B', (value & 0x7F) | 0x80))
            value >>= 7

        stream.write(struct.pack('B', value & 0x7F))

    @staticmethod
    def read_v_int(stream) -> int:
        """Read variable-length integer from stream"""
        result = 0
        shift = 0

        while shift < 32:  # Prevent infinite loop
            byte_data = stream.read(1)
            if len(byte_data) < 1:
                break

            byte_val = struct.unpack('B', byte_data)[0]
            result |= (byte_val & 0x7F) << shift

            if (byte_val & 0x80) == 0:
                break

            shift += 7

        return result

    @staticmethod
    def write_v_long(stream, value: int) -> None:
        """Write variable-length long to stream"""
        value = value & 0xFFFFFFFFFFFFFFFF  # Ensure 64-bit

        while value >= 0x80:
            stream.write(struct.pack('B', (value & 0x7F) | 0x80))
            value >>= 7

        stream.write(struct.pack('B', value & 0x7F))

    @staticmethod
    def read_v_long(stream) -> int:
        """Read variable-length long from stream"""
        result = 0
        shift = 0

        while shift < 64:  # Prevent infinite loop
            byte_data = stream.read(1)
            if len(byte_data) < 1:
                break

            byte_val = struct.unpack('B', byte_data)[0]
            result |= (byte_val & 0x7F) << shift

            if (byte_val & 0x80) == 0:
                break

            shift += 7

        return result

    @staticmethod
    def write_float(stream, value: float) -> None:
        """Write 32-bit float to stream"""
        stream.write(struct.pack('>f', value))

    @staticmethod
    def read_float(stream) -> float:
        """Read 32-bit float from stream"""
        data = stream.read(4)
        if len(data) < 4:
            return 0.0
        return struct.unpack('>f', data)[0]

    @staticmethod
    def write_double(stream, value: float) -> None:
        """Write 64-bit double to stream"""
        stream.write(struct.pack('>d', value))

    @staticmethod
    def read_double(stream) -> float:
        """Read 64-bit double from stream"""
        data = stream.read(8)
        if len(data) < 8:
            return 0.0
        return struct.unpack('>d', data)[0]

    @staticmethod
    def write_byte_array(stream, data: bytes) -> None:
        """Write byte array to stream with length prefix"""
        if data is None:
            ByteStreamHelper.write_v_int(stream, 0)
        else:
            ByteStreamHelper.write_v_int(stream, len(data))
            stream.write(data)

    @staticmethod
    def read_byte_array(stream) -> bytes:
        """Read byte array from stream"""
        length = ByteStreamHelper.read_v_int(stream)
        if length <= 0:
            return b""

        data = stream.read(length)
        return data if len(data) == length else b""

    @staticmethod
    def write_int_array(stream, values: List[int]) -> None:
        """Write integer array to stream"""
        if values is None:
            ByteStreamHelper.write_v_int(stream, 0)
        else:
            ByteStreamHelper.write_v_int(stream, len(values))
            for value in values:
                ByteStreamHelper.write_v_int(stream, value)

    @staticmethod
    def read_int_array(stream) -> List[int]:
        """Read integer array from stream"""
        length = ByteStreamHelper.read_v_int(stream)
        if length <= 0:
            return []

        result = []
        for i in range(length):
            result.append(ByteStreamHelper.read_v_int(stream))

        return result

    @staticmethod
    def write_string_array(stream, values: List[str]) -> None:
        """Write string array to stream"""
        if values is None:
            ByteStreamHelper.write_v_int(stream, 0)
        else:
            ByteStreamHelper.write_v_int(stream, len(values))
            for value in values:
                ByteStreamHelper.write_string(stream, value)

    @staticmethod
    def read_string_array(stream) -> List[str]:
        """Read string array from stream"""
        length = ByteStreamHelper.read_v_int(stream)
        if length <= 0:
            return []

        result = []
        for i in range(length):
            result.append(ByteStreamHelper.read_string(stream))

        return result

    @staticmethod
    def get_stream_position(stream) -> int:
        """Get current stream position"""
        try:
            return stream.tell()
        except:
            return 0

    @staticmethod
    def set_stream_position(stream, position: int) -> bool:
        """Set stream position"""
        try:
            stream.seek(position)
            return True
        except:
            return False

    @staticmethod
    def get_remaining_bytes(stream) -> int:
        """Get number of remaining bytes in stream"""
        try:
            current_pos = stream.tell()
            stream.seek(0, 2)  # Seek to end
            end_pos = stream.tell()
            stream.seek(current_pos)  # Restore position
            return end_pos - current_pos
        except:
            return 0
