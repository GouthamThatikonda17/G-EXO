"""
=========================================================
Project G-EXO Desktop Main Window Version : 9.2
Developer : Thatikonda Goutham Teja
=========================================================
"""

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QMainWindow
from assistant import GEXOBrain
from scene.gexo_scene import GEXOScene
from behavior.face_state import FaceState


class MainWindow(QMainWindow):
    state_signal = Signal(object)

    def __init__(self, brain: GEXOBrain):
        super().__init__()
        self.brain = brain
        self.behavior = self.brain.behavior
        self.setWindowTitle("G-EXO")
        self.resize(1200, 750)
        self.scene = GEXOScene()
        self.setCentralWidget(
            self.scene
        )
        # ==========================================
        # Behavior -> Signal Bridge -> Scene
        # ==========================================
        self.state_signal.connect(
            self.scene.set_state
        )
        self.behavior.add_listener(
            self._on_behavior_state_changed
        )
        self.behavior.set_state(
            FaceState.IDLE
        )

    # =====================================================
    # Behavior State Slot (Thread-Safe Bridge)
    # =====================================================
    @Slot(object)
    def _on_behavior_state_changed(
        self,
        state,
    ):
        self.state_signal.emit(state)

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