import sys

from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtWidgets import QApplication

from generator.assets import Assets
from screens.main import SecureVault
from screens.setup_master_password import SetupMasterPasswordPage
from password.utilities import PasswordUtilities

if __name__ == "__main__":
    # UI loader
    app = QApplication(sys.argv)

    # Global font loader
    font_id = QFontDatabase.addApplicationFont(Assets.ubuntu_ttf)
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    app.setFont(QFont(font_family))

    # Check if there is already a stored master password
    master_password = PasswordUtilities.get_master_password()

    if master_password is None:
        # Show setup page if no password is found
        setup_page = SetupMasterPasswordPage()
        setup_page.show()
    else:
        # Show the main application window if password is found
        window = SecureVault()
        window.show()

    sys.exit(app.exec())
