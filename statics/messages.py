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
    VALIDATE_MASTER_PASSWORD = "Validate Master Password"
    CURRENT_MASTER_PASSWORD = "Current Master Password"
    NEW_MASTER_PASSWORD = "New master password"
    ENTER_CURRENT_PASSWORD = "Enter current password"
    ENTER_NEW_PASSWORD = "Enter new password"
    CONFIRM_NEW_PASSWORD = "Confirm new password"
    CONFIRM_MASTER_PASSWORD = "Confirm master password"
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
Restarting the app might work until the next update! but if it did not work either,
You do not have access to any of your previous passwords until you give me the previous master password."""
    ERROR = "Error"
    ERROR_HAPPENED = "An error occurred."
    SUCCESS = "Success"
    SUBMIT = "Submit"
    CANCEL = "Cancel"
    PASSWORDS_DO_NOT_MATCH = "Passwords do not match."
    PASSWORD_UPDATE_SUCCESS = "Password updated successfully."
    CURRENT_PASSWORD_INCORRECT = "Current master password is incorrect."
    CONFIRM_PASSWORD_INCORRECT = "Confirm master password is incorrect."
    CONFIRM_PASSWORD_EMPTY = "Confirmation password is empty."
    NEW_PASSWORD_EMPTY = "New password is empty."
    CURRENT_PASSWORD_EMPTY = "Current master password is empty."
    EXPORTED_DATA_SUCCESSFULLY = "All passwords have been exported as a JSON file."
    IMPORTED_DATA_SUCCESSFULLY = "Data imported successfully from JSON file."
    DELETED_SUCCESSFULLY = "Everything deleted successfully."
    DELETE = "Delete"
    DELETION_CONFIRMATION_MESSAGE = "Are you sure you want to delete?"
    DATA_IS_VALID = "Data validated successfully."
    PLEASE_RESTART_THE_APP = "Please restart the previous instance of the app to avoid bugs."
    AGREE_TERMS = "I agree to the terms."
    DELETION_EVERYTHING_CONFIRMATION = "Delete everything confirmation"
    UPDATE = "Update"


    @staticmethod
    def field_is_required(field):
        return f"Field '{field}' is required."

    @staticmethod
    def enter_field(field):
        return f"Enter {field}..."
