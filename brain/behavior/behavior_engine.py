"""
=========================================================
Project G-EXO Behavior Engine
Version : 3.0
Developer : Thatikonda Goutham Teja
=========================================================
"""
from behavior.face_state import FaceState

class BehaviorEngine:
    """
    Manages the physical or visual manifestation of internal state.
    Evaluates prioritization between active tasks and passive cognitive emotions.
    """
    def __init__(self):
        self.active_state = None
        self.passive_state = FaceState.IDLE
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
    # Cognitive State Mapping
    # =====================================================
    def update_cognitive_state(self, emotion):
        """
        Maps continuous internal emotion to a baseline behavior expression.
        Only displays if no active task state is running.
        """
        cat = emotion.categorical.lower()
        if cat in ["happy", "content"]:
            new_passive = FaceState.HAPPY
        elif cat == "sad":
            new_passive = FaceState.SAD
        elif cat == "angry":
            new_passive = FaceState.ANGRY
        else:
            new_passive = FaceState.IDLE

        if self.passive_state != new_passive:
            self.passive_state = new_passive
            self._emit_effective_state()

    # =====================================================
    # Task State Override
    # =====================================================
    def set_state(
        self,
        state: FaceState,
    ):
        """
        Legacy compatible state trigger.
        Passing an active state masks the cognitive emotion.
        Passing IDLE clears the active state, restoring emotion.
        """
        active_states = {
            FaceState.LISTENING,
            FaceState.THINKING,
            FaceState.SPEAKING,
            FaceState.ERROR,
            FaceState.SLEEPING,
        }

        changed = False
        if state in active_states:
            if self.active_state != state:
                self.active_state = state
                changed = True
        elif state == FaceState.IDLE:
            if self.active_state is not None:
                self.active_state = None
                changed = True
        else:
            if self.passive_state != state:
                self.passive_state = state
                changed = True

        if changed:
            self._emit_effective_state()

    # =====================================================
    # State Resolution
    # =====================================================
    def _emit_effective_state(self):
        effective = self.get_state()
        print(f"[Behavior] {effective.value}")
        for listener in self.listeners:
            listener(effective)

    def get_state(self):
        return self.active_state if self.active_state is not None else self.passive_state

    # =====================================================
    # Helpers
    # =====================================================
    def is_idle(self):
        return self.get_state() == FaceState.IDLE

    def is_listening(self):
        return self.get_state() == FaceState.LISTENING

    def is_thinking(self):
        return self.get_state() == FaceState.THINKING

    def is_speaking(self):
        return self.get_state() == FaceState.SPEAKING
