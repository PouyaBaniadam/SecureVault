from PySide6.QtWidgets import QLabel

from themes.ui_utilities import UIUtilities


class TextLabel(QLabel, UIUtilities):
    """
    This class is for showing a label with text on it.
    """

    def __init__(self, parent=None, text="", x=0, y=0, w=0, h=0, word_wrap=False, **kwargs):
        super().__init__(text, parent)

        self.word_wrap = word_wrap  # Store word wrap setting
        self.load_QLabelStyle(**kwargs)

        self.setWordWrap(self.word_wrap)  # Enable or disable word wrapping

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

    def setWordWrap(self, enable):
        """Enable or disable word wrapping for the label."""
        super().setWordWrap(enable)
