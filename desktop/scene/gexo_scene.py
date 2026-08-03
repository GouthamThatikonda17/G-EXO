"""
=========================================================
Project G-EXO Desktop
G-EXO Scene
Version : 4.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from PySide6.QtWidgets import QWidget

from visual.engine.scene import VisualScene


class GEXOScene(QWidget):

    def __init__(self):

        super().__init__()

        self.setStyleSheet(
            """
            background:#060A12;
            """
        )

        # =====================================================
        # Visual Engine
        # =====================================================

        self.visual = VisualScene(self)

        self.visual.lower()

    # =====================================================
    # State
    # =====================================================

    def set_state(

        self,

        state,

    ):

        self.visual.set_state(

            state,

        )

    # =====================================================
    # Resize
    # =====================================================

    def resizeEvent(self, event):

        self.visual.setGeometry(

            self.rect()

        )

        super().resizeEvent(event)