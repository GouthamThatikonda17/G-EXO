"""
=========================================================
Project G-EXO Desktop
Eyebrow Animator
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from behavior.face_state import FaceState


class EyebrowAnimator:

    def __init__(self):

        self.state = FaceState.IDLE

        self.left_offset = 0.0
        self.right_offset = 0.0

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

        self.left_offset = 0.0
        self.right_offset = 0.0

        if self.state == FaceState.LISTENING:

            self.left_offset = -4.0
            self.right_offset = -4.0

        elif self.state == FaceState.THINKING:

            self.left_offset = 3.0
            self.right_offset = -3.0

        elif self.state == FaceState.ERROR:

            self.left_offset = 6.0
            self.right_offset = 6.0