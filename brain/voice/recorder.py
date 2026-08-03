"""
=========================================================
Project G-EXO
Recorder
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from __future__ import annotations

import threading
from typing import Optional

import numpy as np
import sounddevice as sd


class Recorder:
    """
    Owns microphone recording.

    Responsibilities
    ----------------
    - Capture microphone audio
    - Return float32 mono PCM at 16 kHz
    - No STT, VAD, Brain or UI logic
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        dtype: str = "float32",
    ) -> None:
        self.sample_rate = sample_rate
        self.channels = channels
        self.dtype = dtype
        self._lock = threading.Lock()

    def record(self, duration: float) -> np.ndarray:
        if duration <= 0:
            raise ValueError("duration must be greater than zero")

        frames = int(duration * self.sample_rate)

        with self._lock:
            audio = sd.rec(
                frames,
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype=self.dtype,
            )
            sd.wait()

        audio = np.asarray(audio, dtype=np.float32).reshape(-1)

        return audio

    def close(self) -> None:
        """Reserved for future resource cleanup."""
        return