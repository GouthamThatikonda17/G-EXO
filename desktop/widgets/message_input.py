"""
=========================================================
Project G-EXO Desktop
Message Input Widget
Version : 1.1
Developer : Thatikonda Goutham Teja
=========================================================
"""

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QSizePolicy,
)


class MessageInput(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        self.setFixedHeight(80)

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed,
        )

        layout = QHBoxLayout()

        layout.setContentsMargins(15, 15, 15, 15)

        layout.setSpacing(10)

        self.input = QLineEdit()

        self.input.setPlaceholderText(
            "Type your message..."
        )

        self.send_button = QPushButton("Send")

        self.send_button.setMinimumWidth(120)

        self.send_button.setMinimumHeight(45)

        layout.addWidget(self.input)

        layout.addWidget(self.send_button)

        self.setLayout(layout)