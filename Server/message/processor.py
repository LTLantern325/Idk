"""
Python conversion of Supercell.Laser.Server.Message.Processor.cs
Message processing queue system
"""

import threading
import time
from queue import Queue
from typing import NamedTuple
from dataclasses import dataclass

from networking.connection import Connection
from logic.message.game_message import GameMessage
from logger import Logger

@dataclass
class QueueItem:
    """Item in message queue"""
    connection: Connection
    message: GameMessage

class Processor:
    """Static class for processing messages"""

    _incoming_queue: Queue = Queue(maxsize=1024)
    _outgoing_queue: Queue = Queue(maxsize=1024)

    _receive_event: threading.Event = threading.Event()
    _send_event: threading.Event = threading.Event()

    _receive_thread: threading.Thread = None
    _send_thread: threading.Thread = None
    _running: bool = False

    @classmethod
    def init(cls) -> None:
        """Initialize message processor"""
        cls._incoming_queue = Queue(maxsize=1024)
        cls._outgoing_queue = Queue(maxsize=1024)

        cls._receive_event = threading.Event()
        cls._send_event = threading.Event()

        cls._running = True

        # Start processing threads
        cls._receive_thread = threading.Thread(target=cls._update_receive, daemon=True)
        cls._send_thread = threading.Thread(target=cls._update_send, daemon=True)

        cls._receive_thread.start()
        cls._send_thread.start()

    @classmethod
    def receive(cls, connection: Connection, message: GameMessage) -> bool:
        """Queue incoming message for processing"""
        if not message:
            return False

        try:
            if cls._incoming_queue.full():
                Logger.print_log(f"Processor: Incoming message queue full. Message of type {message.get_message_type()} discarded.")
                return False

            cls._incoming_queue.put_nowait(QueueItem(connection, message))
            cls._receive_event.set()
            return True

        except Exception as e:
            Logger.error(f"Error queuing incoming message: {e}")
            return False

    @classmethod
    def send(cls, connection: Connection, message: GameMessage) -> None:
        """Queue outgoing message for sending"""
        if not message:
            return

        try:
            if cls._outgoing_queue.full():
                Logger.print_log(f"Processor: Outgoing message queue full. Message of type {message.get_message_type()} discarded.")
                return

            cls._outgoing_queue.put_nowait(QueueItem(connection, message))
            cls._send_event.set()

        except Exception as e:
            Logger.error(f"Error queuing outgoing message: {e}")

    @classmethod
    def _update_receive(cls) -> None:
        """Process incoming messages"""
        while cls._running:
            try:
                cls._receive_event.wait()

                while not cls._incoming_queue.empty():
                    try:
                        item = cls._incoming_queue.get_nowait()
                        if item.connection and item.connection.message_manager:
                            item.connection.message_manager.receive_message(item.message)
                    except Exception as e:
                        Logger.error(f"Error processing incoming message: {e}")

                cls._receive_event.clear()

            except Exception as e:
                Logger.error(f"Error in receive thread: {e}")
                time.sleep(0.1)

    @classmethod
    def _update_send(cls) -> None:
        """Process outgoing messages"""
        while cls._running:
            try:
                cls._send_event.wait()

                while not cls._outgoing_queue.empty():
                    try:
                        item = cls._outgoing_queue.get_nowait()
                        if item.connection and item.connection.messaging:
                            item.connection.messaging.encrypt_and_write(item.message)
                    except Exception as e:
                        Logger.error(f"Error processing outgoing message: {e}")

                cls._send_event.clear()

            except Exception as e:
                Logger.error(f"Error in send thread: {e}")
                time.sleep(0.1)

    @classmethod
    def shutdown(cls) -> None:
        """Shutdown processor"""
        cls._running = False
        cls._receive_event.set()
        cls._send_event.set()

        if cls._receive_thread and cls._receive_thread.is_alive():
            cls._receive_thread.join(timeout=5)
        if cls._send_thread and cls._send_thread.is_alive():
            cls._send_thread.join(timeout=5)
