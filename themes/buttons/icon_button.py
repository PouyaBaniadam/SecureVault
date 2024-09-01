from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize

from themes.ui_utilities import UIUtilities


class IconButton(QPushButton, UIUtilities):
    def __init__(self, parent=None, text="", icon_path="", x=0, y=0, w=0, h=0, on_click=None, **kwargs):
        super().__init__(text, parent)

        self.load_QPushButtonStyle(**kwargs)

        darker_color = self.darken_color(self.background_color, factor=0.9)

        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(w - 10, h - 10))

        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.background_color}; 
                color: {self.color}; 
                font-weight: {self.font_weight};
                border-radius: {self.border_radius}px;
                padding: {self.padding}px;
                text-align: {self.text_align};
            }}
            QPushButton:hover {{
                background-color: {darker_color};
            }}
            """
        )

        self.setFixedSize(w, h)

        self.setGeometry(x, y, w, h)

        self.setCursor(Qt.PointingHandCursor)

        self.clicked.connect(on_click)
