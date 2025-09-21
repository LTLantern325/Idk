"""
Python conversion of Supercell.Laser.Server.Handler.ExitHandler.cs
Handles graceful server shutdown
"""

import sys
import signal
import atexit
from database.cache.account_cache import AccountCache  
from database.cache.alliance_cache import AllianceCache
from networking.session.sessions import Sessions
from logger import Logger

class ExitHandler:
    """Static class for handling server exit/shutdown"""

    @staticmethod
    def exit(signum=None, frame=None):
        """Handle exit signal and perform graceful shutdown"""
        try:
            Sessions.start_shutdown()

            Logger.print_log("Shutting down...")

            # Save all cached data
            AccountCache.save_all()
            AllianceCache.save_all()

            # Stop cache threads
            AccountCache._started = False
            AllianceCache._started = False

            print("Server is now in maintenance mode.")
            print("Shutdown complete!")

        except Exception as e:
            print(f"Error during shutdown: {e}")

        finally:
            sys.exit(0)

    @staticmethod
    def init():
        """Initialize exit handler with signal handlers"""
        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, ExitHandler.exit)   # Ctrl+C
        signal.signal(signal.SIGTERM, ExitHandler.exit)  # Termination signal

        # Register atexit handler as fallback
        atexit.register(ExitHandler._cleanup)

        print("Exit handler initialized")

    @staticmethod
    def _cleanup():
        """Cleanup function called on normal exit"""
        try:
            AccountCache.save_all()
            AllianceCache.save_all()
        except Exception as e:
            print(f"Error during cleanup: {e}")
