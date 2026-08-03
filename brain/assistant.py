"""
=========================================================
Project G-EXO
Brain
Version : 4.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from core.dispatcher import Dispatcher
from core.request import Request
from core.response import Response


class GEXOBrain:
    """
    Main entry point of G-EXO Brain.

    Every interface communicates with this class.

    Examples:
        - Desktop
        - Mobile
        - Robot
        - Voice
        - API
    """

    def __init__(self):

        self.dispatcher = Dispatcher()

    # =====================================================
    # PROCESS
    # =====================================================

    def process(
        self,
        message: str,
        source: str = "desktop",
    ) -> Response:

        request = Request(

            message=message,

            source=source,

        )

        return self.dispatcher.dispatch(request)