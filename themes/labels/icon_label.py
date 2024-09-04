from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, Qt


class IconLabel(QLabel):
    """
    This class is for showing an icon with a specific size.
    """

    def __init__(self, parent=None, icon_path="", x=0, y=0, w=0, h=0):
        super().__init__(parent)

        # Load and display the icon if provided
        self.setGeometry(x, y, w, h)
        self.setFixedSize(w, h)

        if icon_path:
            self.set_icon(icon_path)

    def set_icon(self, icon_path):
        """
        Sets an icon to the QLabel.

        :param icon_path: Path to the icon image file.
        """
        pixmap = QPixmap(icon_path)
        self.setPixmap(pixmap.scaled(self.width(), self.height()))

        self.setScaledContents(True)
