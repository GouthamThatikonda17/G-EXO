"""
=========================================================
Project G-EXO Desktop
Eye Tracker
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import time

from PySide6.QtCore import QPointF


class EyeTracker:

    def __init__(self):

        self.mouse = QPointF(0, 0)

        self.last_move = time.time()

        self.idle_target = QPointF(0, 0)

        self.direction = 1

    # =====================================================
    # Mouse
    # =====================================================

    def update_mouse(self, x, y):

        self.mouse.setX(x)

        self.mouse.setY(y)

        self.last_move = time.time()

    # =====================================================
    # Target
    # =====================================================

    def get_offset(self, eye_x, eye_y):

        now = time.time()

        if now - self.last_move > 3:

            self.idle_target.setX(

                self.idle_target.x() + 0.08 * self.direction

            )

            if self.idle_target.x() > 6:

                self.direction = -1

            elif self.idle_target.x() < -6:

                self.direction = 1

            return QPointF(

                self.idle_target.x(),

                self.idle_target.y(),

            )

        dx = (self.mouse.x() - eye_x) * 0.02

        dy = (self.mouse.y() - eye_y) * 0.02

        dx = max(-6, min(6, dx))

        dy = max(-6, min(6, dy))

        return QPointF(dx, dy)