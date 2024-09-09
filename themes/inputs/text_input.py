from PySide6.QtWidgets import QLineEdit
from themes.ui_utilities import UIUtilities


class TextInput(QLineEdit, UIUtilities):
    def __init__(self, parent=None, placeholder_text="", default_value="", x=0, y=0, w=0, h=0, on_text_change=None, **kwargs):
        super().__init__(parent)

        # Set the placeholder text
        self.setPlaceholderText(placeholder_text)

        # Set the default value
        self.setText(default_value)

        # Apply styles using UIUtilities
        self.load_QLineEditStyle(**kwargs)

        # Set the stylesheet
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

        # Set size and geometry
        self.setFixedSize(w, h)
        self.setGeometry(x, y, w, h)

        # Connect the textChanged signal if a callback is provided
        if on_text_change is not None:
            self.textChanged.connect(on_text_change)
