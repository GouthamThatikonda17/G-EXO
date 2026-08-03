"""
=========================================================
Project G-EXO
Wake Word Pipeline
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from wakeword.listener import MicrophoneListener
from wakeword.detector import WakeWordDetector


class WakeWordPipeline:

    def __init__(self):

        self.listener = MicrophoneListener()

        self.detector = WakeWordDetector()

        self.callback = None

        self.listener.set_callback(

            self.detector.process

        )

        self.detector.set_callback(

            self._on_detected

        )

    # =====================================================
    # Callback
    # =====================================================

    def set_callback(

        self,

        callback,

    ):

        self.callback = callback

    # =====================================================
    # Wake Word
    # =====================================================

    def _on_detected(

        self,

        wakeword,

    ):

        print(

            f"[Pipeline] Wake Word: {wakeword}"

        )

        if self.callback:

            self.callback(

                wakeword,

            )

    # =====================================================
    # Start
    # =====================================================

    def start(self):

        self.listener.start()

    # =====================================================
    # Stop
    # =====================================================

    def stop(self):

        self.listener.stop()