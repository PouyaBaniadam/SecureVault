from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QMessageBox

from generator.assets import Assets
from password.utilities import PasswordUtilities
from screens.main import SecureVault
from statics.messages import MESSAGES
from statics.settings import SETTINGS
from themes.buttons.text_icon_button import TextIconButton
from themes.inputs.text_input import TextInput
from themes.labels.text_label import TextLabel


class SetupMasterPasswordPage(QMainWindow):
    def __init__(self, database_utilities):
        super().__init__()

        self.main_window = None
        self.setWindowTitle(MESSAGES.SETUP_MASTER_PASSWORD)
        self.database_utilities = database_utilities

        self.setFixedSize(400, 250)

        self.setWindowIcon(QIcon(Assets.lock_png))

        self.label_status = TextLabel(
            parent=self,
            text=MESSAGES.SETUP_MASTER_INFO,
            x=20,
            y=10,
            w=365,
            h=150,
        )

        # Input field for password
        self.input_password = TextInput(
            parent=self,
            placeholder_text=MESSAGES.enter_field(field="password"),
            x=10,
            y=150,
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
            y=150,
            w=120,
            h=30,
            border_radius=SETTINGS.BUTTON_BORDER_RADIUS,
            background_color=SETTINGS.PRIMARY_COLOR,
            color=SETTINGS.LIGHT_COLOR,
        )

        self.password_status = TextLabel(
            parent=self,
            text="",
            x=10,
            y=185,
            w=380,
            h=20,
        )

        self.confirm_button = TextIconButton(
            parent=self,
            text=MESSAGES.CONFIRM,
            icon_path=Assets.verified_png,
            on_click=lambda : self.save_password(self.input_password.text()),
            x=130,
            y=210,
            w=120,
            h=30,
            border_radius=SETTINGS.BUTTON_BORDER_RADIUS,
            background_color=SETTINGS.PRIMARY_COLOR,
            color=SETTINGS.LIGHT_COLOR,
        )

        self.input_password.textChanged.connect(self.on_input_password_changed)

    def on_input_password_changed(self):
        """
        Evaluates the strength of the input password and updates the status label.
        """
        password = self.input_password.text()

        # Determine password strength
        strength, color = PasswordUtilities.evaluate_password_strength(password)

        # Update the status label based on strength
        self.password_status.update_text(strength)
        self.password_status.setStyleSheet(f"color: {color};")

    def save_password(self, master_password: str) -> None:
        if master_password:
            PasswordUtilities.save_master_password(master_password=master_password)
            self.close()

            self.main_window = SecureVault(database_utilities=self.database_utilities)
            self.main_window.show()

        else:
            self.show_error_dialog(MESSAGES.field_is_required("Password"))

    def show_error_dialog(self, message: str):
        """
        Show an error dialog with the given message.
        """
        QMessageBox.critical(self, "Error", message)

    def generate_password(self):
        # Generate a random password
        generated_password = PasswordUtilities.generate_random_code(
            SETTINGS.MAX_PASSWORD_LENGTH,
            SETTINGS.GENERIC_PASSWORD_ALLOWED_CHARACTERS,
        )

        self.input_password.setText(generated_password)
