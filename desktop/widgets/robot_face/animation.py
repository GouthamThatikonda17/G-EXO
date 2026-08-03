"""
=========================================================
Project G-EXO Desktop
Face Animator
Version : 3.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import random
import time

from PySide6.QtCore import QPointF


class FaceAnimator:

    def __init__(self):

        # =====================================================
        # Pupils
        # =====================================================

        self.left_pupil_x = 0.0
        self.left_pupil_y = 0.0

        self.right_pupil_x = 0.0
        self.right_pupil_y = 0.0

        # =====================================================
        # Blink
        # =====================================================

        self.blink = 1.0

        self.next_blink = time.time() + random.uniform(3.0, 7.0)

        self.blink_speed = 0.18

        self.closing = False

        self.opening = False

        # =====================================================
        # Idle
        # =====================================================

        self.idle_offset = QPointF(0.0, 0.0)

        self.last_idle_change = time.time()

        self.idle_target = QPointF(0.0, 0.0)

    # =====================================================
    # Update
    # =====================================================

    def update(self, left_target, right_target):

        self.update_idle()

        left_target += self.idle_offset

        right_target += self.idle_offset

        speed = 0.15

        self.left_pupil_x += (
            left_target.x() - self.left_pupil_x
        ) * speed

        self.left_pupil_y += (
            left_target.y() - self.left_pupil_y
        ) * speed

        self.right_pupil_x += (
            right_target.x() - self.right_pupil_x
        ) * speed

        self.right_pupil_y += (
            right_target.y() - self.right_pupil_y
        ) * speed

        self.update_blink()

    # =====================================================
    # Idle Curiosity
    # =====================================================

    def update_idle(self):

        now = time.time()

        if now - self.last_idle_change > 4:

            self.last_idle_change = now

            self.idle_target = QPointF(

                random.uniform(-3, 3),

                random.uniform(-2, 2),

            )

        self.idle_offset.setX(

            self.idle_offset.x()
            + (
                self.idle_target.x()
                - self.idle_offset.x()
            )
            * 0.02

        )

        self.idle_offset.setY(

            self.idle_offset.y()
            + (
                self.idle_target.y()
                - self.idle_offset.y()
            )
            * 0.02

        )

    # =====================================================
    # Blink
    # =====================================================

    def update_blink(self):

        now = time.time()

        if (

            not self.closing

            and not self.opening

            and now >= self.next_blink

        ):

            self.closing = True

        if self.closing:

            self.blink -= self.blink_speed

            if self.blink <= 0.08:

                self.blink = 0.08

                self.closing = False

                self.opening = True

        elif self.opening:

            self.blink += self.blink_speed

            if self.blink >= 1.0:

                self.blink = 1.0

                self.opening = False

                self.next_blink = (

                    time.time()

                    + random.uniform(3.5, 8.0)

                )