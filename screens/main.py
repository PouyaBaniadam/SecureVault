from PySide6.QtCore import Qt, QRect, QEvent
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QMainWindow, QLabel, QListWidget, QListWidgetItem, QMessageBox, QFileDialog

from generator.assets import Assets
from notification.utilities import show_message_box
from screens.add_password import AddPasswordDialog
from screens.master_password_dialog import MasterPasswordDialog
from screens.password_detail import PasswordDetailsDialog
from statics.messages import MESSAGES
from statics.settings import SETTINGS
from themes.buttons.icon_button import IconButton
from themes.buttons.text_icon_button import TextIconButton
from themes.inputs.text_input import TextInput


class SecureVault(QMainWindow):
    def __init__(self, database_utilities):
        super().__init__()

        self.master_password_button = None
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
            on_click=self.import_data
        )

        self.export_button = TextIconButton(
            parent=self,
            text=MESSAGES.EXPORT_DATA,
            icon_path=Assets.export_png,
            on_click=self.export_data,
            x=245,
            y=450,
            w=140,
            h=SETTINGS.BUTTON_HEIGHT,
            border_radius=SETTINGS.BUTTON_BORDER_RADIUS,
            background_color=SETTINGS.PRIMARY_COLOR,
            color=SETTINGS.LIGHT_COLOR,
        )

        self.master_password_button = TextIconButton(
            parent=self,
            icon_path=Assets.lock_png,
            text=MESSAGES.UPDATE_MASTER_PASSWORD,
            x=85,
            y=380,
            w=225,
            h=SETTINGS.BUTTON_HEIGHT,
            on_click=self.show_master_password_dialog,
            border_radius=SETTINGS.BUTTON_BORDER_RADIUS,
            background_color=SETTINGS.PRIMARY_COLOR,
            color=SETTINGS.LIGHT_COLOR,
        )

    def create_search_results_widget(self):
        # Create a QListWidget for search results
        self.results_list = QListWidget(self)
        self.results_list.setGeometry(QRect(30, 100, 300, 200))
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
        self.results_list.setSpacing(1)

        self.results_list.itemClicked.connect(self.on_result_item_clicked)

    def perform_search(self):
        """
        Perform the search based on the current input text and update the list.
        """
        search_query = self.search_input.text().lower()

        if not search_query:
            self.results_list.hide()
            return

        self.results_list.clear()  # Clear previous results

        self.database_utilities.load_all_labels()
        all_labels = self.database_utilities.labels_cache

        filtered_labels = [label for label in all_labels if search_query in label.lower()]

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
        has_errors, message, decrypted_password = self.database_utilities.retrieve_password(label_text)

        if has_errors:
            show_message_box(self, title=MESSAGES.ERROR, icon_type=QMessageBox.Critical, message=message)


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

    def show_master_password_dialog(self):
        dialog = MasterPasswordDialog(self)
        dialog.exec()

    def export_data(self):
        """
        Handle exporting data to a JSON file.
        """
        # Open a file dialog to select the export location
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            caption=MESSAGES.EXPORT_DATA,
            dir="",
            filter="JSON Files (*.json);;All Files (*)"
        )

        if file_path:
            if not file_path.lower().endswith('.json'):
                file_path += '.json'

            has_errors, message = self.database_utilities.export_data_to_json(file_path)

            if has_errors:
                show_message_box(self, title=MESSAGES.ERROR, icon_type=QMessageBox.Critical, message=message)

            else:
                show_message_box(self, title=MESSAGES.SUCCESS, icon_type=QMessageBox.Information, message=message)

    def import_data(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            caption=MESSAGES.IMPORT_DATA,
            dir="",
            filter="JSON Files (*.json);;All Files (*)"
        )

        if file_path:
            has_errors, message = self.database_utilities.import_data_from_json(file_path)
            if has_errors:
                show_message_box(self, title=MESSAGES.ERROR, icon_type=QMessageBox.Critical, message=message)

            else:
                show_message_box(self, title=MESSAGES.SUCCESS, icon_type=QMessageBox.Information, message=message)
