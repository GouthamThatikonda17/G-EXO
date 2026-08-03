"""
=========================================================
Project G-EXO Desktop
Animation Controller
Version : 3.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from .eye_animator import EyeAnimator
from .eyebrow_animator import EyebrowAnimator


class AnimationController:

    def __init__(self):

        self.eye = EyeAnimator()

        self.eyebrow = EyebrowAnimator()

        self.state = None

    # =====================================================
    # State
    # =====================================================

    def set_state(

        self,

        state,

    ):

        self.state = state

        self.eye.set_state(

            state,

        )

        self.eyebrow.set_state(

            state,

        )

    # =====================================================
    # Update
    # =====================================================

    def update(self):

        self.eye.update()

        self.eyebrow.update()