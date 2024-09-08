import os
import sys
from PySide6.QtWidgets import QMessageBox

from notification.utilities import show_message_box
from statics.messages import MESSAGES


def restart_application(parent):
    """Restarts the application after showing an information message."""

    # Show an information message before restarting
    result = show_message_box(
        parent=parent,
        title=MESSAGES.SUCCESS,
        icon_type=QMessageBox.Information,
        message=f"{MESSAGES.DELETED_SUCCESSFULLY}\n{MESSAGES.APP_RESTARTS_NOW}",
    )

    # Check if the user clicked "OK"
    if result == QMessageBox.Ok:
        # Close the current application window
        parent.close()

        # Re-execute the current Python script
        python = sys.executable
        os.execl(python, python, *sys.argv)
