"""
=========================================================
Project G-EXO
Speech To Text
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from __future__ import annotations

from voice.recorder import Recorder
from voice.vad import VoiceActivityDetector
from voice.whisper_engine import WhisperEngine


class SpeechToText:
    """
    Coordinates the speech recognition pipeline.

    Pipeline:
        Recorder -> VAD -> WhisperEngine
    """

    def __init__(self) -> None:
        self.recorder = Recorder()
        self.vad = VoiceActivityDetector()
        self.engine = WhisperEngine()

    # =====================================================
    # Listen
    # =====================================================

    def listen(self) -> str:
        """
        Temporary orchestration.

        Records a short utterance and transcribes it.
        This will evolve into continuous VAD-driven capture
        as the recorder is upgraded.
        """
        audio = self.recorder.record(duration=5.0)

        if audio is None or len(audio) == 0:
            return ""

        text = self.engine.transcribe(audio)

        return text.strip()

    # =====================================================
    # Shutdown
    # =====================================================

    def shutdown(self) -> None:
        self.recorder.close()