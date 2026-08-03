"""
=========================================================
Project G-EXO Desktop
Cube World Renderer
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QColor,
    QBrush,
    QPen,
)

from widgets.cube_world.face_mask import (
    FACE_GRID,
    GRID_ROWS,
    GRID_COLS,
    Cell,
)

from widgets.cube_world.animation import CubeWorldAnimation


class CubeWorldRenderer:

    def __init__(self):

        self.animation = CubeWorldAnimation()

        self.cube_size = 8

        self.spacing = 11

        self.background_color = QColor(25, 35, 50)

        self.face_color = QColor(0, 220, 255)

        self.eye_color = QColor(0, 255, 255)

        self.mouth_color = QColor(0, 220, 255)

        self.eyebrow_color = QColor(120, 255, 255)

    # =====================================================
    # Draw
    # =====================================================

    def draw(

        self,

        painter,

        width,

        height,

    ):

        start_x = (

            width

            - GRID_COLS * self.spacing

        ) / 2

        start_y = (

            height

            - GRID_ROWS * self.spacing

        ) / 2

        painter.setPen(Qt.NoPen)

        pulse = self.animation.pulse()

        brightness = self.animation.brightness()

        for row in range(GRID_ROWS):

            for col in range(GRID_COLS):

                x = start_x + col * self.spacing

                y = start_y + row * self.spacing

                wave = self.animation.background_height(

                    row,

                    col,

                )

                cell = FACE_GRID[row][col]

                if cell == Cell.EMPTY:

                    color = QColor(

                        self.background_color

                    )

                    color.setAlpha(120)

                    size = self.cube_size

                elif cell == Cell.EYE:

                    color = QColor(

                        self.eye_color

                    )

                    color = color.lighter(

                        int(

                            120 * pulse

                        )

                    )

                    size = self.cube_size + 4

                elif cell == Cell.MOUTH:

                    color = QColor(

                        self.mouth_color

                    )

                    color = color.lighter(

                        int(

                            110 * pulse

                        )

                    )

                    size = self.cube_size + 3

                elif cell == Cell.EYEBROW:

                    color = QColor(

                        self.eyebrow_color

                    )

                    size = self.cube_size + 2

                else:

                    color = QColor(

                        self.face_color

                    )

                    size = self.cube_size + 2

                painter.setBrush(

                    QBrush(color)

                )

                painter.setPen(

                    QPen(color)

                )

                painter.drawRoundedRect(

                    x,

                    y - wave,

                    size,

                    size,

                    2,

                    2,

                )