""" =========================================================
Project G-EXO
Desktop Main Window
Version : 9.5
Developer : Thatikonda Goutham Teja
=========================================================
"""
from PySide6.QtCore import Qt, QThread
from PySide6.QtGui import QKeyEvent, QCloseEvent
from PySide6.QtWidgets import QMainWindow

from assistant import GEXOBrain
from scene.gexo_scene import GEXOScene
from behavior.behavior_engine import BehaviorEngine
from behavior.face_state import FaceState
from workers.chat_worker import ChatWorker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.brain = GEXOBrain()
        self.behavior = BehaviorEngine()
        
        self._is_processing = False
        self._worker_thread = None
        self._worker = None

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
    # AI Processing
    # =====================================================
    def process_message(self, message: str):
        if self._is_processing:
            print("[Desktop] Request rejected: Another interaction is already running.")
            return
            
        self._is_processing = True
        self.behavior.set_state(FaceState.THINKING)
        
        self._worker_thread = QThread()
        self._worker = ChatWorker(
            self.brain.process,
            message,
            source="desktop"
        )
        self._worker.moveToThread(self._worker_thread)
        
        # Execution flow
        self._worker_thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_process_finished)
        self._worker.failed.connect(self._on_process_failed)
        
        # Qt Recommended Thread Lifecycle Cleanup
        self._worker.finished.connect(self._worker_thread.quit)
        self._worker.failed.connect(self._worker_thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._worker.failed.connect(self._worker.deleteLater)
        self._worker_thread.finished.connect(self._worker_thread.deleteLater)
        
        # Safely clear references only when the thread has fully finished
        self._worker_thread.finished.connect(self._clear_thread_references)
        
        self._worker_thread.start()

    def _clear_thread_references(self):
        self._worker_thread = None
        self._worker = None

    def _on_process_finished(self, response):
        self.behavior.set_state(FaceState.SPEAKING)
        
        if response is not None and hasattr(response, "message"):
            print(f"[Desktop] G-EXO: {response.message}")
        else:
            print("[Desktop] G-EXO: Received invalid response.")
            
        self.behavior.set_state(FaceState.IDLE)
        self._is_processing = False

    def _on_process_failed(self, error: str):
        self.behavior.set_state(FaceState.ERROR)
        print(f"[Desktop Error] {error}")
        
        self.behavior.set_state(FaceState.IDLE)
        self._is_processing = False

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

    # =====================================================
    # Shutdown
    # =====================================================
    def closeEvent(self, event: QCloseEvent):
        # Blocking wait is required here to prevent application crash during shutdown
        if self._worker_thread is not None and self._worker_thread.isRunning():
            self._worker_thread.quit()
            self._worker_thread.wait()
            
        super().closeEvent(event)