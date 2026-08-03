"""
=========================================================
Project G-EXO Desktop
Eye Mapper
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""


class EyeMapper:

    def __init__(self):

        self.left_eye = set()

        self.right_eye = set()

    # =====================================================
    # Build
    # =====================================================

    def build(

        self,

        rows,

        cols,

    ):

        self.left_eye.clear()

        self.right_eye.clear()

        center_row = rows // 2

        center_col = cols // 2

        self.build_eye(

            self.left_eye,

            center_row,

            center_col - 14,

        )

        self.build_eye(

            self.right_eye,

            center_row,

            center_col + 14,

        )

    # =====================================================
    # Eye Shape
    # =====================================================

    def build_eye(

        self,

        eye,

        row,

        col,

    ):

        shape = [

            "....XXXX....",

            "..XXXXXXXX..",

            ".XXXXXXXXXX.",

            "XXXXXXXXXXXX",

            "XXXXXXXXXXXX",

            ".XXXXXXXXXX.",

            "..XXXXXXXX..",

            "....XXXX....",

        ]

        for r, line in enumerate(shape):

            for c, value in enumerate(line):

                if value == "X":

                    eye.add(

                        (

                            row + r - 4,

                            col + c - 6,

                        )

                    )