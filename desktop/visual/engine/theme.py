"""
=========================================================
Project G-EXO Desktop
Visual Engine Theme
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from PySide6.QtGui import QColor


class VisualTheme:

    def __init__(self):

        # =====================================================
        # World
        # =====================================================

        self.background = QColor(8, 10, 16)

        self.cube = QColor(35, 45, 65)

        self.glow = QColor(0, 220, 255)

        self.eye = QColor(0, 255, 255)

        self.mouth = QColor(0, 220, 255)

        self.eyebrow = QColor(120, 255, 255)

        self.error = QColor(255, 70, 70)

        self.thinking = QColor(180, 220, 255)

        self.listening = QColor(80, 255, 255)

        # =====================================================
        # Grid
        # =====================================================

        self.cube_size = 6

        self.spacing = 10

        self.corner_radius = 2

        self.rows = 75

        self.cols = 140

        # =====================================================
        # Animation
        # =====================================================

        self.wave_speed = 1.15

        self.wave_height = 2.8

        self.breath_speed = 0.35

        self.glow_strength = 0.35

        self.pulse_speed = 2.0

        # =====================================================
        # Face
        # =====================================================

        self.eye_radius = 7

        self.eye_distance = 24

        self.mouth_width = 12

        self.mouth_height = 2

        self.eyebrow_length = 10

        # =====================================================
        # Performance
        # =====================================================

        self.target_fps = 60

        self.frame_interval = 16