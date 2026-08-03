"""
=========================================================
Project G-EXO
Voice Runtime
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

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