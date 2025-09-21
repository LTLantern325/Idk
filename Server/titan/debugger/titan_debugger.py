"""
Python conversion of Supercell.Laser.Titan.Debug.Debugger.cs
Debug logging and assertion system
"""

from abc import ABC, abstractmethod
from typing import Optional

class IDebuggerListener(ABC):
    """Interface for debugger listeners"""

    @abstractmethod
    def print(self, message: str) -> None:
        """Print debug message"""
        pass

    @abstractmethod
    def warning(self, message: str) -> None:
        """Print warning message"""
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        """Print error message"""
        pass

class Debugger:
    """Static debugger class"""

    _debugger_listener: Optional[IDebuggerListener] = None

    @classmethod
    def set_listener(cls, listener: IDebuggerListener) -> None:
        """Set debugger listener"""
        cls._debugger_listener = listener

    @classmethod
    def print_log(cls, log: str) -> None:
        """Print debug log"""
        if cls._debugger_listener:
            cls._debugger_listener.print(log)
        else:
            print(f"[DEBUG] {log}")

    @classmethod
    def warning(cls, log: str) -> None:
        """Print warning log"""
        if cls._debugger_listener:
            cls._debugger_listener.warning(log)
        else:
            print(f"[WARNING] {log}")

    @classmethod
    def error(cls, log: str) -> None:
        """Print error log"""
        if cls._debugger_listener:
            cls._debugger_listener.error(log)
        else:
            print(f"[ERROR] {log}")

    @classmethod
    def do_assert(cls, assertion: bool, assertion_error: str) -> bool:
        """Perform assertion and log error if failed"""
        if not assertion:
            cls.error(assertion_error)
        return assertion

class ConsoleDebuggerListener(IDebuggerListener):
    """Default console debugger listener"""

    def print(self, message: str) -> None:
        print(f"[DEBUG] {message}")

    def warning(self, message: str) -> None:
        print(f"[WARNING] {message}")

    def error(self, message: str) -> None:
        print(f"[ERROR] {message}")
