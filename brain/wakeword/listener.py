"""
=========================================================
Project G-EXO
Microphone Listener
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import threading
import sounddevice as sd


class MicrophoneListener:

    def __init__(self):

        self.running = False

        self.sample_rate = 16000

        self.channels = 1

        self.callback = None

        self.stream = None

    # =====================================================
    # Callback
    # =====================================================

    def set_callback(self, callback):

        self.callback = callback

    # =====================================================
    # Audio
    # =====================================================

    def _audio_callback(

        self,

        indata,

        frames,

        time,

        status,

    ):

        if status:

            return

        if self.callback:
            self.callback(
                bytes(indata),
            )

    # =====================================================
    # Start
    # =====================================================

    def start(self):

        if self.running:

            return

        self.running = True

        self.stream = sd.RawInputStream(
  
             samplerate=self.sample_rate,

             channels=self.channels,

             dtype="int16",

             blocksize=1280,

             device=1,

             callback=self._audio_callback,

         )

        self.stream.start()

        print("[WakeWord] Listening...")

    # =====================================================
    # Stop
    # =====================================================

    def stop(self):

        self.running = False

        if self.stream:

            self.stream.stop()

            self.stream.close()

            self.stream = None