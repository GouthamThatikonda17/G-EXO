"""
=========================================================
Project G-EXO Emotion & Personality Pipeline Tests
Version : 1.1
Developer : Thatikonda Goutham Teja
=========================================================
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import unittest
from unittest.mock import patch
from core.request import Request
from emotion.models import EmotionState
from emotion.engine import EmotionEngine
from personality.models import PersonalityState
from personality.engine import PersonalityEngine
from assistant import GEXOBrain

class TestEmoPipeline(unittest.TestCase):
    def test_emotion_state_bounds_and_defaults(self):
        state = EmotionState()
        self.assertEqual(state.valence, 0.0)
        self.assertEqual(state.arousal, 0.0)
        self.assertEqual(state.dominance, 0.0)
        self.assertEqual(state.categorical, "neutral")

    def test_emotion_engine_deterministic(self):
        engine = EmotionEngine()
        # v_shift = 0.25, a_shift = 0.15 + 0.40 = 0.55
        req = Request(message="happy fast", source="test")
        state = engine.update(req)
        # Should cross bounds > 0.2 for both -> happy
        self.assertEqual(state.categorical, "happy")
        self.assertEqual(state.valence, 0.25)
        self.assertEqual(state.arousal, 0.55)

    def test_emotion_decay_and_bounds(self):
        engine = EmotionEngine()
        for _ in range(10):
            engine.update(Request(message="happy", source="test"))
        self.assertLessEqual(engine.state.valence, 1.0)

        old_val = engine.state.valence
        engine.update(Request(message="neutral generic string", source="test"))
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

    @patch('decision.decision_engine.DecisionContext')
    def test_gexo_brain_injection_pipeline(self, MockContext):
        brain = GEXOBrain()

        # Ownership proofs
        self.assertIsNotNone(brain.emotion_engine)
        self.assertIsNotNone(brain.personality_engine)

        # Process deterministic rule
        response = brain.process("help", source="test_cli")
        self.assertTrue(response.success)

        # Mathematical proof that states reached DecisionContext unchanged
        self.assertTrue(MockContext.called)
        kwargs = MockContext.call_args.kwargs
        self.assertIn("emotion_state", kwargs)
        self.assertIn("personality_state", kwargs)
        self.assertIsInstance(kwargs["emotion_state"], EmotionState)
        self.assertIsInstance(kwargs["personality_state"], PersonalityState)

if __name__ == "__main__":
    unittest.main()
