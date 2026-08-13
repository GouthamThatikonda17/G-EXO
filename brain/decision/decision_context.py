"""
=========================================================
Project G-EXO Decision Context
Version : 1.1
Developer : Thatikonda Goutham Teja
=========================================================
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from emotion.models import EmotionState
from personality.models import PersonalityState

@dataclass
class DecisionContext:
    """
    Contains every piece of information the
    Decision Engine needs before making a decision.
    Future versions will continuously expand this
    object without changing the Decision Engine API.
    """
    # =====================================================
    # REQUEST
    # =====================================================
    user_input: str
    source: str
    intent: str | None = None
    # =====================================================
    # USER
    # =====================================================
    user_id: str | None = None
    conversation_id: str | None = None
    # =====================================================
    # MEMORY
    # =====================================================
    working_memory: list[Any] = field(
        default_factory=list
    )
    short_memory: list[Any] = field(
        default_factory=list
    )
    long_memory: list[Any] = field(
        default_factory=list
    )
    # =====================================================
    # EMOTION & PERSONALITY (Preserved Legacy & Added Classes)
    # =====================================================
    detected_emotion: str | None = None
    emotion_confidence: float = 0.0
    personality_mode: str = "default"

    emotion_state: EmotionState | None = None
    personality_state: PersonalityState | None = None
    # =====================================================
    # DEVICE
    # =====================================================
    internet_available: bool = True
    battery_level: int | None = None
    location: str | None = None
    # =====================================================
    # SKILLS
    # =====================================================
    available_skills: list[str] = field(
        default_factory=list
    )
    # =====================================================
    # EXTRA
    # =====================================================
    metadata: dict[str, Any] = field(
        default_factory=dict
    )
    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )
