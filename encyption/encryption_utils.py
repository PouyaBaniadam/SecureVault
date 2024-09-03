import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class EncryptionUtils:
    def __init__(self, master_password):
        """
        Initialize the EncryptionUtils class with a master password.

        :param master_password: The master password to generate the encryption key.
        """
        self.master_password = master_password.encode()
        self.salt = os.urandom(16)
        self.backend = default_backend()
        self.key = self.derive_key(self.master_password, self.salt)

    def derive_key(self, password, salt):
        """
        Derive an encryption key from the master password using PBKDF2.

        :param password: The master password in bytes.
        :param salt: The salt for key derivation.
        :return: The derived encryption key.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=self.backend
        )
        return kdf.derive(password)

    def encrypt_password(self, plain_password):
        """
        Encrypt a plaintext password using AES encryption.

        :param plain_password: The plaintext password to encrypt.
        :return: The encrypted password and the nonce used for encryption.
        """
        # Generate a random nonce (number used once) for AES GCM
        nonce = os.urandom(12)
        cipher = Cipher(algorithms.AES(self.key), modes.GCM(nonce), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plain_password.encode()) + encryptor.finalize()
        return ciphertext, nonce, encryptor.tag

    def decrypt_password(self, ciphertext, nonce, tag):
        """
        Decrypt an AES-encrypted password.

        :param ciphertext: The encrypted password.
        :param nonce: The nonce used for encryption.
        :param tag: The tag used for authentication.
        :return: The decrypted plaintext password.
        """

        cipher = Cipher(algorithms.AES(self.key), modes.GCM(nonce, tag), backend=self.backend)
        decryptor = cipher.decryptor()
        decrypted_password = decryptor.update(ciphertext) + decryptor.finalize()

        return decrypted_password.decode()
