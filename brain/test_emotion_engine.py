# brain/test_emotion_engine.py
"""
=========================================================
Project G-EXO Emotion Engine Test
Version : 3.0
Developer : Thatikonda Goutham Teja
=========================================================
"""
import os
import sys
import unittest

_brain_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_brain_dir, ".."))

if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

if _brain_dir not in sys.path:
    sys.path.insert(0, _brain_dir)

from emotion.models import EmotionState, EmotionEvent, EmotionType
from emotion.emotion_engine import EmotionEngine
from personality.engine import PersonalityEngine

class TestEmotionEngine(unittest.TestCase):
    def setUp(self):
        self.engine = EmotionEngine()

    def test_01_initialization(self):
        self.assertEqual(self.engine.state.valence, 0.0)
        self.assertEqual(self.engine.state.arousal, 0.0)
        self.assertEqual(self.engine.state.dominance, 0.0)
        self.assertEqual(self.engine.state.categorical, EmotionType.NEUTRAL)

    def test_02_invalid_event_rejection(self):
        # Explicit validation must reject raw strings instead of treating them as NEUTRAL
        with self.assertRaises(TypeError):
            self.engine.update("POSITIVE_INTERACTION")
        with self.assertRaises(TypeError):
            self.engine.update(None)

    def test_03_positive_event(self):
        state = self.engine.update(EmotionEvent.POSITIVE_INTERACTION)
        self.assertEqual(state.valence, 0.25)
        self.assertEqual(state.arousal, 0.15)
        self.assertEqual(state.dominance, 0.0)
        self.assertEqual(state.categorical, EmotionType.HAPPY)

    def test_04_negative_event(self):
        state = self.engine.update(EmotionEvent.NEGATIVE_INTERACTION)
        self.assertEqual(state.valence, -0.35)
        self.assertEqual(state.arousal, 0.25)
        self.assertEqual(state.dominance, 0.0)
        self.assertEqual(state.categorical, EmotionType.SAD)

    def test_05_error_event(self):
        state = self.engine.update(EmotionEvent.ERROR_CONDITION)
        self.assertEqual(state.valence, -0.35)
        self.assertEqual(state.arousal, 0.40)
        self.assertEqual(state.dominance, -0.20)
        self.assertEqual(state.categorical, EmotionType.ANGRY)
    def test_06_neutral_event(self):
        # A neutral event should apply decay but zero explicit shift
        self.engine.update(EmotionEvent.POSITIVE_INTERACTION)
        val1 = self.engine.state.valence
        self.engine.update(EmotionEvent.NEUTRAL_INTERACTION)
        val2 = self.engine.state.valence
        self.assertLess(val2, val1)
        self.assertEqual(self.engine.state.categorical, EmotionType.NEUTRAL)

    def test_07_pad_bounds(self):
        for _ in range(20):
            self.engine.update(EmotionEvent.POSITIVE_INTERACTION)
        self.assertLessEqual(self.engine.state.valence, 1.0)
        self.assertLessEqual(self.engine.state.arousal, 1.0)

        for _ in range(40):
            self.engine.update(EmotionEvent.NEGATIVE_INTERACTION)
        self.assertGreaterEqual(self.engine.state.valence, -1.0)
        # NEGATIVE_INTERACTION adds arousal, so we check the upper bound clamp
        self.assertLessEqual(self.engine.state.arousal, 1.0)
        self.assertGreaterEqual(self.engine.state.dominance, -1.0)

    def test_08_exponential_decay(self):
        self.engine.update(EmotionEvent.POSITIVE_INTERACTION)
        val1 = self.engine.state.valence
        # Math verification: 0.25 * (1.0 - 0.15)
        self.engine.update(EmotionEvent.NEUTRAL_INTERACTION)
        val2 = self.engine.state.valence
        self.assertAlmostEqual(val2, val1 * 0.85, places=4)

    def test_09_reset(self):
        self.engine.update(EmotionEvent.ERROR_CONDITION)
        self.assertNotEqual(self.engine.state.valence, 0.0)
        self.engine.reset()
        self.assertEqual(self.engine.state.valence, 0.0)
        self.assertEqual(self.engine.state.arousal, 0.0)
        self.assertEqual(self.engine.state.dominance, 0.0)
        self.assertEqual(self.engine.state.categorical, EmotionType.NEUTRAL)

    def test_10_defensive_copy(self):
        transport_state = self.engine.update(EmotionEvent.POSITIVE_INTERACTION)
        original_val = transport_state.valence
        # Modify the transport copy
        transport_state.valence = 99.9
        # Prove internal state isolation
        self.assertNotEqual(self.engine.state.valence, 99.9)
        self.assertEqual(self.engine.state.valence, original_val)

    def test_11_compatibility_import(self):
        # Ensures legacy import paths resolve accurately
        from emotion.engine import EmotionEngine as LegacyEngine
        legacy_instance = LegacyEngine()
        self.assertIsInstance(legacy_instance, EmotionEngine)

if __name__ == '__main__':
    unittest.main()