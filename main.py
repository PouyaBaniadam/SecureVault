import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QFont

from database.database_utils import DatabaseUtils
from database.queries import Queries
from settings import Settings
from ui import SecureVault
from resource_path import ResourcePath

if __name__ == "__main__":
    # Database loader
    db_util = DatabaseUtils(Settings.db_name)
    db_util.connect()
    db_util.create_table(Queries.create_password_table)
    db_util.load_sql_to_dict()

    # UI loader
    app = QApplication(sys.argv)

    # Global font loader
    font_id = QFontDatabase.addApplicationFont(ResourcePath.font_path)
    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app.setFont(QFont(font_family))

    window = SecureVault()
    window.show()
    sys.exit(app.exec())
