class MESSAGES:
    APP_NAME = "Secure vault"
    ADD_PASSWORD = "Add password"
    VALID_LABEL = "This label is valid."
    ALREADY_TAKEN_LABEL = "This label has been already taken."
    SEARCH_LABEL = "Search for label..."
    IMPORT_DATA = "Import data"
    EXPORT_DATA = "Export data"
    GENERATE = "Generate"
    PASSWORD_SAVED = "Your new password has been saved."
    BOTH_LABEL_AND_PASSWORD_REQUIRED = "Both 'Label' and 'Password' fields are required."
    SAVE = "Save"
    CONFIRM = "Confirm"
    KEYRING_USERNAME = "user_master_password"
    SETUP_MASTER_PASSWORD = "Setup Master Password"
    SETUP_MASTER_INFO = """Enter a strong master password for the first time

Remember if you reset your computer, you 
should enter this password again.
So keep it in a safe place."""

    @staticmethod
    def field_is_required(field):
        return f"Field '{field}' is required."

    @staticmethod
    def enter_field(field):
        return f"Enter {field}..."
