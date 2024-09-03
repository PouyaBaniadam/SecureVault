import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QFont

from generator.assets import Assets
from screens.main import SecureVault

if __name__ == "__main__":
    # UI loader
    app = QApplication(sys.argv)

    # Global font loader
    font_id = QFontDatabase.addApplicationFont(Assets.ubuntu_ttf)
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    app.setFont(QFont(font_family))

    window = SecureVault()
    window.show()
    sys.exit(app.exec())
