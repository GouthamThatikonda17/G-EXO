"""
=========================================================
Project G-EXO Personality Engine
Version : 1.1
Developer : Thatikonda Goutham Teja
=========================================================
"""
import copy
from personality.models import PersonalityState
from emotion.models import EmotionState

class PersonalityEngine:
    """
    Acts as a filter between raw emotional generation and context ingestion.
    Does not mutate underlying Engine states.
    """
    def __init__(self):
        self.state = PersonalityState()

    def modulate(self, raw_emotion: EmotionState) -> EmotionState:
        """
        Calculates and returns a modified emotion representation driven by traits.
        """
        # Strictly unbind reference so EmotionEngine state isn't poisoned
        emotion = copy.deepcopy(raw_emotion)
        traits = self.state.traits

        mod_v = emotion.valence
        mod_a = emotion.arousal
        mod_d = emotion.dominance

        # Negative scale amplified by Neuroticism, Positive scale by Agreeableness
        if mod_v < 0:
            mod_v *= (1.0 + traits.get("neuroticism", 0.2) * 0.5)
        else:
            mod_v *= (1.0 + traits.get("agreeableness", 0.8) * 0.2)

        # Arousal amplified by Extraversion, dampened by Conscientiousness
        mod_a *= (1.0 + traits.get("extraversion", 0.6) * 0.3)
        mod_a *= (1.0 - (traits.get("conscientiousness", 0.7) - 0.5) * 0.2)

        # Dominance influenced by Openness limits
        mod_d *= (1.0 + (traits.get("openness", 0.5) - 0.5) * 0.2)

        # Clamp limits
        emotion.valence = max(-1.0, min(1.0, mod_v))
        emotion.arousal = max(-1.0, min(1.0, mod_a))
        emotion.dominance = max(-1.0, min(1.0, mod_d))

        return emotion
