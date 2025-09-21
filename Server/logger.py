"""
Python conversion of Supercell.Laser.Server Logger.cs
Logging functionality for the Supercell Laser Server
"""

import sys
from datetime import datetime
from colorama import Fore, Back, Style, init
from typing import Protocol

# Initialize colorama for colored console output
init(autoreset=True)

class IDebuggerListener(Protocol):
    """Interface for debugger listener"""
    def error(self, message: str) -> None: ...
    def print(self, message: str) -> None: ...
    def warning(self, message: str) -> None: ...

class Logger:
    """Static logger class for console output with colored messages"""

    @staticmethod
    def print_log(log: str) -> None:
        """Print debug message to console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{Fore.MAGENTA}[DEBUG] {timestamp} - {log}{Style.RESET_ALL}")

    @staticmethod
    def init() -> None:
        """Initialize logger and set debugger listener"""
        print(f"{Fore.MAGENTA}Logger initialized{Style.RESET_ALL}")
        # Set debugger listener
        from titan.debug.debugger import Debugger
        Debugger.set_listener(DebuggerListener())

    @staticmethod
    def warning(log: str) -> None:
        """Print warning message to console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{Fore.YELLOW}[WARNING] {timestamp} - {log}{Style.RESET_ALL}")

    @staticmethod
    def error(log: str) -> None:
        """Print error message to console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{Fore.RED}[ERROR] {timestamp} - {log}{Style.RESET_ALL}")

    @staticmethod
    def info(log: str) -> None:
        """Print info message to console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{Fore.CYAN}[INFO] {timestamp} - {log}{Style.RESET_ALL}")

class DebuggerListener:
    """Implementation of IDebuggerListener for handling debugger messages"""

    def error(self, message: str) -> None:
        """Handle error messages from debugger"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{Fore.RED}[LOGIC] Error: {timestamp} - {message}{Style.RESET_ALL}")

    def print(self, message: str) -> None:
        """Handle info messages from debugger"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{Fore.CYAN}[LOGIC] Info: {timestamp} - {message}{Style.RESET_ALL}")

    def warning(self, message: str) -> None:
        """Handle warning messages from debugger"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{Fore.YELLOW}[LOGIC] Warning: {timestamp} - {message}{Style.RESET_ALL}")

# Singleton instance for global access
logger_instance = Logger()
