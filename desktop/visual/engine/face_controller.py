"""
=========================================================
Project G-EXO Desktop
Face Controller
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from behavior.face_state import FaceState


class FaceController:

    def __init__(self):

        self.state = FaceState.IDLE

    # =====================================================
    # State
    # =====================================================

    def set_state(self, state):

        self.state = state

    def get_state(self):

        return self.state