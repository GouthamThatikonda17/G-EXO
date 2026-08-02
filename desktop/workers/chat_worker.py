"""
=========================================================
Project G-EXO Desktop
Chat Worker
Version : 1.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
)


class ChatWorker(QObject):

    finished = Signal(object)

    failed = Signal(str)

    def __init__(self, function, *args, **kwargs):

        super().__init__()

        self.function = function

        self.args = args

        self.kwargs = kwargs

    @Slot()
    def run(self):

        try:

            result = self.function(

                *self.args,

                **self.kwargs,

            )

            self.finished.emit(

                result

            )

        except Exception as e:

            self.failed.emit(

                str(e)

            )