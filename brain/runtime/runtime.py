"""
=========================================================
Project G-EXO
Runtime Engine
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from behavior.behavior_engine import BehaviorEngine
from behavior.face_state import FaceState

from voice.voice_pipeline import VoicePipeline

from assistant import GEXOBrain


class Runtime:

    def __init__(self):

        self.behavior = BehaviorEngine()

        self.voice = VoicePipeline()

        self.brain = GEXOBrain()

        self.running = False

    # =====================================================
    # Start
    # =====================================================

    def start(self):

        self.running = True

        self.voice.start()

        self.behavior.set_state(

            FaceState.IDLE

        )

        print(

            "[Runtime] Started"

        )

    # =====================================================
    # Stop
    # =====================================================

    def stop(self):

        self.running = False

        self.voice.stop()

        print(

            "[Runtime] Stopped"

        )

    # =====================================================
    # Process
    # =====================================================

    def process(

        self,

        text,

    ):

        if not self.voice.process(

            text,

        ):

            return None

        self.behavior.set_state(

            FaceState.LISTENING

        )

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

        return response

    # =====================================================
    # Idle
    # =====================================================

    def idle(self):

        self.behavior.set_state(

            FaceState.IDLE

        )