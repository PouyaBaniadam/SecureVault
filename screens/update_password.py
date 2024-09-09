from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QHBoxLayout, QLineEdit, QVBoxLayout

class UpdatePasswordDialog(QDialog):
    def __init__(self, current_label, current_password, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Update Password")
        self.setFixedSize(300, 200)

        # Create layout
        layout = QVBoxLayout(self)

        # Label edit
        self.label_edit = QLineEdit(self)
        self.label_edit.setText(current_label)
        layout.addWidget(QLabel("Label:", self))
        layout.addWidget(self.label_edit)

        # Password edit
        self.password_edit = QLineEdit(self)
        self.password_edit.setText(current_password)
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Password:", self))
        layout.addWidget(self.password_edit)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.accept)
        buttons_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)