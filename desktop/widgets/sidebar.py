"""
=========================================================
Project G-EXO Desktop
Sidebar Widget
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class Sidebar(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(15, 20, 15, 20)

        layout.setSpacing(15)

        title = QLabel("G-EXO")

        title.setStyleSheet("""

            QLabel{

                color:white;

                font-size:24px;

                font-weight:bold;

            }

        """)

        layout.addWidget(title)

        layout.addSpacing(20)

        buttons = [

            "💬 Chats",

            "🧠 Memory",

            "📋 Tasks",

            "📝 Notes",

            "📁 Files",

            "⚙ Settings",

        ]

        for text in buttons:

            button = QPushButton(text)

            button.setMinimumHeight(42)

            button.setStyleSheet("""

                QPushButton{

                    background:#1D1D1D;

                    color:white;

                    border:none;

                    border-radius:8px;

                    text-align:left;

                    padding-left:15px;

                    font-size:14px;

                }

                QPushButton:hover{

                    background:#00BCD4;

                    color:black;

                }

            """)

            layout.addWidget(button)

        layout.addStretch()

        self.setLayout(layout)

        self.setFixedWidth(220)

        self.setStyleSheet("""

            QWidget{

                background:#111111;

                border-right:1px solid #2D2D2D;

            }

        """)