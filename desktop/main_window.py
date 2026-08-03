"""
=========================================================
Project G-EXO Desktop
Main Window
Version : 9.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QMainWindow

from assistant import GEXOBrain

from scene.gexo_scene import GEXOScene

from behavior.behavior_engine import BehaviorEngine
from behavior.face_state import FaceState


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.brain = GEXOBrain()

        self.behavior = BehaviorEngine()

        self.setWindowTitle("G-EXO")

        self.resize(1200, 750)

        self.scene = GEXOScene()

        self.setCentralWidget(

            self.scene

        )

        # ==========================================
        # Behavior -> Scene
        # ==========================================

        self.behavior.add_listener(

            self.scene.set_state

        )

        self.behavior.set_state(

            FaceState.IDLE

        )

    # =====================================================
    # Keyboard (Temporary)
    # =====================================================

    def keyPressEvent(

        self,

        event: QKeyEvent,

    ):

        key = event.key()

        if key == Qt.Key_1:

            self.behavior.set_state(

                FaceState.IDLE

            )

        elif key == Qt.Key_2:

            self.behavior.set_state(

                FaceState.LISTENING

            )

        elif key == Qt.Key_3:

            self.behavior.set_state(

                FaceState.THINKING

            )

        elif key == Qt.Key_4:

            self.behavior.set_state(

                FaceState.SPEAKING

            )

        elif key == Qt.Key_5:

            self.behavior.set_state(

                FaceState.ERROR

            )

        else:

            super().keyPressEvent(

                event

            )