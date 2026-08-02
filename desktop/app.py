"""
=========================================================
Project G-EXO Desktop
Application Entry
Version : 1.2
Developer : Thatikonda Goutham Teja
=========================================================
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

BRAIN_DIR = os.path.join(
    PROJECT_ROOT,
    "brain"
)

if BRAIN_DIR not in sys.path:

    sys.path.insert(0, BRAIN_DIR)

from PySide6.QtWidgets import QApplication

from main_window import MainWindow

from themes.dark_theme import DARK_THEME


def main():

    app = QApplication(sys.argv)

    app.setStyleSheet(DARK_THEME)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":

    main()