"""
=========================================================
Project G-EXO Desktop
Digital Cell
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import random


class DigitalCell:

    def __init__(self, width, height):

        self.reset(width, height)

    def reset(self, width, height):

        self.x = random.randint(0, width)

        self.y = random.randint(0, height)

        self.layer = random.randint(0, 2)

        self.size = random.randint(2, 4)

        self.alpha = random.randint(50, 220)

        self.phase = random.random() * 6.28