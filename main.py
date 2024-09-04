import sys

from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtWidgets import QApplication

from database.utilities import DatabaseUtilities
from encyption.utilities import EncryptionUtils
from generator.assets import Assets
from password.utilities import PasswordUtilities
from screens.main import SecureVault
from screens.setup_master_password import SetupMasterPasswordPage
from statics.settings import SETTINGS

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
        # Initialize Encryption Utilities with the stored master password
        encryption_util = EncryptionUtils(master_password=master_password)

        # Initialize Password Manager with the database name and encryption utilities
        database_utilities = DatabaseUtilities(db_name=SETTINGS.DB_NAME, encryption_util=encryption_util)

        # Load all labels into memory at the beginning
        database_utilities._load_all_labels()  # Load labels at the start

        # Show the main application window
        window = SecureVault(database_utilities)
        window.show()

    sys.exit(app.exec())
