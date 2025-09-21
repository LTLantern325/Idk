"""
Python conversion of Supercell.Laser.Titan.Library.Blake.Blake2BConfig.cs
Blake2B configuration class
"""

from typing import Optional

class Blake2BConfig:
    """Blake2B configuration"""

    def __init__(self):
        """Initialize Blake2B configuration"""
        self._output_size = 24
        self._key: Optional[bytes] = None
        self._salt: Optional[bytes] = None
        self._personalization: Optional[bytes] = None

    @property
    def key(self) -> Optional[bytes]:
        """Get key"""
        return self._key

    @key.setter
    def key(self, value: Optional[bytes]) -> None:
        """Set key"""
        self._key = value

    @property
    def output_size(self) -> int:
        """Get output size in bytes"""
        return self._output_size

    @output_size.setter
    def output_size(self, value: int) -> None:
        """Set output size in bytes"""
        if 1 <= value <= 64:
            self._output_size = value
        else:
            raise ValueError("Output size must be between 1 and 64 bytes")

    @property
    def output_size_in_bits(self) -> int:
        """Get output size in bits"""
        return self._output_size * 8

    @output_size_in_bits.setter
    def output_size_in_bits(self, value: int) -> None:
        """Set output size in bits"""
        if value % 8 != 0:
            raise ValueError("Output size in bits must be multiple of 8")
        self.output_size = value // 8

    @property
    def personalization(self) -> Optional[bytes]:
        """Get personalization"""
        return self._personalization

    @personalization.setter
    def personalization(self, value: Optional[bytes]) -> None:
        """Set personalization"""
        if value is not None and len(value) > 16:
            raise ValueError("Personalization must be 16 bytes or less")
        self._personalization = value

    @property
    def salt(self) -> Optional[bytes]:
        """Get salt"""
        return self._salt

    @salt.setter
    def salt(self, value: Optional[bytes]) -> None:
        """Set salt"""
        if value is not None and len(value) > 16:
            raise ValueError("Salt must be 16 bytes or less")
        self._salt = value

    def clone(self) -> 'Blake2BConfig':
        """Clone configuration"""
        config = Blake2BConfig()
        config.output_size = self.output_size
        config.key = self.key
        config.salt = self.salt
        config.personalization = self.personalization
        return config
