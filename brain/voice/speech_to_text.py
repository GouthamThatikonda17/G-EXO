"""
=========================================================
Project G-EXO
Speech To Text
Version : 3.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from __future__ import annotations

import logging

import numpy as np
from voice.recorder import Recorder
from voice.vad import VoiceActivityDetector
from voice.whisper_engine import WhisperEngine

logger = logging.getLogger(__name__)


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

    def listen(self, wait_timeout: float = 10.0, max_speech: float = 30.0) -> str:
        """
        Coordinates continuous VAD-driven capture.
        Records until end-of-speech is detected, then transcribes.
        """
        self.recorder.start()
        self.vad.reset()

        audio_buffer = []
        speech_started = False
        
        # Timeout Calculations:
        # To determine how many frames correspond to the requested timeout durations,
        # we calculate: (Total Timeout Seconds * Sample Rate) / Chunk Size per Frame
        # This converts a real-world second limitation into an exact loop-iteration limit.
        wait_limit = int((wait_timeout * self.recorder.sample_rate) / self.recorder.chunk_size)
        speech_limit = int((max_speech * self.recorder.sample_rate) / self.recorder.chunk_size)
        
        frames_waited = 0
        speech_frames = 0

        try:
            while True:
                frame = self.recorder.read(timeout=0.5)
                    

                
                
                if not speech_started:
                    frames_waited += 1       
                    if self.vad.is_speech(frame):
                        speech_started = True
                        audio_buffer.append(frame)
                    elif frames_waited >= wait_limit:
                        break
                else:
                    speech_frames += 1
                    audio_buffer.append(frame)
                    
                    if self.vad.update(frame) or speech_frames >= speech_limit:
                        break
        except Exception as e:
            logger.error(f"[SpeechToText] Pipeline error during listen loop: {e}")
        finally:
            self.recorder.stop()

        if not audio_buffer:
            return ""

        full_audio = np.concatenate(audio_buffer)
        

        # Ignore bursts shorter than a typical syllable (e.g. 0.5 seconds)
        if len(full_audio) < self.recorder.sample_rate * 0.5:
            return ""

       

       

       
        text = self.engine.transcribe(full_audio)
       

        return text.strip()

    # =====================================================
    # Shutdown
    # =====================================================

    def shutdown(self) -> None:
        self.recorder.close()