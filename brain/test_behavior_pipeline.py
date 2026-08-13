"""
=========================================================
Project G-EXO Behavior Pipeline Tests
Version : 1.7
Developer : Thatikonda Goutham Teja
=========================================================
"""
import os
import sys

# --- Force headless Qt execution for CI environments ---
os.environ["QT_QPA_PLATFORM"] = "offscreen"

# --- Fix for import path during direct and module execution ---
_brain_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_brain_dir, ".."))
_desktop_dir = os.path.join(_project_root, "desktop")

if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
if _brain_dir not in sys.path:
    sys.path.insert(0, _brain_dir)
if _desktop_dir not in sys.path:
    sys.path.insert(0, _desktop_dir)
# --------------------------------------------------------------

import unittest
from unittest.mock import patch

# Explicitly import main_window directly since desktop/ is in sys.path
import main_window

from behavior.behavior_engine import BehaviorEngine
from behavior.face_state import FaceState
from emotion.models import EmotionState
from voice.text_to_speech import TextToSpeech
from assistant import GEXOBrain


class TestBehaviorPipeline(unittest.TestCase):

    def test_default_passive_idle(self):
        engine = BehaviorEngine()
        self.assertEqual(engine.get_state(), FaceState.IDLE)

    def test_emotion_happy(self):
        engine = BehaviorEngine()
        engine.update_cognitive_state(EmotionState(categorical="happy"))
        self.assertEqual(engine.get_state(), FaceState.HAPPY)

    def test_emotion_sad(self):
        engine = BehaviorEngine()
        engine.update_cognitive_state(EmotionState(categorical="sad"))
        self.assertEqual(engine.get_state(), FaceState.SAD)

    def test_emotion_angry(self):
        engine = BehaviorEngine()
        engine.update_cognitive_state(EmotionState(categorical="angry"))
        self.assertEqual(engine.get_state(), FaceState.ANGRY)

    def test_active_speaking_overrides_happy(self):
        engine = BehaviorEngine()
        engine.update_cognitive_state(EmotionState(categorical="happy"))
        engine.set_state(FaceState.SPEAKING)
        self.assertEqual(engine.get_state(), FaceState.SPEAKING)

    def test_clearing_active_restores_passive(self):
        engine = BehaviorEngine()
        engine.update_cognitive_state(EmotionState(categorical="happy"))
        engine.set_state(FaceState.SPEAKING)
        engine.set_state(FaceState.IDLE) # clears active state
        self.assertEqual(engine.get_state(), FaceState.HAPPY)

    def test_listening_thinking_overrides(self):
        engine = BehaviorEngine()
        engine.update_cognitive_state(EmotionState(categorical="sad"))

        engine.set_state(FaceState.LISTENING)
        self.assertEqual(engine.get_state(), FaceState.LISTENING)

        engine.set_state(FaceState.THINKING)
        self.assertEqual(engine.get_state(), FaceState.THINKING)

        engine.set_state(FaceState.IDLE)
        self.assertEqual(engine.get_state(), FaceState.SAD)

    @patch('subprocess.run')
    @patch('voice.text_to_speech.Path.exists')
    @patch('voice.text_to_speech.shutil.which')
    def test_tts_callbacks_normal(self, mock_which, mock_exists, mock_run):
        mock_exists.return_value = True
        mock_which.return_value = "piper"
        mock_run.return_value.returncode = 0

        tts = TextToSpeech()
        events = []
        tts.on_speech_start = lambda: events.append("start")
        tts.on_speech_end = lambda: events.append("end")
        tts._play_audio = lambda p: events.append("play")

        # Bypass queue to call internal logic directly for synchronous hardware mocking
        tts._generate_and_play("test")

        self.assertEqual(events, ["start", "play", "end"])
        tts.shutdown()

    @patch('subprocess.run')
    @patch('voice.text_to_speech.Path.exists')
    @patch('voice.text_to_speech.shutil.which')
    def test_tts_callback_on_playback_failure(self, mock_which, mock_exists, mock_run):
        mock_exists.return_value = True
        mock_which.return_value = "piper"
        mock_run.return_value.returncode = 0

        tts = TextToSpeech()
        events = []
        tts.on_speech_start = lambda: events.append("start")
        tts.on_speech_end = lambda: events.append("end")

        def raise_error(p):
            events.append("play_fail")
            raise RuntimeError("Audio device busy")

        tts._play_audio = raise_error

        with self.assertRaises(RuntimeError):
            tts._generate_and_play("test")

        self.assertEqual(events, ["start", "play_fail", "end"])
        tts.shutdown()

    @patch('subprocess.run')
    @patch('voice.text_to_speech.Path.exists')
    @patch('voice.text_to_speech.shutil.which')
    def test_tts_callback_on_generation_failure(self, mock_which, mock_exists, mock_run):
        mock_exists.return_value = True
        mock_which.return_value = "piper"

        # Simulate Piper generation failure BEFORE playback block
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "Piper error"

        tts = TextToSpeech()
        events = []
        tts.on_speech_start = lambda: events.append("start")
        tts.on_speech_end = lambda: events.append("end")
        tts._play_audio = lambda p: events.append("play")

        with self.assertRaises(RuntimeError):
            tts._generate_and_play("test")

        # Verify NEITHER callback fired
        self.assertEqual(events, [])
        tts.shutdown()

    @patch('subprocess.run')
    @patch('voice.text_to_speech.Path.exists')
    @patch('voice.text_to_speech.shutil.which')
    def test_tts_callback_exceptions_dont_kill_worker(self, mock_which, mock_exists, mock_run):
        mock_exists.return_value = True
        mock_which.return_value = "piper"
        mock_run.return_value.returncode = 0

        tts = TextToSpeech()
        def bad_callback():
            raise ValueError("Callback crash")

        tts.on_speech_start = bad_callback
        tts.on_speech_end = bad_callback

        try:
            tts._play_audio = lambda p: None
            tts._generate_and_play("test")
        except Exception as e:
            self.fail(f"Generate raised an exception: {e}")
        finally:
            tts.shutdown()

    def test_desktop_shared_state(self):
        from PySide6.QtWidgets import QApplication, QWidget
        app = QApplication.instance() or QApplication(sys.argv)

        # Lightweight PySide6 double replacing the heavy visual engine
        class FakeScene(QWidget):
            def set_state(self, state):
                pass

        with patch('main_window.GEXOScene', new=FakeScene):
            from main_window import MainWindow

            brain = GEXOBrain()
            window = MainWindow(brain=brain)

            # The Window MUST consume the exact injected Brain's behavior Engine
            self.assertIs(window.brain, brain)
            self.assertIs(window.behavior, brain.behavior)

    def test_process_preserves_pipeline(self):
        brain = GEXOBrain()
        response = brain.process("help", source="test")
        self.assertTrue(response.success)


if __name__ == "__main__":
    unittest.main()