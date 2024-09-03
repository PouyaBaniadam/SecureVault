import re

from PySide6.QtWidgets import QDialog, QMessageBox

from database.fake_data import FakeData
from encyption.encryption_utils import EncryptionUtils
from messages import Messages
from options import OPTIONS
from settings import Settings
from themes.buttons.text_button import TextButton
from themes.inputs.text_input import TextInput
from themes.labels.text_label import TextLabel


# TODO: Separate functions from the UI
class AddPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(Messages.ADD_PASSWORD)
        self.setFixedSize(300, 200)

        # Input field for label
        self.input_label = TextInput(
            parent=self,
            placeholder_text=Messages.enter_field(field="label"),
            x=10,
            y=30,
            w=275,
            h=30,
            on_text_change=lambda: self.does_label_exist(self.input_label.text()),
            background_color=Settings.LIGHT_COLOR,
            color=Settings.DARK_COLOR,
            border_color=Settings.LIGHT_COLOR,
            border_radius=10,
            padding=5,
            selection_background_color=Settings.PRIMARY_COLOR
        )

        # Status label for label input
        self.label_status = TextLabel(
            parent=self,
            text="",
            x=10,
            y=50,
            w=250,
            h=50,
        )

        self.input_label.textChanged.connect(self.on_input_label_changed)

        # Input field for password
        self.input_password = TextInput(
            parent=self,
            placeholder_text=Messages.enter_field(field="password"),
            x=10,
            y=90,
            w=275,
            h=30,
            background_color=Settings.LIGHT_COLOR,
            color=Settings.DARK_COLOR,
            border_color=Settings.LIGHT_COLOR,
            border_radius=10,
            padding=5,
            selection_background_color=Settings.PRIMARY_COLOR
        )

        # Status label for password strength
        self.password_status = TextLabel(
            parent=self,
            text="",
            x=10,
            y=110,
            w=250,
            h=50,
        )

        self.input_password.textChanged.connect(self.on_input_password_changed)

        # Save button
        self.save_button = TextButton(
            parent=self,
            text="Save",
            x=50,
            y=150,
            w=200,
            h=30,
            on_click=self.validate_and_save,
            background_color=Settings.PRIMARY_COLOR,
            color=Settings.LIGHT_COLOR,
            border_radius=10,
        )

    def on_input_label_changed(self):
        """
        Checks if the input label exists and updates the status label.
        """
        label_name = self.input_label.text()

        if label_name != "":
            if self.does_label_exist(label_name):
                self.label_status.update_text(Messages.ALREADY_TAKEN_LABEL)
                self.label_status.setStyleSheet(f"color: {Settings.DANGER_COLOR};")
            else:
                self.label_status.update_text(Messages.VALID_LABEL)
                self.label_status.setStyleSheet(f"color: {Settings.SUCCESS_COLOR};")
        else:
            self.label_status.update_text(Messages.field_is_required(field="label"))
            self.label_status.setStyleSheet(f"color: {Settings.DANGER_COLOR};")

    def on_input_password_changed(self):
        """
        Evaluates the strength of the input password and updates the status label.
        """
        password = self.input_password.text()

        # Determine password strength
        strength, color = self.evaluate_password_strength(password)

        # Update the status label based on strength
        self.password_status.update_text(strength)
        self.password_status.setStyleSheet(f"color: {color};")

    @staticmethod
    def evaluate_password_strength(plain_password: str) -> tuple:
        """
        Evaluates the strength of a password and returns a tuple with the strength message and color.
        """

        if plain_password != "":
            if len(plain_password) < 6:
                status = OPTIONS.WEAK
                color = Settings.WARNING_COLOR

            elif len(plain_password) >= 6 and (
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
            status = OPTIONS.EMPTY
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

    def validate_and_save(self):
        """
        Validates the inputs and saves the data if everything is correct.
        """
        label_name = self.input_label.text()
        plain_password = self.input_password.text()

        is_valid, message = self.submit_new_data(label_name=label_name, plain_password=plain_password)

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

    def submit_new_data(self, label_name: str, plain_password: str) -> tuple[bool, str]:
        if label_name == "" or plain_password == "":
            message = Messages.BOTH_LABEL_AND_PASSWORD_REQUIRED

            return False, message

        elif self.does_label_exist(label_name=label_name):
            message = Messages.ALREADY_TAKEN_LABEL

            return False, message

        else:
            encryption_utils = EncryptionUtils(master_password=Settings.MASTER_PASSWORD)
            encrypted_password, nonce, tag = encryption_utils.encrypt_password(plain_password=plain_password)

            print(encrypted_password, nonce, tag)

            message = Messages.PASSWORD_SAVED

            return True, message
