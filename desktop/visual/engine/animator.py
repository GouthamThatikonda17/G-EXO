"""
=========================================================
Project G-EXO Desktop
Visual Animator
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import math


class VisualAnimator:

    def __init__(self):

        self.time = 0.0

        self.float_offset = 0.0

        self.blink = 1.0

        self._blink_timer = 0.0

    # =====================================================
    # Update
    # =====================================================

    def update(self):

        self.time += 0.05

        self.float_offset = math.sin(self.time * 0.8) * 2.5

        self._blink_timer += 0.05

        if self._blink_timer > 4.0:

            self.blink -= 0.25

            if self.blink <= 0.05:

                self.blink = 1.0
                self._blink_timer = 0.0