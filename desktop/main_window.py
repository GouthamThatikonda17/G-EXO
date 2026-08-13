"""
=========================================================
Project G-EXO Desktop Main Window
Version : 9.5
Developer : Thatikonda Goutham Teja
=========================================================
"""
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QMainWindow

from assistant import GEXOBrain
from scene.gexo_scene import GEXOScene
from behavior.face_state import FaceState

class MainWindow(QMainWindow):
    # Cross-thread UI boundary signal
    state_changed = Signal(object)

    def __init__(self, brain: GEXOBrain):
        super().__init__()

        # Share the authoritative Composition Root engine
        self.brain = brain
        self.behavior = self.brain.behavior

        self.setWindowTitle("G-EXO")
        self.resize(1200, 750)

        self.scene = GEXOScene()
        self.setCentralWidget(
            self.scene
        )

        # ==========================================
        # Behavior -> Scene (Thread-Safe Binding)
        # ==========================================
        self.state_changed.connect(self.scene.set_state)
        self.behavior.add_listener(self.state_changed.emit)

        self.behavior.set_state(
            FaceState.IDLE
        )

    # =====================================================
    # Keyboard (Temporary Overrides)
    # =====================================================
    def keyPressEvent(
        self,
        event: QKeyEvent,
    ):
        key = event.key()
        if key == Qt.Key_1:
            self.behavior.set_state(FaceState.IDLE)
        elif key == Qt.Key_2:
            self.behavior.set_state(FaceState.LISTENING)
        elif key == Qt.Key_3:
            self.behavior.set_state(FaceState.THINKING)
        elif key == Qt.Key_4:
            self.behavior.set_state(FaceState.SPEAKING)
        elif key == Qt.Key_5:
            self.behavior.set_state(FaceState.ERROR)
        else:
            super().keyPressEvent(event)
