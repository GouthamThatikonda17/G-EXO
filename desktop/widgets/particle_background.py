"""
=========================================================
Project G-EXO Desktop
Particle Background
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import random

from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import QColor, QPainter, QBrush
from PySide6.QtWidgets import QWidget


class Particle:

    def __init__(self, width, height):

        self.x = random.randint(0, width)
        self.y = random.randint(0, height)

        self.radius = random.uniform(1.0, 3.5)

        self.speed = random.uniform(0.2, 0.8)

        self.alpha = random.randint(40, 160)


class ParticleBackground(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.particles = []

        self.timer = QTimer(self)

        self.timer.timeout.connect(self.animate)

        self.timer.start(16)

    # =====================================================
    # Resize
    # =====================================================

    def resizeEvent(self, event):

        self.create_particles()

        super().resizeEvent(event)

    # =====================================================
    # Create Particles
    # =====================================================

    def create_particles(self):

        self.particles.clear()

        for _ in range(350):

            self.particles.append(

                Particle(

                    self.width(),

                    self.height(),

                )

            )

    # =====================================================
    # Animation
    # =====================================================

    def animate(self):

        if self.width() <= 0 or self.height() <= 0:

            return

        for particle in self.particles:

            particle.y -= particle.speed

            if particle.y < -5:

                particle.y = self.height() + 5

                particle.x = random.randint(0, self.width())

        self.update()

    # =====================================================
    # Paint
    # =====================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(

            self.rect(),

            QColor(6, 10, 18),

        )

        painter.setPen(Qt.NoPen)

        for particle in self.particles:

            painter.setBrush(

                QBrush(

                    QColor(

                        0,

                        220,

                        255,

                        particle.alpha,

                    )

                )

            )

            painter.drawEllipse(

                QPointF(

                    particle.x,

                    particle.y,

                ),

                particle.radius,

                particle.radius,

            )