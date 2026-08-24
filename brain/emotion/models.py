# brain/emotion/models.py
"""
=========================================================
Project G-EXO Emotion Models
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class EmotionType(str, Enum):
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"

class EmotionEvent(str, Enum):
    POSITIVE_INTERACTION = "positive_interaction"
    NEGATIVE_INTERACTION = "negative_interaction"
    ERROR_CONDITION = "error_condition"
    NEUTRAL_INTERACTION = "neutral_interaction"

@dataclass
class EmotionState:
    """
    Transient internal emotional state using PAD dimensions.
    All dimensional values strictly bounded between [-1.0, 1.0].
    """
    valence: float = 0.0
    arousal: float = 0.0
    dominance: float = 0.0
    categorical: EmotionType = EmotionType.NEUTRAL
    timestamp: datetime = field(default_factory=datetime.utcnow)