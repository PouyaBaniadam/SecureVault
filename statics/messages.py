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
    UPDATE_MASTER_PASSWORD = "Update Master Password"
    CURRENT_MASTER_PASSWORD = "Current Master Password"
    NEW_MASTER_PASSWORD = "New master password"
    ENTER_CURRENT_PASSWORD = "Enter current password"
    ENTER_NEW_PASSWORD = "Enter new password"
    CONFIRM_NEW_PASSWORD = "Confirm new password"
    RE_ENTER_NEW_PASSWORD = "Re-enter new password"
    SETUP_MASTER_INFO = """Enter a strong master password for the first time

Remember if you reset your computer or
make any unusual changes, you should 
enter this password again. otherwise 
all your passwords are gonna be lost."""
    LABEL = "Label"
    PASSWORD = "Password"
    CLOSE = "Close"
    PASSWORD_COPIED = "Password copied successfully."
    MASTER_PASSWORD_NOT_THE_SAME = """Your current master password is not the same as the previous one.
You do not have access to any of your previous passwords until you give me the previous master password."""
    ERROR = "Error"
    ERROR_HAPPENED = "An error occurred."
    SUBMIT = "Submit"
    CANCEL = "Cancel"

    @staticmethod
    def field_is_required(field):
        return f"Field '{field}' is required."

    @staticmethod
    def enter_field(field):
        return f"Enter {field}..."