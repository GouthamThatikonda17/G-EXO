"""
=========================================================
Project G-EXO
Face States
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from enum import Enum


class FaceState(Enum):

    IDLE = "idle"

    LISTENING = "listening"

    THINKING = "thinking"

    SPEAKING = "speaking"

    HAPPY = "happy"

    SAD = "sad"

    ANGRY = "angry"

    SLEEPING = "sleeping"

    ERROR = "error"