from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QMainWindow, QLabel

from generator.assets import Assets
from settings import Settings
from themes.buttons.icon_button import IconButton
from themes.buttons.text_icon_button import TextIconButton
from themes.inputs.text_input import TextInput
from utilities import Utilities


class SecureVault(QMainWindow, Utilities, Settings):
    def __init__(self):
        super().__init__()

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
            font_size=14,
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
            w=50,
            h=50,
            on_click=self.print_test,
            background_color=self.primary_color,
            color=self.dark_color,
        )

        self.import_button = TextIconButton(
            parent=self,
            text="Import Data",
            icon_path=Assets.import_png,
            x=30,
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
            x=230,
            y=450,
            w=140,
            h=40,
            border_radius=15,
            on_click=self.print_test,
            background_color=self.primary_color,
            color=self.light_color,
        )
