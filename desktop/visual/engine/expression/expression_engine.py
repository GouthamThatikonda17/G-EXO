"""
=========================================================
Project G-EXO Desktop
Expression Engine
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from behavior.face_state import FaceState

from .expressions import EXPRESSIONS


class ExpressionEngine:

    def __init__(self):

        self.state = FaceState.IDLE

    # =====================================================
    # State
    # =====================================================

    def set_state(self, state):

        self.state = state

    # =====================================================
    # Current
    # =====================================================

    def current(self):

        if self.state == FaceState.IDLE:
            return EXPRESSIONS["idle"]

        if self.state == FaceState.LISTENING:
            return EXPRESSIONS["listening"]

        if self.state == FaceState.THINKING:
            return EXPRESSIONS["thinking"]

        if self.state == FaceState.SPEAKING:
            return EXPRESSIONS["speaking"]

        if self.state == FaceState.ERROR:
            return EXPRESSIONS["error"]

        return EXPRESSIONS["idle"]