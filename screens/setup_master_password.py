from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QMainWindow, QMessageBox, QLabel

from generator.assets import Assets
from password.utilities import PasswordUtilities
from screens.main import SecureVault
from statics.messages import MESSAGES
from statics.settings import SETTINGS
from themes.buttons.text_icon_button import TextIconButton
from themes.check_box.check_box import TextCheckBox
from themes.inputs.text_input import TextInput
from themes.labels.text_label import TextLabel


class SetupMasterPasswordPage(QMainWindow):
    def __init__(self, database_utilities):
        super().__init__()

        self.password_status = None
        self.generate_password_button = None
        self.input_password = None
        self.label_status = None
        self.confirm_button = None
        self.checkbox_agree = None  # Checkbox to confirm agreement
        self.bg_label = None
        self.main_window = None
        self.setWindowTitle(MESSAGES.SETUP_MASTER_PASSWORD)
        self.database_utilities = database_utilities

        self.setFixedSize(400, 300)

        self.set_background_image()

        self.setWindowIcon(QIcon(Assets.lock_png))

        self.load_base_widgets()

    def set_background_image(self):
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap(Assets.dialog_background_png))
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.setScaledContents(True)

    def load_base_widgets(self):
        self.label_status = TextLabel(
            parent=self,
            text=MESSAGES.SETUP_MASTER_INFO,
            x=20,
            y=10,
            w=365,
            h=150,
        )

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
            h=SETTINGS.BUTTON_HEIGHT,
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

        # Custom checkbox to agree before enabling the confirm button
        self.checkbox_agree = TextCheckBox(
            parent=self,
            text=MESSAGES.AGREE_TERMS,
            x=20,
            y=210,
            w=200,
            h=30,
            color=SETTINGS.LIGHT_COLOR,
        )
        self.checkbox_agree.stateChanged.connect(self.on_checkbox_state_changed)

        self.confirm_button = TextIconButton(
            parent=self,
            text=MESSAGES.CONFIRM,
            icon_path=Assets.verified_png,
            on_click=lambda: self.save_password(self.input_password.text()),
            x=130,
            y=250,
            w=120,
            h=SETTINGS.BUTTON_HEIGHT,
            border_radius=SETTINGS.BUTTON_BORDER_RADIUS,
            background_color=SETTINGS.PRIMARY_COLOR,
            color=SETTINGS.LIGHT_COLOR,
            checkbox_color=SETTINGS.PRIMARY_COLOR,
            border_color=SETTINGS.LIGHT_COLOR,
        )
        self.confirm_button.setEnabled(False)

        self.input_password.textChanged.connect(self.on_input_password_changed)

    def on_input_password_changed(self):
        """
        Evaluates the strength of the input password and updates the status label.
        """
        password = self.input_password.text()

        strength, color = PasswordUtilities.evaluate_password_strength(password)

        # Update the status label based on strength
        self.password_status.update_text(strength)
        self.password_status.setStyleSheet(f"color: {color};")

    def on_checkbox_state_changed(self):
        """
        Enable or disable the confirm button based on the checkbox state.
        """
        self.confirm_button.setEnabled(self.checkbox_agree.isChecked())

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
        generated_password = PasswordUtilities.generate_random_code(
            SETTINGS.MAX_PASSWORD_LENGTH,
            SETTINGS.GENERIC_PASSWORD_ALLOWED_CHARACTERS,
        )

        self.input_password.setText(generated_password)
