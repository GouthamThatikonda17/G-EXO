"""
=========================================================
Project G-EXO Desktop
Face Mapper
Version : 6.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from .expression.expression_engine import ExpressionEngine


class FaceMapper:

    def __init__(self):

        self.expression_engine = ExpressionEngine()

        self.left_eye = set()
        self.right_eye = set()

        self.left_brow = set()
        self.right_brow = set()

    # =====================================================
    # State
    # =====================================================

    def set_state(self, state):

        self.expression_engine.set_state(state)

    # =====================================================
    # Build
    # =====================================================

    def build(self, rows, cols):

        self.left_eye.clear()
        self.right_eye.clear()

        self.left_brow.clear()
        self.right_brow.clear()

        expression = self.expression_engine.current()

        center_row = rows // 2
        center_col = cols // 2

        self._draw_pattern(

            expression["left_eye"],

            center_row - 3,

            center_col - 18,

            self.left_eye,

        )

        self._draw_pattern(

            expression["right_eye"],

            center_row - 3,

            center_col + 10,

            self.right_eye,

        )

        self._draw_pattern(

            expression["left_brow"],

            center_row - 10,

            center_col - 18,

            self.left_brow,

        )

        self._draw_pattern(

            expression["right_brow"],

            center_row - 10,

            center_col + 10,

            self.right_brow,

        )

    # =====================================================
    # Pattern
    # =====================================================

    def _draw_pattern(

        self,

        pattern,

        start_row,

        start_col,

        output,

    ):

        for r, line in enumerate(pattern):

            for c, ch in enumerate(line):

                if ch == "#":

                    output.add(

                        (

                            start_row + r,

                            start_col + c,

                        )

                    )