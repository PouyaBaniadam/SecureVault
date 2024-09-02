from typing import Tuple

from database.fake_data import FakeData
from encyption.encryption_utils import EncryptionUtils
from settings import Settings


class Utilities:
    unavailable_label_message = "This label is not available"
    available_label_message = "This label is available."
    both_fields_needed_message = "Please fill both 'label' and 'password' fields."
    password_saved = "Your new password has been saved."

    def __init__(self):
        self.message = None
        self.encryption_utils = EncryptionUtils(master_password=Settings.master_password)

    @staticmethod
    def print_test() -> None:
        """
        A simple function that prints TESTING.
        This is used for testing purposes.
        """
        print("TESTING...")

    @staticmethod
    def print_text(text: str) -> None:
        """
        Prints the current text
        Usually used for input texts.
        """
        print(f"Current Text: {text}")

    def submit_new_data(self, label_name: str, plain_password: str) -> tuple[bool, str]:
        if label_name == "" or plain_password == "":
            self.message = self.both_fields_needed_message

            return False, self.message

        elif self.does_label_exist(label_name=label_name):
            self.message = self.unavailable_label_message

            return False, self.message

        else:
            encrypted_password, nonce, tag = self.encryption_utils.encrypt_password(plain_password=plain_password)

            self.message = self.password_saved

            return True, self.message

    def does_label_exist(self, label_name: str) -> bool:
        exist_flag = False

        for data in FakeData.fake_data:
            if label_name == data["label"]:
                exist_flag = True

        return exist_flag
