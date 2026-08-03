"""
=========================================================
Project G-EXO Desktop
Eye Animator
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import math

from behavior.face_state import FaceState


class EyeAnimator:

    def __init__(self):

        self.time = 0.0

        self.offset_x = 0.0

        self.offset_y = 0.0

        self.state = FaceState.IDLE

    # =====================================================
    # State
    # =====================================================

    def set_state(

        self,

        state,

    ):

        self.state = state

    # =====================================================
    # Update
    # =====================================================

    def update(self):

        self.time += 0.05

        if self.state == FaceState.IDLE:

            self.offset_x = math.sin(

                self.time * 0.9

            ) * 2.0

            self.offset_y = math.cos(

                self.time * 0.7

            ) * 1.5

        elif self.state == FaceState.LISTENING:

            self.offset_x = 0.0

            self.offset_y = -2.0

        elif self.state == FaceState.THINKING:

            self.offset_x = math.sin(

                self.time * 2.0

            ) * 4.0

            self.offset_y = 0.0

        elif self.state == FaceState.SPEAKING:

            self.offset_x = math.sin(

                self.time * 5.0

            ) * 1.2

            self.offset_y = 0.0

        elif self.state == FaceState.ERROR:

            self.offset_x = 0.0

            self.offset_y = 3.0

        else:

            self.offset_x = 0.0

            self.offset_y = 0.0