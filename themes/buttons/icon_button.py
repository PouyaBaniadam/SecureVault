from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize

from themes.ui_utilities import UIUtilities


class IconButton(QPushButton, UIUtilities):
    """
    This class creates a button with only an icon on it.
    """
    def __init__(self, parent=None, icon_path="", x=0, y=0, w=0, h=0, on_click=None, **kwargs):
        super().__init__(parent)

        self.load_QPushButtonStyle(**kwargs)

        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(w - 10, h - 10))

        self.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: transparent;
            }
            """
        )

        self.setFixedSize(w, h)

        self.setGeometry(x, y, w, h)

        self.setCursor(Qt.PointingHandCursor)

        self.clicked.connect(on_click)
