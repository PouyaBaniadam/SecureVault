from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QMainWindow, QLabel

from generator.assets import Assets
from statics.messages import MESSAGES
from screens.add_password import AddPasswordDialog
from statics.settings import Settings
from themes.buttons.icon_button import IconButton
from themes.buttons.text_icon_button import TextIconButton
from themes.inputs.text_input import TextInput


class SecureVault(QMainWindow):
    def __init__(self):
        super().__init__()

        self.add_password = None
        self.search_button = None
        self.search_input = None
        self.bg_label = None
        self.import_button = None
        self.export_button = None
        self.setWindowTitle(MESSAGES.APP_NAME)
        self.setFixedSize(400, 500)

        self.setWindowIcon(QIcon(Assets.lock_png))

        self.set_background_image()

        self.load_base_widgets()

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
            background_color=Settings.LIGHT_COLOR,
            color=Settings.DARK_COLOR,
            border_color=Settings.LIGHT_COLOR,
            border_radius=Settings.BUTTON_BORDER_RADIUS,
            padding=5,
            selection_background_color=Settings.PRIMARY_COLOR
        )

        self.search_button = IconButton(
            parent=self,
            icon_path=Assets.search_password_png,
            x=330,
            y=60,
            w=Settings.ICON_SIZE,
            h=Settings.ICON_SIZE,
            background_color=Settings.PRIMARY_COLOR,
            color=Settings.DARK_COLOR,
        )

        self.add_password = IconButton(
            parent=self,
            icon_path=Assets.padlock_png,
            x=175,
            y=440,
            w=Settings.ICON_SIZE,
            h=Settings.ICON_SIZE,
            on_click=self.show_add_password_dialog,  # Connect button click to show the dialog
        )

        self.import_button = TextIconButton(
            parent=self,
            text=MESSAGES.IMPORT_DATA,
            icon_path=Assets.import_png,
            x=15,
            y=450,
            w=140,
            h=Settings.BUTTON_HEIGHT,
            border_radius=Settings.BUTTON_BORDER_RADIUS,
            background_color=Settings.PRIMARY_COLOR,
            color=Settings.LIGHT_COLOR,
        )

        self.export_button = TextIconButton(
            parent=self,
            text=MESSAGES.EXPORT_DATA,
            icon_path=Assets.export_png,
            x=245,
            y=450,
            w=140,
            h=Settings.BUTTON_HEIGHT,
            border_radius=Settings.BUTTON_BORDER_RADIUS,
            background_color=Settings.PRIMARY_COLOR,
            color=Settings.LIGHT_COLOR,
        )

    def show_add_password_dialog(self):
        dialog = AddPasswordDialog(self)
        dialog.exec()
