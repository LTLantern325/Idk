"""
Python conversion of Supercell.Laser.Titan.Cryptography.StreamEncrypter.cs
Stream encryption for network communication
"""

import hashlib
from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Random import get_random_bytes

class StreamEncrypter:
    """Stream encryption for secure network communication"""

    def __init__(self):
        """Initialize stream encrypter"""
        self.key = None
        self.nonce_counter = 0

    def initialize(self, shared_key: bytes) -> None:
        """Initialize with shared key"""
        if len(shared_key) == 32:
            self.key = shared_key
        else:
            # Derive 32-byte key from input
            self.key = hashlib.sha256(shared_key).digest()

        self.nonce_counter = 0

    def generate_nonce(self) -> bytes:
        """Generate nonce for encryption"""
        self.nonce_counter += 1
        nonce = self.nonce_counter.to_bytes(8, 'little')
        nonce += get_random_bytes(4)  # Add random bytes
        return nonce

    def encrypt_stream(self, plaintext: bytes) -> bytes:
        """Encrypt data stream"""
        if not self.key:
            raise ValueError("Stream encrypter not initialized")

        # Generate nonce
        nonce = self.generate_nonce()

        # Create cipher
        cipher = ChaCha20_Poly1305.new(key=self.key, nonce=nonce)

        # Encrypt and get authentication tag
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)

        # Return nonce + tag + ciphertext
        return nonce + tag + ciphertext

    def decrypt_stream(self, encrypted_data: bytes) -> bytes:
        """Decrypt data stream"""
        if not self.key:
            raise ValueError("Stream encrypter not initialized")

        if len(encrypted_data) < 28:  # 12 nonce + 16 tag minimum
            raise ValueError("Invalid encrypted stream data")

        # Extract components
        nonce = encrypted_data[:12]
        tag = encrypted_data[12:28]
        ciphertext = encrypted_data[28:]

        # Create cipher
        cipher = ChaCha20_Poly1305.new(key=self.key, nonce=nonce)

        # Decrypt and verify
        try:
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            return plaintext
        except ValueError:
            raise ValueError("Decryption failed - invalid tag or corrupted data")

    def encrypt_packet(self, packet_data: bytes, packet_id: int) -> bytes:
        """Encrypt network packet"""
        # Add packet ID to data
        packet_with_id = packet_id.to_bytes(2, 'big') + packet_data
        return self.encrypt_stream(packet_with_id)

    def decrypt_packet(self, encrypted_packet: bytes) -> tuple[int, bytes]:
        """Decrypt network packet and return (packet_id, data)"""
        decrypted = self.decrypt_stream(encrypted_packet)

        if len(decrypted) < 2:
            raise ValueError("Invalid packet data")

        packet_id = int.from_bytes(decrypted[:2], 'big')
        packet_data = decrypted[2:]

        return packet_id, packet_data

    def reset_nonce_counter(self) -> None:
        """Reset nonce counter"""
        self.nonce_counter = 0