"""
=========================================================
Project G-EXO Desktop
Top Bar Widget
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
)


class TopBar(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QHBoxLayout()

        layout.setContentsMargins(15, 10, 15, 10)

        # =====================================================
        # TITLE
        # =====================================================

        self.title = QLabel("G-EXO")

        

        # =====================================================
        # STATUS
        # =====================================================

        self.status = QLabel("● Connected")

        self.status.setAlignment(Qt.AlignRight)

        

        layout.addWidget(self.title)

        layout.addStretch()

        layout.addWidget(self.status)

        self.setLayout(layout)

        self.setFixedHeight(60)

       