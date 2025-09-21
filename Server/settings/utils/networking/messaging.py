"""
Python conversion of Supercell.Laser.Server.Networking.Messaging.cs (simplified)
Message encryption and processing
"""

import secrets
import hashlib
from typing import Optional
import struct

from logic.message.game_message import GameMessage
from logic.message.account.auth.authentication_failed_message import AuthenticationFailedMessage
from message.processor import Processor
from message.message_factory import MessageFactory
from titan.debug.debugger import Debugger
from logger import Logger

class StreamEncrypter:
    """Simplified stream encrypter"""
    def __init__(self, key: bytes, nonce: bytes):
        self.key = key
        self.nonce = nonce

    def encrypt(self, data: bytes, output: bytes, length: int) -> int:
        # Simplified encryption
        return 0

    def decrypt(self, data: bytes, output: bytes, length: int) -> int:
        # Simplified decryption  
        return 0

    def get_encryption_overhead(self) -> int:
        return 16

class PepperEncrypter(StreamEncrypter):
    """Pepper encryption implementation"""
    pass

class TweetNaCl:
    """Simplified TweetNaCl crypto functions"""

    @staticmethod
    def random_bytes(buffer: bytes) -> None:
        buffer[:] = secrets.token_bytes(len(buffer))

    @staticmethod
    def crypto_scalarmult_base(private_key: bytes) -> bytes:
        return secrets.token_bytes(32)

    @staticmethod
    def crypto_box_beforenm(public_key: bytes, private_key: bytes) -> bytes:
        return secrets.token_bytes(32)

    @staticmethod
    def crypto_box_open_afternm(ciphertext: bytes, nonce: bytes, shared_secret: bytes) -> bytes:
        return secrets.token_bytes(len(ciphertext) - 16)

    @staticmethod
    def crypto_box_afternm(plaintext: bytes, nonce: bytes, shared_secret: bytes) -> bytes:
        return secrets.token_bytes(len(plaintext) + 16)

class Blake2BHasher:
    """Simplified Blake2B hasher"""
    def __init__(self):
        self.hasher = hashlib.blake2b()

    def update(self, data: bytes) -> None:
        self.hasher.update(data)

    def finish(self) -> bytes:
        return self.hasher.digest()[:24]

class Messaging:
    """Message encryption and processing"""

    def __init__(self, connection):
        """Initialize messaging"""
        from networking.connection import Connection
        self.connection: Connection = connection
        self.message_factory = MessageFactory.instance

        self.pepper_state = 2
        self.seed = 0
        self.disable_crypto = False

        # Crypto keys and nonces
        self.session_token = secrets.token_bytes(24)
        self.s_nonce = secrets.token_bytes(24) 
        self.secret_key = secrets.token_bytes(32)

        self.server_private_key = bytes([158, 217, 110, 5, 87, 249, 222, 234, 204, 121, 177, 228, 59, 79, 93, 217, 25, 33, 113, 185, 119, 171, 205, 246, 11, 185, 185, 22, 140, 152, 107, 20])
        self.server_public_key = TweetNaCl.crypto_scalarmult_base(self.server_private_key)

        self.r_nonce: Optional[bytes] = None
        self.client_pk: Optional[bytes] = None
        self.s: Optional[bytes] = None

        self.encrypter: Optional[StreamEncrypter] = None
        self.decrypter: Optional[StreamEncrypter] = None

    def send(self, message: GameMessage) -> None:
        """Send message"""
        Debugger.print_log(f"{message.__class__.__name__} sent!")

        if message.get_message_type() == 20100:
            self.encrypt_and_write(message)
        else:
            Processor.send(self.connection, message)

    def encrypt_and_write(self, message: GameMessage) -> None:
        """Encrypt and write message"""
        if message.get_encoding_length() == 0:
            message.encode()

        payload = message.get_message_bytes()
        message_type = message.get_message_type()
        version = message.get_version()

        # Handle encryption based on pepper state
        if not self.disable_crypto:
            if self.pepper_state == 4:
                payload = self._send_pepper_login_response(payload)
            elif self.pepper_state == 5 and self.encrypter:
                encrypted = bytearray(len(payload) + self.encrypter.get_encryption_overhead())
                self.encrypter.encrypt(payload, encrypted, len(payload))
                payload = bytes(encrypted)

        # Create stream with header
        length = len(payload)
        stream = bytearray(length + 7)

        # Pack header
        struct.pack_into('>HHH', stream, 0, message_type, length, version)
        stream[7:] = payload

        self.connection.write(bytes(stream))

    def on_receive(self) -> int:
        """Handle received data"""
        try:
            memory = self.connection.memory
            if len(memory.getvalue()) < 7:
                return 0

            position = memory.tell()
            memory.seek(0)

            # Read header
            header = memory.read(7)
            message_type, length, version = struct.unpack('>HHH', header)

            # Check if full message received
            if len(memory.getvalue()) - 7 < length:
                memory.seek(position)
                return 0

            # Read payload
            payload = memory.read(length)

            # Process message
            result = self._read_new_message(message_type, length, version, payload)

            # Update memory stream
            remaining = memory.read()
            memory.close()
            from io import BytesIO
            self.connection.memory = BytesIO(remaining)

            # Process more messages if available
            if len(remaining) >= 7:
                self.on_receive()

            return result

        except Exception as e:
            Logger.error(f"Error in on_receive: {e}")
            return -1

    def _read_new_message(self, message_type: int, length: int, version: int, payload: bytes) -> int:
        """Process new message"""
        try:
            if message_type != 10504:  # Not friend list request
                Debugger.print_log(f"{message_type} received! (version {version})")

            # Handle pepper authentication
            if self.pepper_state == 2 and message_type == 10101:
                self.disable_crypto = True

            if not self.disable_crypto:
                if self.pepper_state == 2:
                    if message_type == 10100:
                        self.pepper_state = 3
                    else:
                        self.connection.send(AuthenticationFailedMessage(
                            error_code=8,
                            update_url="https://github.com/allbrawl/ProjectColette-public"
                        ))
                        return -1
                elif self.pepper_state == 3:
                    if message_type != 10101:
                        return -1
                    payload = self._handle_pepper_login(payload)
                    if not payload:
                        return -1
                elif self.pepper_state == 5 and self.decrypter:
                    decrypted = bytearray(length - self.decrypter.get_encryption_overhead())
                    result = self.decrypter.decrypt(payload, decrypted, length)
                    if result != 0:
                        return -1
                    payload = bytes(decrypted)

            # Create message and process
            message = self.message_factory.create_message_by_type(message_type)
            if message:
                message.get_byte_stream().set_byte_array(payload, len(payload))
                message.decode()

                if message_type == 10100:
                    self.connection.message_manager.receive_message(message)
                else:
                    Processor.receive(self.connection, message)

            return 0

        except Exception as e:
            Logger.error(f"Error processing message {message_type}: {e}")
            return -1

    def _handle_pepper_login(self, payload: bytes) -> Optional[bytes]:
        """Handle pepper login authentication"""
        try:
            self.client_pk = payload[:32]
            hasher = Blake2BHasher()
            hasher.update(self.client_pk)
            hasher.update(self.server_public_key)
            nonce = hasher.finish()

            self.s = TweetNaCl.crypto_box_beforenm(self.client_pk, self.server_private_key)
            decrypted = TweetNaCl.crypto_box_open_afternm(payload[32:], nonce, self.s)

            self.pepper_state = 4
            self.r_nonce = decrypted[24:48]

            return decrypted[48:]

        except Exception:
            Logger.error("Failed to decrypt 10101")
            return None

    def _send_pepper_login_response(self, payload: bytes) -> bytes:
        """Send pepper login response"""
        packet = bytearray(len(payload) + 32 + 24)
        packet[:24] = self.s_nonce
        packet[24:56] = self.secret_key
        packet[56:] = payload

        hasher = Blake2BHasher()
        hasher.update(self.r_nonce)
        hasher.update(self.client_pk)
        hasher.update(self.server_public_key)
        nonce = hasher.finish()

        encrypted = TweetNaCl.crypto_box_afternm(bytes(packet), nonce, self.s)

        self.pepper_state = 5
        self.decrypter = PepperEncrypter(self.secret_key, self.r_nonce)
        self.encrypter = PepperEncrypter(self.secret_key, self.s_nonce)

        return encrypted
