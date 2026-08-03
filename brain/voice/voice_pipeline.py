"""
=========================================================
Project G-EXO
Voice Pipeline
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from .audio_manager import AudioManager
from .wake_word import WakeWordEngine


class VoicePipeline:

    def __init__(self):

        self.audio = AudioManager()

        self.wake_word = WakeWordEngine()

    # =====================================================
    # Start
    # =====================================================

    def start(self):

        self.audio.start()

        self.wake_word.enable()

        print(

            "[Voice] Pipeline Started"

        )

    # =====================================================
    # Stop
    # =====================================================

    def stop(self):

        self.audio.stop()

        self.wake_word.disable()

        print(

            "[Voice] Pipeline Stopped"

        )

    # =====================================================
    # Process
    # =====================================================

    def process(

        self,

        text,

    ):

        if self.wake_word.detected(

            text,

        ):

            print(

                "[Wake Word] Detected"

            )

            return True

        return False