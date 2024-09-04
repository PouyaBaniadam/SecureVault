import random
import re
import string

import keyring
import pyperclip

from database.utilities import DatabaseUtilities
from encyption.utilities import EncryptionUtils
from statics.messages import MESSAGES
from statics.options import OPTIONS
from statics.settings import SETTINGS


class PasswordUtilities:
    def __init__(self, db_name=SETTINGS.DB_NAME):
        """
        Initialize the PasswordUtilities class with database and encryption utilities.
        """
        # Get master password from keyring or some secure storage
        self.master_password = self.get_master_password()

        # Initialize encryption utilities with the master password
        self.encryption_util = EncryptionUtils(master_password=self.master_password)

        # Initialize password manager
        self.password_manager = DatabaseUtilities(db_name, self.encryption_util)

    @staticmethod
    def evaluate_password_strength(plain_password: str) -> tuple:
        """Evaluates the strength of a password and returns a tuple with the strength message and color."""
        if plain_password != "":
            if len(plain_password) < SETTINGS.MIN_PASSWORD_LENGTH:
                status = OPTIONS.WEAK
                color = SETTINGS.WARNING_COLOR

            elif len(plain_password) >= SETTINGS.MIN_PASSWORD_LENGTH and (
                    re.search("[a-zA-Z]", plain_password) and re.search("[0-9]", plain_password)):
                if len(plain_password) >= 8 and re.search("[!@#$%^&*(),.?\":{}|<>]", plain_password):
                    status = OPTIONS.STRONG
                    color = SETTINGS.SUCCESS_COLOR

                else:
                    status = OPTIONS.NORMAL
                    color = SETTINGS.INFO_COLOR

            else:
                status = OPTIONS.WEAK
                color = SETTINGS.WARNING_COLOR

        else:
            status = MESSAGES.field_is_required(field="Password")
            color = SETTINGS.DANGER_COLOR

        return status, color

    def does_label_exist(self, label_name: str) -> bool:
        """Checks if the label already exists in the database."""
        label_name = label_name.strip().lower()
        labels = self.password_manager.list_labels()
        return label_name in labels

    def submit_new_data(self, label_name: str, plain_password: str) -> tuple[bool, str]:
        """Encrypts and saves a new password to the database."""
        if label_name == "" or plain_password == "":
            message = MESSAGES.BOTH_LABEL_AND_PASSWORD_REQUIRED
            return False, message

        elif self.does_label_exist(label_name=label_name):
            message = MESSAGES.ALREADY_TAKEN_LABEL
            return False, message

        else:
            # Save encrypted password to the database
            self.password_manager.add_password(label_name, plain_password)
            message = MESSAGES.PASSWORD_SAVED
            return True, message

    @staticmethod
    def generate_random_code(code_length: int = SETTINGS.MIN_PASSWORD_LENGTH, *allowed_characters: str) -> str:
        """Generates a random string of characters with at least one letter, one number, and one punctuation."""
        allowed_characters: str = "".join(allowed_characters)

        # Use default allowed characters if none are specified
        if len(allowed_characters) == 0:
            allowed_characters = string.digits

        # Ensure allowed_characters include at least letters, digits, and punctuation
        if not any(char.isalpha() for char in allowed_characters):
            allowed_characters += string.ascii_uppercase
        if not any(char.isdigit() for char in allowed_characters):
            allowed_characters += string.digits
        if not any(char in string.punctuation for char in allowed_characters):
            allowed_characters += string.punctuation

        # Ensure the password has at least one letter, one digit, and one punctuation
        password_chars = [
            random.choice(string.ascii_uppercase),  # At least one letter
            random.choice(string.digits),  # At least one digit
            random.choice(string.punctuation)  # At least one punctuation
        ]

        # Generate remaining characters randomly from the allowed set
        password_chars.extend(random.choice(allowed_characters) for _ in range(code_length - 3))
        random.shuffle(password_chars)  # Shuffle the characters to ensure randomness

        code = "".join(password_chars)
        pyperclip.copy(text=code)  # Copy the generated code to clipboard
        return code

    @staticmethod
    def delete_master_password():
        """Deletes the master password from the keyring."""
        keyring.delete_password(MESSAGES.APP_NAME, MESSAGES.KEYRING_USERNAME)

    @staticmethod
    def get_master_password():
        """Retrieves the master password from the keyring."""
        return keyring.get_password(MESSAGES.APP_NAME, MESSAGES.KEYRING_USERNAME) or ""

    @staticmethod
    def save_master_password(master_password: str):
        """Saves the master password securely in the keyring."""
        keyring.set_password(MESSAGES.APP_NAME, MESSAGES.KEYRING_USERNAME, master_password)