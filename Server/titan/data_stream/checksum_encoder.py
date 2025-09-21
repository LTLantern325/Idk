"""
Python conversion of Supercell.Laser.Titan.DataStream.ChecksumEncoder.cs
Checksum encoder for data integrity
"""

import hashlib
import struct
from typing import bytes, Union

class ChecksumEncoder:
    """Checksum encoder for data integrity verification"""

    def __init__(self):
        """Initialize checksum encoder"""
        self.data = bytearray()
        self.checksum = 0
        self.use_crc32 = True

    def enable_crc32(self, enable: bool = True) -> None:
        """Enable/disable CRC32 checksums"""
        self.use_crc32 = enable

    def write_byte(self, value: int) -> None:
        """Write byte and update checksum"""
        byte_val = value & 0xFF
        self.data.append(byte_val)
        self._update_checksum_byte(byte_val)

    def write_int(self, value: int) -> None:
        """Write 32-bit integer and update checksum"""
        packed = struct.pack('>i', value)
        for byte_val in packed:
            self.write_byte(byte_val)

    def write_long(self, value: int) -> None:
        """Write 64-bit long and update checksum"""
        packed = struct.pack('>q', value)
        for byte_val in packed:
            self.write_byte(byte_val)

    def write_v_int(self, value: int) -> None:
        """Write variable-length integer and update checksum"""
        value = value & 0xFFFFFFFF

        while value >= 0x80:
            self.write_byte((value & 0x7F) | 0x80)
            value >>= 7

        self.write_byte(value & 0x7F)

    def write_string(self, value: str) -> None:
        """Write string and update checksum"""
        if value is None:
            self.write_v_int(0)
        else:
            encoded = value.encode('utf-8')
            self.write_v_int(len(encoded))
            for byte_val in encoded:
                self.write_byte(byte_val)

    def write_bytes(self, data: bytes) -> None:
        """Write byte array and update checksum"""
        if data is None:
            self.write_v_int(0)
        else:
            self.write_v_int(len(data))
            for byte_val in data:
                self.write_byte(byte_val)

    def _update_checksum_byte(self, byte_val: int) -> None:
        """Update checksum with single byte"""
        if self.use_crc32:
            # Simple CRC32-like update
            self.checksum = ((self.checksum << 1) ^ byte_val) & 0xFFFFFFFF
        else:
            # Simple additive checksum
            self.checksum = (self.checksum + byte_val) & 0xFFFFFFFF

    def get_checksum(self) -> int:
        """Get current checksum"""
        return self.checksum

    def get_data(self) -> bytes:
        """Get encoded data"""
        return bytes(self.data)

    def get_data_with_checksum(self) -> bytes:
        """Get data with appended checksum"""
        result = bytearray(self.data)
        result.extend(struct.pack('>I', self.checksum))
        return bytes(result)

    def verify_checksum(self, expected_checksum: int) -> bool:
        """Verify checksum matches expected value"""
        return self.checksum == expected_checksum

    def reset(self) -> None:
        """Reset encoder"""
        self.data.clear()
        self.checksum = 0

    def calculate_md5(self) -> bytes:
        """Calculate MD5 hash of data"""
        return hashlib.md5(self.data).digest()

    def calculate_sha256(self) -> bytes:
        """Calculate SHA256 hash of data"""
        return hashlib.sha256(self.data).digest()

    def add_integrity_check(self) -> bytes:
        """Add integrity check to data"""
        # Add both checksum and MD5 hash
        result = bytearray(self.data)
        result.extend(struct.pack('>I', self.checksum))
        result.extend(self.calculate_md5())
        return bytes(result)

    def verify_integrity(self, data_with_check: bytes) -> tuple:
        """Verify data integrity, returns (is_valid, data)"""
        if len(data_with_check) < 20:  # 4 bytes checksum + 16 bytes MD5
            return False, b""

        # Extract components
        data = data_with_check[:-20]
        stored_checksum = struct.unpack('>I', data_with_check[-20:-16])[0]
        stored_md5 = data_with_check[-16:]

        # Recalculate checksums
        temp_encoder = ChecksumEncoder()
        temp_encoder.use_crc32 = self.use_crc32
        for byte_val in data:
            temp_encoder.write_byte(byte_val)

        # Verify
        checksum_valid = temp_encoder.get_checksum() == stored_checksum
        md5_valid = temp_encoder.calculate_md5() == stored_md5

        return checksum_valid and md5_valid, data
