"""
=========================================================
Project G-EXO Emotion Engine
Version : 1.1
Developer : Thatikonda Goutham Teja
=========================================================
"""
import copy
from datetime import datetime
from emotion.models import EmotionState
from core.request import Request

class EmotionEngine:
    """
    Deterministic, offline emotional state generator.
    Maintains persistent state across the session with incremental
    transitions and exponential decay.
    """
    def __init__(self):
        self.state = EmotionState()
        self.decay_rate = 0.15

    def update(self, request: Request) -> EmotionState:
        text = request.message.lower()

        v_shift = 0.0
        a_shift = 0.0
        d_shift = 0.0

        # Deterministic heuristic analysis
        if any(w in text for w in ["good", "happy", "great", "excellent", "love", "thanks", "beautiful"]):
            v_shift += 0.25
            a_shift += 0.15

        if any(w in text for w in ["bad", "sad", "terrible", "hate", "angry", "frustrated", "error", "fail"]):
            v_shift -= 0.35
            a_shift += 0.25

        if any(w in text for w in ["urgent", "quick", "fast", "emergency", "help", "alert"]):
            a_shift += 0.40
            d_shift -= 0.20

        if any(w in text for w in ["calm", "quiet", "relax", "stop", "wait"]):
            a_shift -= 0.30
            v_shift += 0.10

        # Apply exponential decay towards 0.0 before applying the shift
        self.state.valence *= (1.0 - self.decay_rate)
        self.state.arousal *= (1.0 - self.decay_rate)
        self.state.dominance *= (1.0 - self.decay_rate)

        # Apply dimensional shift and clamp values
        self.state.valence = max(-1.0, min(1.0, self.state.valence + v_shift))
        self.state.arousal = max(-1.0, min(1.0, self.state.arousal + a_shift))
        self.state.dominance = max(-1.0, min(1.0, self.state.dominance + d_shift))

        # Determine categorical expression mapping
        self.state.categorical = self._classify(self.state.valence, self.state.arousal)
        self.state.timestamp = datetime.utcnow()

        # Yield an immutable snapshot to prevent accidental mutation by PersonalityEngine
        return copy.deepcopy(self.state)

    def _classify(self, v: float, a: float) -> str:
        """Determines base category thresholding."""
        if v > 0.2 and a > 0.2:
            return "happy"
        if v > 0.2 and a <= 0.2:
            return "content"
        if v < -0.2 and a > 0.2:
            return "angry"
        if v < -0.2 and a <= 0.2:
            return "sad"
        if -0.2 <= v <= 0.2 and a > 0.4:
            return "surprised"
        return "neutral"
