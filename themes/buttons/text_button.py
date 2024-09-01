from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt

from themes.ui_utilities import UIUtilities


class TextButton(QPushButton, UIUtilities):
    def __init__(self, parent=None, text="", x=0, y=0, w=120, h=40, on_click=None, **kwargs):
        super().__init__(text, parent)

        self.load_QPushButtonStyle(**kwargs)

        darker_color = self.darken_color(self.background_color, factor=0.9)

        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.background_color}; 
                color: {self.color}; 
                font-weight: {self.font_weight};
                border-radius: {self.border_radius}px;
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
