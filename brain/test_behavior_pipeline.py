"""
=========================================================
Project G-EXO Behavior Pipeline Tests
Version : 2.2
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

import time
import unittest
from unittest.mock import patch, MagicMock

# Explicitly import main_window directly since desktop/ is in sys.path
import main_window

from behavior.behavior_engine import BehaviorEngine
from behavior.face_state import FaceState
from emotion.models import EmotionState
from voice.text_to_speech import TextToSpeech
from assistant import GEXOBrain
from core.response import Response


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

    def test_desktop_shared_state_and_ui_layout(self):
        from PySide6.QtWidgets import QApplication, QWidget
        from PySide6.QtGui import QKeyEvent, QCloseEvent
        from PySide6.QtCore import Qt
        app = QApplication.instance() or QApplication(sys.argv)

        # Lightweight PySide6 double replacing the heavy visual engine
        class FakeScene(QWidget):
            def set_state(self, state):
                pass

        with patch('main_window.GEXOScene', new=FakeScene):
            from main_window import MainWindow

            brain = GEXOBrain()
            window = MainWindow(brain=brain)

            window.show()
            app.processEvents()
            # The Window MUST consume the exact injected Brain's behavior Engine
            self.assertIs(window.brain, brain)
            self.assertIs(window.behavior, brain.behavior)

            # Verify Phase 4 requirements: Developer Console is completely hidden on launch
            self.assertFalse(window.dev_console.isVisible())

            # Assert Developer Mode Hotkey (F12) successfully surfaces the hidden interface
            event = QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key_F12, Qt.KeyboardModifier.NoModifier)
            window.keyPressEvent(event)
            self.assertTrue(window.dev_console.isVisible())

            # Assert Toggle functionality cleanly hides the UI component back off-screen
            event = QKeyEvent(QKeyEvent.Type.KeyPress, Qt.Key_QuoteLeft, Qt.KeyboardModifier.NoModifier)
            window.keyPressEvent(event)
            self.assertFalse(window.dev_console.isVisible())

            window.closeEvent(QCloseEvent())

    def test_repeated_message_lifecycle(self):
        """
        Validates the Phase 3 fix: ensuring sequential messaging creates new background
        threads smoothly without relying on stale QThread references or premature cleanup.
        """
        from PySide6.QtWidgets import QApplication, QWidget
        from PySide6.QtGui import QCloseEvent
        app = QApplication.instance() or QApplication(sys.argv)

        class FakeScene(QWidget):
            def set_state(self, state):
                pass

        with patch('main_window.GEXOScene', new=FakeScene):
            from main_window import MainWindow
            brain = GEXOBrain()

            def fake_process_1(*args, **kwargs):
                time.sleep(0.1)
                return Response(success=True, message="Test 1")

            brain.process = MagicMock(side_effect=fake_process_1)

            window = MainWindow(brain=brain)

            # ----------------------------------------------------
            # A. First message
            # ----------------------------------------------------
            window.message_input.input.setText("Message 1")
            window._send_message()
            self.assertIsNotNone(window.thread)
            first_thread = window.thread

            # D. Attempt second message while first is genuinely running
            # Because self.thread is undeniably not None, the UI correctly rejects the input.
            with patch.object(window.thread, 'isRunning', return_value=True):
                window.message_input.input.setText("Concurrent Message")
                window._send_message()
            self.assertEqual(window.thread, first_thread) # Thread did not change

            # E. Verify actual thread resolution via Qt Event Loop
            timeout = time.time() + 2.0
            while window.thread is not None and time.time() < timeout:
                app.processEvents()

            self.assertIsNone(window.thread) # References correctly clear ONLY upon completion
            self.assertTrue(window.message_input.input.isEnabled())

            # ----------------------------------------------------
            # B. Second message starts fresh (Simulating failure context)
            # ----------------------------------------------------
            def fake_process_2(*args, **kwargs):
                time.sleep(0.1)
                raise Exception("Simulated Error")

            brain.process = MagicMock(side_effect=fake_process_2)
            window.message_input.input.setText("Message 2")
            window._send_message()
            self.assertIsNotNone(window.thread)
            second_thread = window.thread
            self.assertNotEqual(second_thread, first_thread)

            timeout = time.time() + 2.0
            while window.thread is not None and time.time() < timeout:
                app.processEvents()

            # F. Worker failure safely resolves thread states
            self.assertIsNone(window.thread)
            self.assertTrue(window.message_input.input.isEnabled())

            # ----------------------------------------------------
            # C. Third message (Proof of continued stability)
            # ----------------------------------------------------
            def fake_process_3(*args, **kwargs):
                time.sleep(0.1)
                return Response(success=True, message="Test 3")

            brain.process = MagicMock(side_effect=fake_process_3)
            window.message_input.input.setText("Message 3")
            window._send_message()
            self.assertIsNotNone(window.thread)

            timeout = time.time() + 2.0
            while window.thread is not None and time.time() < timeout:
                app.processEvents()

            self.assertIsNone(window.thread)

            # ----------------------------------------------------
            # G. Close Event handles active thread safely
            # ----------------------------------------------------
            def fake_process_4(*args, **kwargs):
                time.sleep(0.1)
                return Response(success=True, message="Test 4")

            brain.process = MagicMock(side_effect=fake_process_4)
            window.message_input.input.setText("Message 4")
            window._send_message()
            self.assertIsNotNone(window.thread)

            window.closeEvent(QCloseEvent())
            self.assertIsNone(window.thread)

    def test_process_preserves_pipeline(self):
        brain = GEXOBrain()
        response = brain.process("help", source="test")
        self.assertTrue(response.success)


if __name__ == "__main__":
    unittest.main()
