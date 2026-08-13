"""
=========================================================
Project G-EXO Personality Models
Version : 1.1
Developer : Thatikonda Goutham Teja
=========================================================
"""
from dataclasses import dataclass, field

@dataclass
class PersonalityState:
    """
    Stable behavioral traits based on the OCEAN model.
    Utilized to internally scale or dampen emotional expressions.
    """
    mode: str = "default"
    traits: dict[str, float] = field(default_factory=lambda: {
        "openness": 0.5,
        "conscientiousness": 0.7,
        "extraversion": 0.6,
        "agreeableness": 0.8,
        "neuroticism": 0.2
    })