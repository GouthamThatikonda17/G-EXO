"""
=========================================================
Project G-EXO Desktop
Robot Face Renderer
Version : 5.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
    QBrush,
)

from behavior.face_state import FaceState


class FaceRenderer:

    def __init__(self):

        self.primary = QColor(0, 220, 255)

        self.listening = QColor(70, 240, 255)

        self.thinking = QColor(180, 220, 255)

        self.error = QColor(255, 70, 70)

    # =====================================================
    # DRAW
    # =====================================================

    def draw(
        self,
        painter,
        width,
        height,
        offset,
        state,
        animator,
    ):

        center_x = width / 2
        center_y = height / 2 - 50

        color = self.get_color(state)

        self.draw_eyebrows(
            painter,
            center_x,
            center_y,
            offset,
            state,
            color,
        )

        self.draw_eyes(
            painter,
            center_x,
            center_y,
            offset,
            state,
            color,
            animator,
        )

        self.draw_mouth(
            painter,
            center_x,
            center_y,
            state,
            color,
        )

    # =====================================================
    # COLORS
    # =====================================================

    def get_color(self, state):

        if state == FaceState.LISTENING:

            return self.listening

        elif state == FaceState.THINKING:

            return self.thinking

        elif state == FaceState.ERROR:

            return self.error

        return self.primary

    # =====================================================
    # EYEBROWS
    # =====================================================

    def draw_eyebrows(
        self,
        painter,
        center_x,
        center_y,
        offset,
        state,
        color,
    ):

        pen = QPen(color)

        pen.setWidth(5)

        painter.setPen(pen)

        left_y = center_y - 75 + offset
        right_y = center_y - 75 + offset

        if state == FaceState.LISTENING:

            left_y -= 8
            right_y -= 8

        elif state == FaceState.THINKING:

            left_y += 5
            right_y += 5

        painter.drawLine(

            center_x - 185,
            left_y,

            center_x - 115,
            left_y - 10,

        )

        painter.drawLine(

            center_x + 115,
            right_y - 10,

            center_x + 185,
            right_y,

        )

    # =====================================================
    # EYES
    # =====================================================

    def draw_eyes(
        self,
        painter,
        center_x,
        center_y,
        offset,
        state,
        color,
        animator,
    ):

        eye_width = 90

        base_height = 60

        if state == FaceState.THINKING:

            base_height = 46

        eye_height = base_height * animator.blink

        eye_height = max(6, eye_height)

        spacing = 160

        glow = QColor(color)

        glow.setAlpha(40)

        painter.setPen(Qt.NoPen)

        painter.setBrush(QBrush(glow))

        painter.drawEllipse(

            QRectF(

                center_x - spacing - 25,

                center_y - 45 + offset,

                140,

                100,

            )

        )

        painter.drawEllipse(

            QRectF(

                center_x + spacing - eye_width - 25,

                center_y - 45 + offset,

                140,

                100,

            )

        )

        pen = QPen(color)

        pen.setWidth(4)

        painter.setPen(pen)

        painter.setBrush(Qt.NoBrush)

        left_eye = QRectF(

            center_x - spacing,

            center_y - eye_height / 2 + offset,

            eye_width,

            eye_height,

        )

        right_eye = QRectF(

            center_x + spacing - eye_width,

            center_y - eye_height / 2 + offset,

            eye_width,

            eye_height,

        )

        painter.drawRoundedRect(

            left_eye,

            20,

            20,

        )

        painter.drawRoundedRect(

            right_eye,

            20,

            20,

        )

        if animator.blink > 0.20:

            painter.setBrush(QBrush(color))

            pupil_size = 22

            if state == FaceState.LISTENING:

                pupil_size = 26

            painter.drawEllipse(

                center_x - spacing + 32 + animator.left_pupil_x,

                center_y - 8 + offset + animator.left_pupil_y,

                pupil_size,

                pupil_size,

            )

            painter.drawEllipse(

                center_x + spacing - eye_width + 36 + animator.right_pupil_x,

                center_y - 8 + offset + animator.right_pupil_y,

                pupil_size,

                pupil_size,

            )

    # =====================================================
    # MOUTH
    # =====================================================

    def draw_mouth(
        self,
        painter,
        center_x,
        center_y,
        state,
        color,
    ):

        pen = QPen(color)

        pen.setWidth(6)

        painter.setPen(pen)

        mouth_width = 35

        if state == FaceState.SPEAKING:

            mouth_width = 24

        painter.drawLine(

            center_x - mouth_width,

            center_y + 105,

            center_x + mouth_width,

            center_y + 105,

        )