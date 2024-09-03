class Messages:
    APP_NAME = "Secure vault"
    ADD_PASSWORD = "Add password"

    VALID_LABEL = "This label is valid."
    ALREADY_TAKEN_LABEL = "This label has been already taken."
    SEARCH_LABEL = "Search for label..."
    IMPORT_DATA = "Import data"
    EXPORT_DATA = "Export data"
    PASSWORD_SAVED = "Your new password has been saved."
    BOTH_LABEL_AND_PASSWORD_REQUIRED = "Both 'label' and 'password' fields are required."

    @staticmethod
    def field_is_required(field):
        return f"Field '{field}' is required."

    @staticmethod
    def enter_field(field):
        return f"Enter {field}..."
