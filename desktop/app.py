"""
=========================================================
Project G-EXO Desktop Application Entry
Version : 2.0
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
from runtime.application import Application

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_THEME)

    # 1. Enforce Composition Root Ownership
    app_root = Application()

    # 2. Inject Shared Brain into Platform Frontend
    window = MainWindow(brain=app_root.brain)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()