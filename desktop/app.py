"""
=========================================================
Project G-EXO Desktop
Application Entry
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

import sys

from PySide6.QtWidgets import QApplication

from main_window import MainWindow


def main():

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":

    main()