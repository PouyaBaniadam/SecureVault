import sys
from PySide6.QtWidgets import QApplication
from ui import SecureVault

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SecureVault()
    window.show()
    sys.exit(app.exec())
