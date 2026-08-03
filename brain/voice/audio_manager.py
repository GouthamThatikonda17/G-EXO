"""
=========================================================
Project G-EXO
Audio Manager
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

class AudioManager:

    def __init__(self):

        self.is_listening = False

    # =====================================================
    # Start
    # =====================================================

    def start(self):

        self.is_listening = True

    # =====================================================
    # Stop
    # =====================================================

    def stop(self):

        self.is_listening = False

    # =====================================================
    # Status
    # =====================================================

    def active(self):

        return self.is_listening