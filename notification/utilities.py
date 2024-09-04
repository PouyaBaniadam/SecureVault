from PySide6.QtWidgets import QMessageBox


def show_message_box(parent, title, message, icon_type):
    """
    Utility function to display a QMessageBox with the specified message, icon, and title.

    :param parent: The parent widget for the QMessageBox.
    :param message: The message to display in the QMessageBox.
    :param icon_type: The icon type for the QMessageBox (e.g., QMessageBox.Critical, QMessageBox.Information).
    :param title: The title of the QMessageBox.
    """
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setIcon(icon_type)
    msg_box.exec()
