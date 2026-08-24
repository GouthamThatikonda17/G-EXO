# brain/emotion/emotion_engine.py
"""
=========================================================
Project G-EXO Emotion Engine
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""
import copy
from datetime import datetime
from emotion.models import EmotionState, EmotionEvent, EmotionType

class EmotionEngine:
    """
    Deterministic, offline emotional state generator.
    Maintains persistent state across the session with incremental
    transitions and exponential decay driven strictly by explicit EmotionEvents.
    """
    def __init__(self):
        self.state = EmotionState()
        self.decay_rate = 0.15

    def reset(self):
        """Resets the emotional state to baseline."""
        self.state = EmotionState()

    def update(self, event: EmotionEvent) -> EmotionState:
        # Explicitly validate that event is an EmotionEvent
        if not isinstance(event, EmotionEvent):
            raise TypeError(f"EmotionEngine.update() requires an EmotionEvent, got {type(event).__name__}")

        v_shift = 0.0
        a_shift = 0.0
        d_shift = 0.0
        categorical = EmotionType.NEUTRAL

        if event == EmotionEvent.POSITIVE_INTERACTION:
            v_shift = 0.25
            a_shift = 0.15
            d_shift = 0.00
            categorical = EmotionType.HAPPY
        elif event == EmotionEvent.NEGATIVE_INTERACTION:
            v_shift = -0.35
            a_shift = 0.25
            d_shift = 0.00
            categorical = EmotionType.SAD
        elif event == EmotionEvent.ERROR_CONDITION:
            v_shift = -0.35
            a_shift = 0.40
            d_shift = -0.20
            categorical = EmotionType.ANGRY
        elif event == EmotionEvent.NEUTRAL_INTERACTION:
            v_shift = 0.00
            a_shift = 0.00
            d_shift = 0.00
            categorical = EmotionType.NEUTRAL

        # Apply exponential decay towards 0.0 before applying the shift
        self.state.valence *= (1.0 - self.decay_rate)
        self.state.arousal *= (1.0 - self.decay_rate)
        self.state.dominance *= (1.0 - self.decay_rate)

        # Apply dimensional shift and clamp values
        self.state.valence = max(-1.0, min(1.0, self.state.valence + v_shift))
        self.state.arousal = max(-1.0, min(1.0, self.state.arousal + a_shift))
        self.state.dominance = max(-1.0, min(1.0, self.state.dominance + d_shift))

        # Determine categorical expression mapping
        self.state.categorical = categorical
        self.state.timestamp = datetime.utcnow()

        # Yield a defensive transport copy. This copy remains mutable because
        # PersonalityEngine requires modifying PAD attributes, but mutability
        # is safely isolated from the engine's internal state.
        return copy.deepcopy(self.state)