""" =========================================================
Project G-EXO
Voice Runtime
Version : 1.2
Developer : Thatikonda Goutham Teja
=========================================================
"""
import threading

from behavior.behavior_engine import BehaviorEngine
from behavior.face_state import FaceState
from wakeword.listener import MicrophoneListener
from wakeword.detector import WakeWordDetector
from voice.speech_to_text import SpeechToText
from voice.text_to_speech import TextToSpeech
from assistant import GEXOBrain


class VoiceRuntime:
    def __init__(self):
        self.behavior = BehaviorEngine()
        self.listener = MicrophoneListener()
        self.detector = WakeWordDetector()
        self.stt = SpeechToText()
        self.tts = TextToSpeech()
        self.brain = GEXOBrain()

        self._interaction_lock = threading.Lock()
        self._is_processing = False

        self.listener.set_callback(
            self.detector.process
        )
        self.detector.set_callback(
            self.on_wake_word
        )

    # =====================================================
    # Start
    # =====================================================
    def start(self):
        print(
            "[Runtime] Started"
        )
        self.behavior.set_state(
            FaceState.IDLE
        )
        self.listener.start()

    # =====================================================
    # Stop
    # =====================================================
    def stop(self):
        self.listener.stop()

    # =====================================================
    # Wake Word
    # =====================================================
    def on_wake_word(
        self,
        wakeword,
    ):
        with self._interaction_lock:
            if self._is_processing:
                return
            self._is_processing = True

        threading.Thread(
            target=self._process_interaction,
            args=(wakeword,),
            daemon=True,
            name="VoiceInteractionWorker"
        ).start()

    # =====================================================
    # Interaction Worker
    # =====================================================
    def _process_interaction(
        self,
        wakeword,
    ):
        print("[Runtime] Voice interaction started")
        
        try:
            try:
                self.listener.stop()
            except Exception as e:
                print(f"[Runtime] Failed to stop listener: {e}")

            print(
                f"[Wake] {wakeword}"
            )
            self.behavior.set_state(
                FaceState.LISTENING
            )

            text = self.stt.listen()

            if not text:
                self.behavior.set_state(
                    FaceState.IDLE
                )
                return

            self.behavior.set_state(
                FaceState.THINKING
            )
            
            response = self.brain.process(
                text,
                source="voice",
            )

            self.behavior.set_state(
                FaceState.SPEAKING
            )
            
            self.tts.speak(
                response.message
            )

            self.behavior.set_state(
                FaceState.IDLE
            )

        finally:
            try:
                self.listener.start()
            except Exception as e:
                print(f"[Runtime] Failed to start listener: {e}")
                
            with self._interaction_lock:
                self._is_processing = False
                
            print("[Runtime] Voice interaction finished")