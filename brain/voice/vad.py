"""
=========================================================
Project G-EXO
Voice Activity Detector
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from __future__ import annotations

import numpy as np


class VoiceActivityDetector:
    """
    Lightweight energy-based VAD.

    Responsibilities
    ----------------
    - Detect whether a frame contains speech.
    - Determine when speech has ended.
    """

    def __init__(
        self,
        threshold: float = 0.015,
        silence_frames: int = 20,
    ) -> None:
        self.threshold = threshold
        self.silence_frames = silence_frames
        self._silence_count = 0

    def reset(self) -> None:
        self._silence_count = 0

    def is_speech(self, frame: np.ndarray) -> bool:
        if frame is None or frame.size == 0:
            return False
        energy = float(np.sqrt(np.mean(np.square(frame))))
        return energy >= self.threshold

    def update(self, frame: np.ndarray) -> bool:
        """
        Returns True when end-of-speech is detected.
        """
        if self.is_speech(frame):
            self._silence_count = 0
            return False

        self._silence_count += 1
        return self._silence_count >= self.silence_frames