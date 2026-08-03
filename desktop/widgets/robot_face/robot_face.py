"""
=========================================================
Project G-EXO Desktop
Robot Face Widget
Version : 9.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget

from behavior.face_state import FaceState

from widgets.robot_face.renderer import FaceRenderer
from widgets.robot_face.eye_tracker import EyeTracker
from widgets.robot_face.animation import FaceAnimator


class RobotFace(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setMouseTracking(True)

        self.setAttribute(Qt.WA_TranslucentBackground)

        # =====================================================
        # Renderer
        # =====================================================

        self.renderer = FaceRenderer()

        # =====================================================
        # Systems
        # =====================================================

        self.eye_tracker = EyeTracker()

        self.animator = FaceAnimator()

        self.state = FaceState.IDLE

        # =====================================================
        # Floating Animation
        # =====================================================

        self.offset = 0.0

        self.direction = 1

        # =====================================================
        # Timer
        # =====================================================

        self.timer = QTimer(self)

        self.timer.timeout.connect(self.animate)

        self.timer.start(16)

    # =====================================================
    # State
    # =====================================================

    def set_state(self, state):

        self.state = state

    # =====================================================
    # Mouse
    # =====================================================

    def mouseMoveEvent(self, event):

        self.eye_tracker.update_mouse(

            event.position().x(),

            event.position().y(),

        )

    # =====================================================
    # Animation
    # =====================================================

    def animate(self):

        self.offset += 0.12 * self.direction

        if self.offset >= 4:

            self.direction = -1

        elif self.offset <= -4:

            self.direction = 1

        width = self.width()

        height = self.height()

        center_x = width / 2

        center_y = height / 2 - 50 + self.offset

        eye_spacing = 160

        eye_width = 90

        left_eye_x = center_x - eye_spacing + eye_width / 2

        right_eye_x = center_x + eye_spacing - eye_width / 2

        left_target = self.eye_tracker.get_offset(

            left_eye_x,

            center_y,

        )

        right_target = self.eye_tracker.get_offset(

            right_eye_x,

            center_y,

        )

        self.animator.update(

            left_target,

            right_target,

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

            self.offset,

            self.state,

            self.animator,

        )