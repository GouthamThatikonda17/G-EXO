"""
=========================================================
Project G-EXO Desktop
Visual Engine Renderer
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QColor,
    QBrush,
    QPainter,
)

from .engine import Cube


class VisualRenderer:

    def __init__(self):

        pass

    # =====================================================
    # Render
    # =====================================================

    def render(

        self,

        painter: QPainter,

        cubes: list[Cube],

    ):

        painter.setRenderHint(

            QPainter.Antialiasing,

            True,

        )

        painter.setPen(Qt.NoPen)

        for cube in cubes:

            color = QColor(cube.color)

            color.setAlpha(cube.alpha)

            painter.setBrush(

                QBrush(color)

            )

            painter.drawRoundedRect(

                cube.x,

                cube.y,

                cube.size,

                cube.size,

                cube.radius,

                cube.radius,

            )