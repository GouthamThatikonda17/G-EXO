"""
=========================================================
Project G-EXO
Behavior Engine
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from behavior.face_state import FaceState


class BehaviorEngine:

    def __init__(self):

        self.state = FaceState.IDLE

        self.listeners = []

    # =====================================================
    # Listener
    # =====================================================

    def add_listener(

        self,

        listener,

    ):

        if listener not in self.listeners:

            self.listeners.append(

                listener,

            )

    # =====================================================
    # State
    # =====================================================

    def set_state(

        self,

        state: FaceState,

    ):

        if self.state == state:

            return

        self.state = state

        print(

            f"[Behavior] {state.value}"

        )

        for listener in self.listeners:

            listener(

                state,

            )

    def get_state(self):

        return self.state

    # =====================================================
    # Helpers
    # =====================================================

    def is_idle(self):

        return self.state == FaceState.IDLE

    def is_listening(self):

        return self.state == FaceState.LISTENING

    def is_thinking(self):

        return self.state == FaceState.THINKING

    def is_speaking(self):

        return self.state == FaceState.SPEAKING