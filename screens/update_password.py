from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QMessageBox, QLabel

from database.utilities import DatabaseUtilities
from generator.assets import Assets
from notification.utilities import show_message_box
from password.utilities import PasswordUtilities
from statics.messages import MESSAGES
from statics.settings import SETTINGS
from themes.buttons.text_button import TextButton
from themes.buttons.text_icon_button import TextIconButton
from themes.inputs.text_input import TextInput
from themes.labels.text_label import TextLabel


class UpdatePasswordDialog(QDialog):
    def __init__(self, current_label, current_password, parent=None):
        super().__init__(parent)
        self.label = QLabel(self)
        self.setWindowTitle("Update Password")
        self.setFixedSize(300, 200)

        self.password_label = current_label
        self.current_password = current_password

        # Set the dialog size before setting the background image
        self.setWindowTitle(MESSAGES.ADD_PASSWORD)
        self.setFixedSize(400, 250)

        self.set_background_image()

        self.password_status = None
        self.generate_password_button = None
        self.input_password = None
        self.label_password = None
        self.label_status = None
        self.input_label = None
        self.save_button = None

        self.password_utilities = PasswordUtilities()

        self.load_base_widgets()

    def set_background_image(self):
        self.label.setPixmap(QPixmap(Assets.dialog_background_png))
        self.label.setGeometry(0, 0, self.width(), self.height())
        self.label.setScaledContents(True)

    def load_base_widgets(self):
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
            default_value=self.current_password,
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
            on_click=self.update_password_in_db,
            background_color=SETTINGS.PRIMARY_COLOR,
            color=SETTINGS.LIGHT_COLOR,
            border_radius=SETTINGS.BUTTON_BORDER_RADIUS,
        )

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

    def update_password_in_db(self):
        new_password = self.input_password.text()

        if not new_password:
            show_message_box(
                self,
                title=MESSAGES.ERROR,
                icon_type=QMessageBox.Critical,
                message=MESSAGES.EMPTY_PASSWORD_ERROR
            )
            return

        database_utilities = DatabaseUtilities()

        has_errors, message = database_utilities.update_password(label=self.password_label, new_plain_password=new_password)

        if has_errors:
            show_message_box(
                self,
                title=MESSAGES.ERROR,
                icon_type=QMessageBox.Critical,
                message=message
            )

        else:
            show_message_box(
                self,
                title=MESSAGES.SUCCESS,
                icon_type=QMessageBox.Information,
                message=MESSAGES.PASSWORD_UPDATE_SUCCESS
            )

            self.parent().password_label.setText(f"{MESSAGES.PASSWORD} : {new_password}")
            self.close()

    def generate_password(self):
        generated_password = self.password_utilities.generate_random_code(
            SETTINGS.MAX_PASSWORD_LENGTH,
            SETTINGS.GENERIC_PASSWORD_ALLOWED_CHARACTERS,
        )

        self.input_password.setText(generated_password)
