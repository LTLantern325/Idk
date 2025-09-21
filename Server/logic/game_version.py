"""
Python conversion of Supercell.Laser.Logic.GameVersion.cs
Game version management class
"""

class GameVersion:
    """Game version management class"""

    # Version constants
    MAJOR_VERSION = 61
    MINOR_VERSION = 0
    BUILD_VERSION = 0

    # Version strings
    VERSION_STRING = f"{MAJOR_VERSION}.{MINOR_VERSION}.{BUILD_VERSION}"
    FULL_VERSION_STRING = f"Supercell.Laser.Logic v{VERSION_STRING}"

    def __init__(self):
        """Initialize game version"""
        self.major = self.MAJOR_VERSION
        self.minor = self.MINOR_VERSION
        self.build = self.BUILD_VERSION
        self.revision = 0

        # Build information
        self.build_date = ""
        self.build_branch = "main"
        self.build_commit = ""

        # Compatibility
        self.min_supported_version = "60.0.0"
        self.max_supported_version = "62.0.0"

        # Protocol version
        self.protocol_version = 3
        self.min_protocol_version = 2
        self.max_protocol_version = 4

    def get_major_version(self) -> int:
        """Get major version"""
        return self.major

    def get_minor_version(self) -> int:
        """Get minor version"""
        return self.minor

    def get_build_version(self) -> int:
        """Get build version"""
        return self.build

    def get_revision(self) -> int:
        """Get revision number"""
        return self.revision

    def get_version_string(self) -> str:
        """Get version string"""
        return f"{self.major}.{self.minor}.{self.build}"

    def get_full_version_string(self) -> str:
        """Get full version string with revision"""
        if self.revision > 0:
            return f"{self.major}.{self.minor}.{self.build}.{self.revision}"
        return self.get_version_string()

    def get_protocol_version(self) -> int:
        """Get protocol version"""
        return self.protocol_version

    def set_protocol_version(self, version: int) -> None:
        """Set protocol version"""
        self.protocol_version = max(self.min_protocol_version, 
                                   min(self.max_protocol_version, version))

    def is_compatible_version(self, version_string: str) -> bool:
        """Check if version is compatible"""
        try:
            other_version = self._parse_version_string(version_string)
            min_version = self._parse_version_string(self.min_supported_version)
            max_version = self._parse_version_string(self.max_supported_version)

            return min_version <= other_version <= max_version
        except:
            return False

    def is_compatible_protocol(self, protocol_version: int) -> bool:
        """Check if protocol version is compatible"""
        return (self.min_protocol_version <= protocol_version <= 
                self.max_protocol_version)

    def compare_version(self, other_version: str) -> int:
        """Compare with another version string"""
        try:
            current = self._version_to_number(self.get_version_string())
            other = self._version_to_number(other_version)

            if current < other:
                return -1
            elif current > other:
                return 1
            else:
                return 0
        except:
            return 0

    def is_newer_version(self, version_string: str) -> bool:
        """Check if given version is newer"""
        return self.compare_version(version_string) < 0

    def is_older_version(self, version_string: str) -> bool:
        """Check if given version is older"""
        return self.compare_version(version_string) > 0

    def is_same_version(self, version_string: str) -> bool:
        """Check if versions are the same"""
        return self.compare_version(version_string) == 0

    def _parse_version_string(self, version_string: str) -> tuple:
        """Parse version string into tuple"""
        parts = version_string.split('.')
        if len(parts) >= 3:
            return (int(parts[0]), int(parts[1]), int(parts[2]))
        elif len(parts) == 2:
            return (int(parts[0]), int(parts[1]), 0)
        elif len(parts) == 1:
            return (int(parts[0]), 0, 0)
        else:
            return (0, 0, 0)

    def _version_to_number(self, version_string: str) -> int:
        """Convert version string to comparable number"""
        major, minor, build = self._parse_version_string(version_string)
        return (major * 10000) + (minor * 100) + build

    def set_build_info(self, build_date: str, branch: str, commit: str) -> None:
        """Set build information"""
        self.build_date = build_date
        self.build_branch = branch
        self.build_commit = commit

    def get_build_info(self) -> dict:
        """Get build information"""
        return {
            'version': self.get_full_version_string(),
            'protocol': self.protocol_version,
            'build_date': self.build_date,
            'branch': self.build_branch,
            'commit': self.build_commit[:8] if self.build_commit else ""
        }

    def get_compatibility_info(self) -> dict:
        """Get compatibility information"""
        return {
            'min_version': self.min_supported_version,
            'max_version': self.max_supported_version,
            'min_protocol': self.min_protocol_version,
            'max_protocol': self.max_protocol_version
        }

    @classmethod
    def get_current_version(cls) -> 'GameVersion':
        """Get current game version instance"""
        version = cls()
        return version

    @classmethod
    def create_version(cls, major: int, minor: int, build: int = 0) -> 'GameVersion':
        """Create version with specific numbers"""
        version = cls()
        version.major = major
        version.minor = minor
        version.build = build
        return version

    def encode(self, stream) -> None:
        """Encode version to stream"""
        stream.write_v_int(self.major)
        stream.write_v_int(self.minor)
        stream.write_v_int(self.build)
        stream.write_v_int(self.revision)
        stream.write_v_int(self.protocol_version)
        stream.write_string(self.build_date)
        stream.write_string(self.build_branch)
        stream.write_string(self.build_commit)

    def decode(self, stream) -> None:
        """Decode version from stream"""
        self.major = stream.read_v_int()
        self.minor = stream.read_v_int()
        self.build = stream.read_v_int()
        self.revision = stream.read_v_int()
        self.protocol_version = stream.read_v_int()
        self.build_date = stream.read_string()
        self.build_branch = stream.read_string()
        self.build_commit = stream.read_string()

    def __str__(self) -> str:
        """String representation"""
        return f"GameVersion({self.get_full_version_string()}, protocol={self.protocol_version})"

    def __eq__(self, other) -> bool:
        """Equality comparison"""
        if not isinstance(other, GameVersion):
            return False
        return (self.major == other.major and 
                self.minor == other.minor and 
                self.build == other.build and
                self.revision == other.revision)

    def __lt__(self, other) -> bool:
        """Less than comparison"""
        if not isinstance(other, GameVersion):
            return False
        return ((self.major, self.minor, self.build, self.revision) < 
                (other.major, other.minor, other.build, other.revision))

    def __le__(self, other) -> bool:
        """Less than or equal comparison"""
        return self < other or self == other

    def __gt__(self, other) -> bool:
        """Greater than comparison"""
        return not self <= other

    def __ge__(self, other) -> bool:
        """Greater than or equal comparison"""
        return not self < other
