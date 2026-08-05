"""
=========================================================
Project G-EXO
Recorder
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from __future__ import annotations

import logging
import queue
import threading
from typing import Optional

import numpy as np
import sounddevice as sd

logger = logging.getLogger(__name__)


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
        chunk_size: int = 1024,
        max_queue_size: int = 200,
    ) -> None:
        self.sample_rate = sample_rate
        self.channels = channels
        self.dtype = dtype
        self.chunk_size = chunk_size
        self._lock = threading.Lock()
        
        self._queue: queue.Queue[np.ndarray] = queue.Queue(maxsize=max_queue_size)
        self._stream: Optional[sd.InputStream] = None
        self._is_recording = False

    def _callback(
            
            
        self,
        indata: np.ndarray,
        frames: int,
        time_info: dict,
        status: sd.CallbackFlags
    ) -> None:
        

        """Processes audio input chunks and manages callback status logs."""
        if status:
            logger.warning(f"[Recorder] Callback status: {status}")

        if self._is_recording:
            try:
                processed_data = indata.copy().reshape(-1)

                self._queue.put_nowait(processed_data)

            except queue.Full:
                logger.warning("[Recorder] Audio queue is full. Dropping frame.")
            

    def start(self) -> None:
        """Initializes and starts the continuous audio stream."""
        with self._lock:
            if self._is_recording:
                return

            try:
            
                self._stream = sd.InputStream(
                    samplerate=self.sample_rate,
                    channels= self.channels,
                    dtype=self.dtype,
                    blocksize=self.chunk_size,
                    device=1,
                    callback=self._callback
                )
    
                self._stream.start()
                self._is_recording = True
            except sd.PortAudioError as e:
                self._is_recording = False
                if self._stream is not None:
                    self._stream.close()
                    self._stream = None
                logger.error(f"[Recorder] Audio device initialization failure: {e}")
                raise RuntimeError(f"Microphone initialization failed due to audio device error: {e}")
            except Exception as e:
                self._is_recording = False
                if self._stream is not None:
                    self._stream.close()
                    self._stream = None
                logger.error(f"[Recorder] Unexpected initialization failure: {e}")
                raise RuntimeError(f"Microphone initialization failed: {e}")

    def stop(self) -> None:
        """Stops the stream, cleans up resources, and clears unbounded data."""
        with self._lock:
            if not self._is_recording:
                return
            self._is_recording = False

            if self._stream is not None:
                try:
                    self._stream.stop()
                    self._stream.close()
                except sd.PortAudioError as e:
                    logger.error(f"[Recorder] Audio device cleanup error: {e}")
                except Exception as e:
                    logger.error(f"[Recorder] Unexpected cleanup error: {e}")
                finally:
                    self._stream = None

            while not self._queue.empty():
                try:
                    self._queue.get_nowait()
                except queue.Empty:
                    break

    def read(self, timeout: float = 1.0) -> Optional[np.ndarray]:
        """Reads the next available audio frame from the queue safely."""
        try:
            return self._queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def record(self, duration: float) -> np.ndarray:
        """
        Backward compatible blocking record method.
        Retained to avoid breaking external synchronous dependencies.
        """
        if duration <= 0:
            raise ValueError("duration must be greater than zero")

        frames = int(duration * self.sample_rate)

        with self._lock:
            try:
                audio = sd.rec(
                    frames,
                    samplerate=self.sample_rate,
                    channels=self.channels,
                    dtype=self.dtype,
                )
                sd.wait()
            except sd.PortAudioError as e:
                logger.error(f"[Recorder] PortAudio failed to record: {e}")
                raise RuntimeError(f"Recording failed at device level: {e}")
            except Exception as e:
                logger.error(f"[Recorder] Failed to record: {e}")
                raise RuntimeError(f"Recording failed: {e}")

        return np.asarray(audio, dtype=np.float32).reshape(-1)

    def close(self) -> None:
        """Resource cleanup."""
        self.stop()