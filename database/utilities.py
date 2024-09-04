import sqlite3

from cryptography.exceptions import InvalidTag

from database.queries import Queries
from statics.messages import MESSAGES


class DatabaseUtilities:
    def __init__(self, db_name, encryption_util):
        """
        Initialize the PasswordManager class with a database name and an encryption utility instance.
        """
        self.db_name = db_name
        self.encryption_util = encryption_util
        self.labels_cache = []  # List to cache labels
        self.password_cache = {}  # Optional: Dictionary to cache recently accessed passwords
        self._initialize_database()
        self._load_all_labels()  # Load all labels on initialization

    def _initialize_database(self):
        """Create the database and the passwords table if it doesn't exist."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        # Make sure your table definition includes a field for 'salt'
        cursor.execute(Queries.create_password_table)
        conn.commit()
        conn.close()

    def _load_all_labels(self):
        """Load all labels from the database into memory."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(Queries.load_labels)
        rows = cursor.fetchall()
        conn.close()

        # Populate the labels cache
        self.labels_cache = [row[0] for row in rows]

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
            # Update the labels cache
            self.labels_cache.append(label)
            print(self.labels_cache)
        except sqlite3.IntegrityError:
            print(f"Error: A password with label '{label}' already exists.")
        finally:
            conn.close()

    def retrieve_password(self, label):
        """Retrieve and decrypt a password from the database on demand."""
        has_errors = False
        error_message = ""
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
                error_message = MESSAGES.MASTER_PASSWORD_NOT_THE_SAME

        return has_errors, error_message, decrypted_password

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

    def list_labels(self):
        """List all labels from the in-memory cache."""
        return self.labels_cache

    def get_all_labels(self):
        """Return all labels from the in-memory cache."""
        return self.list_labels()
