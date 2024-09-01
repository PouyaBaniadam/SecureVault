from PySide6.QtWidgets import QMainWindow, QLabel
from PySide6.QtGui import QIcon, QPixmap
from resource_path import ResourcePath

class SecureVault(QMainWindow, ResourcePath):
    def __init__(self):
        super().__init__()

        self.bg_label = None
        self.setWindowTitle("Secure Vault")
        self.setFixedSize(400, 500)

        icon_path = self.lock_path
        self.setWindowIcon(QIcon(icon_path))

        self.set_background_image()

    def set_background_image(self):
        bg_image_path = self.background_path
        bg_pixmap = QPixmap(bg_image_path)

        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(bg_pixmap)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.setScaledContents(True)
