"""
=========================================================
Project G-EXO Desktop
Main Window
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import os
import sys

from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)

# =====================================================
# IMPORT G-EXO CORE
# =====================================================

ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from brain.core.dispatcher import Dispatcher
from brain.core.request import Request


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.dispatcher = Dispatcher()

        self.setWindowTitle("G-EXO")

        self.resize(1000, 700)

        self.setup_ui()

        self.setup_connections()

    # =====================================================

    def setup_ui(self):

        central_widget = QWidget()

        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        central_widget.setLayout(main_layout)

        self.chat_area = QTextEdit()

        self.chat_area.setReadOnly(True)

        self.chat_area.setPlaceholderText(
            "Welcome to G-EXO..."
        )

        bottom_layout = QHBoxLayout()

        self.message_input = QLineEdit()

        self.message_input.setPlaceholderText(
            "Type your message..."
        )

        self.send_button = QPushButton("Send")

        bottom_layout.addWidget(self.message_input)

        bottom_layout.addWidget(self.send_button)

        main_layout.addWidget(self.chat_area)

        main_layout.addLayout(bottom_layout)

    # =====================================================

    def setup_connections(self):

        self.send_button.clicked.connect(
            self.send_message
        )

        self.message_input.returnPressed.connect(
            self.send_message
        )

    # =====================================================

    def send_message(self):

        message = self.message_input.text().strip()

        if not message:

            return

        self.chat_area.append(f"You: {message}")

        request = Request(
            message=message,
            source="desktop",
        )

        response = self.dispatcher.dispatch(request)

        self.chat_area.append(
            f"G-EXO: {response.message}"
        )

        self.chat_area.append("")

        self.message_input.clear()