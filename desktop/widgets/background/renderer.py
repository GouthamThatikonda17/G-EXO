"""
=========================================================
Project G-EXO Desktop
Background Renderer
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import math

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QPainter,
    QColor,
    QBrush,
)

from widgets.background.theme import (
    BACKGROUND,
    CELL_PRIMARY,
    CELL_SECONDARY,
    LAYER_SPEEDS,
)

from widgets.background.cell import DigitalCell


class BackgroundRenderer:

    def __init__(self):

        self.cells = []

    # =====================================================
    # BUILD
    # =====================================================

    def build(self, width, height, count):

        self.cells.clear()

        for _ in range(count):

            self.cells.append(

                DigitalCell(

                    width,

                    height,

                )

            )

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, width, height):

        for cell in self.cells:

            cell.y -= LAYER_SPEEDS[cell.layer]

            cell.phase += 0.03

            if cell.y < -10:

                cell.reset(width, height)

                cell.y = height + 5

    # =====================================================
    # DRAW
    # =====================================================

    def draw(self, painter: QPainter, width, height):

        painter.fillRect(

            0,

            0,

            width,

            height,

            BACKGROUND,

        )

        painter.setPen(Qt.NoPen)

        for cell in self.cells:

            pulse = (math.sin(cell.phase) + 1) / 2

            alpha = int(cell.alpha * (0.35 + pulse * 0.65))

            if cell.layer == 0:

                color = QColor(CELL_PRIMARY)

            elif cell.layer == 1:

                color = QColor(CELL_SECONDARY)

            else:

                color = QColor(255, 255, 255)

            color.setAlpha(alpha)

            painter.setBrush(

                QBrush(color)

            )

            painter.drawRoundedRect(

                int(cell.x),

                int(cell.y),

                cell.size,

                cell.size,

                1,

                1,

            )