"""
=========================================================
Project G-EXO Desktop
Cube World Face Mask
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from enum import IntEnum


# =========================================================
# Cell Types
# =========================================================

class Cell(IntEnum):

    EMPTY = 0

    FACE = 1

    EYE = 2

    MOUTH = 3

    EYEBROW = 4


# =========================================================
# Grid Configuration
# =========================================================

GRID_ROWS = 60

GRID_COLS = 110


# =========================================================
# Face Size
# =========================================================

FACE_WIDTH = 34

FACE_HEIGHT = 18


# =========================================================
# Face Layout
# =========================================================

FACE_LAYOUT = [

"..................................",

"...EEEEEE..........EEEEEE.........",
"...EEEEEE..........EEEEEE.........",
"...EEEEEE..........EEEEEE.........",

"..BBBBBBB........BBBBBBB..........",

"..................................",

"..................................",

"...........MMMMMMMMMM.............",

"...........MMMMMMMMMM.............",

"..................................",

"..................................",

"..................................",

"..................................",

"..................................",

"..................................",

"..................................",

"..................................",

"..................................",

]


# =========================================================
# Build Grid
# =========================================================

def build_face_grid():

    grid = [

        [Cell.EMPTY for _ in range(GRID_COLS)]

        for _ in range(GRID_ROWS)

    ]

    start_row = GRID_ROWS // 2 - FACE_HEIGHT // 2

    start_col = GRID_COLS // 2 - FACE_WIDTH // 2

    for r, line in enumerate(FACE_LAYOUT):

        for c, ch in enumerate(line):

            row = start_row + r

            col = start_col + c

            if ch == "E":

                grid[row][col] = Cell.EYE

            elif ch == "M":

                grid[row][col] = Cell.MOUTH

            elif ch == "B":

                grid[row][col] = Cell.EYEBROW

            elif ch == "#":

                grid[row][col] = Cell.FACE

    return grid


FACE_GRID = build_face_grid()