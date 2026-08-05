"""
=========================================================
Project G-EXO Application Composition Root
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from assistant import GEXOBrain
from runtime.voice_runtime import VoiceRuntime


class Application:
    """
    Composition Root for Project G-EXO.
    Responsible strictly for dependency wiring and lifecycle management.
    Contains zero business, AI, UI, voice, or memory logic.
    """

    def __init__(self):
        self.brain = GEXOBrain()

    def create_voice_runtime(self) -> VoiceRuntime:
        """Creates and returns VoiceRuntime injected with the shared GEXOBrain."""
        return VoiceRuntime(self.brain)