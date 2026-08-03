"""
=========================================================
Project G-EXO
Memory Types
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from enum import Enum


class MemoryType(str, Enum):

    PERSON = "person"

    PET = "pet"

    CONTACT = "contact"

    PLACE = "place"

    EVENT = "event"

    GOAL = "goal"

    TASK = "task"

    NOTE = "note"

    PROJECT = "project"

    EDUCATION = "education"

    WORK = "work"

    HEALTH = "health"

    PREFERENCE = "preference"

    ROUTINE = "routine"

    REMINDER = "reminder"

    EMOTION = "emotion"

    CONVERSATION = "conversation"

    FACT = "fact"

    SKILL = "skill"

    OTHER = "other"