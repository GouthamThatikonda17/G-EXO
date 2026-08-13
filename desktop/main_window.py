"""
=========================================================
Project G-EXO Desktop Main Window
Version : 12.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal, QThread, QTimer
from PySide6.QtGui import QCloseEvent, QKeyEvent
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
)

from assistant import GEXOBrain
from behavior.face_state import FaceState

from scene.gexo_scene import GEXOScene
from widgets.chat_area import ChatArea
from widgets.message_input import MessageInput
from workers.chat_worker import ChatWorker


class MainWindow(QMainWindow):
    """
    Face-first G-EXO desktop window.

    The GEXOScene is the primary interface.

    ChatArea and MessageInput exist only as an optional developer
    console overlay and are hidden during normal operation.
    """

    state_changed = Signal(object)

    def __init__(self, brain: GEXOBrain):
        super().__init__()

        self.brain = brain
        self.behavior = self.brain.behavior

        self.setWindowTitle("G-EXO")
        self.resize(1200, 750)

        self.thread: QThread | None = None
        self.worker: ChatWorker | None = None
        self._closing = False

        self._setup_ui()
        self._connect_behavior()

    # =====================================================
    # UI
    # =====================================================

    def _setup_ui(self) -> None:
        """
        Construct the face-first interface.

        GEXOScene occupies the complete central area.
        Developer console is a floating child overlay.
        """

        self.scene = GEXOScene()
        self.setCentralWidget(self.scene)

        # -------------------------------------------------
        # Developer Console
        # -------------------------------------------------

        self.dev_console = QWidget(self.scene)
        self.dev_console.setObjectName("developer_console")

        self.dev_console.setAttribute(
            Qt.WA_StyledBackground,
            True,
        )

        self.dev_console.setStyleSheet(
            """
            QWidget#developer_console {
                background-color: rgba(15, 15, 20, 235);
                border: 1px solid rgba(255, 255, 255, 45);
                border-radius: 10px;
            }
            """
        )

        console_layout = QVBoxLayout(self.dev_console)
        console_layout.setContentsMargins(10, 10, 10, 10)
        console_layout.setSpacing(6)

        self.chat_area = ChatArea()
        self.message_input = MessageInput()

        console_layout.addWidget(
            self.chat_area,
            stretch=1,
        )

        console_layout.addWidget(
            self.message_input,
            stretch=0,
        )

        # Developer console is NOT part of the normal UI.
        self.dev_console.hide()

        # Initial floating-console geometry.
        self._position_developer_console()

        # -------------------------------------------------
        # Developer console input
        # -------------------------------------------------

        self.message_input.send_button.clicked.connect(
            self._send_message
        )

        self.message_input.input.returnPressed.connect(
            self._send_message
        )

    def _connect_behavior(self) -> None:
        """
        Connect BehaviorEngine state changes to the visual scene.

        No backend knowledge of PySide6 exists.
        """

        self.state_changed.connect(
            self.scene.set_state
        )

        self.behavior.add_listener(
            self.state_changed.emit
        )

        self.behavior.set_state(
            FaceState.IDLE
        )

    # =====================================================
    # DEVELOPER CONSOLE
    # =====================================================

    def _toggle_developer_console(self) -> None:
        if self._closing:
            return

        visible = not self.dev_console.isVisible()

        self.dev_console.setVisible(
            visible
        )

        if visible:
            self._position_developer_console()
            self.message_input.input.setFocus()

    def _position_developer_console(self) -> None:
        """
        Position the developer console as a floating overlay.

        It does NOT consume layout space and therefore does not
        resize or push the GEXO face.
        """

        if not hasattr(self, "dev_console"):
            return

        scene_width = self.scene.width()
        scene_height = self.scene.height()

        console_width = min(
            520,
            max(360, scene_width - 40),
        )

        console_height = min(
            420,
            max(260, scene_height - 40),
        )

        x = scene_width - console_width - 20
        y = scene_height - console_height - 20

        self.dev_console.setGeometry(
            x,
            y,
            console_width,
            console_height,
        )

        self.dev_console.raise_()

    def resizeEvent(self, event) -> None:
        """
        Keep the developer console floating over the face
        when the application window is resized.
        """

        super().resizeEvent(event)

        if hasattr(self, "dev_console"):
            self._position_developer_console()

    # =====================================================
    # ASYNCHRONOUS CHAT EXECUTION
    # =====================================================

    def _send_message(self) -> None:
        if self._closing:
            return

        text = self.message_input.input.text().strip()

        if not text:
            return

        # Never start a second worker while the previous QThread
        # still exists.
        if self.thread is not None:
            return

        # -------------------------------------------------
        # UI state
        # -------------------------------------------------

        self.message_input.input.clear()
        self.message_input.input.setEnabled(False)
        self.message_input.send_button.setEnabled(False)

        self.chat_area.add_message(
            "You",
            text,
        )

        # -------------------------------------------------
        # Behavior state
        # -------------------------------------------------

        self.behavior.set_state(
            FaceState.THINKING
        )

        # -------------------------------------------------
        # Worker
        # -------------------------------------------------

        thread = QThread(self)

        worker = ChatWorker(
            self.brain.process,
            text,
            source="desktop",
        )

        self.thread = thread
        self.worker = worker

        worker.moveToThread(thread)

        # Worker execution.
        thread.started.connect(
            worker.run
        )

        # Worker result.
        worker.finished.connect(
            self._on_worker_finished
        )

        worker.failed.connect(
            self._on_worker_failed
        )

        # Worker completion causes thread termination.
        worker.finished.connect(
            thread.quit
        )

        worker.failed.connect(
            thread.quit
        )

        # Worker object cleanup.
        worker.finished.connect(
            worker.deleteLater
        )

        worker.failed.connect(
            worker.deleteLater
        )

        # Thread lifecycle.
        thread.finished.connect(
            self._on_thread_finished
        )

        thread.finished.connect(
            thread.deleteLater
        )

        thread.start()

    # =====================================================
    # WORKER RESULT
    # =====================================================

    def _on_worker_finished(self, response) -> None:
        if self._closing:
            return

        self.chat_area.add_message(
            "G-EXO",
            response.message,
        )

        # Returning to IDLE releases the active THINKING state
        # and allows the passive cognitive state to become visible.
        self.behavior.set_state(
            FaceState.IDLE
        )

    def _on_worker_failed(self, error_str) -> None:
        if self._closing:
            return

        self.chat_area.add_message(
            "System Error",
            error_str,
        )

        self.behavior.set_state(
            FaceState.ERROR
        )

        QTimer.singleShot(
            3000,
            self._clear_error_state,
        )

    def _clear_error_state(self) -> None:
        if self._closing:
            return

        if self.behavior.get_state() == FaceState.ERROR:
            self.behavior.set_state(
                FaceState.IDLE
            )

    # =====================================================
    # THREAD LIFECYCLE
    # =====================================================

    def _on_thread_finished(self) -> None:
        """
        Called only after QThread has actually terminated.

        This is the single normal cleanup point for the worker
        lifecycle.
        """

        thread = self.thread

        self.worker = None
        self.thread = None

        self._restore_input()

        if thread is not None:
            thread.deleteLater()

    def _restore_input(self) -> None:
        if self._closing:
            return

        self.message_input.input.setEnabled(
            True
        )

        self.message_input.send_button.setEnabled(
            True
        )

        self.message_input.input.setFocus()

    # =====================================================
    # KEYBOARD
    # =====================================================

    def keyPressEvent(
        self,
        event: QKeyEvent,
    ) -> None:

        key = event.key()

        # -------------------------------------------------
        # Developer console
        # -------------------------------------------------

        if key in (
            Qt.Key_F12,
            Qt.Key_QuoteLeft,
        ):
            self._toggle_developer_console()
            return

        # -------------------------------------------------
        # Legacy behavior overrides
        # -------------------------------------------------

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
            super().keyPressEvent(event)

    # =====================================================
    # SHUTDOWN
    # =====================================================

    def closeEvent(
        self,
        event: QCloseEvent,
    ) -> None:
        """
        Gracefully stop an active worker thread before
        allowing the Qt window to be destroyed.
        """

        self._closing = True

        thread = self.thread
        worker = self.worker

        if thread is not None:
            try:
                if worker is not None:
                    try:
                        worker.finished.disconnect(
                            self._on_worker_finished
                        )
                    except (RuntimeError, TypeError):
                        pass

                    try:
                        worker.failed.disconnect(
                            self._on_worker_failed
                        )
                    except (RuntimeError, TypeError):
                        pass

                try:
                    thread.finished.disconnect(
                        self._on_thread_finished
                    )
                except (RuntimeError, TypeError):
                    pass

                if thread.isRunning():
                    thread.quit()
                    thread.wait()

            except RuntimeError:
                # The underlying Qt object may already have been
                # destroyed. Do not access it again.
                pass

            self.thread = None
            self.worker = None

        super().closeEvent(event)