import sys

from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtWidgets import QApplication

from database.utilities import DatabaseUtilities
from encyption.utilities import EncryptionUtilities
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

    # Master password loader
    master_password = PasswordUtilities.get_master_password()
    # master_password = PasswordUtilities.delete_master_password()

    # Initializations
    encryption_utilities = EncryptionUtilities(master_password=master_password)
    database_utilities = DatabaseUtilities(db_name=SETTINGS.DB_NAME, encryption_utilities=encryption_utilities)

    # Page loading
    if master_password == "":
        setup_page = SetupMasterPasswordPage(database_utilities=database_utilities)
        setup_page.show()

    else:
        database_utilities.load_all_labels()

        window = SecureVault(database_utilities=database_utilities)
        window.show()

    sys.exit(app.exec())
