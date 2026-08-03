"""
=========================================================
Project G-EXO Desktop
Cube World Animation
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import math
import time


class CubeWorldAnimation:

    def __init__(self):

        self.start_time = time.time()

        self.wave_speed = 1.2

        self.wave_height = 4.0

        self.face_glow = 1.0

    # =====================================================
    # Time
    # =====================================================

    def time(self):

        return time.time() - self.start_time

    # =====================================================
    # Background Wave
    # =====================================================

    def background_height(self, row, col):

        t = self.time()

        value = math.sin(

            row * 0.18 +

            col * 0.12 +

            t * self.wave_speed

        )

        return value * self.wave_height

    # =====================================================
    # Face Pulse
    # =====================================================

    def pulse(self):

        t = self.time()

        return (

            math.sin(t * 2.5) * 0.08

        ) + 1.0

    # =====================================================
    # Brightness
    # =====================================================

    def brightness(self):

        t = self.time()

        return (

            math.sin(t * 1.8) * 0.15

        ) + 0.85