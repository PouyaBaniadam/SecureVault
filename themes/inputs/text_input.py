from PySide6.QtWidgets import QLineEdit

from themes.ui_utilities import UIUtilities


class TextInput(QLineEdit, UIUtilities):
    def __init__(self, parent=None, placeholder_text="", x=0, y=0, w=0, h=0, on_enter=None, **kwargs):
        super().__init__(parent)

        self.setPlaceholderText(placeholder_text)

        self.load_QLineEditStyle(**kwargs)

        self.setStyleSheet(
            f"""
            QLineEdit {{
                background-color: {self.background_color}; 
                color: {self.color}; 
                font-size: {self.font_size}px;
                border: 1px solid {self.border_color};
                border-radius: {self.border_radius}px;
                padding: {self.padding}px;
                selection-color: {self.selection_color};
                selection-background-color: {self.selection_background_color};
            }}
            """
        )

        self.setFixedSize(w, h)
        self.setGeometry(x, y, w, h)

        if on_enter:
            self.returnPressed.connect(on_enter)
