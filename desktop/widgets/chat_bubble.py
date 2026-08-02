"""
=========================================================
Project G-EXO Desktop
Chat Bubble Widget
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)


class ChatBubble(QWidget):

    def __init__(self, sender, message):

        super().__init__()

        self.sender = sender

        self.message = message

        self.setup_ui()

    def setup_ui(self):

        root_layout = QHBoxLayout()

        root_layout.setContentsMargins(10, 5, 10, 5)

        bubble = QWidget()

        bubble.setMaximumWidth(700)

        bubble.setSizePolicy(
            QSizePolicy.Maximum,
            QSizePolicy.Preferred
        )

        bubble_layout = QVBoxLayout()

        bubble_layout.setContentsMargins(15, 12, 15, 12)

        title = QLabel(self.sender)

        title.setStyleSheet("""

            QLabel{

                font-weight:bold;

                color:#00BCD4;

                font-size:13px;

            }

        """)

        message = QLabel(self.message)

        message.setWordWrap(True)

        message.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        message.setStyleSheet("""

            QLabel{

                color:white;

                font-size:14px;

            }

        """)

        bubble_layout.addWidget(title)

        bubble_layout.addWidget(message)

        bubble.setLayout(bubble_layout)

        if self.sender.lower() == "you":

            bubble.setStyleSheet("""

                QWidget{

                    background:#005C6B;

                    border-radius:15px;

                }

            """)

            root_layout.addStretch()

            root_layout.addWidget(bubble)

        else:

            bubble.setStyleSheet("""

                QWidget{

                    background:#1F232B;

                    border-radius:15px;

                }

            """)

            root_layout.addWidget(bubble)

            root_layout.addStretch()

        self.setLayout(root_layout)