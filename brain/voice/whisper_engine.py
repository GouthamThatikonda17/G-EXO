"""
=========================================================
Project G-EXO
Whisper Engine
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from __future__ import annotations

import threading
from typing import Optional

import numpy as np
from faster_whisper import WhisperModel


class WhisperEngine:
    """
    Owns the Faster-Whisper model.
    """

    def __init__(
        self,
        model_name: str = "small",
        device: Optional[str] = None,
        compute_type: Optional[str] = None,
    ) -> None:

        self._lock = threading.Lock()

        if device is None:
            try:
                import torch
                device = "cuda" if torch.cuda.is_available() else "cpu"
            except Exception:
                device = "cpu"

        if compute_type is None:
            compute_type = "float16" if device == "cuda" else "int8"

        self._model = WhisperModel(
            model_name,
            device=device,
            compute_type=compute_type,
        )

    def transcribe(self, audio: np.ndarray) -> str:
        if audio is None:
            return ""

        if not isinstance(audio, np.ndarray):
            raise TypeError("audio must be numpy.ndarray")

       
        with self._lock:
            segments, info = self._model.transcribe(
                audio,
                beam_size=5,
                vad_filter=True,
            )

            segment_list = list(segments)

       
        text = " ".join(
            segment.text.strip()
            for segment in segment_list
            if segment.text.strip()
        ).strip()

       
        return text
    