"""
Python conversion of Zip entry utilities (simplified)
Zip file entry representation
"""

from typing import Optional
from datetime import datetime

class ZipEntry:
    """Zip file entry"""

    def __init__(self, filename: str = ""):
        """Initialize zip entry"""
        self.filename = filename
        self.comment = ""
        self.compressed_size = 0
        self.uncompressed_size = 0
        self.crc32 = 0
        self.compression_method = 0
        self.last_modified = datetime.now()
        self.is_directory = False
        self.external_file_attributes = 0
        self.internal_file_attributes = 0

    @property
    def name(self) -> str:
        """Get entry name"""
        return self.filename

    @name.setter
    def name(self, value: str) -> None:
        """Set entry name"""
        self.filename = value
        self.is_directory = value.endswith('/')

    def __str__(self) -> str:
        """String representation"""
        return f"ZipEntry({self.filename})"
