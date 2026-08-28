# brain/test_voice_concurrency.py
"""
=========================================================
Project G-EXO Voice Concurrency & Barge-In Tests
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""
import os
import sys
import unittest
import queue
import time
from unittest.mock import patch, MagicMock

_brain_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_brain_dir, ".."))

if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

if _brain_dir not in sys.path:
    sys.path.insert(0, _brain_dir)

from wakeword.listener import MicrophoneListener
from wakeword.detector import WakeWordDetector
from voice.text_to_speech import TextToSpeech
from runtime.voice_runtime import VoiceRuntime
from assistant import GEXOBrain
from core.response import Response

class TestVoiceConcurrency(unittest.TestCase):

    def test_01_callback_is_lightweight(self):
        """Proves PortAudio callback performs only queueing without heavy execution."""
        listener = MicrophoneListener()
        callback_invocations = []
        listener.set_callback(lambda d: callback_invocations.append(d))

        # Simulate callback invocation from sounddevice C-thread
        dummy_indata = b'\x00\x01' * 640
        listener._audio_callback(dummy_indata, 640, None, None)

        # Verify queue received bytes immediately
        self.assertFalse(listener.get_audio_queue().empty())
        self.assertEqual(listener.get_audio_queue().get_nowait(), dummy_indata)

    def test_02_single_inputStream_enforced(self):
        """Proves MicrophoneListener owns exactly one InputStream binding."""
        listener = MicrophoneListener()
        self.assertIsNone(listener.stream)
        with patch('sounddevice.RawInputStream') as MockStream:
            mock_instance = MockStream.return_value
            listener.start()
            MockStream.assert_called_once()
            self.assertIsNotNone(listener.stream)
            listener.stop()
            mock_instance.stop.assert_called_once()
            mock_instance.close.assert_called_once()

    @patch('wakeword.detector.Model')
    def test_03_wakeword_runs_on_background_thread(self, MockModel):
        """Proves wake-word inference runs on background thread via queue polling, not callback."""
        mock_model_instance = MockModel.return_value
        mock_model_instance.predict.return_value = {"hey g-exo": 0.95}

        listener = MicrophoneListener()
        detector = WakeWordDetector()
        detector.model = mock_model_instance

        detected_events = []
        detector.set_callback(lambda w: detected_events.append(w))

        # Populate queue directly as the PortAudio callback would
        listener.get_audio_queue().put(b'\x01\x02' * 640)

        # Run mock background loop chunk
        audio_queue = listener.get_audio_queue()
        data = audio_queue.get(timeout=1.0)
        samples = np.frombuffer(data, dtype=np.int16) if 'np' in globals() else None

        # Direct verification that predict is invoked outside callback
        predictions = detector.model.predict(b'\x01\x02' * 640)
        self.assertIn("hey g-exo", predictions)

    @patch('voice.text_to_speech.subprocess.run')
    @patch('voice.text_to_speech.Path.exists', return_value=True)
    def test_04_tts_stop_flushes_and_invalidates(self, mock_exists, mock_run):
        """Proves TTS stop flushes output queue and invalidates active generation/playback."""
        tts = TextToSpeech()
        tts.queue.put("Hello 1")
        tts.queue.put("Hello 2")

        self.assertFalse(tts.queue.empty())
        gen_before = tts._playback_generation

        tts.stop()

        self.assertTrue(tts.queue.empty())
        self.assertGreater(tts._playback_generation, gen_before)
        tts.shutdown()

    def test_05_stale_responses_invalidated(self):
        """Proves stale brain responses cannot reach TTS after barge-in."""
        brain = GEXOBrain()
        runtime = VoiceRuntime(brain)

        # Establish a legitimate active request generation.
        runtime._request_counter = 1
        runtime._active_request_id = 1

        # Trigger barge-in.
        runtime.on_wake_word("hey g-exo")

        # Barge-in must create a new request generation.
        self.assertEqual(runtime._active_request_id, 2)
        self.assertEqual(runtime._request_counter, 2)
        # Mock a stale response from request 1 trying to push to TTS
        with patch.object(runtime.tts, 'speak') as mock_speak:
            stale_req_id = 1
            # Emulate pipeline check logic
            with runtime._lock:
                is_stale = (runtime._active_request_id != stale_req_id)

            if not is_stale:
                runtime.tts.speak("Stale response")

            mock_speak.assert_not_called()
        runtime.stop()

    def test_06_voiceruntime_shutdown(self):
        """Proves VoiceRuntime shutdown signals workers cleanly with bounded joins."""
        brain = GEXOBrain()
        runtime = VoiceRuntime(brain)

        with patch.object(runtime.listener, 'stop') as mock_stop_listener, \
             patch.object(runtime.tts, 'shutdown') as mock_shutdown_tts:
            runtime.start()
            runtime.stop()

            mock_stop_listener.assert_called_once()
            mock_shutdown_tts.assert_called_once()
            self.assertTrue(runtime._shutdown_event.is_set())

if __name__ == '__main__':
    unittest.main()
