"""
=========================================================
Project G-EXO Desktop
Background Widget
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget

from widgets.background.renderer import BackgroundRenderer
from widgets.background.theme import CELL_COUNT


class BackgroundWidget(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.renderer = BackgroundRenderer()

        self.initialized = False

        self.timer = QTimer(self)

        self.timer.timeout.connect(self.animate)

        self.timer.start(16)

    # =====================================================
    # Resize
    # =====================================================

    def resizeEvent(self, event):

        if not self.initialized:

            self.renderer.build(

                self.width(),

                self.height(),

                CELL_COUNT,

            )

            self.initialized = True

        super().resizeEvent(event)

    # =====================================================
    # Animation
    # =====================================================

    def animate(self):

        if not self.initialized:

            return

        self.renderer.update(

            self.width(),

            self.height(),

        )

        self.update()

    # =====================================================
    # Paint
    # =====================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)

        self.renderer.draw(

            painter,

            self.width(),

            self.height(),

        )