# brain/wakeword/listener.py
"""
=========================================================
Project G-EXO Microphone Listener
Version : 2.2
Developer : Thatikonda Goutham Teja
=========================================================
"""
import threading
import queue
import sounddevice as sd

class MicrophoneListener:
    """
    Authoritative single-stream microphone listener.
    Maintains a single lightweight sounddevice RawInputStream stream
    and pushes raw audio chunks into a thread-safe queue immediately without blocking.
    """
    def __init__(self, sample_rate: int = 16000, channels: int = 1, blocksize: int = 1280):
        self.running = False
        self.sample_rate = sample_rate
        self.channels = channels
        self.blocksize = blocksize
        self.stream = None
        self._queue: queue.Queue[bytes] = queue.Queue(maxsize=300)
        self._lock = threading.Lock()

    def set_callback(self, callback):
        """Deprecated: Maintained for backward compatibility only. Callback is not invoked from callback thread."""
        pass

    def _audio_callback(
        self,
        indata,
        frames,
        time,
        status,
    ):
        """
        Extremely lightweight non-blocking callback.
        Performs only: bytes(indata) -> queue.put_nowait(...) -> return.
        Does not execute callbacks, inference, STT, or heavy work.
        """
        if status:
            return
        try:
            self._queue.put_nowait(bytes(indata))
        except queue.Full:
            pass
        except Exception:
            pass

    def get_audio_queue(self) -> queue.Queue[bytes]:
        """Provides access to the raw shared audio queue for single-stream consumers."""
        return self._queue

    def start(self):
        """Initializes the single authoritative microphone stream."""
        with self._lock:
            if self.running:
                return
            self.running = True
            try:
                self.stream = sd.RawInputStream(
                    samplerate=self.sample_rate,
                    channels=self.channels,
                    dtype="int16",
                    blocksize=self.blocksize,
                    device=1,
                    callback=self._audio_callback,
                )
                self.stream.start()
                print("[MicrophoneListener] Authoritative stream started.")
            except Exception as e:
                self.running = False
                if self.stream:
                    try:
                        self.stream.close()
                    except Exception:
                        pass
                    self.stream = None
                raise RuntimeError(f"Failed to start authoritative microphone listener: {e}")

    def stop(self):
        """Stops the audio stream and cleans up resources."""
        with self._lock:
            self.running = False
            if self.stream:
                try:
                    self.stream.stop()
                    self.stream.close()
                except Exception:
                    pass
                finally:
                    self.stream = None
            while not self._queue.empty():
                try:
                    self._queue.get_nowait()
                except queue.Empty:
                    break
