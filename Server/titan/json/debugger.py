"""
Python conversion of Supercell.Laser.Titan.Debugger.Debugger.cs
Debug system for server logging and diagnostics
"""

import sys
import os
import traceback
import logging
from datetime import datetime
from typing import Any, Optional
from enum import IntEnum

class LogLevel(IntEnum):
    """Debug log levels"""
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

class Debugger:
    """Debug system for server logging"""

    _instance = None
    _initialized = False
    _log_level = LogLevel.INFO
    _log_file = None
    _console_enabled = True
    _file_enabled = True

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def initialize(cls, log_file: str = "server.log", log_level: LogLevel = LogLevel.INFO):
        """Initialize debugger system"""
        if cls._initialized:
            return

        cls._log_level = log_level
        cls._log_file = log_file
        cls._initialized = True

        # Setup Python logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )

        cls.print("Debugger initialized")

    @classmethod
    def set_log_level(cls, level: LogLevel):
        """Set minimum log level"""
        cls._log_level = level

    @classmethod
    def enable_console(cls, enabled: bool = True):
        """Enable/disable console output"""
        cls._console_enabled = enabled

    @classmethod
    def enable_file(cls, enabled: bool = True):
        """Enable/disable file output"""
        cls._file_enabled = enabled

    @classmethod
    def print(cls, message: str, level: LogLevel = LogLevel.INFO):
        """Print debug message"""
        if level < cls._log_level:
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        level_name = level.name
        formatted_message = f"[{timestamp}] [{level_name}] {message}"

        # Console output
        if cls._console_enabled:
            if level >= LogLevel.ERROR:
                print(formatted_message, file=sys.stderr)
            else:
                print(formatted_message)

        # File output
        if cls._file_enabled and cls._log_file:
            try:
                with open(cls._log_file, 'a', encoding='utf-8') as f:
                    f.write(formatted_message + '\n')
                    f.flush()
            except Exception:
                pass  # Ignore file write errors

    @classmethod
    def debug(cls, message: str):
        """Log debug message"""
        cls.print(f"DEBUG: {message}", LogLevel.DEBUG)

    @classmethod
    def info(cls, message: str):
        """Log info message"""
        cls.print(f"INFO: {message}", LogLevel.INFO)

    @classmethod
    def warning(cls, message: str):
        """Log warning message"""
        cls.print(f"WARNING: {message}", LogLevel.WARNING)

    @classmethod
    def error(cls, message: str, exception: Optional[Exception] = None):
        """Log error message"""
        error_msg = f"ERROR: {message}"

        if exception:
            error_msg += f"\nException: {str(exception)}"
            error_msg += f"\nTraceback: {traceback.format_exc()}"

        cls.print(error_msg, LogLevel.ERROR)

    @classmethod
    def critical(cls, message: str, exception: Optional[Exception] = None):
        """Log critical message"""
        critical_msg = f"CRITICAL: {message}"

        if exception:
            critical_msg += f"\nException: {str(exception)}"
            critical_msg += f"\nTraceback: {traceback.format_exc()}"

        cls.print(critical_msg, LogLevel.CRITICAL)

    @classmethod
    def assert_condition(cls, condition: bool, message: str = "Assertion failed"):
        """Assert condition and log error if false"""
        if not condition:
            cls.error(f"ASSERTION FAILED: {message}")
            if cls._log_level <= LogLevel.DEBUG:
                cls.print(f"Assertion stacktrace:\n{traceback.format_stack()}", LogLevel.DEBUG)

    @classmethod
    def log_function_entry(cls, function_name: str, *args, **kwargs):
        """Log function entry with parameters"""
        if cls._log_level <= LogLevel.DEBUG:
            args_str = ", ".join(str(arg) for arg in args)
            kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
            params = ", ".join(filter(None, [args_str, kwargs_str]))
            cls.debug(f"ENTER: {function_name}({params})")

    @classmethod
    def log_function_exit(cls, function_name: str, result: Any = None):
        """Log function exit with result"""
        if cls._log_level <= LogLevel.DEBUG:
            if result is not None:
                cls.debug(f"EXIT: {function_name} -> {result}")
            else:
                cls.debug(f"EXIT: {function_name}")

    @classmethod
    def log_performance(cls, operation: str, duration_ms: float):
        """Log performance metrics"""
        if duration_ms > 100:  # Warn for slow operations
            cls.warning(f"PERF: {operation} took {duration_ms:.2f}ms")
        else:
            cls.debug(f"PERF: {operation} took {duration_ms:.2f}ms")

    @classmethod
    def log_memory_usage(cls):
        """Log current memory usage"""
        try:
            import psutil
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            cls.debug(f"MEMORY: Current usage {memory_mb:.1f} MB")
        except ImportError:
            cls.debug("MEMORY: psutil not available for memory monitoring")

    @classmethod
    def dump_object(cls, obj: Any, name: str = "Object"):
        """Dump object details for debugging"""
        if cls._log_level <= LogLevel.DEBUG:
            obj_info = f"DUMP: {name}\n"
            obj_info += f"  Type: {type(obj).__name__}\n"
            obj_info += f"  Value: {repr(obj)}\n"

            if hasattr(obj, '__dict__'):
                obj_info += f"  Attributes:\n"
                for key, value in obj.__dict__.items():
                    obj_info += f"    {key}: {repr(value)}\n"

            cls.debug(obj_info.rstrip())

    @classmethod
    def log_network_packet(cls, packet_id: int, data: bytes, direction: str = "UNKNOWN"):
        """Log network packet for debugging"""
        if cls._log_level <= LogLevel.DEBUG:
            data_hex = data.hex() if len(data) <= 64 else data[:64].hex() + "..."
            cls.debug(f"PACKET {direction}: ID={packet_id}, Size={len(data)}, Data={data_hex}")

    @classmethod
    def create_crash_report(cls, exception: Exception):
        """Create detailed crash report"""
        crash_report = f"""
CRASH REPORT
============
Time: {datetime.now().isoformat()}
Exception: {type(exception).__name__}: {str(exception)}

Traceback:
{traceback.format_exc()}

System Information:
- Python: {sys.version}
- Platform: {sys.platform}
- Working Directory: {os.getcwd()}

Process Information:
- PID: {os.getpid()}
"""

        try:
            # Try to get additional system info
            import platform
            crash_report += f"- System: {platform.system()} {platform.release()}\n"
            crash_report += f"- Architecture: {platform.machine()}\n"
        except ImportError:
            pass

        cls.critical("SERVER CRASH", exception)

        # Save crash report to file
        try:
            crash_filename = f"crash_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(crash_filename, 'w', encoding='utf-8') as f:
                f.write(crash_report)
            cls.print(f"Crash report saved to: {crash_filename}", LogLevel.CRITICAL)
        except Exception:
            pass

# Initialize debugger on import
Debugger.initialize()
