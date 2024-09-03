from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QMainWindow, QLabel, QDialog, QVBoxLayout, QMessageBox

from generator.assets import Assets
from settings import Settings
from themes.buttons.icon_button import IconButton
from themes.buttons.text_button import TextButton
from themes.buttons.text_icon_button import TextIconButton
from themes.inputs.text_input import TextInput
from utilities import Utilities


class SecureVault(QMainWindow, Utilities, Settings):
    def __init__(self):
        super().__init__()

        self.add_password = None
        self.search_button = None
        self.search_input = None
        self.bg_label = None
        self.import_button = None
        self.export_button = None
        self.setWindowTitle("Secure Vault")
        self.setFixedSize(400, 500)

        self.setWindowIcon(QIcon(Assets.lock_png))

        self.set_background_image()

        self.load_base_widgets()

    def set_background_image(self):
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap(Assets.background_png))
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.setScaledContents(True)

    def load_base_widgets(self):
        self.search_input = TextInput(
            parent=self,
            placeholder_text="Search for label...",
            x=30,
            y=70,
            w=300,
            h=30,
            on_text_change=lambda: self.print_text(self.search_input.text()),
            background_color=self.light_color,
            color=self.dark_color,
            border_color=self.light_color,
            border_radius=10,
            padding=5,
            selection_background_color=self.primary_color
        )

        self.search_button = IconButton(
            parent=self,
            icon_path=Assets.search_password_png,
            x=330,
            y=60,
            w=Settings.icon_size,
            h=Settings.icon_size,
            on_click=self.print_test,
            background_color=self.primary_color,
            color=self.dark_color,
        )

        self.add_password = IconButton(
            parent=self,
            icon_path=Assets.padlock_png,
            x=175,
            y=448,
            w=Settings.icon_size,
            h=Settings.icon_size,
            on_click=self.show_add_password_dialog,  # Connect button click to show the dialog
        )

        self.import_button = TextIconButton(
            parent=self,
            text="Import Data",
            icon_path=Assets.import_png,
            x=15,
            y=450,
            w=140,
            h=40,
            border_radius=15,
            on_click=self.print_test,
            background_color=self.primary_color,
            color=self.light_color,
        )

        self.export_button = TextIconButton(
            parent=self,
            text="Export Data",
            icon_path=Assets.export_png,
            x=245,
            y=450,
            w=140,
            h=40,
            border_radius=15,
            on_click=self.print_test,
            background_color=self.primary_color,
            color=self.light_color,
        )

    def show_add_password_dialog(self):
        dialog = AddPasswordDialog(self)
        dialog.exec()


class AddPasswordDialog(QDialog, Utilities, Settings):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Password")
        self.setFixedSize(300, 200)

        # Set up the layout for the dialog
        layout = QVBoxLayout()

        self.input_label = TextInput(
            parent=self,
            placeholder_text="Enter a label...",
            x=10,
            y=30,
            w=275,
            h=30,
            on_text_change=lambda: self.does_label_exist(self.input_label.text()),
            background_color=self.light_color,
            color=self.dark_color,
            border_color=self.light_color,
            border_radius=10,
            padding=5,
            selection_background_color=self.primary_color
        )

        self.input_password = TextInput(
            parent=self,
            placeholder_text="Enter password...",
            x=10,
            y=90,
            w=275,
            h=30,
            background_color=self.light_color,
            color=self.dark_color,
            border_color=self.light_color,
            border_radius=10,
            padding=5,
            selection_background_color=self.primary_color
        )

        self.save_button = TextButton(
            parent=self,
            text="Save",
            x=50,
            y=150,
            w=200,
            h=30,
            on_click=self.validate_and_save,
            background_color=self.primary_color,
            color=self.light_color,
            border_radius=10,
        )

    def validate_and_save(self):
        # Get the text from inputs
        label_name = self.input_label.text()
        plain_password = self.input_password.text()

        # Call submit_new_data and get validity and message
        is_valid, message = self.submit_new_data(label_name=label_name, plain_password=plain_password)

        # Show message box based on validity
        msg_box = QMessageBox(self)
        msg_box.setText(message)

        if is_valid:
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("Success")
            self.accept()  # Close the dialog if the data is valid
        else:
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("Error")

        msg_box.exec()  # Display the message box
