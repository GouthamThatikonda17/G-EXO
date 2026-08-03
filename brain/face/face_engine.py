"""
=========================================================
Project G-EXO
Face Engine
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from face.face_models import (
    FaceState,
    Expression,
    EyeState,
    MouthState,
)


class FaceEngine:
    """
    Central controller for G-EXO facial expressions.

    The Brain updates the Face Engine.
    The UI only renders the current FaceState.
    """

    def __init__(self):

        self._state = FaceState()

    # =====================================================
    # GET CURRENT STATE
    # =====================================================

    def state(self) -> FaceState:

        return self._state

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        self._state = FaceState()

    # =====================================================
    # SET EXPRESSION
    # =====================================================

    def set_expression(
        self,
        expression: Expression,
    ):

        self._state.expression = expression

        if expression == Expression.IDLE:

            self._state.left_eye = EyeState.OPEN
            self._state.right_eye = EyeState.OPEN
            self._state.mouth = MouthState.CLOSED
            self._state.speaking = False

        elif expression == Expression.HAPPY:

            self._state.left_eye = EyeState.OPEN
            self._state.right_eye = EyeState.OPEN
            self._state.mouth = MouthState.SMILE
            self._state.speaking = False

        elif expression == Expression.SAD:

            self._state.left_eye = EyeState.HALF
            self._state.right_eye = EyeState.HALF
            self._state.mouth = MouthState.SAD
            self._state.speaking = False

        elif expression == Expression.THINKING:

            self._state.left_eye = EyeState.HALF
            self._state.right_eye = EyeState.HALF
            self._state.mouth = MouthState.CLOSED
            self._state.speaking = False

        elif expression == Expression.LISTENING:

            self._state.left_eye = EyeState.OPEN
            self._state.right_eye = EyeState.OPEN
            self._state.mouth = MouthState.CLOSED
            self._state.speaking = False

        elif expression == Expression.SPEAKING:

            self._state.left_eye = EyeState.OPEN
            self._state.right_eye = EyeState.OPEN
            self._state.mouth = MouthState.OPEN
            self._state.speaking = True

        elif expression == Expression.SURPRISED:

            self._state.left_eye = EyeState.OPEN
            self._state.right_eye = EyeState.OPEN
            self._state.mouth = MouthState.SURPRISED
            self._state.speaking = False

        elif expression == Expression.SLEEPING:

            self._state.left_eye = EyeState.CLOSED
            self._state.right_eye = EyeState.CLOSED
            self._state.mouth = MouthState.CLOSED
            self._state.speaking = False

        elif expression == Expression.ANGRY:

            self._state.left_eye = EyeState.HALF
            self._state.right_eye = EyeState.HALF
            self._state.mouth = MouthState.CLOSED
            self._state.speaking = False

        elif expression == Expression.CONFUSED:

            self._state.left_eye = EyeState.HALF
            self._state.right_eye = EyeState.OPEN
            self._state.mouth = MouthState.SMALL
            self._state.speaking = False

        elif expression == Expression.WINK:

            self._state.left_eye = EyeState.CLOSED
            self._state.right_eye = EyeState.OPEN
            self._state.mouth = MouthState.SMILE
            self._state.speaking = False

    # =====================================================
    # SPEAKING
    # =====================================================

    def start_speaking(self):

        self._state.speaking = True

        self._state.expression = Expression.SPEAKING

        self._state.mouth = MouthState.OPEN

    def stop_speaking(self):

        self._state.speaking = False

        self.set_expression(Expression.IDLE)

    # =====================================================
    # BLINK
    # =====================================================

    def blink(self):

        self._state.left_eye = EyeState.CLOSED

        self._state.right_eye = EyeState.CLOSED

    def open_eyes(self):

        self._state.left_eye = EyeState.OPEN

        self._state.right_eye = EyeState.OPEN