# brain/runtime/voice_runtime.py
"""
=========================================================
Project G-EXO Voice Runtime
Version : 2.1
Developer : Thatikonda Goutham Teja
=========================================================
"""
import threading
import queue
import numpy as np
from behavior.face_state import FaceState
from wakeword.listener import MicrophoneListener
from wakeword.detector import WakeWordDetector
from voice.speech_to_text import SpeechToText
from voice.text_to_speech import TextToSpeech
from assistant import GEXOBrain

class VoiceRuntime:
    """
    Asynchronous, non-blocking voice runtime supporting background execution,
    shared single-stream microphone access, and cooperative request cancellation (barge-in).
    """
    def __init__(self, brain: GEXOBrain):
        self.brain = brain
        self.behavior = self.brain.behavior
        self.listener = MicrophoneListener()
        self.detector = WakeWordDetector()
        self.stt = SpeechToText()
        self.tts = TextToSpeech()

        # Request tracking and token generation for barge-in / stale invalidation
        self._request_counter = 0
        self._active_request_id = 0
        self._lock = threading.Lock()

        # Shutdown flag
        self._shutdown_event = threading.Event()

        # Securely bind TTS physical lifecycle events to visual behavior engine.
        self.tts.on_speech_start = lambda: self.behavior.set_state(FaceState.SPEAKING)
        self.tts.on_speech_end = lambda: self.behavior.set_state(FaceState.IDLE)

        # Background workers
        self._wakeword_worker_thread = threading.Thread(
            target=self._wakeword_loop,
            daemon=True,
            name="WakeWordWorker"
        )
        self._voice_pipeline_thread = threading.Thread(
            target=self._pipeline_loop,
            daemon=True,
            name="VoicePipelineWorker"
        )

        self._utterance_trigger = threading.Event()

    def _wakeword_loop(self):
        """
        Background thread pulling from MicrophoneListener's authoritative audio queue
        and running ONNX wake-word detection completely outside the PortAudio callback thread.
        """
        accumulated_samples = np.array([], dtype=np.int16)
        audio_queue = self.listener.get_audio_queue()

        while not self._shutdown_event.is_set():
            try:
                data = audio_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            if not self.detector.enabled:
                continue

            samples = np.frombuffer(data, dtype=np.int16)
            if samples.size == 0:
                continue

            accumulated_samples = np.concatenate((accumulated_samples, samples))

            # Process chunks of suitable size for openWakeWord model expectations
            while accumulated_samples.size >= 1280:
                chunk = accumulated_samples[:1280]
                accumulated_samples = accumulated_samples[1280:]

                predictions = self.detector.model.predict(chunk)
                if predictions:
                    for wakeword, confidence in predictions.items():
                        if confidence >= self.detector.threshold:
                            print(f"[WakeWord] Detected: {wakeword} ({confidence:.2f})")
                            self.on_wake_word(wakeword)
                            break

    def on_wake_word(self, wakeword: str):
        """Handles wake word detection, enforcing barge-in and request invalidation."""
        with self._lock:
            # 1. Increment request ID to invalidate any currently running stale brain/STT tasks
            self._request_counter += 1
            self._active_request_id = self._request_counter

        # 2. Stop active TTS playback and flush pending output immediately
        self.tts.stop()

        # 3. Transition behavior state to LISTENING
        self.behavior.set_state(FaceState.LISTENING)

        # 4. Trigger the pipeline loop worker to capture utterance
        self._utterance_trigger.set()

    def _pipeline_loop(self):
        """Background worker handling speech capture, STT, and GEXOBrain execution off the callback path."""
        while not self._shutdown_event.is_set():
            triggered = self._utterance_trigger.wait(timeout=0.5)
            if not triggered:
                continue
            self._utterance_trigger.clear()

            with self._lock:
                req_id = self._active_request_id

            try:
                # Disable wake-word detector temporarily while capturing user utterance
                self.detector.disable()

                text = self._capture_utterance(req_id)

                if not text:
                    with self._lock:
                        if self._active_request_id == req_id:
                            self.behavior.set_state(FaceState.IDLE)
                    continue

                with self._lock:
                    if self._active_request_id != req_id:
                        # Request was superseded/interrupted during STT
                        continue
                    self.behavior.set_state(FaceState.THINKING)

                # Execute Brain processing on background worker thread (cooperative cancellation via token check after return)
                response = self.brain.process(text, source="voice")

                with self._lock:
                    if self._active_request_id != req_id:
                        # Stale response check: discard output if barge-in happened during brain processing
                        print("[VoiceRuntime] Discarding stale response due to barge-in interruption.")
                        continue

                # Pass response message to TTS
                if response and response.message:
                    self.tts.speak(response.message)
                else:
                    self.behavior.set_state(FaceState.IDLE)

            except Exception as e:
                print(f"[VoiceRuntime Error] Pipeline execution failed: {e}")
                with self._lock:
                    self.behavior.set_state(FaceState.IDLE)
            finally:
                self.detector.enable()

    def _capture_utterance(self, req_id: int) -> str:
        """
        Captures user speech using VAD while consuming from the shared single listener queue,
        avoiding competing hardware InputStream conflicts.
        """
        self.stt.vad.reset()
        audio_buffer = []
        speech_started = False

        wait_timeout = 8.0
        max_speech = 25.0
        sample_rate = self.listener.sample_rate
        chunk_size = self.listener.blocksize

        wait_limit = int((wait_timeout * sample_rate) / chunk_size)
        speech_limit = int((max_speech * sample_rate) / chunk_size)

        frames_waited = 0
        speech_frames = 0

        shared_queue = self.listener.get_audio_queue()

        while not self._shutdown_event.is_set():
            with self._lock:
                if self._active_request_id != req_id:
                    return ""

            try:
                data = shared_queue.get(timeout=0.2)
            except queue.Empty:
                frames_waited += 1
                if frames_waited >= wait_limit and not speech_started:
                    break
                continue

            frame = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0

            if not speech_started:
                frames_waited += 1
                if self.stt.vad.is_speech(frame):
                    speech_started = True
                    audio_buffer.append(frame)
                elif frames_waited >= wait_limit:
                    break
            else:
                speech_frames += 1
                audio_buffer.append(frame)
                if self.stt.vad.update(frame) or speech_frames >= speech_limit:
                    break

        if not audio_buffer:
            return ""

        full_audio = np.concatenate(audio_buffer)
        if len(full_audio) < sample_rate * 0.4:
            return ""

        return self.stt.engine.transcribe(full_audio).strip()

    def start(self):
        """Starts the voice runtime, audio listener, and background processing workers."""
        print("[VoiceRuntime] Starting asynchronous voice runtime...")
        self.behavior.set_state(FaceState.IDLE)
        self.listener.start()
        self._wakeword_worker_thread.start()
        self._voice_pipeline_thread.start()

    def stop(self):
        """Cleanly stops the voice runtime, worker threads, and audio streams with bounded joins."""
        print("[VoiceRuntime] Stopping voice runtime...")
        self._shutdown_event.set()
        self._utterance_trigger.set()  # Unblock thread wait
        self.listener.stop()
        self.tts.shutdown()

        if self._wakeword_worker_thread.is_alive():
            self._wakeword_worker_thread.join(timeout=1.0)
        if self._voice_pipeline_thread.is_alive():
            self._voice_pipeline_thread.join(timeout=1.0)
