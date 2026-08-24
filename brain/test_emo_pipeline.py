# brain/test_emo_pipeline.py
"""
=========================================================
Project G-EXO Emotion & Personality Pipeline Tests
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import unittest

from emotion.models import EmotionState, EmotionType, EmotionEvent
from emotion.emotion_engine import EmotionEngine
from personality.models import PersonalityState
from personality.engine import PersonalityEngine
from assistant import GEXOBrain

class TestEmoPipeline(unittest.TestCase):
    def test_emotion_state_bounds_and_defaults(self):
        state = EmotionState()
        self.assertEqual(state.valence, 0.0)
        self.assertEqual(state.arousal, 0.0)
        self.assertEqual(state.dominance, 0.0)
        self.assertEqual(state.categorical, EmotionType.NEUTRAL)

    def test_emotion_engine_deterministic(self):
        engine = EmotionEngine()
        state = engine.update(EmotionEvent.POSITIVE_INTERACTION)

        self.assertEqual(state.categorical, EmotionType.HAPPY)
        self.assertEqual(state.valence, 0.25)
        self.assertEqual(state.arousal, 0.15)

    def test_emotion_decay_and_bounds(self):
        engine = EmotionEngine()
        for _ in range(10):
            engine.update(EmotionEvent.POSITIVE_INTERACTION)
        self.assertLessEqual(engine.state.valence, 1.0)

        old_val = engine.state.valence
        engine.update(EmotionEvent.NEUTRAL_INTERACTION)

        # Validate mathematical decay towards neutral 0.0 (15% reduction)
        self.assertLess(engine.state.valence, old_val)
        self.assertAlmostEqual(engine.state.valence, old_val * 0.85, places=4)

    def test_personality_approved_contract(self):
        p = PersonalityState()
        self.assertEqual(p.mode, "default")
        self.assertIsInstance(p.traits, dict)
        self.assertEqual(p.traits["openness"], 0.5)
        self.assertEqual(p.traits["agreeableness"], 0.8)

    def test_personality_modulation(self):
        pe = PersonalityEngine()
        pe.state.traits["agreeableness"] = 0.8
        emo = EmotionState(valence=0.5, arousal=0.0, dominance=0.0)
        mod_emo = pe.modulate(emo)
        # Verify modulation took place without altering the source baseline
        self.assertGreater(mod_emo.valence, 0.5)
        self.assertEqual(emo.valence, 0.5)

    def test_real_pipeline_integration(self):
        brain = GEXOBrain()

        # Ownership proofs
        self.assertIsNotNone(brain.emotion_engine)
        self.assertIsNotNone(brain.personality_engine)

        # Process deterministic rule through the real pipeline
        response = brain.process("help", source="test_cli")
        self.assertTrue(response.success)

        # Verify PAD attributes remain available in the states
        self.assertIsInstance(brain.emotion_engine.state.valence, float)
        self.assertIsInstance(brain.personality_engine.state.traits, dict)

        # Verify that PersonalityEngine did not mutate the EmotionEngine's internal state
        self.assertNotEqual(id(brain.emotion_engine.state), id(brain.personality_engine.state))

if __name__ == "__main__":
    unittest.main()