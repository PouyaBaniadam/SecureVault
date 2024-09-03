import random
import re
import string

from PySide6.QtWidgets import QDialog, QMessageBox

from database.fake_data import FakeData
from encyption.encryption_utils import EncryptionUtils
from generator.assets import Assets
from messages import Messages
from options import OPTIONS
from settings import Settings
from themes.buttons.text_button import TextButton
from themes.buttons.text_icon_button import TextIconButton
from themes.inputs.text_input import TextInput
from themes.labels.text_label import TextLabel


class BackEnd:
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
            status = Messages.field_is_required(field="Password")
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
            message = Messages.BOTH_LABEL_AND_PASSWORD_REQUIRED
            return False, message

        elif BackEnd.does_label_exist(label_name=label_name):
            message = Messages.ALREADY_TAKEN_LABEL
            return False, message

        else:
            encryption_utils = EncryptionUtils(master_password=Settings.MASTER_PASSWORD)
            encrypted_password, nonce, tag = encryption_utils.encrypt_password(plain_password=plain_password)

            print(encrypted_password, nonce, tag)

            message = Messages.PASSWORD_SAVED
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

        return code


class AddPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(Messages.ADD_PASSWORD)
        self.setFixedSize(400, 250)

        # Label of Input field for label
        self.label_status = TextLabel(
            parent=self,
            text="Label",
            x=10,
            y=0,
            w=60,
            h=30,
        )

        # Input field for label
        self.input_label = TextInput(
            parent=self,
            placeholder_text=Messages.enter_field(field="label"),
            x=10,
            y=30,
            w=380,
            h=30,
            on_text_change=lambda: BackEnd.does_label_exist(self.input_label.text()),
            background_color=Settings.LIGHT_COLOR,
            color=Settings.DARK_COLOR,
            border_color=Settings.LIGHT_COLOR,
            border_radius=Settings.BUTTON_BORDER_RADIUS,
            padding=5,
            selection_background_color=Settings.PRIMARY_COLOR
        )

        # Status label for label input
        self.label_status = TextLabel(
            parent=self,
            text="",
            x=10,
            y=65,
            w=380,
            h=20,
        )

        self.input_label.textChanged.connect(self.on_input_label_changed)

        # Label of Input field for password
        self.label_password = TextLabel(
            parent=self,
            text="Password",
            x=10,
            y=85,
            w=80,
            h=30,
        )

        # Input field for password
        self.input_password = TextInput(
            parent=self,
            placeholder_text=Messages.enter_field(field="password"),
            x=10,
            y=115,
            w=260,
            h=30,
            background_color=Settings.LIGHT_COLOR,
            color=Settings.DARK_COLOR,
            border_color=Settings.LIGHT_COLOR,
            border_radius=Settings.BUTTON_BORDER_RADIUS,
            padding=5,
            selection_background_color=Settings.PRIMARY_COLOR
        )

        self.generate_password_button = TextIconButton(
            parent=self,
            text=Messages.GENERATE,
            icon_path=Assets.generate_password_png,
            on_click=self.generate_password,
            x=275,
            y=115,
            w=120,
            h=30,
            border_radius=Settings.BUTTON_BORDER_RADIUS,
            background_color=Settings.PRIMARY_COLOR,
            color=Settings.LIGHT_COLOR,
        )

        # Status label for password strength
        self.password_status = TextLabel(
            parent=self,
            text="",
            x=10,
            y=150,
            w=380,
            h=20,
        )

        self.input_password.textChanged.connect(self.on_input_password_changed)

        # Save button
        self.save_button = TextButton(
            parent=self,
            text=Messages.SAVE,
            x=100,
            y=200,
            w=200,
            h=30,
            on_click=self.validate_and_save,
            background_color=Settings.PRIMARY_COLOR,
            color=Settings.LIGHT_COLOR,
            border_radius=Settings.BUTTON_BORDER_RADIUS,
        )

    def on_input_label_changed(self):
        """
        Checks if the input label exists and updates the status label.
        """
        label_name = self.input_label.text()

        if label_name != "":
            if BackEnd.does_label_exist(label_name):
                self.label_status.update_text(Messages.ALREADY_TAKEN_LABEL)
                self.label_status.setStyleSheet(f"color: {Settings.DANGER_COLOR};")
            else:
                self.label_status.update_text(Messages.VALID_LABEL)
                self.label_status.setStyleSheet(f"color: {Settings.SUCCESS_COLOR};")
        else:
            self.label_status.update_text(Messages.field_is_required(field="Label"))
            self.label_status.setStyleSheet(f"color: {Settings.DANGER_COLOR};")

    def on_input_password_changed(self):
        """
        Evaluates the strength of the input password and updates the status label.
        """
        password = self.input_password.text()

        # Determine password strength
        strength, color = BackEnd.evaluate_password_strength(password)

        # Update the status label based on strength
        self.password_status.update_text(strength)
        self.password_status.setStyleSheet(f"color: {color};")

    def validate_and_save(self):
        """
        Validates the inputs and saves the data if everything is correct.
        """
        label_name = self.input_label.text()
        plain_password = self.input_password.text()

        is_valid, message = BackEnd.submit_new_data(label_name=label_name, plain_password=plain_password)

        msg_box = QMessageBox(self)
        msg_box.setText(message)

        if is_valid:
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle(OPTIONS.SUCCESS)
            self.accept()

        else:
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle(OPTIONS.ERROR)

        msg_box.exec()

    def generate_password(self):
        # Generate a random password
        generated_password = BackEnd.generate_random_code(
            Settings.MAX_PASSWORD_LENGTH,
            Settings.GENERIC_PASSWORD_ALLOWED_CHARACTERS,
        )

        self.input_password.setText(generated_password)
