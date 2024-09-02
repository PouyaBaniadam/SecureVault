from PySide6.QtWidgets import QMainWindow, QLabel
from PySide6.QtGui import QIcon, QPixmap
from resource_path import ResourcePath
from settings import BaseSettings
from themes.buttons.icon_button import IconButton
from themes.buttons.text_icon_button import TextIconButton
from themes.inputs.text_input import TextInput
from utilities import Utilities


class SecureVault(QMainWindow, ResourcePath, Utilities, BaseSettings):
    def __init__(self):
        super().__init__()

        self.search_button = None
        self.search_input = None
        self.bg_label = None
        self.import_button = None
        self.export_button = None
        self.setWindowTitle("Secure Vault")
        self.setFixedSize(400, 500)

        icon_path = self.lock_path
        self.setWindowIcon(QIcon(icon_path))

        self.set_background_image()

        self.load_base_widgets()

    def set_background_image(self):
        bg_image_path = self.background_path
        bg_pixmap = QPixmap(bg_image_path)

        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(bg_pixmap)
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
            on_enter=self.print_test,
            background_color="#FFFFFF",
            color="#000000",
            font_size=14,
            border_color="#dddddd",
            border_radius=10,
            padding=5,
            selection_background_color=self.primary_color
        )

        self.search_button = IconButton(
            parent=self,
            icon_path=self.search_password,
            x=330,
            y=60,
            w=50,
            h=50,
            on_click=self.print_test,
            background_color=self.primary_color,
            color="#000000",
        )

        self.import_button = TextIconButton(
            parent=self,
            text="Import Data",
            icon_path=self.import_path,
            x=30,
            y=450,
            w=140,
            h=40,
            border_radius=15,
            on_click=self.print_test,
            background_color=self.primary_color,
            color="#ffffff",
        )

        self.export_button = TextIconButton(
            parent=self,
            text="Export Data",
            icon_path=self.export_path,
            x=230,
            y=450,
            w=140,
            h=40,
            border_radius=15,
            on_click=self.print_test,
            background_color=self.primary_color,
            color="#ffffff",
        )
