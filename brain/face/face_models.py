"""
=========================================================
Project G-EXO
Face Models
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from dataclasses import dataclass
from enum import Enum


# =====================================================
# EXPRESSIONS
# =====================================================

class Expression(str, Enum):

    IDLE = "idle"

    HAPPY = "happy"

    SAD = "sad"

    THINKING = "thinking"

    LISTENING = "listening"

    SPEAKING = "speaking"

    SURPRISED = "surprised"

    SLEEPING = "sleeping"

    ANGRY = "angry"

    CONFUSED = "confused"

    WINK = "wink"


# =====================================================
# EYE STATE
# =====================================================

class EyeState(str, Enum):

    OPEN = "open"

    CLOSED = "closed"

    HALF = "half"

    WINK_LEFT = "wink_left"

    WINK_RIGHT = "wink_right"


# =====================================================
# MOUTH STATE
# =====================================================

class MouthState(str, Enum):

    CLOSED = "closed"

    SMALL = "small"

    OPEN = "open"

    SMILE = "smile"

    SAD = "sad"

    SURPRISED = "surprised"


# =====================================================
# FACE STATE
# =====================================================

@dataclass
class FaceState:

    expression: Expression = Expression.IDLE

    left_eye: EyeState = EyeState.OPEN

    right_eye: EyeState = EyeState.OPEN

    mouth: MouthState = MouthState.CLOSED

    blinking: bool = True

    speaking: bool = False

    animation_speed: float = 1.0