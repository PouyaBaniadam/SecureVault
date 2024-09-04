import random
import re
import string

import keyring
import pyperclip

from database.fake_data import FakeData
from encyption.utilities import EncryptionUtils
from statics.messages import MESSAGES
from statics.options import OPTIONS
from statics.settings import Settings


class PasswordUtilities:
    @staticmethod
    def evaluate_password_strength(plain_password: str) -> tuple:
        """
        Evaluates the strength of a password and returns a tuple with the strength message and color.
        """
        if plain_password != "":
            if len(plain_password) < Settings.MIN_PASSWORD_LENGTH:
                status = OPTIONS.WEAK
                color = Settings.WARNING_COLOR

            elif len(plain_password) >= Settings.MIN_PASSWORD_LENGTH and (
                    re.search("[a-zA-Z]", plain_password) and re.search("[0-9]", plain_password)):
                if len(plain_password) >= 8 and re.search("[!@#$%^&*(),.?\":{}|<>]", plain_password):
                    status = OPTIONS.STRONG
                    color = Settings.SUCCESS_COLOR

                else:
                    status = OPTIONS.NORMAL
                    color = Settings.INFO_COLOR

            else:
                status = OPTIONS.WEAK
                color = Settings.WARNING_COLOR

        else:
            status = MESSAGES.field_is_required(field="Password")
            color = Settings.DANGER_COLOR

        return status, color

    @staticmethod
    def does_label_exist(label_name: str) -> bool:
        """
        Checks if the label already exists in the data.
        """
        label_name = label_name.strip().lower()

        exist_flag = False
        for data in FakeData.fake_data:
            if label_name == data["label"]:
                exist_flag = True

        return exist_flag

    @staticmethod
    def submit_new_data(label_name: str, plain_password: str) -> tuple[bool, str]:
        if label_name == "" or plain_password == "":
            message = MESSAGES.BOTH_LABEL_AND_PASSWORD_REQUIRED
            return False, message

        elif PasswordUtilities.does_label_exist(label_name=label_name):
            message = MESSAGES.ALREADY_TAKEN_LABEL
            return False, message

        else:
            encryption_utils = EncryptionUtils(master_password=Settings.MASTER_PASSWORD)
            encrypted_password, nonce, tag = encryption_utils.encrypt_password(plain_password=plain_password)

            print(encrypted_password, nonce, tag)

            message = MESSAGES.PASSWORD_SAVED
            return True, message

    @staticmethod
    def generate_random_code(code_length: int = Settings.MIN_PASSWORD_LENGTH, *allowed_characters: str) -> str:
        """
        This function generates a random string of characters.
        By default, it generates 8 random digits. But if you prefer more, just give it the arguments!

        optional param code_length: The length of the generated code
        :optional param allowed_characters: A tuple of strings that defines which characters are allowed
        :return: A randomly generated string with at least one letter, one number, and one punctuation
        """

        # Combine all allowed characters into a single string
        allowed_characters: str = "".join(allowed_characters)

        # If no allowed characters are specified, use default allowed characters (digits)
        if len(allowed_characters) == 0:
            allowed_characters = string.digits

        # Ensure that allowed_characters include at least letters, digits, and punctuation
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

        # Generate the remaining characters randomly from the allowed set
        password_chars.extend(random.choice(allowed_characters) for _ in range(code_length - 3))

        # Shuffle the characters to ensure randomness
        random.shuffle(password_chars)

        # Convert list to a string and return
        code = "".join(password_chars)

        # Copy the generated code into clipboard
        pyperclip.copy(text=code)

        return code

    @staticmethod
    def delete_master_password():
        keyring.delete_password(MESSAGES.APP_NAME, MESSAGES.KEYRING_USERNAME)

    @staticmethod
    def get_master_password():
        return keyring.get_password(MESSAGES.APP_NAME, MESSAGES.KEYRING_USERNAME)

    @staticmethod
    def save_master_password(master_password: str):
        keyring.set_password(MESSAGES.APP_NAME, MESSAGES.KEYRING_USERNAME, master_password)
