import base64
import json
import os
import sqlite3

from PySide6.QtWidgets import QMessageBox
from cryptography.exceptions import InvalidTag

from database.queries import Queries
from encyption.utilities import EncryptionUtilities
from general.utilities import restart_application
from notification.utilities import show_message_box
from statics.messages import MESSAGES


class DatabaseUtilities:
    def __init__(self, db_name, encryption_utilities):
        """
        Initialize the PasswordManager class with a database name and an encryption utility instance.
        """
        self.db_name = db_name
        self.encryption_util = encryption_utilities
        self.labels_cache = []  # Cache for labels
        self.password_cache = {}  # Cache for passwords
        self._initialize_database()
        self.load_all_labels()  # Load all labels on initialization

    def _initialize_database(self):
        """Create the database and the passwords table if it doesn't exist."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(Queries.create_password_table)
        conn.commit()
        conn.close()

    def load_all_labels(self):
        """Load all labels from the database into memory."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(Queries.load_labels)
        rows = cursor.fetchall()
        conn.close()
        self.labels_cache = [row[0] for row in rows]

    def clear_cache(self):
        """Clear all caches when the master password is changed."""
        self.labels_cache = []
        self.password_cache = {}

    def add_password(self, label, plain_password):
        """Encrypt and add a password to the database and update the labels cache."""
        # Encrypt the password
        encrypted_password, nonce, tag, salt = self.encryption_util.encrypt_password(plain_password)

        # Save to the database
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            # Insert encrypted password, nonce, tag, and salt into the database
            cursor.execute(Queries.add_password, (label, encrypted_password, nonce, tag, salt))
            conn.commit()
            # Update the labels and password caches
            self.labels_cache.append(label)
            self.password_cache[label] = plain_password
        except sqlite3.IntegrityError:
            print(f"Error: A password with label '{label}' already exists.")
        finally:
            conn.close()

    def retrieve_password(self, label):
        """Retrieve and decrypt a password from the database on demand."""
        has_errors = False
        message = ""
        decrypted_password = None

        # If we have the password in the cache, then there is no point of an extra query at all!
        if label in self.password_cache:
            decrypted_password = self.password_cache[label]

        else:
            # Fetch from the database
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(Queries.retrieve_password, (label,))
            row = cursor.fetchone()
            conn.close()

            encrypted_password, nonce, tag, salt = row
            try:
                # Decrypt the password
                decrypted_password = self.encryption_util.decrypt_password(encrypted_password, nonce, tag, salt)
                self.password_cache[label] = decrypted_password

            # This usually happens if the master password is not the same. So we rely on that :)
            except InvalidTag:
                has_errors = True
                message = MESSAGES.MASTER_PASSWORD_NOT_THE_SAME

        return has_errors, message, decrypted_password

    def update_password(self, label, new_plain_password):
        """Update an existing password in the database and clear the cache for the updated label."""
        # Encrypt the new password
        encrypted_password, nonce, tag, salt = self.encryption_util.encrypt_password(new_plain_password)

        # Update in the database
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(Queries.update_password, (encrypted_password, nonce, tag, salt, label))
        conn.commit()
        conn.close()

        # Remove from the cache if it exists
        if label in self.password_cache:
            del self.password_cache[label]

    def delete_password(self, label):
        """Delete a password from the database and update the labels cache."""
        # Remove from the database
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(Queries.delete_password, (label,))
        conn.commit()
        conn.close()

        # Update the labels cache
        if label in self.labels_cache:
            self.labels_cache.remove(label)

        # Remove from the optional cache
        if label in self.password_cache:
            del self.password_cache[label]

    def reencrypt_passwords(self, old_master_password, new_master_password):
        """
        Re-encrypt all stored passwords with the new master password.

        :param old_master_password: The current master password.
        :param new_master_password: The new master password.
        :return: None
        """

        old_encryption_util = EncryptionUtilities(old_master_password)
        new_encryption_util = EncryptionUtilities(new_master_password)

        for label in self.labels_cache:
            # Retrieve the encrypted data for the given label
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(Queries.retrieve_password, (label,))
            row = cursor.fetchone()
            conn.close()

            if not row:
                continue

            encrypted_password, nonce, tag, salt = row

            # Decrypt the password using the old master password
            try:
                decrypted_password = old_encryption_util.decrypt_password(
                    encrypted_password, nonce, tag, salt
                )

            except InvalidTag:
                print(f"Failed to decrypt password for label '{label}' with the old master password.")
                continue

            # Encrypt the password using the new master password
            new_encrypted_password, new_nonce, new_tag, new_salt = new_encryption_util.encrypt_password(
                decrypted_password)

            # Update the database with the newly encrypted password
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(
                Queries.update_password,
                (new_encrypted_password, new_nonce, new_tag, new_salt, label)
            )
            conn.commit()
            conn.close()

            # Update the cache with the newly encrypted password
            self.password_cache[label] = decrypted_password

    def export_data_to_json(self, file_path):
        """
        Export encrypted passwords and their metadata to a JSON file.
        :param file_path: The path where the JSON file will be saved.
        """
        has_errors = False
        message = f"{MESSAGES.EXPORTED_DATA_SUCCESSFULLY} to \n\n{file_path}"

        try:
            # Fetch all data from the database
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(Queries.load_all_passwords)
            rows = cursor.fetchall()
            conn.close()

            data = []
            for label, encrypted_password, nonce, tag, salt in rows:
                data.append(
                    {
                        'label': label,
                        'encrypted_password': base64.b64encode(encrypted_password).decode('utf-8'),
                        'nonce': base64.b64encode(nonce).decode('utf-8'),
                        'tag': base64.b64encode(tag).decode('utf-8'),
                        'salt': base64.b64encode(salt).decode('utf-8')
                    }
                )

            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

        except Exception as e:
            has_errors = True
            message = e

        return has_errors, message

    def import_data_from_json(self, file_path):
        has_errors = False
        message = MESSAGES.IMPORTED_DATA_SUCCESSFULLY

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Clear existing data
            cursor.execute(Queries.delete_password_table)
            conn.commit()

            for item in data:
                label = item.get("label")
                encrypted_password_b64 = item.get("encrypted_password")
                nonce_b64 = item.get("nonce")
                tag_b64 = item.get("tag")
                salt_b64 = item.get("salt")

                try:
                    # Decode from Base64 to bytes
                    encrypted_password = base64.b64decode(encrypted_password_b64)
                    nonce = base64.b64decode(nonce_b64)
                    tag = base64.b64decode(tag_b64)
                    salt = base64.b64decode(salt_b64)

                    # Insert the new data into the database
                    cursor.execute(
                        Queries.add_password,
                        (label, encrypted_password, nonce, tag, salt)
                    )
                    conn.commit()

                except (ValueError, TypeError) as e:
                    has_errors = True
                    message = e

                    conn.close()

            conn.close()

            # Update the labels and password caches
            self.load_all_labels()
            self.clear_cache()

        except Exception as e:
            has_errors = True
            message = e

        return has_errors, message

    @staticmethod
    def delete_database(parent, path):
        os.remove(path=path)
        parent.close()

        restart_application(parent=parent)
