from PySide6.QtWidgets import QMainWindow, QLabel
from PySide6.QtGui import QIcon, QPixmap
from resource_path import ResourcePath
from themes.buttons.icon_button import IconButton
from utilities import Utilities


class SecureVault(QMainWindow, ResourcePath, Utilities):
    def __init__(self):
        super().__init__()

        self.bg_label = None
        self.import_button = None
        self.export_button = None
        self.setWindowTitle("Secure Vault")
        self.setFixedSize(400, 500)

        icon_path = self.lock_path
        self.setWindowIcon(QIcon(icon_path))

        self.set_background_image()

        self.import_button = IconButton(
            parent=self,
            text="Import Data",
            icon_path=self.import_path,
            x=30,
            y=450,
            w=140,
            h=40,
            border_radius=15,
            on_click=self.print_test,
            background_color="#5200BA",
            color="#ffffff",
        )

        self.export_button = IconButton(
            parent=self,
            text="Export Data",
            icon_path=self.export_path,
            x=230,
            y=450,
            w=140,
            h=40,
            border_radius=15,
            on_click=self.print_test,
            background_color="#5200BA",
            color="#ffffff",
        )

    def set_background_image(self):
        bg_image_path = self.background_path
        bg_pixmap = QPixmap(bg_image_path)

        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(bg_pixmap)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.setScaledContents(True)
