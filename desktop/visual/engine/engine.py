"""
=========================================================
Project G-EXO Desktop
Visual Engine
Version : 8.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from dataclasses import dataclass

from PySide6.QtGui import QColor

from .theme import VisualTheme
from .face_mapper import FaceMapper


# =========================================================
# Cube
# =========================================================

@dataclass(slots=True)
class Cube:

    base_x: float
    base_y: float

    x: float
    y: float

    size: float
    radius: float

    color: QColor
    alpha: int

    height: float = 0.0
    target_height: float = 0.0

    glow: float = 0.0

    is_eye: bool = False
    is_eyebrow: bool = False
    is_background: bool = True


# =========================================================
# Visual Engine
# =========================================================

class VisualEngine:

    def __init__(self):

        self.theme = VisualTheme()

        self.face_mapper = FaceMapper()

        self.cubes = []

        self.initialized = False

        self.width = 0
        self.height = 0

        self.rows = 0
        self.cols = 0

    # =====================================================
    # Initialize
    # =====================================================

    def initialize(

        self,

        width,

        height,

    ):

        if self.initialized:

            return

        self.width = width
        self.height = height

        self.cubes.clear()

        spacing = self.theme.spacing

        self.cols = int(width / spacing) + 2
        self.rows = int(height / spacing) + 2

        self.face_mapper.build(

            self.rows,

            self.cols,

        )

        for row in range(self.rows):

            for col in range(self.cols):

                x = col * spacing
                y = row * spacing

                position = (row, col)

                is_eye = (

                    position in self.face_mapper.left_eye

                    or position in self.face_mapper.right_eye

                )

                is_eyebrow = (

                    position in self.face_mapper.left_brow

                    or position in self.face_mapper.right_brow

                )

                if is_eye:

                    color = QColor(self.theme.eye)
                    alpha = 255

                elif is_eyebrow:

                    color = QColor(self.theme.eyebrow)
                    alpha = 255

                else:

                    color = QColor(self.theme.cube)
                    alpha = 120

                self.cubes.append(

                    Cube(

                        base_x=x,
                        base_y=y,

                        x=x,
                        y=y,

                        size=self.theme.cube_size,
                        radius=self.theme.corner_radius,

                        color=color,
                        alpha=alpha,

                        is_eye=is_eye,
                        is_eyebrow=is_eyebrow,
                        is_background=not (
                            is_eye
                            or is_eyebrow
                        ),

                    )

                )

        self.initialized = True

    # =====================================================
    # Update
    # =====================================================

    def update(

        self,

        animator,

    ):

        animator.apply(

            self.cubes,

        )

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self.initialized = False

        self.cubes.clear()