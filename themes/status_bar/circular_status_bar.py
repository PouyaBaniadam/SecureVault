from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QWidget

from statics.settings import SETTINGS


class CircularStatusBar(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.text = text
        self.setFixedSize(200, 200)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        pen = QPen(QColor(SETTINGS.PRIMARY_COLOR), 7.5)
        painter.setPen(pen)
        painter.drawEllipse(rect.adjusted(10, 10, -10, -10))

        painter.setPen(QColor(SETTINGS.LIGHT_COLOR))
        painter.drawText(rect, Qt.AlignCenter, self.text)
