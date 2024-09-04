from PySide6.QtWidgets import QDialog

from generator.assets import Assets
from password.utilities import PasswordUtilities
from statics.messages import MESSAGES
from statics.settings import SETTINGS
from themes.buttons.text_button import TextButton
from themes.buttons.text_icon_button import TextIconButton
from themes.labels.text_label import TextLabel
from themes.labels.icon_label import IconLabel
from themes.inputs.text_input import TextInput


class MasterPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(MESSAGES.UPDATE_MASTER_PASSWORD)
        self.setFixedSize(400, 350)

        # Create an instance of PasswordUtilities
        self.password_utilities = PasswordUtilities()

        self.icon_label = IconLabel(
            parent=self,
            icon_path=Assets.lock_png,
            x=10,
            y=20,
            w=SETTINGS.ICON_SIZE / 1.5,
            h=SETTINGS.ICON_SIZE / 1.5,
        )

        self.old_password_label = TextLabel(
            parent=self,
            text=f"{MESSAGES.CURRENT_MASTER_PASSWORD} : ",
            x=20,
            y=60,
            w=360,
            h=30,
            color=SETTINGS.LIGHT_COLOR,
        )

        self.old_password_input = TextInput(
            parent=self,
            placeholder_text=MESSAGES.ENTER_CURRENT_PASSWORD,
            x=20,
            y=90,
            w=360,
            h=30,
            background_color=SETTINGS.DARK_COLOR,
            color=SETTINGS.LIGHT_COLOR,
            border_color=SETTINGS.PRIMARY_COLOR,
            border_radius=SETTINGS.BUTTON_BORDER_RADIUS,
            padding=5,
            selection_background_color=SETTINGS.PRIMARY_COLOR
        )

        self.new_password_label = TextLabel(
            parent=self,
            text=f"{MESSAGES.NEW_MASTER_PASSWORD} : ",
            x=20,
            y=130,
            w=250,
            h=30,
            color=SETTINGS.LIGHT_COLOR,
        )

        self.new_password_input = TextInput(
            parent=self,
            placeholder_text=MESSAGES.ENTER_NEW_PASSWORD,
            x=20,
            y=160,
            w=250,
            h=30,
            background_color=SETTINGS.DARK_COLOR,
            color=SETTINGS.LIGHT_COLOR,
            border_color=SETTINGS.PRIMARY_COLOR,
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
            y=160,
            w=105,
            h=SETTINGS.BUTTON_HEIGHT,
            border_radius=SETTINGS.BUTTON_BORDER_RADIUS,
            background_color=SETTINGS.PRIMARY_COLOR,
            color=SETTINGS.LIGHT_COLOR,
        )

        self.new_password_status = TextLabel(
            parent=self,
            text="",
            x=20,
            y=190,
            w=360,
            h=20,
        )

        self.confirm_password_label = TextLabel(
            parent=self,
            text=f"{MESSAGES.CONFIRM_NEW_PASSWORD} : ",
            x=20,
            y=220,
            w=360,
            h=30,
            color=SETTINGS.LIGHT_COLOR,
        )

        self.confirm_password_input = TextInput(
            parent=self,
            placeholder_text=MESSAGES.RE_ENTER_NEW_PASSWORD,
            x=20,
            y=250,
            w=360,
            h=30,
            background_color=SETTINGS.DARK_COLOR,
            color=SETTINGS.LIGHT_COLOR,
            border_color=SETTINGS.PRIMARY_COLOR,
            border_radius=SETTINGS.BUTTON_BORDER_RADIUS,
            padding=5,
            selection_background_color=SETTINGS.PRIMARY_COLOR
        )

        self.confirm_password_status = TextLabel(
            parent=self,
            text="",
            x=20,
            y=280,
            w=360,
            h=20,
        )

        self.submit_button = TextButton(
            parent=self,
            text=MESSAGES.SUBMIT,
            x=100,
            y=310,
            w=100,
            h=30,
            on_click=self.submit_changes,
            background_color=SETTINGS.PRIMARY_COLOR,
            color=SETTINGS.LIGHT_COLOR,
            border_radius=SETTINGS.BUTTON_BORDER_RADIUS,
        )

        self.cancel_button = TextButton(
            parent=self,
            text=MESSAGES.CANCEL,
            x=220,
            y=310,
            w=100,
            h=30,
            on_click=self.close,
            background_color=SETTINGS.PRIMARY_COLOR,
            color=SETTINGS.LIGHT_COLOR,
            border_radius=SETTINGS.BUTTON_BORDER_RADIUS,
        )

        self.new_password_input.textChanged.connect(self.on_new_password_changed)
        self.confirm_password_input.textChanged.connect(self.on_confirm_password_changed)

    def on_new_password_changed(self):
        """
        Evaluates the strength of the new password and updates the status label.
        """
        password = self.new_password_input.text()
        strength, color = self.password_utilities.evaluate_password_strength(password)
        self.new_password_status.update_text(strength)
        self.new_password_status.setStyleSheet(f"color: {color};")

    def on_confirm_password_changed(self):
        """
        Evaluates the strength of the confirm-password and updates the status label.
        """
        password = self.confirm_password_input.text()
        strength, color = self.password_utilities.evaluate_password_strength(password)
        self.confirm_password_status.update_text(strength)
        self.confirm_password_status.setStyleSheet(f"color: {color};")

    def generate_password(self):
        generated_password = self.password_utilities.generate_random_code(
            SETTINGS.MAX_PASSWORD_LENGTH,
            SETTINGS.GENERIC_PASSWORD_ALLOWED_CHARACTERS,
        )

        self.new_password_input.setText(generated_password)
        self.confirm_password_input.setText(generated_password)

    def submit_changes(self):
        old_password = self.old_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        self.close()
