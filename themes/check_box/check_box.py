from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox

from themes.ui_utilities import UIUtilities


class TextCheckBox(QCheckBox, UIUtilities):
    """
    Custom checkbox widget with basic styling.
    """

    def __init__(self, parent=None, text="", x=0, y=0, w=0, h=0, **kwargs):
        super().__init__(text, parent)

        self.load_QCheckBoxStyle(**kwargs)

        self.setStyleSheet(
            f"""
             QCheckBox {{
                 color: {self.color};
                 padding: {self.padding}px;
                 font-weight: {self.font_weight};
             }}
             """
        )

        self.setGeometry(x, y, w, h)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(w, h)
