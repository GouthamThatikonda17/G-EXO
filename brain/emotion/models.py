"""
=========================================================
Project G-EXO Emotion Models
Version : 1.1
Developer : Thatikonda Goutham Teja
=========================================================
"""
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class EmotionState:
    """
    Transient internal emotional state using PAD dimensions.
    All dimensional values strictly bounded between [-1.0, 1.0].
    """
    valence: float = 0.0
    arousal: float = 0.0
    dominance: float = 0.0
    categorical: str = "neutral"
    timestamp: datetime = field(default_factory=datetime.utcnow)