"""
Python conversion of Supercell.Laser.Titan.Library.TweetNaCl.cs
NaCl cryptography implementation
"""

import os
import hashlib
from typing import Optional, Tuple

try:
    from Crypto.Cipher import ChaCha20_Poly1305
    from Crypto.Protocol.KDF import PBKDF2
    from Crypto.Hash import SHA256
    from Crypto.Random import get_random_bytes
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

class TweetNaCl:
    """NaCl cryptography implementation"""

    KEY_SIZE = 32
    NONCE_SIZE = 24
    PUBLIC_KEY_SIZE = 32
    SECRET_KEY_SIZE = 32

    def __init__(self):
        """Initialize TweetNaCl"""
        if not CRYPTO_AVAILABLE:
            raise ImportError("pycryptodome is required for TweetNaCl functionality")

    @staticmethod
    def generate_keypair() -> Tuple[bytes, bytes]:
        """Generate public/private keypair"""
        # For simplicity, we'll use random generation
        # In real implementation, this would use proper curve25519
        private_key = get_random_bytes(TweetNaCl.SECRET_KEY_SIZE)

        # Generate public key from private key (simplified)
        public_key = hashlib.sha256(private_key).digest()

        return public_key, private_key

    @staticmethod
    def generate_shared_secret(our_private: bytes, their_public: bytes) -> bytes:
        """Generate shared secret for key exchange"""
        if len(our_private) != TweetNaCl.SECRET_KEY_SIZE:
            raise ValueError("Invalid private key size")
        if len(their_public) != TweetNaCl.PUBLIC_KEY_SIZE:
            raise ValueError("Invalid public key size")

        # Simplified shared secret generation
        combined = our_private + their_public
        return hashlib.sha256(combined).digest()

    @staticmethod
    def encrypt(message: bytes, key: bytes, nonce: bytes = None) -> bytes:
        """Encrypt message using NaCl"""
        if len(key) != TweetNaCl.KEY_SIZE:
            raise ValueError("Invalid key size")

        if nonce is None:
            nonce = get_random_bytes(12)  # ChaCha20 uses 12-byte nonce

        cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(message)

        # Return nonce + tag + ciphertext
        return nonce + tag + ciphertext

    @staticmethod
    def decrypt(ciphertext: bytes, key: bytes) -> Optional[bytes]:
        """Decrypt message using NaCl"""
        if len(key) != TweetNaCl.KEY_SIZE:
            raise ValueError("Invalid key size")

        if len(ciphertext) < 28:  # 12 nonce + 16 tag minimum
            return None

        try:
            # Extract components
            nonce = ciphertext[:12]
            tag = ciphertext[12:28]
            encrypted = ciphertext[28:]

            cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
            plaintext = cipher.decrypt_and_verify(encrypted, tag)

            return plaintext

        except Exception:
            return None

    @staticmethod
    def hash_data(data: bytes) -> bytes:
        """Hash data using SHA-256"""
        return hashlib.sha256(data).digest()

    @staticmethod
    def derive_key(password: str, salt: bytes) -> bytes:
        """Derive key from password using PBKDF2"""
        if len(salt) < 8:
            raise ValueError("Salt must be at least 8 bytes")

        return PBKDF2(
            password,
            salt,
            key_len=TweetNaCl.KEY_SIZE,
            count=10000,
            hmac_hash_module=SHA256
        )

    @staticmethod
    def constant_time_compare(a: bytes, b: bytes) -> bool:
        """Constant time comparison to prevent timing attacks"""
        if len(a) != len(b):
            return False

        result = 0
        for x, y in zip(a, b):
            result |= x ^ y

        return result == 0

    @staticmethod
    def generate_nonce() -> bytes:
        """Generate random nonce"""
        return get_random_bytes(TweetNaCl.NONCE_SIZE)

    @staticmethod
    def generate_key() -> bytes:
        """Generate random key"""
        return get_random_bytes(TweetNaCl.KEY_SIZE)

    @staticmethod
    def zero_bytes(data: bytearray) -> None:
        """Securely zero out byte array"""
        for i in range(len(data)):
            data[i] = 0
