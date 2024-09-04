from PySide6.QtWidgets import QDialog, QMessageBox

from generator.assets import Assets
from statics.messages import MESSAGES
from statics.options import OPTIONS
from statics.settings import SETTINGS
from themes.buttons.text_button import TextButton
from themes.buttons.text_icon_button import TextIconButton
from themes.inputs.text_input import TextInput
from themes.labels.text_label import TextLabel
from password.utilities import PasswordUtilities


class AddPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(MESSAGES.ADD_PASSWORD)
        self.setFixedSize(400, 250)

        # Create an instance of PasswordUtilities
        self.password_utilities = PasswordUtilities()

        self.label_status = TextLabel(
            parent=self,
            text="Label",
            x=10,
            y=0,
            w=60,
            h=30,
        )

        self.input_label = TextInput(
            parent=self,
            placeholder_text=MESSAGES.enter_field(field="label"),
            x=10,
            y=30,
            w=380,
            h=30,
            on_text_change=lambda: self.password_utilities.does_label_exist(self.input_label.text()),
            background_color=SETTINGS.LIGHT_COLOR,
            color=SETTINGS.DARK_COLOR,
            border_color=SETTINGS.LIGHT_COLOR,
            border_radius=SETTINGS.BUTTON_BORDER_RADIUS,
            padding=5,
            selection_background_color=SETTINGS.PRIMARY_COLOR
        )

        self.label_status = TextLabel(
            parent=self,
            text="",
            x=10,
            y=65,
            w=380,
            h=20,
        )

        self.input_label.textChanged.connect(self.on_input_label_changed)

        self.label_password = TextLabel(
            parent=self,
            text="Password",
            x=10,
            y=85,
            w=80,
            h=30,
        )

        self.input_password = TextInput(
            parent=self,
            placeholder_text=MESSAGES.enter_field(field="password"),
            x=10,
            y=115,
            w=260,
            h=30,
            background_color=SETTINGS.LIGHT_COLOR,
            color=SETTINGS.DARK_COLOR,
            border_color=SETTINGS.LIGHT_COLOR,
            border_radius=SETTINGS.BUTTON_BORDER_RADIUS,
            padding=5,
            selection_background_color=SETTINGS.PRIMARY_COLOR
        )

        self.generate_password_button = TextIconButton(
            parent=self,
            text=MESSAGES.GENERATE,
            icon_path=Assets.generate_password_png,
            on_click=self.generate_password,
            x=275,
            y=115,
            w=120,
            h=SETTINGS.BUTTON_HEIGHT,
            border_radius=SETTINGS.BUTTON_BORDER_RADIUS,
            background_color=SETTINGS.PRIMARY_COLOR,
            color=SETTINGS.LIGHT_COLOR,
        )

        self.password_status = TextLabel(
            parent=self,
            text="",
            x=10,
            y=150,
            w=380,
            h=20,
        )

        self.input_password.textChanged.connect(self.on_input_password_changed)

        self.save_button = TextButton(
            parent=self,
            text=MESSAGES.SAVE,
            x=100,
            y=200,
            w=200,
            h=30,
            on_click=self.validate_and_save,
            background_color=SETTINGS.PRIMARY_COLOR,
            color=SETTINGS.LIGHT_COLOR,
            border_radius=SETTINGS.BUTTON_BORDER_RADIUS,
        )

    def on_input_label_changed(self):
        """
        Checks if the input label exists and updates the status label.
        """
        label_name = self.input_label.text()

        if label_name != "":
            if self.password_utilities.does_label_exist(label_name):
                self.label_status.update_text(MESSAGES.ALREADY_TAKEN_LABEL)
                self.label_status.setStyleSheet(f"color: {SETTINGS.DANGER_COLOR};")
            else:
                self.label_status.update_text(MESSAGES.VALID_LABEL)
                self.label_status.setStyleSheet(f"color: {SETTINGS.SUCCESS_COLOR};")
        else:
            self.label_status.update_text(MESSAGES.field_is_required(field="Label"))
            self.label_status.setStyleSheet(f"color: {SETTINGS.DANGER_COLOR};")

    def on_input_password_changed(self):
        """
        Evaluates the strength of the input password and updates the status label.
        """
        password = self.input_password.text()

        # Determine password strength
        strength, color = self.password_utilities.evaluate_password_strength(password)

        # Update the status label based on strength
        self.password_status.update_text(strength)
        self.password_status.setStyleSheet(f"color: {color};")

    def validate_and_save(self):
        """
        Validates the inputs and saves the data if everything is correct.
        """
        label_name = self.input_label.text()
        plain_password = self.input_password.text()

        is_valid, message = self.password_utilities.submit_new_data(label_name=label_name, plain_password=plain_password)

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
        generated_password = self.password_utilities.generate_random_code(
            SETTINGS.MAX_PASSWORD_LENGTH,
            SETTINGS.GENERIC_PASSWORD_ALLOWED_CHARACTERS,
        )

        self.input_password.setText(generated_password)
