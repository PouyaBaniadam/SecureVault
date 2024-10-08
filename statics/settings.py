import os
import string
from pathlib import Path


class SETTINGS:
    # Data base
    @staticmethod
    def get_documents_directory():
        """Get the path to the user's Documents directory, regardless of OS."""
        # For Windows
        if os.name == "nt":
            documents_dir = Path(os.environ["USERPROFILE"]) / "Documents/SecureVault/Database"
        else:  # For macOS and Linux
            documents_dir = Path.home() / "Documents/SecureVault/Database"

        # Ensure the directory exists
        documents_dir.mkdir(parents=True, exist_ok=True)
        return documents_dir

    DB_NAME = str(get_documents_directory() / "password_manager.db")

    # UI
    PRIMARY_COLOR = "#5200BA"
    DARK_COLOR = "#1E1E1E"
    LIGHT_COLOR = "#B7B7B7"
    DANGER_COLOR = "#A50D0D"
    SUCCESS_COLOR = "#31C169"
    WARNING_COLOR = "#FF6E24"
    INFO_COLOR = "#0895DA"
    SHADOW_COLOR = "#151515"

    # Dimensions
    ICON_SIZE = 50
    BUTTON_BORDER_RADIUS = 10
    BUTTON_HEIGHT = 30
    SHADOW_OFFSET = 5

    # Password
    GENERIC_PASSWORD_ALLOWED_CHARACTERS = string.ascii_letters + string.digits + string.punctuation
    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 24
    MASTER_PASSWORD = "master_password"

    # Timer
    NOTIFICATION_TIMER = 5000
