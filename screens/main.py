from PySide6.QtCore import Qt, QRect, QEvent
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QMainWindow, QLabel, QListWidget, QListWidgetItem, QMessageBox

from generator.assets import Assets
from screens.add_password import AddPasswordDialog
from screens.password_detail import PasswordDetailsDialog
from statics.messages import MESSAGES
from statics.settings import SETTINGS
from themes.buttons.icon_button import IconButton
from themes.buttons.text_icon_button import TextIconButton
from themes.inputs.text_input import TextInput


class SecureVault(QMainWindow):
    def __init__(self, database_utilities):
        super().__init__()

        self.search_input = None
        self.database_utilities = database_utilities

        self.add_password = None
        self.search_button = None
        self.bg_label = None
        self.import_button = None
        self.export_button = None
        self.results_list = None

        self.setWindowTitle(MESSAGES.APP_NAME)
        self.setFixedSize(400, 500)
        self.setWindowIcon(QIcon(Assets.lock_png))

        self.set_background_image()
        self.load_base_widgets()
        self.create_search_results_widget()

        # Connect the search input textChanged signal to perform_search
        self.search_input.textChanged.connect(self.perform_search)

        # Install event filter to detect clicks outside
        self.installEventFilter(self)

    def set_background_image(self):
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap(Assets.background_png))
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.setScaledContents(True)

    def load_base_widgets(self):
        self.search_input = TextInput(
            parent=self,
            placeholder_text=MESSAGES.SEARCH_LABEL,
            x=30,
            y=70,
            w=300,
            h=30,
            background_color=SETTINGS.DARK_COLOR,
            color=SETTINGS.LIGHT_COLOR,
            border_color=SETTINGS.PRIMARY_COLOR,
            border_radius=SETTINGS.BUTTON_BORDER_RADIUS,
            padding=5,
            selection_background_color=SETTINGS.PRIMARY_COLOR
        )

        self.search_button = IconButton(
            parent=self,
            icon_path=Assets.search_password_png,
            x=335,
            y=60,
            w=SETTINGS.ICON_SIZE,
            h=SETTINGS.ICON_SIZE,
            background_color=SETTINGS.PRIMARY_COLOR,
            color=SETTINGS.DARK_COLOR,
        )

        self.add_password = IconButton(
            parent=self,
            icon_path=Assets.padlock_png,
            x=175,
            y=440,
            w=SETTINGS.ICON_SIZE,
            h=SETTINGS.ICON_SIZE,
            on_click=self.show_add_password_dialog,
        )

        self.import_button = TextIconButton(
            parent=self,
            text=MESSAGES.IMPORT_DATA,
            icon_path=Assets.import_png,
            x=15,
            y=450,
            w=140,
            h=SETTINGS.BUTTON_HEIGHT,
            border_radius=SETTINGS.BUTTON_BORDER_RADIUS,
            background_color=SETTINGS.PRIMARY_COLOR,
            color=SETTINGS.LIGHT_COLOR,
        )

        self.export_button = TextIconButton(
            parent=self,
            text=MESSAGES.EXPORT_DATA,
            icon_path=Assets.export_png,
            x=245,
            y=450,
            w=140,
            h=SETTINGS.BUTTON_HEIGHT,
            border_radius=SETTINGS.BUTTON_BORDER_RADIUS,
            background_color=SETTINGS.PRIMARY_COLOR,
            color=SETTINGS.LIGHT_COLOR,
        )

    def create_search_results_widget(self):
        # Create a QListWidget for search results
        self.results_list = QListWidget(self)
        self.results_list.setGeometry(QRect(30, 100, 300, 200))  # Adjust size and position as needed
        self.results_list.setStyleSheet("""
            QListWidget {
                background-color: %s;
                color: %s;
                border: 1px solid %s;
                border-radius: 8px;
            }
            QListWidget::item {
                padding: 10px;
            }
        """ % (SETTINGS.DARK_COLOR, SETTINGS.LIGHT_COLOR, SETTINGS.PRIMARY_COLOR))

        self.results_list.hide()  # Hide the results list initially
        self.results_list.setFocusPolicy(Qt.NoFocus)
        self.results_list.setSpacing(1)  # Optional: Adjust spacing between items

        self.results_list.itemClicked.connect(self.on_result_item_clicked)

    def perform_search(self):
        """
        Perform the search based on the current input text and update the list.
        """
        search_query = self.search_input.text().lower()

        if not search_query:
            self.results_list.hide()  # Hide the results list if search query is empty
            return

        self.results_list.clear()  # Clear previous results

        # Fetch all labels from the database
        all_labels = self.database_utilities.list_labels()

        # Filter labels based on the search query
        filtered_labels = [label for label in all_labels if search_query in label.lower()]

        # Populate the results list
        if filtered_labels:
            self.results_list.show()  # Show the results list if there are results
            for label in filtered_labels:
                item = QListWidgetItem(label)
                self.results_list.addItem(item)
        else:
            self.results_list.hide()  # Hide the results list if no results

    def on_result_item_clicked(self, item):
        """
        Handles the click event on a result item.
        """
        label_text = item.text()
        has_errors, error_message, decrypted_password = self.database_utilities.retrieve_password(label_text)

        if has_errors:
            error_dialog = QMessageBox(self)
            error_dialog.setIcon(QMessageBox.Critical)

            error_dialog.setWindowTitle(MESSAGES.ERROR)
            error_dialog.setText(MESSAGES.ERROR_HAPPENED)
            error_dialog.setInformativeText(error_message)
            error_dialog.exec()

        else:
            # Show the password details dialog
            dialog = PasswordDetailsDialog(label_text, decrypted_password, self)
            dialog.exec()

    def eventFilter(self, obj, event):
        """
        Filter events to hide the results list if clicking outside the search area.
        """
        if event.type() == QEvent.MouseButtonPress:
            if not (self.search_input.rect().contains(event.pos()) or
                    self.results_list.rect().contains(event.pos())):
                self.results_list.hide()  # Hide the results list if clicking outside
        return super().eventFilter(obj, event)

    def show_add_password_dialog(self):
        dialog = AddPasswordDialog(self)
        dialog.exec()
