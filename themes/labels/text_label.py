from PySide6.QtWidgets import QLabel

from themes.ui_utilities import UIUtilities


class TextLabel(QLabel, UIUtilities):
    """
    This class is for showing a label with text on it.
    """

    def __init__(self, parent=None, text="", x=0, y=0, w=0, h=0, **kwargs):
        super().__init__(text, parent)

        self.load_QLabelStyle(**kwargs)

        self.setStyleSheet(
            f"""
            QLabel {{
                background-color: {self.background_color}; 
                color: {self.color}; 
                font-weight: {self.font_weight};
            }}
            """
        )

        self.setFixedSize(w, h)
        self.setGeometry(x, y, w, h)

    def update_text(self, text):
        self.setText(text)
