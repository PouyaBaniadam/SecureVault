import pyperclip
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QLabel, QMessageBox

from database.utilities import DatabaseUtilities
from generator.assets import Assets
from notification.utilities import show_message_box, show_confirmation_dialog
from statics.messages import MESSAGES
from statics.settings import SETTINGS
from themes.buttons.icon_button import IconButton
from themes.buttons.text_button import TextButton
from themes.labels.icon_label import IconLabel
from themes.labels.text_label import TextLabel


class PasswordDetailsDialog(QDialog):
    def __init__(self, label, password, parent=None):
        super().__init__(parent)
        self.delete_button = None
        self.trash_button = None
        self.bg_label = None
        self.password_label = None
        self.copy_password = None
        self.password_icon = None
        self.label_status = None
        self.tag_icon = None
        self.close_button = None
        self.setWindowTitle("Password Details")
        self.setFixedSize(400, 250)

        self.set_background_image()

        self.label = label
        self.password = password

        self.notification_label = None  # Notification label to show confirmation
        self.load_base_widgets()

    def set_background_image(self):
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap(Assets.dialog_background_png))
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.setScaledContents(True)

    def load_base_widgets(self):
        self.tag_icon = IconLabel(
            parent=self,
            icon_path=Assets.tags_png,
            x=5,
            y=25,
            w=SETTINGS.ICON_SIZE / 1.5,
            h=SETTINGS.ICON_SIZE / 1.5,
        )

        self.label_status = TextLabel(
            parent=self,
            text=f"{MESSAGES.LABEL} : {self.label}",
            x=50,
            y=-35,
            w=365,
            h=150,
        )

        self.password_icon = IconLabel(
            parent=self,
            icon_path=Assets.lock_png,
            x=5,
            y=110,
            w=SETTINGS.ICON_SIZE / 1.5,
            h=SETTINGS.ICON_SIZE / 1.5,
        )

        self.password_label = TextLabel(
            parent=self,
            text=f"{MESSAGES.PASSWORD} : {self.password}",
            x=45,
            y=50,
            w=365,
            h=150,
            word_wrap=True
        )

        self.copy_password = IconButton(
            parent=self,
            icon_path=Assets.copy_png,
            on_click=self.copy_password_to_clipboard,
            x=350,
            y=110,
            w=SETTINGS.ICON_SIZE / 1.25,
            h=SETTINGS.ICON_SIZE / 1.25,
        )

        self.notification_label = TextLabel(
            parent=self,
            text="",
            x=80,
            y=5,
            w=250,
            h=30,
            color=SETTINGS.SUCCESS_COLOR,
        )

        self.close_button = TextButton(
            parent=self,
            text=MESSAGES.CLOSE,
            x=30,
            y=200,
            w=150,
            h=30,
            on_click=self.close,
            background_color=SETTINGS.PRIMARY_COLOR,
            color=SETTINGS.LIGHT_COLOR,
            border_radius=SETTINGS.BUTTON_BORDER_RADIUS,
        )

        self.delete_button = TextButton(
            parent=self,
            text=MESSAGES.DELETE,
            x=210,
            y=200,
            w=150,
            h=30,
            on_click=self.delete_password,
            background_color=SETTINGS.DANGER_COLOR,
            color=SETTINGS.LIGHT_COLOR,
            border_radius=SETTINGS.BUTTON_BORDER_RADIUS,
        )

        self.notification_label.setGeometry(80, 5, 250, 30)
        self.notification_label.hide()

    def copy_password_to_clipboard(self):
        pyperclip.copy(self.password)
        self.show_notification(MESSAGES.PASSWORD_COPIED)

    def show_notification(self, message):
        self.notification_label.setText(message)
        self.notification_label.show()

        QTimer.singleShot(SETTINGS.NOTIFICATION_TIMER, self.hide_notification)

    def hide_notification(self):
        self.notification_label.hide()

    def delete_password(self):
        if show_confirmation_dialog(parent=self, message=MESSAGES.DELETION_CONFIRMATION_MESSAGE):
            database_utilities = DatabaseUtilities()
            database_utilities.delete_password(label=self.label)

            show_message_box(
                self,
                title=MESSAGES.SUCCESS,
                icon_type=QMessageBox.Information,
                message=MESSAGES.DELETED_SUCCESSFULLY
            )

            # Clear the search input in the main window (parent) and hide the results list
            self.parent().clear_search_input()

            self.close()
