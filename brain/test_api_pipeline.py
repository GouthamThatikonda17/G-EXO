# brain/test_api_pipeline.py
"""
=========================================================
Project G-EXO API Pipeline Tests
Version : 1.3
Developer : Thatikonda Goutham Teja
=========================================================
"""
import io
import wave
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

_brain_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_brain_dir, ".."))

if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

if _brain_dir not in sys.path:
    sys.path.insert(0, _brain_dir)

from fastapi.testclient import TestClient
from api.app import app
from assistant import GEXOBrain

def _create_test_wav_bytes(
    sample_rate: int = 16000,
    channels: int = 1,
    sample_width: int = 2,
    duration_sec: float = 0.5,
) -> bytes:
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        n_frames = int(sample_rate * duration_sec)
        wf.writeframes(b"\x00" * (sample_width * n_frames * channels))
    return buf.getvalue()

class TestAPIPipeline(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_01_root_endpoint(self):
        """Validates the GET / contract."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["project"], "G-EXO")
        self.assertEqual(data["status"], "Running")
        self.assertEqual(data["version"], "2.2")

    @patch("assistant.GEXOBrain.process")
    def test_02_chat_reaches_gexobrain(self, mock_process):
        """Proves /chat delegates directly to GEXOBrain without AIRouter."""
        mock_response = MagicMock()
        mock_response.success = True
        mock_response.message = "Hello Android"
        mock_process.return_value = mock_response

        response = self.client.post("/chat", json={
            "message": "hello",
            "source": "android",
            "session_id": "test_session"
        })

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["response"], "Hello Android")
        self.assertIn("face_state", data)
        self.assertIn("emotion", data)
        mock_process.assert_called_once_with("hello", source="android")

    def test_03_invalid_chat_payload(self):
        """Malformed JSON payloads yield HTTP 422."""
        response = self.client.post("/chat", json={})
        self.assertEqual(response.status_code, 422)

    @patch("voice.whisper_engine.WhisperEngine.transcribe")
    def test_04_voice_transcribe_valid_mono(self, mock_transcribe):
        """Valid 16 kHz 16-bit PCM mono WAV upload returns transcribed text."""
        mock_transcribe.return_value = "transcribed voice"
        wav_data = _create_test_wav_bytes(sample_rate=16000, channels=1, sample_width=2)

        response = self.client.post(
            "/api/v1/voice/transcribe",
            files={"file": ("test.wav", wav_data, "audio/wav")}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["text"], "transcribed voice")
        mock_transcribe.assert_called_once()

    @patch("voice.whisper_engine.WhisperEngine.transcribe")
    def test_05_voice_transcribe_valid_stereo(self, mock_transcribe):
        """Valid 16 kHz 16-bit PCM stereo WAV upload is accepted and downmixed."""
        mock_transcribe.return_value = "transcribed stereo"
        wav_data = _create_test_wav_bytes(sample_rate=16000, channels=2, sample_width=2)

        response = self.client.post(
            "/api/v1/voice/transcribe",
            files={"file": ("stereo.wav", wav_data, "audio/wav")}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["text"], "transcribed stereo")
        mock_transcribe.assert_called_once()

    def test_06_voice_transcribe_unsupported_sample_rate(self):
        """WAV files not recorded at 16 kHz return HTTP 400."""
        wav_data = _create_test_wav_bytes(sample_rate=44100, channels=1, sample_width=2)

        response = self.client.post(
            "/api/v1/voice/transcribe",
            files={"file": ("wrong_rate.wav", wav_data, "audio/wav")}
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("Unsupported sample rate: expected 16000 Hz, got 44100 Hz", response.json()["detail"])

    def test_07_voice_transcribe_unsupported_sample_width(self):
        """WAV files not encoded as 16-bit PCM return HTTP 400."""
        wav_data = _create_test_wav_bytes(sample_rate=16000, channels=1, sample_width=1)

        response = self.client.post(
            "/api/v1/voice/transcribe",
            files={"file": ("8bit.wav", wav_data, "audio/wav")}
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("Unsupported audio encoding: expected 16-bit PCM, got 8-bit", response.json()["detail"])

    def test_08_voice_transcribe_malformed_wav(self):
        """Malformed/non-WAV bytes produce HTTP 400."""
        response = self.client.post(
            "/api/v1/voice/transcribe",
            files={"file": ("corrupt.wav", b"NOT_A_WAV_FILE", "audio/wav")}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Malformed or invalid WAV container", response.json()["detail"])

    def test_09_voice_transcribe_empty(self):
        """Empty audio payload produces HTTP 400."""
        response = self.client.post(
            "/api/v1/voice/transcribe",
            files={"file": ("empty.wav", b"", "audio/wav")}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Empty audio payload provided", response.json()["detail"])

    @patch("voice.text_to_speech.TextToSpeech.synthesize_bytes")
    def test_10_voice_synthesize_valid(self, mock_synthesize):
        """Valid synthesis returns audio/wav binary bytes without local playback."""
        mock_synthesize.return_value = b"RIFF_TEST_SYNTH_WAV"

        response = self.client.post("/api/v1/voice/synthesize", json={
            "text": "Hello voice"
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "audio/wav")
        self.assertEqual(response.content, b"RIFF_TEST_SYNTH_WAV")
        mock_synthesize.assert_called_once_with("Hello voice")

    def test_11_voice_synthesize_empty_text(self):
        """Empty synthesis text triggers Pydantic HTTP 422 validation failure."""
        response = self.client.post("/api/v1/voice/synthesize", json={
            "text": "   "
        })
        self.assertEqual(response.status_code, 422)

    @patch("ai.router.AIRouter.__init__", return_value=None)
    def test_12_architecture_invariant_no_airouter(self, mock_airouter):
        """Proves API relies on app.state.brain without instantiating AIRouter."""
        self.assertIsInstance(app.state.brain, GEXOBrain)
        self.assertEqual(mock_airouter.call_count, 0)

if __name__ == "__main__":
    unittest.main()