import string


class SETTINGS:
    # Data base
    DB_NAME = "password_manager.db"

    # UI
    PRIMARY_COLOR = "#5200BA"
    DARK_COLOR = "#1E1E1E"
    LIGHT_COLOR = "#B7B7B7"
    DANGER_COLOR = "#D62323"
    SUCCESS_COLOR = "#31C169"
    WARNING_COLOR = "#FF6E24"
    INFO_COLOR = "#0895DA"

    # Dimensions
    ICON_SIZE = 50
    BUTTON_BORDER_RADIUS = 10
    BUTTON_HEIGHT = 30

    # Password
    GENERIC_PASSWORD_ALLOWED_CHARACTERS = string.ascii_letters + string.digits + string.punctuation
    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 24

    MASTER_PASSWORD = "master_password"