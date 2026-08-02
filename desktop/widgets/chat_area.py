"""
=========================================================
Project G-EXO Desktop
Chat Area Widget
Version : 1.1
Developer : Thatikonda Goutham Teja
=========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QSizePolicy,
)

from widgets.chat_bubble import ChatBubble


class ChatArea(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding,
        )

        self.main_layout = QVBoxLayout()

        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.main_layout)

        self.scroll_area = QScrollArea()

        self.scroll_area.setWidgetResizable(True)

        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.container = QWidget()

        self.chat_layout = QVBoxLayout()

        self.chat_layout.setContentsMargins(
            15,
            15,
            15,
            15,
        )

        self.chat_layout.setSpacing(10)

        self.chat_layout.addStretch()

        self.container.setLayout(
            self.chat_layout
        )

        self.scroll_area.setWidget(
            self.container
        )

        self.main_layout.addWidget(
            self.scroll_area
        )

    def add_message(
        self,
        sender,
        message,
    ):

        bubble = ChatBubble(
            sender,
            message,
        )

        self.chat_layout.insertWidget(
            self.chat_layout.count() - 1,
            bubble,
        )

        scrollbar = self.scroll_area.verticalScrollBar()

        scrollbar.setValue(
            scrollbar.maximum()
        )