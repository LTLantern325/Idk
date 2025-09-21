"""
Python conversion of Supercell.Laser.Titan.DataStream.BitStream.cs
Bit-level data stream operations
"""

class BitStream:
    """Bit-level data stream for precise bit manipulation"""

    def __init__(self, data: bytes = None):
        """Initialize bit stream"""
        self.data = bytearray(data) if data else bytearray()
        self.bit_offset = 0
        self.byte_offset = 0
        self.read_mode = data is not None

    def write_bit(self, bit: int) -> None:
        """Write single bit"""
        if self.read_mode:
            raise ValueError("Stream is in read mode")

        # Ensure we have enough bytes
        byte_index = self.bit_offset // 8
        while len(self.data) <= byte_index:
            self.data.append(0)

        bit_index = self.bit_offset % 8

        if bit:
            self.data[byte_index] |= (1 << (7 - bit_index))
        else:
            self.data[byte_index] &= ~(1 << (7 - bit_index))

        self.bit_offset += 1

    def read_bit(self) -> int:
        """Read single bit"""
        if not self.read_mode:
            raise ValueError("Stream is in write mode")

        byte_index = self.bit_offset // 8
        if byte_index >= len(self.data):
            return 0  # EOF

        bit_index = self.bit_offset % 8
        bit = (self.data[byte_index] >> (7 - bit_index)) & 1

        self.bit_offset += 1
        return bit

    def write_bits(self, value: int, bit_count: int) -> None:
        """Write multiple bits from integer"""
        for i in range(bit_count - 1, -1, -1):
            bit = (value >> i) & 1
            self.write_bit(bit)

    def read_bits(self, bit_count: int) -> int:
        """Read multiple bits as integer"""
        value = 0
        for i in range(bit_count):
            bit = self.read_bit()
            value = (value << 1) | bit
        return value

    def write_byte(self, value: int) -> None:
        """Write byte (8 bits)"""
        self.write_bits(value & 0xFF, 8)

    def read_byte(self) -> int:
        """Read byte (8 bits)"""
        return self.read_bits(8)

    def write_int(self, value: int) -> None:
        """Write 32-bit integer"""
        self.write_bits(value & 0xFFFFFFFF, 32)

    def read_int(self) -> int:
        """Read 32-bit integer"""
        return self.read_bits(32)

    def write_boolean(self, value: bool) -> None:
        """Write boolean as bit"""
        self.write_bit(1 if value else 0)

    def read_boolean(self) -> bool:
        """Read boolean from bit"""
        return self.read_bit() != 0

    def pad_to_byte_boundary(self) -> None:
        """Pad to next byte boundary with zeros"""
        while self.bit_offset % 8 != 0:
            self.write_bit(0)

    def get_bytes(self) -> bytes:
        """Get byte array"""
        if not self.read_mode:
            self.pad_to_byte_boundary()
        return bytes(self.data)

    def get_bit_count(self) -> int:
        """Get total number of bits"""
        return self.bit_offset

    def get_byte_count(self) -> int:
        """Get total number of bytes"""
        return (self.bit_offset + 7) // 8

    def reset(self) -> None:
        """Reset stream position"""
        self.bit_offset = 0
        self.byte_offset = 0

    def set_read_mode(self, data: bytes) -> None:
        """Switch to read mode with new data"""
        self.data = bytearray(data)
        self.read_mode = True
        self.reset()

    def set_write_mode(self) -> None:
        """Switch to write mode"""
        self.data.clear()
        self.read_mode = False
        self.reset()
