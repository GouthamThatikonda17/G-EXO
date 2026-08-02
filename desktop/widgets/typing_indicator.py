"""
=========================================================
Project G-EXO Desktop
Typing Indicator Widget
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QSizePolicy,
)


class TypingIndicator(QWidget):

    def __init__(self):

        super().__init__()

        self.frame = 0

        self.setup_ui()

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.animate
        )

    def setup_ui(self):

        root_layout = QHBoxLayout()

        root_layout.setContentsMargins(
            10,
            5,
            10,
            5,
        )

        bubble = QWidget()

        bubble.setMaximumWidth(300)

        bubble.setSizePolicy(
            QSizePolicy.Maximum,
            QSizePolicy.Preferred,
        )

        bubble.setStyleSheet("""

            QWidget{

                background:#1F232B;

                border-radius:15px;

            }

        """)

        bubble_layout = QVBoxLayout()

        bubble_layout.setContentsMargins(
            15,
            12,
            15,
            12,
        )

        title = QLabel("G-EXO")

        title.setStyleSheet("""

            QLabel{

                color:#00D9FF;

                font-size:13px;

                font-weight:bold;

            }

        """)

        self.label = QLabel("Thinking")

        self.label.setAlignment(
            Qt.AlignLeft
        )

        self.label.setStyleSheet("""

            QLabel{

                color:white;

                font-size:14px;

            }

        """)

        bubble_layout.addWidget(title)

        bubble_layout.addWidget(self.label)

        bubble.setLayout(
            bubble_layout
        )

        root_layout.addWidget(
            bubble
        )

        root_layout.addStretch()

        self.setLayout(
            root_layout
        )

    def start(self):

        self.frame = 0

        self.timer.start(400)

    def stop(self):

        self.timer.stop()

    def animate(self):

        self.frame += 1

        dots = "." * (self.frame % 4)

        self.label.setText(
            f"Thinking{dots}"
        )