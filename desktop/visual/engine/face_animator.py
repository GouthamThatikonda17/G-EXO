"""
=========================================================
Project G-EXO Desktop
Face Animator
Version : 6.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import math

from .animation_controller import AnimationController


class FaceAnimator:

    def __init__(self):

        self.time = 0.0

        self.float_offset = 0.0

        self.controller = AnimationController()

        self.blink = 1.0

        self.blink_timer = 0.0

        self.blinking = False

    # =====================================================
    # State
    # =====================================================

    def set_state(

        self,

        state,

    ):

        self.controller.set_state(

            state,

        )

    # =====================================================
    # Update
    # =====================================================

    def update(self):

        self.time += 0.10

        self.float_offset = math.sin(

            self.time

        ) * 6

        self.controller.update()

        self.blink_timer += 0.10

        if not self.blinking and self.blink_timer >= 2.5:

            self.blinking = True

        if self.blinking:

            self.blink -= 0.12

            if self.blink <= 0.0:

                self.blink = 1.0

                self.blink_timer = 0.0

                self.blinking = False

    # =====================================================
    # Apply
    # =====================================================

    def apply(

        self,

        cubes,

    ):

        eye_x = self.controller.eye.offset_x

        eye_y = self.controller.eye.offset_y

        left_brow = self.controller.eyebrow.left_offset

        right_brow = self.controller.eyebrow.right_offset

        for cube in cubes:

            cube.x = cube.base_x

            cube.y = cube.base_y - self.float_offset

            if cube.is_eye:

                cube.x += eye_x

                cube.y += eye_y

                cube.alpha = 255 if self.blink > 0.20 else 0

            elif cube.is_eyebrow:

                if cube.base_x < 600:

                    cube.y += left_brow

                else:

                    cube.y += right_brow

                cube.alpha = 255

            elif cube.is_background:

                cube.alpha = 120

            else:

                cube.alpha = 255