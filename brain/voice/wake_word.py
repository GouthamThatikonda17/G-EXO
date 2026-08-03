"""
=========================================================
Project G-EXO
Wake Word Engine
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""


class WakeWordEngine:

    def __init__(self):

        self.enabled = False

        self.wake_word = "hey g-exo"

    # =====================================================
    # Enable
    # =====================================================

    def enable(self):

        self.enabled = True

    # =====================================================
    # Disable
    # =====================================================

    def disable(self):

        self.enabled = False

    # =====================================================
    # Status
    # =====================================================

    def active(self):

        return self.enabled

    # =====================================================
    # Wake Word
    # =====================================================

    def set_wake_word(

        self,

        text,

    ):

        self.wake_word = text.lower()

    # =====================================================
    # Check
    # =====================================================

    def detected(

        self,

        text,

    ):

        if not self.enabled:

            return False

        return self.wake_word in text.lower()