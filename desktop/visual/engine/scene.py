"""
=========================================================
Project G-EXO Desktop
Visual Engine Scene
Version : 5.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from PySide6.QtCore import QTimer
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget

from behavior.face_state import FaceState

from .engine import VisualEngine
from .renderer import VisualRenderer
from .face_animator import FaceAnimator


class VisualScene(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.engine = VisualEngine()

        self.renderer = VisualRenderer()

        self.face_animator = FaceAnimator()

        self.state = FaceState.IDLE

        self.timer = QTimer(self)

        self.timer.timeout.connect(self.tick)

        self.timer.start(16)

    # =====================================================
    # State
    # =====================================================

    def set_state(

        self,

        state,

    ):

        self.state = state

        self.face_animator.set_state(

            state,

        )

        self.engine.face_mapper.set_state(

            state,

        )

        self.engine.reset()

    # =====================================================
    # Update
    # =====================================================

    def tick(self):

        if not self.engine.initialized:

            self.engine.initialize(

                self.width(),

                self.height(),

            )

        self.face_animator.update()

        self.engine.update(

            self.face_animator,

        )

        self.update()

    # =====================================================
    # Paint
    # =====================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        self.renderer.render(

            painter,

            self.engine.cubes,

        )

    # =====================================================
    # Resize
    # =====================================================

    def resizeEvent(self, event):

        self.engine.reset()

        super().resizeEvent(event)