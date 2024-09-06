from PySide6.QtWidgets import QListWidget
from PySide6.QtCore import QRect, Qt

from themes.ui_utilities import UIUtilities


class ListWidget(QListWidget, UIUtilities):
    def __init__(self, parent=None, x=30, y=100, w=300, h=200, **kwargs):
        super().__init__(parent)

        self.load_ListWidget(**kwargs)

        self.setStyleSheet(
            f"""
            QListWidget {{
                background-color: {self.background_color};
                color: {self.color};
                border: 1px solid {self.border_color};
                border-radius: {self.border_radius}px;
            }}
            QListWidget::item {{
                padding: {self.padding}px;
            }}
            """
        )

        self.setGeometry(QRect(x, y, w, h))

        self.hide()

        self.setSpacing(5)
